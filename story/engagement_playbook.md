# Engagement Playbook

The episode runs read this before animating and apply the **Current rules** and the **Active experiment**. The nightly analytics run updates it.

## Goal

More views per episode, measured fairly: compare episodes at the same age (views at 24h and at 72h after posting), plus retention (average view duration ÷ episode length). Retention matters most for Shorts, because it decides whether YouTube keeps showing a video to new viewers.

## Current rules (apply to every new episode)

Starting rules, based on general Shorts practice. Replace them as our own data comes in.

1. **Hook in the first second.** The first frame should show a character mid-action or a face mid-reaction, not a still or a title.
2. **Make something happen every 3–4 seconds**: a gag, a sound sting, a reveal. Avoid long quiet stretches, except for one deliberate silence before a big payoff.
3. **Keep characters big.** Their faces should fill at least a quarter of the frame width in key moments, because viewers are watching on phones.
4. **End on a clear cliffhanger visual**, then the TO BE CONTINUED card, kept short (about 1.5s).
5. **Titles:** start with the conflict or the mystery ("The Duck Took His Throne"), never "Episode N" first. Keep them under 50 characters, ending with "| Fridge Kingdom Ep. N".
6. **Description:** end with one specific question viewers can answer in the comments ("Where do you think the Duck went?").
7. **The Duck** appears in every episode, always in a new spot.

## Active experiment

**Experiment 1: cold open vs title card first** (starts with Episode 3)

- Variant A (odd episodes): current format, with the 2s "FRIDGE KINGDOM" title card first.
- Variant B (even episodes): cold open. The first frame is mid-action, and the title shows as a small banner across the top for the first 2s while the story plays.
- Measure: retention and views at 72h. Decide after at least 4 episodes of each variant.
- Record each episode's variant in `story/analytics.csv` (the `variant` column) and in the episode's bible row.

## Experiment queue (one at a time, top first)

1. Cold open vs title card (active)
2. Length: about 25s vs about 40s
3. Title style: mystery question ("Why Is the Duck Watching?") vs action statement ("Dill Declares War")
4. Ending: hard cliffhanger vs loop-friendly ending (the last frame matches the first, so replays feel seamless)
5. Focus character: Dill-led vs Crumb-led vs Duck-mystery episodes
6. Emoji in title vs no emoji (Eps 1–3 used emojis, Ep 4 didn't; keep titles consistent until this is tested)

## Guardrails

- Never break the story bible or skip story beats to chase views.
- No misleading titles: a title must match what's actually in the episode.
- Keep it all-ages, with no shock content.
- Change only one variable at a time, so results mean something.
- Early numbers are tiny and noisy, so don't overreact to single videos.

## Findings log (newest first)

| Date | Finding | Evidence | Action taken |
| --- | --- | --- | --- |
| 2026-11-05 (night) | No per-video signal yet; channel is growing. Per-video views/duration/likes are still null for Eps 1–4 even at ~59–94h (YTVV returns 0 rows; YTVP lists only Eps 1–4, all metrics null), so Experiment 1 can't be scored. This is now past the normal 1–2 day lag, so flagged to Megha as a possible Metricool↔YouTube Analytics connection issue. Channel-level numbers did arrive: ~4,945 views total (29 on 11-01, 2,246 on 11-02, 2,670 on 11-03; later days not yet reported) and subscribers 4 → 15 on 11-05. Eps 8 and 9 confirmed PUBLISHED (IDs from planner). Without a per-video split, the 11-02/11-03 daily totals can't be credited to any one episode or variant. | YTVP 11-01→11-06: Eps 1–4 listed, metrics null; YTVV 0 rows; YTEV02 daily views 29 / 2246 / 2670; YTEV05 gained 5 (11-02), 6 (11-03); YTEV01 = 15 (2026-11-05); planner: Eps 8 (yZnUCseGSq0), 9 (AWlRd_zFM2Y) PUBLISHED | None. No rule changes. Experiment 1 continues (A: Eps 3, 5, 7, 9; B: Eps 4, 6, 8). Recommended Megha check that Metricool's YouTube connection has Analytics permission (reconnect if needed). If per-video data is still null after the fix, consider pulling views from YouTube Studio manually into analytics.csv |
| 2026-11-04 (night) | No clear signal yet. Per-video views/duration/likes are still null for every episode, including Eps 1–2 at ~70h, so this is Metricool/YouTube Analytics lag, not low performance. Eps 5–7 are confirmed PUBLISHED on YouTube (planner status) but not yet in Metricool's video analytics; their IDs were taken from the planner. Subscribers still 4 (last data point 11-03). Ep 5 and Ep 6 titles also have no emoji, so the emoji confound in Experiment 1 is now limited to Eps 1–3. | YTVP query 11-01→11-05: Eps 1–4 listed, all metric fields null; YTVV returned 0 rows; YTEV01 = 4 (2026-11-03); YTEV04 = 2 videos on 11-02 and 2 on 11-03; planner shows Eps 4–7 PUBLISHED | None. Experiment 1 continues (A: Eps 3, 5, 7; B: Eps 4, 6). First decision possible once Eps 3–10 reach 72h with real data (~11-09/11-10). If per-video stats are still null on 11-06, flag the Metricool YouTube connection to Megha |
| 2026-11-03 (night) | No clear signal yet. Metricool now lists Eps 1–4 (IDs and publish times recorded in analytics.csv) but per-video views/duration/likes are still null; Ep 5 not listed yet. Channel-level: 29 video views (all dated 11-01, likely YouTube's lagged daily total), subscribers 3 → 4. Note for later: Eps 1–3 titles have emojis, Ep 4 doesn't; watch this as a possible confound in Experiment 1. | YTVP/YTVV per-video query 11-01→11-04 returned metric fields null; YTEV02 = 29; YTEV01 = 4 (2026-11-03) | None. Experiment 1 continues (A: Eps 3, 5; B: Ep 4). Need ≥4 per variant at 72h (earliest ~Eps 3–10, around 11-10) |
| 2026-11-02 (night) | No clear signal yet: no per-video YouTube rows for Eps 1–3 (Eps 1–2 ~22h old, Ep 3 ~4h; within the 1–2 day lag). Channel has 3 subscribers. | Metricool YTVV query 11-01→11-03 returned 0 rows; YTEV01 = 3 (2026-11-02) | None. Experiment 1 continues (Ep 3 = A; Ep 4 will be first B) |
| 2026-11-02 | Loop started; no analytics yet (YouTube data lags 1–2 days) | Metricool returned no rows | Started Experiment 1 |
