from __future__ import annotations
import json, pathlib
from urllib.parse import quote

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / 'content/ready-design'

def link(make, model, condition):
    base = 'searchnew.aspx' if condition == 'new' else 'searchused.aspx'
    return f'https://www.motorinnautogroup.com/{base}?Make={quote(make)}&Model={quote(model)}'

def inv_links(make, model):
    return [
        ('See new inventory', link(make, model, 'new')),
        ('See used listings', link(make, model, 'used')),
        ('Browse used inventory', 'https://www.motorinnautogroup.com/used-inventory'),
    ]

def body_spec(specs, local_angle, inventory):
    rows = '\n'.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a,b,c in specs)
    links = '\n'.join(f'<p><a href="{u}">{t}</a></p>' for t,u in inventory)
    return f'''<aside class="hero"><h1>{{title}}</h1><p>{{intro}}</p></aside>
<h2>What should you check first?</h2>
<div class="table-wrap"><table class="mi-table"><thead><tr><th>Spec</th><th>Model figure</th><th>What to verify</th></tr></thead><tbody>{rows}</tbody></table></div><h2>How it fits Carroll-area driving</h2>
<p>{local_angle}</p>
<h2>How to see the exact vehicle</h2>
<p>Use the live inventory links below, then compare the exact trim, wheels, towing package, cargo space, service history, and price.</p>
<div class="mi-invslot">
{links}
</div>'''

def faq(faqs):
    html = '\n'.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)
    data = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q,a in faqs]}
    return html, json.dumps(data, separators=(',', ':'))

