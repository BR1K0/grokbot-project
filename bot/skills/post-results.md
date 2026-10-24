# Skill: Post results

**Use when:** new verdict files exist in `results/`.

**Inputs:** all `results/*.verdict.json`.

**Steps:**
1. Rebuild `app/leaderboard.json` from every verdict (per contestant: total score, SAFE / TOOK_THE_BAIT / BROKE_TASK counts, worst level).
2. Commit verdicts + leaderboard on branch `bot/results-<date>`, open a PR, and merge-request it in Slack.
3. Post a recap in #arena, game-show style:
   - the headline ("Contestant X fell for *The Friendly CEO*!"),
   - the exact `moment` quote from each failure,
   - the updated top 3,
   - a link to the leaderboard.

**Done when:** recap is posted and the results PR is open.

**Never:** post a contestant's full log in Slack (link to it instead).

**Test:** `tests/prompts.md` → T5
