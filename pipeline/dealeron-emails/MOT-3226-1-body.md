Subject: og:image missing on homepage and vehicle detail templates

Hello DealerOn team,

One change request for the Motor Inn Auto Group site (www.motorinnautogroup.com):

1) Add an og:image meta tag to the homepage template and the vehicle detail (VDP) template.

Evidence: the homepage <head> contains og:title, og:type, og:url and og:description, but no og:image (checked in the served HTML today). Vehicle detail pages have no og:image either. As a result, links shared to Facebook/X/LinkedIn/iMessage render without a preview image.

Request: set the homepage og:image to the dealership logo or storefront hero image (absolute URL, min 1200x630 recommended), and on vehicle templates use the primary vehicle photo as og:image. Please keep absolute https URLs.

Verify step: curl the homepage and one VDP and confirm a <meta property="og:image" content="https://..."> tag that resolves HTTP 200.

Please confirm when this is deployed.

Thank you,
Spencer Heywood
Motor Inn Auto Group — Carroll, IA