def build():
    specs = [
        ('Toyota Grand Highlander', 'Toyota Grand Highlander in Carroll, Iowa', 'Three rows, cargo space, and towing for school runs, sports, and road trips.', [
            ('Cargo space', 'Up to 97.5 cu. ft. [1]', 'Fits suitcases, coolers, sports gear, and the usual family load.'),
            ('Towing', 'Up to 5,000 lb [1]', 'Check the actual trailer and hitch setup.'),
            ('Seating', 'Up to 8 [1]', 'Confirm the exact seat layout.'),
        ], 'Useful space for school, sports, and Iowa winters. Bring your usual seating and cargo load to the lot.', inv_links('Toyota','Grand Highlander')),
        ('Toyota Tacoma', 'Toyota Tacoma in Carroll, Iowa', 'A midsize truck for jobs, gravel roads, and lighter towing work.', [
            ('Engine output', 'Up to 326 horsepower and 465 lb-ft torque [1]', 'Confirm the exact trim and package.'),
            ('Cab choice', 'Available XtraCab or Double Cab [1]', 'Check crew space versus bed length.'),
            ('Local use', 'Commuter-friendly size', 'Confirm towing package and payload on the listing.'),
        ], 'Easy around town, useful on jobs, and comfortable enough for school and weekend trips.', inv_links('Toyota','Tacoma')),
        ('Toyota Camry', 'Toyota Camry in Carroll, Iowa', 'A comfortable sedan with efficiency for commuting and Iowa road trips.', [
            ('Fuel economy', 'Up to 51 combined MPG [1]', 'Confirm the exact trim and drivetrain.'),
            ('Performance', 'Up to 232 net combined horsepower [1]', 'Verify the chosen engine setup.'),
            ('Drivetrain', 'Available FWD or AWD [1]', 'Match winter-road confidence to your route.'),
        ], 'A low-stress commuter and road-trip car. Good for Carroll-to-Des Moines runs and everyday errands.', inv_links('Toyota','Camry')),
        ('Chevrolet Silverado 1500', 'Chevrolet Silverado 1500 in Carroll, Iowa', 'A full-size truck for towing, hauling, and Carroll-area work.', [
            ('Towing', 'Up to 13,700 lb [1]', 'Confirm the tow package and axle.'),
            ('Payload', 'Up to 2,340 lb [1]', 'Check the payload sticker on the exact truck.'),
            ('Engine', 'Available V8 with 481 horsepower and 501 lb-ft torque [1]', 'Match engine to fuel and towing needs.'),
        ], 'Strong full-size capability for trailers, equipment, and everyday family use. Bring the actual load or trailer details.', inv_links('Chevrolet','Silverado 1500')),
        ('Chevrolet Equinox', 'Chevrolet Equinox in Carroll, Iowa', 'A practical SUV for family, school, shopping, and regional drives.', [
            ('Performance', '175 horsepower and 203 lb-ft torque [1]', 'Confirm the engine and drive mode.'),
            ('Towing', 'Up to 1,500 lb [1]', 'Very small trailer only; check the exact setup.'),
            ('Seating', '5 seats [1]', 'Compare with your usual riders and gear.'),
        ], 'A sensible SUV for local errands and easy regional travel. Bring your cargo list to compare space.', inv_links('Chevrolet','Equinox')),
        ('Chevrolet Colorado', 'Chevrolet Colorado in Carroll, Iowa', 'A midsize truck with real towing and bed space for Carroll jobs.', [
            ('Performance', '350 horsepower and 450 lb-ft torque [1]', 'Confirm standard engine output on the trim.'),
            ('Towing', 'Up to 7,700 lb [1]', 'Check hitch and tow package.'),
            ('Cargo bed', '41.9 cu. ft. [1]', 'Bring your tools or gear to test fit.'),
        ], 'A balanced midsize truck for town driving, gravel roads, and lighter work jobs.', inv_links('Chevrolet','Colorado')),
    ]

    sources = {
        'Toyota Grand Highlander': ('https://www.toyota.com/grandhighlander/2026/', 'Toyota Grand Highlander specs'),
        'Toyota Tacoma': ('https://www.toyota.com/tacoma/2026/', 'Toyota Tacoma specs'),
        'Toyota Camry': ('https://www.toyota.com/camry/2026/', 'Toyota Camry specs'),
        'Chevrolet Silverado 1500': ('https://www.chevrolet.com/trucks/silverado/1500/', 'Chevrolet Silverado 1500 specs'),
        'Chevrolet Equinox': ('https://www.chevrolet.com/suvs/equinox/', 'Chevrolet Equinox specs'),
        'Chevrolet Colorado': ('https://www.chevrolet.com/trucks/colorado/', 'Chevrolet Colorado specs'),
    }
    faqs = {
        'Toyota Grand Highlander': [('How much cargo space?', 'Toyota lists up to 97.5 cubic feet with the rear seats folded [1].'), ('Can it tow?', 'Toyota lists up to 5,000 pounds [1]. Check the actual trailer and hitch setup.'), ('How many seats?', 'Toyota lists up to eight [1].')],
        'Toyota Tacoma': [('How much horsepower?', 'Toyota lists up to 326 horsepower and 465 lb-ft torque [1].'), ('What cab choices?', 'Toyota lists XtraCab and Double Cab [1].'), ('Which trim should I choose?', 'Match cab, bed, package, and towing needs to the exact vehicle.')],
        'Toyota Camry': [('What fuel economy?', 'Toyota lists up to 51 combined MPG [1].'), ('Is AWD available?', 'Toyota lists available front-wheel drive or electronic on-demand all-wheel drive [1].'), ('What engine output?', 'Toyota lists up to 232 net combined horsepower [1].')],
        'Chevrolet Silverado 1500': [('How much can it tow?', 'Chevrolet lists up to 13,700 pounds [1]. Check the exact tow package and axle.'), ('How much payload?', 'Chevrolet lists up to 2,340 pounds [1]. Check the payload sticker.'), ('Is V8 available?', 'Chevrolet lists an available V8 with 481 horsepower and 501 lb-ft torque [1].')],
        'Chevrolet Equinox': [('How much can it tow?', 'Chevrolet lists up to 1,500 pounds when properly equipped [1].'), ('How many seats?', 'Chevrolet lists five seats [1].'), ('What performance?', 'Chevrolet lists 175 horsepower and 203 lb-ft torque [1].')],
        'Chevrolet Colorado': [('How much can it tow?', 'Chevrolet lists up to 7,700 pounds [1]. Check the tow package.'), ('How much horsepower?', 'Chevrolet lists 350 horsepower standard [1].'), ('How much bed space?', 'Chevrolet lists 41.9 cubic feet of cargo bed volume [1].')],
    }
    for slug, make, model, intro, specs, angle, inv in specs:
        canonical = f"https://www.motorinnautogroup.com/{slug.replace('-', '-')}"
        faq_html, faq_json = faq(faqs[make])
        src_url, src_label = sources[make]
        rel = '\n'.join(
            f'<li><a href="https://www.motorinnautogroup.com/testdrive.aspx">Test drive in Carroll, Iowa</a></li>\n'
            f'<li><a href="https://www.motorinnautogroup.com/vehicle-trim-levels-explained">Trim levels explained</a></li>\n'
            f'<li><a href="https://www.motorinnautogroup.com/used-trucks">Used trucks in Carroll, Iowa</a></li>\n'
            f'<li><a href="https://www.motorinnautogroup.com/used-trucks-towing-iowa">Used trucks for towing in Iowa</a></li>\n'
            f'<li><a href="https://www.motorinnautogroup.com/used-toyota-suvs">Used Toyota SUVs</a></li>\n'
            f'<li><a href="https://www.motorinnautogroup.com/used-chevrolet-suvs">Used Chevrolet SUVs</a></li>')
        content = body_spec(specs, angle, inv)
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>{title} | Motor Inn Auto Group</title>
<meta content="{intro}" name="description"/>
<link href="{canonical}" rel="canonical"/>
</head>
<body class="seo-landing mi-template-711">
{content}
<section class="mi-faq" id="{slug}-faqs">
<h2>{title} FAQs</h2>
{faq_html}
<script type="application/ld+json">
{faq_json}
</script>
</section>
<section class="mi-related">
<h2>Related pages</h2>
<ul>{rel}</ul>
</section>
<aside class="cta-box"><p><strong>Questions?</strong> <a href="https://www.motorinnautogroup.com/testdrive.aspx">Book a test drive</a>  or call <a href="tel:+17127925000">(712) 792-5000</a>.</p></aside>
<p class="mi-small">Sources: [1] <a href="{src_url}">{src_label}</a></p>
</body>
</html>'''
        path = OUT / f'{slug.html}'
        path.write_text(html, encoding='utf8')
        print(path.name)

if __name__ == '__main__':
    build()