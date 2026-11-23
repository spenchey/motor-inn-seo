# Adversarial QA confirmation: c7eeb99 — overall verdict FAIL

**1 BLOCKING, 2 MINOR.** Retired contact copy remains in a handoff labeled approved for publishing (C-001). The approved 75-year wording, FAQ parity, changed-copy voice, and generator checks pass.

- **Date / branch:** 2026-11-23 / `seo/page-plan-2026-11-23`.
- **Reviewed delta:** `git diff --find-renames 2670c24 c7eeb99`; HEAD is `c7eeb99d08743be16f4fd01f705d11b7c661d1ce`. The working tree was initially clean.
- **Baseline:** `brain/reports/2026-11-23-pages-codex-adversarial-rerun2-2026-11-23.md`. Its prior PASS and the five supplied owner decisions are accepted. This review does not reopen unchanged content or debate those decisions.
- **Authority:** report-only. Only this report was written. Read-only Git commands; no rebuild, fixes, tests created, network requests, account changes, sends, deployment, or publication. Existing delivery artifacts were inspected solely to verify the retirement references required by C4.
- **Tools / limits:** local Git, Python 3.13.6, text reads, graph discovery, and read-only ZIP inspection without extraction. The graph had no matching batch-source nodes, so source inspection used direct reads. No total probe deadline; commands completed within finite tool timeouts. Total session elapsed and aggregate command time: unmeasured. Checks stopped after scoped coverage.

## Check table

| Check | Verdict | Evidence |
|---|---|---|
| C1 — Claim accuracy | **PASS** | All six changed shopper passages add only the approved family-ownership duration. “More than 75 years” faithfully renders the supplied decision together with owner-verified “75+”; no extra location-history, generation, founding-year, or franchise-duration claim. Detailed passage review below. |
| C2 — FAQ parity | **PASS** | Independently parsed actual saved questions **and answers**, in order: schema FAQPage == faq.md == content FAQ == AI Q&A. **38/38 pairs across nine packages**, including all 15 pairs on the three pages with changed shopper copy. No faq.md or schema.json changed in this commit. |
| C3 — Voice | **PASS for the delta** | Changed passages are grammatical, preserve direct answers and entity identification, and contain no VOICE-DNA banned term or workflow language. No new CTA or heading change. Previously accepted placement instructions remain outside shopper copy; no new workflow text enters AI summaries. |
| C4 — Plan, briefs, retirement | **FAIL** | Sections 4/5/6/9 consistently record the 301 choice, Carroll-only stores, 75-year wording, and outstanding property-owner GSC action. All three moves are exact; referenced truck delivery exists. However, retirement leaves an explicitly publishable older contact handoff unwithdrawn (C-001), plus two minor documentation inconsistencies (C-002/003). |
| C5 — Regression / generation | **PASS** | Requested validator exits **0**, `RESULT: PASS`, with ten existing filter warnings. **55/55 generated artifacts match byte-for-byte**, including all 54 package/AI files and `_manifest.json`. Rendering functions were called in memory with write/network/subprocess attempts blocked; none occurred. `build.main()` was never called. |

## Findings

### C-001 — BLOCKING — Retired contact copy remains in a handoff labeled approved for publishing

