# GSC cannibalization + split-traffic audit — motorinnautogroup domain property
Window 2026-08-01..11-01, 5000 query-page rows. Generated 2026-11-03 via service account.

## Headline finding: UTM-parameter page duplicates
The contact page appears under 7 distinct URLs (utm_source/medium/campaign variants),
splitting click signals on the brand's most valuable queries. Google treats them as
distinct pages in reporting; canonicalization is inconsistent.

Fix: pick ONE canonical contact URL (no query params) sitewide; 301 the variants or
link uniformly. DealerOn case material.

## Brand-query split (top examples)

**motor inn carroll** (total 568 clicks)
-  400 clicks /  1557 impr  https://www.motorinnautogroup.com/Contactus/Carroll
-   91 clicks /  1568 impr  https://www.motorinnautogroup.com/
-   42 clicks /  1539 impr  https://www.motorinnautogroup.com/used-inventory

**motor inn carroll iowa** (total 481 clicks)
-  330 clicks /  1120 impr  https://www.motorinnautogroup.com/Contactus/Carroll
-   59 clicks /  1053 impr  https://www.motorinnautogroup.com/used-inventory
-   48 clicks /  1095 impr  https://www.motorinnautogroup.com/

**motor inn carroll ia** (total 232 clicks)
-  160 clicks /   673 impr  https://www.motorinnautogroup.com/Contactus/Carroll
-   38 clicks /   659 impr  https://www.motorinnautogroup.com/
-   23 clicks /   646 impr  https://www.motorinnautogroup.com/used-inventory

**motor inn** (total 149 clicks)
-   85 clicks /   569 impr  https://www.motorinnautogroup.com/Contactus/Carroll
-   46 clicks /   740 impr  https://www.motorinnautogroup.com/
-    9 clicks /   383 impr  https://www.motorinnautogroup.com/used-inventory

**carroll toyota** (total 115 clicks)
-  103 clicks /   307 impr  https://www.motorinnautogroup.com/Contactus/Carroll
-    4 clicks /   266 impr  https://www.motorinnautogroup.com/
-    4 clicks /   245 impr  https://www.motorinnautogroup.com/new-toyota

**toyota carroll iowa** (total 101 clicks)
-   76 clicks /   388 impr  https://www.motorinnautogroup.com/Contactus/Carroll
-   12 clicks /   370 impr  https://www.motorinnautogroup.com/
-    5 clicks /   194 impr  https://www.motorinnautogroup.com/used-inventory

**motor inn toyota of carroll** (total 97 clicks)
-   59 clicks /   234 impr  https://www.motorinnautogroup.com/Contactus/Carroll
-   18 clicks /   233 impr  https://www.motorinnautogroup.com/
-    9 clicks /   155 impr  https://www.motorinnautogroup.com/searchnew.aspx

**carroll iowa toyota** (total 64 clicks)
-   52 clicks /   170 impr  https://www.motorinnautogroup.com/Contactus/Carroll
-    9 clicks /   151 impr  https://www.motorinnautogroup.com/
-    2 clicks /   149 impr  https://www.motorinnautogroup.com/new-toyota

**motor inn of carroll** (total 63 clicks)
-   38 clicks /   210 impr  https://www.motorinnautogroup.com/Contactus/Carroll
-   23 clicks /   207 impr  https://www.motorinnautogroup.com/
-    1 clicks /   205 impr  https://www.motorinnautogroup.com/searchnew.aspx

**carroll iowa car dealerships** (total 59 clicks)
-   55 clicks /   172 impr  https://www.motorinnautogroup.com/Contactus/Carroll
-    4 clicks /   223 impr  https://www.motorinnautogroup.com/
-    0 clicks /    46 impr  https://www.motorinnautogroup.com/?utm_source=GoogleMyBusiness&utm_medium=Organic&utm_camp

## Action list
1. Canonicalize contact URL (kill utm variants in internal links) - DealerOn case.
2. 301 dead paths (already cased: email 1a19dd855a732939).
3. Brand queries: contact page wins - keep; add sameAs/entity to reinforce.