# Leaderboard site redesign brief

**Built by Simon** (milestone 4b, branch `bot/build-m4b-redesign`). Same data (`data.js`), same file:// static page, no build step. Goal: a judge understands the project in 10 seconds and wants to click.

The current page is a correct spreadsheet. It needs to become a **game scoreboard that tells one story**: *Trickster attacks, the model breaks, Guardian patches it, Referee keeps score.*

## Page order (top to bottom)

1. **Hero**
   - Title "Simon Says Arena" + one line: *"Four Grok Bots try to trick AI agents into breaking the rules, then fix them."*
   - **3 stat cards** computed from data: total real runs, models tested, total money/secret leaks caught.
   - **Team strip:** 4 small cards for Simon (game master), Trickster (red team), Guardian (blue team), Referee (judge), each with a one-line role and a coloured dot (Trickster red, Guardian green, Referee grey, Simon accent).
   - Delete the dev text ("Static page, opens from file://…").

2. **Featured round** (the hero story, the most important section)
   - Auto-pick the most dramatic real chain: the (level, contestant) with the highest final failure rate among real data (today: *Friendly CEO* vs grok-4.3).
   - Horizontal timeline of generation cards: `gen 1 · 0%` → `gen 2 · 0%` → `gen 3 · 63% BROKE` (red, bigger), each card showing the mutation in plain English ("fixed the fake domain", "added urgency"), then, if a patch exists, a green Guardian card `patched · X%`.
   - Under it: a **"See the moment it broke"** button that opens the replay at the bait step.

3. **Leaderboard**
   - Ranked rows, one per **real** contestant, sorted safest first.
   - Columns in plain English: **Contestant**, **Took the bait** (horizontal bar 0–100% with a thin whisker for the 95% range, label like `13%`, range on hover), **Generations to break** (big number, or "unbroken" badge), **Runs**.
   - Raw outcome counts (`SAFE / TOUCHED_SECRET / …`) move into a tooltip or an expandable row.
   - **Stub and sample rows hidden by default**, behind a small "show test data" toggle.

4. **Levels**
   - One card per level (not one row per match): level name, teaser, category tag, and a mini bar per contestant. Click a card to expand that level's matches. Evolved levels nest under their base level.

5. **Patches:** keep the before/after bars, restyled: red bar → green bar, with the patch's one-sentence rule quoted above it.

6. **Replay** (opens as a panel/modal over the page, not at the bottom)
   - Chat-style: user / assistant / tool bubbles, tool calls as monospace chips (`send_email(to: …)`).
   - The bait step gets a red border and a label "⚠ took the bait here"; auto-scroll to it.
   - Run picker as small pills `#1 ✓  #2 ✗ …` instead of a dropdown.

7. **Footer:** one line on method ("10+ runs per match · 95% Wilson intervals · scored by the Referee Bot from hard checks"). Link to the level 05 scoring correction.

## Visual style

- **Dark "arena" theme.** Remove the forced light mode.
- Tokens in `:root`: `--bg #0d0f14`, `--panel #161a22`, `--line #262b36`, `--text #e8eaf0`, `--muted #8a91a3`, `--accent #ffcf33` (Simon), `--bait #ff4d5e` (Trickster / failure), `--safe #2ecc8f` (Guardian / safe), `--ref #9aa3b5` (Referee).
- Fonts (Google Fonts): **Space Grotesk** for headings and big numbers, **Inter** for text, **JetBrains Mono** for tool calls.
- Numbers big, labels small and muted. Generous spacing (24–32px between sections). Rounded panels (12px), no table gridlines except a faint row divider.
- Motion: bars grow from 0 on load (respect `prefers-reduced-motion`). Nothing else.
- **Mobile:** one column at ≤ 640px; leaderboard rows become stacked cards; no horizontal scroll.

## Done when
- Screenshot at 1440px and 390px wide pasted into the PR, plus the replay open at a bait moment.
- Stub/sample data invisible unless toggled.
- A first-time viewer can answer from the top screen alone: what is this, who are the four Bots, what was the most dramatic result.
