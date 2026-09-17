from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
import unittest

from automation.content_builder import assemble, build, validate_inventory, verify_link
from automation.page_generator import _validate

NOW = datetime.now(timezone.utc)
URL = 'https://www.motorinntoyotaofcarroll.com/observed-inventory'
CANDIDATE = {'slug':'toyota-tundra-carroll','cluster':'New Toyota','title':'Toyota Tundra in Carroll: Buyer Guide','target_query':'toyota tundra carroll iowa','owner_host':'www.motorinntoyotaofcarroll.com','target_url':'https://www.motorinntoyotaofcarroll.com/toyota-tundra-carroll/','destination':'dealeron','internal_links':[{'url':URL}]}


def inventory():
    source={'source_type':'DealerVault','verified':True,'sha256':'f'*64,'dealer_id':'DVD56054','location':'9','modified_at':(NOW-timedelta(hours=1)).isoformat(),'retrieved_at':NOW.isoformat(),'valid_until':(NOW+timedelta(hours=47)).isoformat(),'row_count':40,'url':'https://motorinn-dealervault-raw.s3.us-east-2.amazonaws.com/fixture_INV.csv'}
    return {'status':'verified','feed':source,'aggregates':{'groups':[
        {'type_code':'N','make':'TOYOTA','model':'TUNDRA CREWMAX','style':'PICKUP','count':7},
        {'type_code':'U','make':'TOYOTA','model':'TUNDRA CREWMAX','style':'PICKUP','count':3},
        {'type_code':'N','make':'TOYOTA','model':'RAV4','style':'WAGON 4 DOOR','count':30}]}}


def page(url):
    return {'url':url,'status':200,'text':f'<html><head><title>New Toyota Tundra Inventory</title><link rel="canonical" href="{url}"></head><body><h1>New Toyota Tundra Inventory</h1></body></html>'}


