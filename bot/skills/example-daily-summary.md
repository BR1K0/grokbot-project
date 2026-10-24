# Skill: Daily summary (example, replace or delete)

**Use when:** the daily-digest routine runs, or a user asks "what happened today?"

**Inputs:** the demo Slack channel #updates

**Steps:**
1. Read every message in #updates from the last 24 hours.
2. Group them by topic.
3. Write at most 5 bullet points, most important first.
4. Post the summary as a reply in #updates.

**Done when:** a single summary message is posted in #updates.

**Never:** post in any other channel. Never post twice in one day.

**Test:** `tests/prompts.md` → T1
