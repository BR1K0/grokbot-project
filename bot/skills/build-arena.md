# Skill: Build arena

**Use when:** told `build milestone <N>` (in chat or #arena), or a reviewer leaves change requests on one of your `bot/build-*` PRs.

**Inputs:** `app/README.md` (the spec), `levels/`, any review comments.

**Steps:**
1. `git pull` on `main`. Read `app/README.md` and find milestone N.
2. Create branch `bot/build-m<N>-<short-name>`.
3. Build only milestone N. Write small, readable code with a short README section for anything a teammate needs to run it.
4. **Test it yourself on your computer** before opening the PR: for the harness, run it on `levels/01-poisoned-webpage.yaml` with at least one contestant and paste the summary output into the PR description. Report only what that milestone has built: a failure rate from milestone 1, and the Wilson confidence interval and cost estimate from milestone 2 onwards. If a run needs a credential you don't have yet, test against the offline stub contestants, say so in the PR, and post the real run as soon as the credential lands.
5. Put any API keys only in `.env` (gitignored). Never print them in logs or PRs.
6. Open a PR titled `Milestone N: <name>` describing what you built, how you tested it, and anything you were unsure about.
7. Post the PR link in #arena and ask for a review.
8. If reviewers request changes, push fixes to the same branch and reply to each comment.

**Done when:** the PR is open, tested, and announced. Merging is a human's job.

**Never:** push to `main`. Never skip milestones. Never change the spec in `app/README.md` yourself; if it's wrong, say so in the PR.

**Test:** `tests/prompts.md` → T12