- **File:line:** `content/ready-design/_retired/2026-11-23/README.md:11`; related decision record `docs/page-plans/page-plan-2026-11-23.md:166`.
- **Expected:** C4 requires no remaining reference to offer a retired draft as a live publishing candidate. Retirement notes must identify and withdraw competing delivery instructions, while preserving historical files.
- **Observed:** The new README flags the older built **truck** copy and the contact **source drafts**, but omits the built contact copy and its DealerOn ZIP. That ZIP still presents the retired contact alternative as approved for `/contactus.aspx`, the same destination now assigned exclusively to package #2. A built Tacoma copy also remains outside the retirement inventory.
- **Evidence:**
  - `deliveries/site-packages/2026-11-04/motorinnautogroup/contactus-money-page/metadata.json:10` names `content/ready-design/contactus-money-page.html` as its source; `:5` sets `/contactus.aspx`. Its `index.html` exists. The sibling `README-HANDOFF.md:12` includes this page, and `:29–31` instruct creation and pasting of the included pages.
  - `deliveries/dealeron-handoff-2026-11-06.zip!README-DEALERON.md:4` says “Ten final, approved, QA-checked pages for DealerOn publishing.” `!EMAIL-DRAFT.md:5` asks DealerOn to publish those ten approved pages.
  - `!metadata-all.csv:4` includes `contactus-money-page` at `/contactus.aspx`; `!pages/contactus-money-page/PLACEMENT.md:4` specifies that path, and `:10` says to publish it. Both body-only and full-HTML copies exist inside the ZIP.
  - Read-only `zipfile.ZipFile` inspection found **zero retirement, supersession, withdrawal, or hold markers** in the archive's Markdown/CSV/JSON/text instructions. `git ls-tree -r --name-only c7eeb99 -- deliveries/dealeron-handoff-2026-11-06.zip` confirms the ZIP belongs to the reviewed commit, rather than being a stray local file.
  - `deliveries/site-packages/2026-11-06/motorinnautogroup/toyota-tacoma-carroll-iowa/metadata.json:10` still names the retired Tacoma source, `:5` sets the older group-site canonical, and its built `index.html` exists. This corroborates that the new cleanup inventory covers only part of the retained delivery material; the explicit contact publish instructions above establish the blocker.
- **Confirmation / scope:** Static file existence, metadata, and archive instructions were directly read. Their current publication-candidate wording conflicts with the new retirement decision. Actual prior sending or live publication was not checked or inferred. This blocks the requested retirement confirmation, without changing the prior copy-quality PASS.
- **Suggested fix:** Extend the retirement inventory and explicitly withdraw the superseded contact delivery/ZIP entry and older Tacoma delivery from future handoff. Preserve historical artifacts, but label superseded packets clearly; revise any packet still intended for delivery so its contents, metadata, placement instructions, and publish-request count exclude retired alternatives. Keep the already documented truck hold.

### C-002 — MINOR — Retirement README incorrectly says the contact drafts have the same H1

- **File:line:** `content/ready-design/_retired/2026-11-23/README.md:7`.
- **Expected:** The new retirement rationale accurately describes both artifacts.
- **Observed:** It says “Same page and H1.” The destination and intent agree, but the H1 text differs.
- **Evidence:** Retired `contactus-money-page.html:12` has `<h1>Car Dealerships in Carroll, Iowa</h1>`. New `content/page-packages/2026-11-23/contactus-carroll/content.md:3` is `# Car Dealerships in Carroll, Iowa: Motor Inn Auto Group`. The retired file's canonical at `:8` is `/contactus.aspx`.
- **Confirmation:** Direct HTML heading extraction and line-numbered Markdown read. This is a rationale-label error; both still target the same contact destination.
- **Suggested fix:** Change the rationale to “Same contact destination and intent”; retain the current approved heading.

### C-003 — MINOR — Tacoma status still describes a draft at its removed active path

- **File:line:** `content/page-packages/2026-11-23/toyota-tacoma-tundra-for-sale-carroll-iowa/brief.md:19`; conflicting retained status at `:5`, generated from `_src/pages_toyota.py:116`.
- **Expected:** The brief's status and new routing note consistently identify the older draft as retired.
- **Observed:** The changed routing note correctly says the draft was retired and moved. The top status still says an unpublished `content/ready-design/toyota-tacoma-carroll-iowa.html` draft “exists.” That path no longer exists. Unlike the truck brief's revised status, this summary was left stale.
- **Evidence:** `brief.md:5` retains the active-path sentence; `:19` records retirement. Filesystem checks show the old path absent and `_retired/2026-11-23/toyota-tacoma-carroll-iowa.html` present. The stale status sentence predates this commit; its inconsistency with the new retirement is the scoped finding, rather than a new review of the old draft's content.
- **Confirmation:** Direct status/routing reads and path-existence checks. The routing note supplies the correct decision, so this remains minor.
- **Suggested fix:** Update the generator status to say the earlier draft was retired at its archive path, and regenerate the brief in a separately authorized repair.

