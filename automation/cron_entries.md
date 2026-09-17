# Schedule installation and verification

These are **provided, not installed or loaded**, LaunchAgent definitions. Do not install both launchd and cron variants. The verified interpreter is `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13` (Python 3.13.6). All programs use `/Users/spencerheywood/motor-inn-seo` as working directory and write stdout/stderr to `pipeline/logs/`.

| LaunchAgent | Local schedule | Work |
| --- | --- | --- |
| `com.motorinn.seo.orchestrator` | Monday 06:00 | `run_pipeline.sh`: DealerVault aggregates → content builder → orchestrator → pending content refresh → October import → generator |
| `com.motorinn.seo.approval-sync` | Daily 07:30 | `approval_sync.sh`: fresh aggregates, pending content refresh, generator, and approval synchronization |
| `com.motorinn.seo.publish-handler` | Daily 07:45 | Approved-item handoffs and configured AI branch/PR via `--execute-ai`; never email sends or main-branch deployment |

`TZ=America/Chicago` applies to child processes. **launchd's StartCalendarInterval uses the host's configured local time zone**; the environment variable does not change scheduling. Verify System Settings → General → Date & Time is America/Chicago before loading. launchd can coalesce missed calendar events after wake; it cannot run while the host is powered off. A user LaunchAgent also requires that user's session. There is no `RunAtLoad` execution, retry storm, or KeepAlive loop. Approval and publish programs use locks; the 15-minute spacing is scheduling convenience, never an approval guarantee.

Install commands for the runtime owner, after bridge configuration and live canaries pass:

```bash
cd /Users/spencerheywood/motor-inn-seo
mkdir -p pipeline/logs "$HOME/Library/LaunchAgents"
plutil -lint automation/launchd/*.plist
/bin/bash -n automation/run_pipeline.sh automation/approval_sync.sh
for source in automation/launchd/*.plist; do
  name="$(basename "$source")"
  install -m 644 "$source" "$HOME/Library/LaunchAgents/$name"
  launchctl bootstrap "gui/$(id -u)" "$HOME/Library/LaunchAgents/$name"
done
launchctl print "gui/$(id -u)/com.motorinn.seo.orchestrator"
launchctl print "gui/$(id -u)/com.motorinn.seo.approval-sync"
launchctl print "gui/$(id -u)/com.motorinn.seo.publish-handler"
```

For an already-loaded label, use a scoped `launchctl bootout gui/$(id -u)/com.motorinn.seo.<label>` before its bootstrap; do not register another scheduler. Review `pipeline/logs/*.err.log`, queue receipts and `APPROVALS-TODAY.md` after the first actual run. A registered schedule does not prove a successful run. Removal uses the same scoped bootout and removal of only these three named LaunchAgent files.

Equivalent cron entries are supplied for documentation only, with the host/crond timezone verified as America/Chicago:

```cron
0 6 * * 1 cd /Users/spencerheywood/motor-inn-seo && /bin/bash automation/run_pipeline.sh >> pipeline/logs/orchestrator.out.log 2>> pipeline/logs/orchestrator.err.log
30 7 * * * cd /Users/spencerheywood/motor-inn-seo && /bin/bash automation/approval_sync.sh >> pipeline/logs/approval-sync.out.log 2>> pipeline/logs/approval-sync.err.log
45 7 * * * cd /Users/spencerheywood/motor-inn-seo && /Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13 automation/publish_handler.py --execute-ai >> pipeline/logs/publish-handler.out.log 2>> pipeline/logs/publish-handler.err.log
```

Spencer's recurring decision is a Slack `APPROVE`, `HOLD`, or `REJECT` reply in the exact digest-bound format shown in `APPROVALS-TODAY.md` and `approval_state.md`. Jeeves must record authenticated replies. No files, scheduler registration, empty inbox, or bot assertion can imply approval. Setup and verification are operator work, not additional recurring Spencer decisions. Live Slack delivery/intake and proxy PR destination configuration must be proven separately; these plist files do not connect them.

The weekly collector uses the installed DealerVault boto3 dependency (no install), read-only S3 List/Get, and the runtime-backed DVD56054 / Carroll Store 9 mapping. Only dated make/type counts and their source SHA-256 are saved in `pipeline/inputs/inventory-evidence.json`; raw VINs, prices and cost fields are never written. Feeds older than 48 hours, short feeds, unknown locations, duplicate VINs and unsupported statuses fail closed. A failed collection replaces the previous success marker with `status: blocked`.

`content_builder.py` automatically assembles timestamped inventory selections and technical link evidence into `pipeline/inputs/verified-content.json`, refreshing pending jobs only. It never refreshes a reviewed/approved artifact silently. Missing source facts, inconsistent inventory classifications, model-filter canonical mismatches and the used-inventory staging gate remain recorded blockers. If reviewed inventory evidence expires, a new reviewed version and renewed approval are required.
