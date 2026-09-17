# Approval state and Jeeves bridge contract

Only an original human Slack message from the configured Spencer user in the configured channel can move a draft. Jobs move `pending → drafts → approved → ready`; `HOLD` and `REJECT` move to their separate terminal queues. Held/rejected work is not silently requeued. A changed draft requires a new digest and approval.

Spencer sees the generated `pipeline/APPROVALS-TODAY.md`: slug, target query, DataForSEO monthly volume (or unavailable), one-line outline, draft path and these commands, with the actual 64-character SHA-256 substituted:

```text
APPROVE page-slug <64-character-draft-digest>
HOLD page-slug <64-character-draft-digest>
REJECT page-slug <64-character-draft-digest>
```

Jeeves delivers the local `pipeline/handoffs/jeeves-approvals.json` markdown and forwards original Slack event bytes, timestamp and signature to:

```bash
python3 automation/approval_sync.py record --event /secure/path/event.json \
  --slack-timestamp "$SLACK_REQUEST_TIMESTAMP" \
  --slack-signature "$SLACK_REQUEST_SIGNATURE"
```

Configure `approval.spencer_slack_user_id`, `slack_channel_id`, `receipt_key_path` and `slack_signing_secret_path` in `automation/config.json`. Secret files must be outside this repository, owned by the runtime user and mode 0600. A trusted bridge must retain the exact HTTP body; reconstructing JSON changes its signature. The receiver verifies Slack v0 HMAC and five-minute request age, rejects bots, edits and replays, and records a Jeeves HMAC receipt bound to the slug and draft digest. Sync and publication both reverify the receipt and current artifacts. A self-authored JSON message claiming to be Spencer is insufficient.

Publication requires fresh evidence and fresh QA. The DealerOn branch creates local request packets and one weekly email draft; Jeeves receives an unsent handoff. The AI branch uses an isolated git worktree and non-main branch, and `--execute-ai` enables the approved push/PR step. No automatic merge exists.

Bridge delivery and intake are not installed by this build. Blank configuration fails closed. The exact Slack event/receipt flow is tested with temporary synthetic keys; that is not proof of a live Slack exchange. The operator must connect the bridge and prove delivery/intake before enabling schedules. This is setup work, not another recurring Spencer approval step.
