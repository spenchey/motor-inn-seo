# Motor Inn — page state baselines
Format: url | as-of | impressions28 | clicks28 | avgpos | keyEvents28 | notes
Update AFTER each weekly pull; keep prior values in git history, do not delete rows.

## as-of 2026-09-23 (28d window)
```
path | imp | clicks | avgpos | keyEvents | verdict
/contactus/carroll | 8113 | 770 | 4.7 | 7166 | KILLER-CAND: leads + visibility gap
 | 7816 | 189 | 7.8 | 11476 | KILLER-CAND: leads + visibility gap
/vehicle-trim-levels-explained | 5696 | 2 | 12.8 | 20 | KILLER-CAND: leads + visibility gap
/used-inventory | 3204 | 54 | 12.5 | 5410 | KILLER-CAND: leads + visibility gap
/searchnew.aspx | 3177 | 23 | 7.4 | 5612 | KILLER-CAND: leads + visibility gap
/service-locations.html | 1723 | 3 | 6.9 | 224 | KILLER-CAND: leads + visibility gap
/finance-locations.html | 1559 | 0 | 6.9 | 36 | KILLER-CAND: leads + visibility gap
/contactus.aspx | 1542 | 2 | 7.6 | 14332 | KILLER-CAND: leads + visibility gap
/new-toyota | 1526 | 20 | 3.9 | 442 | ok
/used-cars | 1443 | 4 | 9.3 | 86 | KILLER-CAND: leads + visibility gap
/searchused.aspx | 1354 | 5 | 3.6 | 0 | TRAP: big traffic, zero leads
/car-maintenance-by-mileage | 1340 | 3 | 10.6 | 34 | KILLER-CAND: leads + visibility gap
/aboutus.aspx | 1240 | 1 | 11.5 | 46 | KILLER-CAND: leads + visibility gap
/new-cars | 927 | 0 | 13.6 | 36 | KILLER-CAND: leads + visibility gap
/highlander-vs-grand-highlander | 829 | 1 | 24.4 | 14 | KILLER-CAND: leads + visibility gap
/used-trucks | 562 | 3 | 33.5 | 116 | KILLER-CAND: leads + visibility gap
/used-suvs | 515 | 1 | 23.5 | 92 | KILLER-CAND: leads + visibility gap
/testdrive.aspx | 504 | 0 | 26.4 | 34 | KILLER-CAND: leads + visibility gap
/locations.html | 481 | 1 | 17.6 | 16 | KILLER-CAND: leads + visibility gap
/service-area | 467 | 0 | 29.5 | 0 | TRAP: big traffic, zero leads
/blog/heavy-duty-vs-light-duty-trucks | 417 | 1 | 13.1 | 0 | TRAP: big traffic, zero leads
/blog | 404 | 1 | 15.7 | 220 | KILLER-CAND: leads + visibility gap
```


## AI-Mode citation check 2026-09-23 (DFS $0.004, gap closed)
Query: 'best used truck dealer near carroll iowa' — Google AI Mode cites 12 dealer refs:
Choice Auto (1st), Wittrock, Pro Auto, Motor Inn Chevrolet Carroll (4th), Car Stop, Thiel,
Toms Trucks, Ascendance, Champion Ford, Motor Inn Toyota+Chevrolet (10th), New Way Ford, Farmer.
=> Motor Inn cited 2x/12 in AI answer. Choice Auto leads. Also: our GSC top-10 for
'car dealerships carroll iowa' does NOT include choiceauto/billionauto but AI Mode does.
Next: consistency hunt on the exact business details AI reads (hours/address/phone).


## NAP consistency check 2026-09-23 (DFS my_business_info, gap closed)
GBP (what AI Mode reads): 'Motor Inn Toyota and Chevrolet of Carroll' | +1712-792-5000 |
1526 Le Clark Rd, Carroll, IA 51401 | 4.6 stars / 225 reviews | category: Toyota dealer
Website footer: 1526 Le Clark Rd / 712-792-5000 -> MATCH.
Open item: 'Motor Inn Chevrolet Carroll' and 'Motor Inn of Carroll Iowa' queries return
NONE -> the Chevy store has no distinct GBP listing surfaced by name; hours null on GBP.
Action queued: verify Chevy-store GBP existence + add hours to GBP.