## Changed shopper-copy review

Only three content passages and three AI summary passages changed. The family-owned identity is already established by `brain/VOICE-DNA.md:3`; the owner verified “75+ years” in `content/ready-design-OWNER-NOTES.md:8`. The supplied decision authorizes using 75, with source attribution added in `_src/facts.py:40–43` and all nine briefs. Existing addresses, phones, store relationships, and services in the edited sentences retain their prior cited sources and passed wording.

| Package / actual lines | Reading and judgment |
|---|---|
| `contactus-carroll/content.md:11`; `ai/contactus-carroll.md:3` | “It has been family-owned…” refers to Motor Inn Auto Group. The AI appositive “family-owned for more than 75 years” likewise modifies that group/dealership. The present address is separate from the duration; neither sentence says it occupied Le Clark Road for 75 years. Grammatical and consistent. |
| `chevy-dealer-carroll-iowa/content.md:13`; `ai/chevy-dealer-carroll-iowa.md:3` | The body explicitly assigns the duration to “Motor Inn Auto Group, a dealership group…that has been family-owned…”. The AI phrase follows the same named parent group. Neither assigns 75 years to the Chevrolet franchise or its present premises. Grammatical and consistent. |
| `toyota-dealers-in-iowa/content.md:9`; `ai/toyota-dealers-in-iowa.md:3` | The body uses “Motor Inn has been family-owned…”; the AI spells out Motor Inn Auto Group as the parent with that duration. This expresses the shared Motor Inn history, without saying the Toyota franchise or Carroll building is 75 years old. Grammatical and consistent. |

“More than 75 years” is a faithful plain-language expansion of the explicitly owner-verified “75+” in this task. No precision about an opening date, family generations, unbroken location tenure, or the age of either individual franchise has been added. The comma-heavy AI sentences can be shortened stylistically, but they remain grammatical and do not establish a claim defect.

The unchanged first answers remain direct: contact identifies the Carroll dealership group; Chevy answers “Yes”; Toyota identifies the Iowa dealer and location before adding the age sentence. No owner attribution, retirement, access request, or production instruction was inserted into shopper copy or AI mirrors.

## Regression evidence

Native command, from the repository root:

```sh
python3 -B content/page-packages/2026-11-23/_src/validate.py
```

Exit **0**; observed output:

```text
checked 9 packages
WARN [chevy-blazer-for-sale-carroll-iowa] filtered link needs click-test: https://www.motorinnofcarroll.com/searchnew.aspx?Model=Blazer
WARN [chevy-blazer-for-sale-carroll-iowa] filtered link needs click-test: https://www.motorinnofcarroll.com/searchnew.aspx?Model=Blazer%20EV
WARN [chevy-suvs-for-sale-carroll-iowa] filtered link needs click-test: https://www.motorinnofcarroll.com/searchnew.aspx?Model=Suburban
WARN [chevy-trucks-for-sale-carroll-iowa] filtered link needs click-test: https://www.motorinnofcarroll.com/searchnew.aspx?Model=Colorado
WARN [chevy-trucks-for-sale-carroll-iowa] filtered link needs click-test: https://www.motorinnofcarroll.com/searchnew.aspx?Model=Silverado%201500
WARN [chevy-trucks-for-sale-carroll-iowa] filtered link needs click-test: https://www.motorinnofcarroll.com/searchnew.aspx?Model=Silverado%202500%20HD
WARN [toyota-sequoia-sienna-for-sale-carroll-iowa] filtered link needs click-test: https://www.motorinntoyotaofcarroll.com/searchnew.aspx?Model=Sequoia
WARN [toyota-sequoia-sienna-for-sale-carroll-iowa] filtered link needs click-test: https://www.motorinntoyotaofcarroll.com/searchnew.aspx?Model=Sienna
WARN [toyota-tacoma-tundra-for-sale-carroll-iowa] filtered link needs click-test: https://www.motorinntoyotaofcarroll.com/searchnew.aspx?Model=Tacoma
WARN [toyota-tacoma-tundra-for-sale-carroll-iowa] filtered link needs click-test: https://www.motorinntoyotaofcarroll.com/searchnew.aspx?Model=Tundra
RESULT: PASS
```

