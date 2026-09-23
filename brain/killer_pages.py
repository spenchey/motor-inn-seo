
import json, sys, datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly",
          "https://www.googleapis.com/auth/analytics.readonly"]
creds = service_account.Credentials.from_service_account_file(
    "/Users/spencerheywood/.config/gcloud/ga4-service-account.json", scopes=SCOPES)
gsc = build("searchconsole", "v1", credentials=creds)
pages = {}
today = datetime.date(2026, 9, 23)
for d in range(28, 0, -1):
    end = (today - datetime.timedelta(days=d)).isoformat()
    body = {"startDate": end, "endDate": end, "dimensions": ["page"], "rowLimit": 250}
    try:
        r = gsc.searchanalytics().query(siteUrl="sc-domain:motorinnautogroup.com", body=body).execute()
    except Exception:
        continue
    for row in r.get("rows", []):
        u = row["keys"][0].split("?")[0]
        path = u.split("motorinnautogroup.com")[-1].rstrip("/").lower()
        agg = pages.setdefault(path, {"imp":0,"clk":0,"pos_sum":0.0})
        agg["imp"] += row.get("impressions",0); agg["clk"] += row.get("clicks",0)
        agg["pos_sum"] += row.get("position",0)*max(row.get("impressions",1),1)
ga4 = build("analyticsdata", "v1beta", credentials=creds)
resp = ga4.properties().runReport(
    property="properties/364125348",
    body={"dimensions":[{"name":"landingPagePlusQueryString"}],
          "metrics":[{"name":"keyEvents"}],
          "dateRanges":[{"startDate":"2026-08-26","endDate":"2026-09-22"}], "limit":500}
).execute()
leads = {}
for row in resp.get("rows", []):
    p = row["dimensionValues"][0]["value"].split("?")[0].rstrip("/").lower()
    leads[p] = leads.get(p,0) + int(row["metricValues"][0]["value"])
# GA4 vs GSC naming variants to merge (contactus forms)
merge = {"/contactus/carroll":"/contactus.aspx"}
print("path | imp | clicks | avgpos | keyEvents | verdict")
rows = []
for p, a in pages.items():
    p2 = merge.get(p, p)
    ke = leads.get(p, 0) + leads.get(p2, 0)
    avgpos = round(a["pos_sum"]/max(a["imp"],1),1)
    rows.append((a["imp"], p, a["clk"], avgpos, ke))
rows.sort(reverse=True)
for imp,p,clk,ap,ke in rows[:22]:
    if imp < 200: continue
    verdict = ("TRAP: big traffic, zero leads" if (ke==0 and imp>=1000) else
               "KILLER: leads + visibility gap" if (ke>=3 and ap>4 and imp>=200) else "ok")
    print(f"{p} | {imp} | {clk} | {ap} | {ke} | {verdict}")
