From: spencer.heywood@motorinnmail.com
To: help@dealeron.com
Subject: Motor Inn of Carroll — Soft 404: windowsticker "not found" placeholder served as HTTP 200 PDF
Status: DRAFT — not sent. Requires Spencer's approval.

Body:

Hi DealerOn team,

One Search Console "Soft 404" is currently flagged on the Chevrolet property
(https://www.motorinnofcarroll.com/) and, based on the same behavior on our other
Motor Inn sites, it appears to originate in the shared window-sticker component.

Evidence:
- URL: https://www.motorinnofcarroll.com/resources/components/windowstickers/windowstickernotfound.pdf
- Returns HTTP 200 with Content-Type application/pdf (65,422 bytes).
- The PDF contains only a placeholder 1046x632 image and no selectable text
  (pdftotext output is a single blank page). It is the "window sticker not found"
  placeholder, not a real vehicle window sticker.
- The same placeholder is served at 200 on:
  - https://www.motorinnautogroup.com/resources/components/windowstickers/windowstickernotfound.pdf
  - https://www.motorinntoyotaofcarroll.com/resources/components/windowstickers/windowstickernotfound.pdf

Diagnosis: when a real window sticker is unavailable, the component serves the
placeholder at 200 instead of a 404, so Google indexes it as a Soft 404.

Requested fix
-------------
Please change the window-sticker component so that when a real sticker is missing it
returns HTTP 404 (or 410) instead of the 200 placeholder PDF, and remove/410 the
placeholder file itself. This eliminates the Soft 404s flagged in Search Console.

We have not changed anything in Search Console and are not validating the fix yet;
we'd like the underlying serving change first, then we can re-check the report.

Thank you,
Spencer Heywood
Motor Inn Auto Group