class ContentBuilderTests(unittest.TestCase):
    def test_exact_model_type_filter_and_generator_contract(self):
        brief=assemble(CANDIDATE,inventory(),fetch=page,now=NOW)
        self.assertEqual(brief['builder_blockers'],[])
        self.assertIn('selection of 7 Toyota Tundra',brief['meta_description'])
        self.assertEqual(brief['source_evidence'][0]['transformation']['group_total'],7)
        self.assertEqual(brief['topology_status'],'verified')
        self.assertNotIn('business',brief)
        job={**CANDIDATE,**brief,'gsc_check':{'status':'checked'},'blockers':[]}
        self.assertEqual(_validate(job)[0],[])

    def test_expired_feed_does_not_create_content(self):
        data=inventory();data['feed']['valid_until']=(NOW-timedelta(seconds=1)).isoformat()
        brief=assemble(CANDIDATE,data,fetch=page,now=NOW)
        self.assertNotIn('sections',brief)
        self.assertIn('expiry',brief['builder_blockers'][0])

    def test_unsupported_clusters_and_suv_mapping_stay_blocked(self):
        for cluster,slug in [('Financing','finance'),('Service/tires','service'),('Trade-in','trade'),('Sell to us','sell'),('Used vehicles','used-suvs')]:
            with self.subTest(cluster=cluster):
                brief=assemble({**CANDIDATE,'cluster':cluster,'slug':slug,'target_query':slug},inventory(),fetch=page,now=NOW)
                self.assertTrue(brief['builder_blockers'])
                self.assertNotIn('sections',brief)

    def test_bad_canonical_or_filter_does_not_verify_topology(self):
        for text in ['<title>New Toyota Tundra</title><link rel="canonical" href="https://www.motorinntoyotaofcarroll.com/other">',f'<title>Used Chevrolet Trucks</title><link rel="canonical" href="{URL}">']:
            brief=assemble(CANDIDATE,inventory(),fetch=lambda url:{'url':url,'status':200,'text':text},now=NOW)
            self.assertEqual(brief['topology_status'],'blocked')

    def test_discovery_uses_real_homepage_hrefs(self):
        candidate={k:v for k,v in CANDIDATE.items() if k!='internal_links'}
        discovered=URL+'/new-tundra'
        seen=[]
        def fetch(url):
            seen.append(url)
            if url.endswith('.com/'):
                return {'url':url,'status':200,'text':f'<a href="{discovered}">Inventory</a><a href="/contact">Contact</a>'}
            return page(url)
        brief=assemble(candidate,inventory(),fetch=fetch,now=NOW)
        self.assertEqual(brief['internal_links'][0]['url'],discovered)
        self.assertEqual(seen,['https://www.motorinntoyotaofcarroll.com/',discovered])

    def test_cross_host_and_noindex_destinations_rejected(self):
        with self.assertRaises(ValueError):
            verify_link('https://attacker.example/inventory',CANDIDATE,page,NOW)
        blocked=lambda url:{**page(url),'text':page(url)['text'].replace('<head>','<head><meta name="robots" content="noindex">')}
        with self.assertRaisesRegex(ValueError,'not indexable'):
            verify_link(URL,CANDIDATE,blocked,NOW)

    def test_general_used_inventory_does_not_prove_truck_filter(self):
        candidate={**CANDIDATE,'cluster':'Used vehicles','slug':'used-trucks','target_query':'used trucks'}
        general=lambda url:{'url':url,'status':200,'text':f'<title>Used Cars, SUVs and Trucks</title><link rel="canonical" href="{url}">'}
        with self.assertRaisesRegex(ValueError,'general used inventory'):
            verify_link(URL,candidate,general,NOW)

    def test_parent_inventory_requires_real_filtered_heading_and_parent_get(self):
        url='https://www.motorinntoyotaofcarroll.com/searchnew.aspx?Make=Toyota&Model=Tundra'
        parent=url.split('?')[0]
        seen=[]
        def fetch(request):
            seen.append(request)
            return {'url':request,'status':200,'text':f'<title>New Toyota Tundra Inventory</title><link rel="canonical" href="{parent}"><h1>New Toyota Tundra</h1>'}
        link,proof,crawl=verify_link(url,CANDIDATE,fetch,NOW)
        self.assertTrue(proof['filter_verified']);self.assertEqual(proof['canonical_scope'],'parent-inventory')
        self.assertEqual(seen,[url,parent]);self.assertEqual(link['canonical'],parent)
        def generic(request):
            return {'url':request,'status':200,'text':f'<title>Toyota New Vehicle Inventory</title><h1>New Vehicles</h1><link rel="canonical" href="{parent}">'}
        with self.assertRaisesRegex(ValueError,'intended make/model/type'):
            verify_link(url,CANDIDATE,generic,NOW)

    def test_aggregate_reconciliation(self):
        data=inventory();data['feed']['row_count']=41
        with self.assertRaisesRegex(ValueError,'do not reconcile'):
            validate_inventory(data,NOW)

    def test_pending_only_refresh_keeps_research_blockers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'inputs').mkdir();(root/'queue/pending').mkdir(parents=True)
            (root/'inputs/inventory-evidence.json').write_text(json.dumps(inventory()))
            candidate_path=root/'candidates.json';candidate_path.write_text(json.dumps([CANDIDATE]))
            marker=root/'queue/pending'/f"{CANDIDATE['slug']}.json"
            marker.write_text(json.dumps({**CANDIDATE,'blockers':['GSC unavailable'],'gsc_check':{'status':'blocked'}}))
            result=build(root,{'candidate_path':str(candidate_path)},fetch=page)
            updated=json.loads(marker.read_text());self.assertEqual(updated['blockers'],['GSC unavailable'])
            self.assertIn('sections',updated)
            review=root/'queue/drafts'/marker.name;review.parent.mkdir();review.write_text('review version unchanged')
            original=marker.read_bytes();build(root,{'candidate_path':str(candidate_path)},fetch=page)
            self.assertEqual(marker.read_bytes(),original);self.assertEqual(review.read_text(),'review version unchanged')


if __name__=='__main__':unittest.main()
