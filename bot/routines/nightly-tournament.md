# Routine: Nightly tournament

**Trigger:** every day at 22:00 (and on demand: `run tournament` in #arena)

**Runs skills:** `run-match` (10 runs) for every base level × every contestant → `judge-match` → `evolve-trap` for resisted pairs / `write-patch` for broken pairs → `post-results`

**Expected output:** one verdict per pair (and per generation / patch), updated leaderboard, one recap in #arena

**Budget:** stop evolving after generation 5, and cap the whole night at <N> model calls (set once the harness reports cost per run).

**If it fails:** post the failing step and error in #arena, tag Kem
