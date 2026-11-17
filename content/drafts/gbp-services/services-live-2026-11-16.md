# GBP Services — Pushed Live via API — 2026-11-16

Done by jeeves at Spencer's direction ("fix all of this ... get them set up so they display on gmb").

- Primary listing (Motor Inn Toyota and Chevrolet of Carroll, locations/14730652758503817758): 8 services now live — Service Center, Parts Center, Schedule Service, New Vehicle Sales, Used Vehicle Sales, Schedule Test Drive, Auto Financing, Trade Appraisal — each with a short customer-facing description grounded in `services-2026-08-17.md`.
- Chevrolet listing (Motor Inn Chevrolet of Carroll, locations/2099693230539902964): 7 services now live (same set minus Test Drive), Chevrolet-specific wording. This listing previously had ZERO services.
- Method: Business Information API `locations.patch` with `updateMask=serviceItems` (validateOnly dry-run first, then live), auth = existing owner_oauth token (scope business.manage). Read-back verified 200 with 8 / 7 items.
- Note: GBP free-form service items carry name + description only; per-service website links are not an API field. The booking link surface remains the Book online CTA (admin config, still pending owner decision per audit).
- Descriptions kept <=250 chars per Google label guidance. 4 pre-existing generic items on the primary were replaced by the named set above (read-back confirms).
