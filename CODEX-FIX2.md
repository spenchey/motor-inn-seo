Small deploy-fix task. Context: /inventory.md is LIVE on ai.motorinnautogroup.com and
ai.motorinntoyotaofcarroll.com (proxy feed-json branch deployed). Problems:
1. https://ai.motorinnofcarroll.com/inventory.md returns 502 - diagnose (container? config?) and fix via redeploy.
2. https://ai.motorinnautogroup.com/feed.json 404 - the feed-json route maybe only on some sites or path differs; check server.py routes + fix + redeploy.
Do it: ssh is NOT needed - deploy from this machine using the repo's deploy.sh (it targets EC2 67.202.51.138). Verify all 3 sites x both endpoints 200. Then git commit+push any repo changes. Print final URL matrix.
Start now.