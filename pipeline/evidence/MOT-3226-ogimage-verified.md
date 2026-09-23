# MOT-3226 evidence — og:image live on homepage + VDPs (2026-09-23 tick)

- DealerOn Case 01921779: deployed & confirmed. Our 'confirmed' reply sent 2026-09-23, messageId 1a0cbc66d1a71e21 (thread 1a0c9527afd362d3).
- Live check (from nada-mini, curl):
  - Homepage https://www.motorinnautogroup.com/ → og:image = https://www.motorinnautogroup.com/static/dealer-32375/logo.png
  - VDP /used-Carroll-2022-Toyota-Highlander-XLE-5TDHZRBH1NS243448 → same og:image tag present
  - VDP /new-Carroll-2026-Chevrolet-Trax-LT-KL77LHEP4TC193487 → same og:image tag present
  - logo.png HTTP status: 200 (content-length 701415)
- Criterion C4 (og:image present and resolving 200 on homepage + VDPs): PASS
- MOT-3226 marked Done.

