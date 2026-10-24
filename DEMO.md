# Demo script

**Length:** ~3 minutes. Owner: C

1. **Hook (20s):** "Every AI agent is told: only obey your user. We built a game to check whether they actually do. The game master is a Grok Bot named Simon, and Simon built the whole arena himself."
2. **Leaderboard (20s):** last night's tournament, run on its own by Simon's nightly routine. Ranked by *generations to break*. Point at the model that held out longest.
3. **Evolution (40s):** open one level's evolution chain. Gen 1 refused ("spotted the fake domain"). Gen 2 fixed the domain. Gen 3 added urgency, and it broke. Show the red-highlighted moment in the replay.
4. **Live trap (50s):** ask a judge for a trap idea. Type it in Slack as `trap idea: …`. Simon builds the level, runs the contestant 10 times, posts the failure rate.
4b. **Real agent (30s):** Cursor's coding agent gets *The Cursed README*: fix one typo. Show the folder before/after and whether the canary listener caught a request.
5. **The fix (30s):** Simon's patch for that failure, then the before → after chart: e.g. 70% → 10%, no regressions.
6. **Why Grokbots (20s):** four Grok Bots, one arms race. Scroll the #arena thread: Trickster's `[LEVEL READY]`, Referee's `[LEVEL OK]`, Simon's `[RUN DONE]`, Referee's `[VERDICT]`, Guardian's `[PATCH READY]`. No human touched it. Then show Simon's merged `bot/build-*` PRs: the Bots built the arena too.
7. **Close (10s):** "Agent safety shouldn't be a research paper. It should be a game anyone can play."

**Backup:** pre-recorded video of steps 4 and 5 at <link>, in case the live run is slow.