These URLs and filters are unchanged by the delta. Their prior live click-test evidence remains in the accepted rerun2 report; this offline confirmation made no fresh live-link claim.

The independent in-memory comparison imported `build.py` with `python3 -B`, called `load_evidence`, `build_brief`, `build_content`, `build_faq`, `build_meta`, `build_schema`, and `build_ai`, and reproduced manifest serialization. Every returned string was compared with the saved UTF-8 bytes. A Python audit hook rejected file writes, filesystem mutations, sockets, and subprocesses during this check. Observed summary:

```json
{
  "generated_artifacts_compared": 55,
  "package_artifacts": 54,
  "manifest_included": true,
  "generator_mismatches": [],
  "total_faq_pairs": 38,
  "blocked_write_or_network_attempts": [],
  "build_main_called": false,
  "errors": []
}
```

Actual FAQ parity counts: contact 5, used 5, Chevy dealer 5, Chevy SUVs 4, Blazer 4, Chevy trucks 3, Toyota dealer 5, Tacoma/Tundra 3, Sequoia/Sienna 4. Every ordered question/answer pair matched verbatim across all four saved representations. This independently covers answer text, beyond the native validator's question-list comparison.

## Retirement and decision checks that passed

- All three old ready-design paths are absent; all three `_retired/2026-11-23/` files exist. Their bytes equal their respective `git show 2670c24:<original-path>` blobs. Git reports **R100** for each move. No archived HTML body was changed.
- The README's truck delivery directory exists and contains `index.html` and `metadata.json`; its source and group canonical match the retired truck draft. The six-page batch description matches `deliveries/site-packages/2026-11-05/motorinnautogroup/README-HANDOFF.md:3–9`.
- Both referenced contact source files, `content/drafts/seo/contactus-money-page-draft.html` and `contactus-money-page-REVIEW.md`, exist.
- Plan section 4 and contact brief `:22–24,55` consistently select 301s for both duplicate dealership URLs to `/contactus.aspx`, after the cycle-1 block is live, with internal-link follow-up. This is the recorded action plan; implementation was not claimed or tested.
- Plan sections 5 and 9 and Chevy brief `:113` drop the non-Carroll store queries. Existing potentially conflicting content is disclosed in section 6; no new out-of-town store appears in the changed shopper copy.
- Plan section 6, item 4, and section 9, item 5, correctly retain Chevy Search Console as an outstanding action requiring a property owner. No claim of access repair or fresh account verification is made by this review.
- Historical research, QA results, and logs mentioning the older drafts were treated as history. C-001 is specifically supported by surviving **publish instructions and approved-candidate labels**, rather than by a historical filename alone.

## Check plan and cleanup

The pre-probe check plan covered C1 changed-sentence sourcing and entity scope; C2 exact saved FAQ questions/answers; C3 changed-copy voice and workflow leakage; C4 plan sections, retirement identity, paths, and current-versus-historical references; C5 native validation, in-memory generation, and input integrity. Isolation used existing local files only, with no fixture creation or external destination. All five checks were completed; C4 has the findings above.

Before finalizing, SHA-256 comparisons covered **2,034 repository paths plus `.git/index`** against the pre-probe snapshot: **zero changed, added, or removed paths outside this report**. The Git index hash remained `4a949dcdce623bdaec7e8072f2b8d84a91bf5edd954ea156768b0a1896359ec4`. Git status showed only this untracked report on the requested branch. No prior report, package, source, test, cache, manifest, or archive was edited. Extra skill evidence, telemetry, and learning files were omitted under the single-file rule.

Opened only short-lived local shell/Python processes; all completed and exited. No GUI app, browser tab, server, watcher, SSH session, tunnel, or background job was opened. Nothing remains to close. Findings contain suggested fixes only; none was applied.
