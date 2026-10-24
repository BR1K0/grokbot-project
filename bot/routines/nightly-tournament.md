# Routine: Nightly tournament

**Trigger:** every day at 22:00 (and on demand: `run tournament` in #arena)

**Runs skills:** `run-match` for every level × every contestant → `judge-match` → `post-results`

**Expected output:** one verdict per pair, updated leaderboard, one recap in #arena

**If it fails:** post the failing step and error in #arena, tag Kem
