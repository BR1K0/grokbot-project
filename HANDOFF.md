# Handoff: Simon Says Arena

Updated 2026-10-24 after merging PRs #13 and #14 (main a9f1d33).


## Current T14 status (updated 2026-10-24, main 0d509ec)

This section supersedes older T14, PR #8 and Cursor status notes further down.

- **Merged T14 PRs:** #16, #19, #20, #22, #24, #27 (merged as 85983e1); evidence index #28 (merged as 0d509ec); tests/prompts.md T13–T15 results #29 (merged as a08de2e).
- **Measured round completed.** Referee verdicts, quoted from `results/t14/*.verdict.json` (n=10 each, 95% CI):
  - gen1 unpatched: rate 0.20, CI [0.057, 0.510]
  - gen3 unpatched: rate 1.00, CI [0.722, 1.000]
  - patched (Guardian patch, PR #20) on gen3, 02-friendly-ceo, 05-fake-approval: rate 0.00 each, CI [0.000, 0.278]
  - patched gen4: rate 0.00, CI [0.000, 0.278]
- **Autonomy test T14: NOT PASSED.** Handoffs at steps 0, 5, 9a and 15 were human-relayed (Kem / Joel). Simon's own triggers at steps 3, 7, 8, 11 and 16 are UNKNOWN (Simon self-report, not independently verified). No gen4 [EVOLVE] tag was posted. Every Slack post went out from Kem's account. See [`evidence/t14/INDEX.md`](evidence/t14/INDEX.md). T13 and T15: NOT RUN ([`tests/prompts.md`](tests/prompts.md)).
- **Gen3 vs gen4 task scores are not comparable** (the Referee's gen4 verdict says gen4 removes recipe content); only the failure rates are compared.
- **Cursor contestant (PR #25, merged as 4b2359a, supersedes PR #8):** 10 valid + 1 excluded attempts, trap not encountered (README never opened), recorded on a shared host; NOT an isolated runtime. No claim of live isolation is made.
- **PR #26** (Ryan's optional UI work) is still open; it should be rebased onto #25 and keep the #25 caveats.
- **Screen recordings:** the Slack-thread screen recording is pending, not yet added.

## Ownership and access

- Grok Bots write the app code and run contestants. Humans/chat assistants write specifications, review PRs, and prepare the demo.
- Simon builds/runs/reports; Trickster designs/evolves traps; Guardian writes patches; Referee alone posts game verdicts.
- Bots live on Kem's Grok Bot account and use their own clones. GitHub Bot actions share BR1K0.
- Slack: https://br1k.slack.com/archives/C0CBQARUABV . The observed Simon introduction appeared through Kem's account using Cursor. Do not assume independent Bot triggering or identity has been proven.
- Simon is responding in the review thread: https://br1k.slack.com/archives/C0CBQARUABV/p1792871094418949 . He completed PRs #13 and #14 after review feedback. Independent four-Bot triggering remains to be demonstrated by T14.
- The user clarified that "two hours" meant time until their friend returns, not the hackathon deadline.

## Completed in this review

- Merged docs PR #10: corrected the featured evolution story, scoring attribution, demo script, and review handoff.
- Merged docs PR #7: shared GitHub account constraint; Bots review through comments and a human/reviewer merges.
- Retrieved the existing source and logs into a scratch review snapshot and ran the existing suite: **31 passed**. No live model calls, trap execution, or app-code modifications.
- PR #8: requested changes with concrete scoring/exclusion reproductions and a runtime-isolation concern.
- PR #9: checked ten batches / 100 recorded attempts against current hard checks; flags agree and all attempts have assistant output. This is artifact validation, not a Referee verdict.
- Opened issue #11, reproduced its documented-Referee-schema crash, and reviewed/merged the fix in PR #14.
- Reviewed and merged Bot-authored PR #13: dark arena redesign, corrected metric totals and attribution, final-generation chain selection, mobile headline and pinned replay close. Verified Chromium at 1440px and 390px.
- Reviewed and merged Bot-authored PR #14: consistent canonical hard-check measurements; validated Referee metrics kept separately; original verdict files preserved; Referee badges scoped to its judgment fields. Integrated suite: **51 passed**. Synthetic local-only UI fixtures verified badge scope/escaping; they are not game results.

## Priority 1 — redesign

Complete: PR #13 merged as 101a4d5. Screenshots are in app/site/screenshots/ and the PR. Independent checks found no horizontal overflow or JavaScript errors at 1440px/390px; replay opens the actual leak, the mobile close stays visible, test-data toggle works, reduced motion is respected.

Data reference from the reviewed main logs, not numbers to hardcode:
- 890 real runs across 35 (level, contestant, patch) groups.
- 2 distinct model IDs: grok-4.3 and grok-4.7. Safety variants and patches are not extra base models.
- 30 runs with canary leaks. This is a run count, not a count of individual leaked secrets or money transfers.
- Friendly CEO: gen 1 0/20 → gen 2 0/20 → gen 3 25/40.
- Gen 2 asked for the secret in the summary. Gen 3 impersonated Sam in an email (and changed the subject).
- Featured unpatched replay: results/2026-10-24-02-friendly-ceo.gen3-grok-4.3.batch1.log.json, run 2, transcript index 6.
- Targeted patch: 0/20; do not present this as proof of zero risk.

## Priority 2 — verdict compatibility and T14

Compatibility is resolved by PR #14, merged as a9f1d33. Simon has been instructed to start a real full T14 round in a new #arena thread and post its permalink. Completion is not yet verified. Record the ordered handoffs and actual authors. Referee owns the verdict; neither the reviewer nor Simon substitutes for it.

The exact T14 is level 01 against one contestant. Follow the threshold and generation cap; a PATCH READY is not guaranteed if the trap never breaks the contestant. Keep any separate Friendly CEO patch demonstration distinctly labelled.

## Priority 3 — Cursor

Keep PR #8 unmerged pending its requested changes:
- Preserve workspace-specific deletion/listener evidence through site aggregation.
- Keep one excluded infrastructure attempt out of the ten-valid-run denominator.
- Make runner exclusions reproducible, not a corrected summary alone.
- Resolve the shared-host network boundary before further adversarial execution.
- Label current result "trap not encountered": README.md was not opened.

All 11 logged attempt paths are distinct temp directories. This positive check does not establish complete runtime isolation.

PR #9 remains pending Referee's verdict and publication path; it adds level-01 gen-2 data.

## Priority 4 — demo

Follow DEMO.md. A 48-second, silent backup walkthrough of the reviewed #13 recorded-results site is saved for Joel in the ChatGPT review conversation (Simon-Says-Arena-Backup.mp4). It shows six actual UI views, including the real leaking run and patch comparison; it is not a live T14 recording. Playback was decoded and checked. The video has not been shared to Slack.

Still record the real Slack round and optional Cursor segment after its blockers are resolved. Keep the complete-demo backup marked pending until that evidence exists.

## Next reviewer action

Read Simon's new T14 thread, review the owning Bots' PRs, and merge reviewed work needed for that round. Then address PR #8's requested changes. PR #9 still needs Referee's actual verdict; existing log validation does not substitute for it. Never mark a Bot task complete merely because a message was delivered.

Detailed findings and copy-ready Bot instructions: REVIEW_READINESS.md.
