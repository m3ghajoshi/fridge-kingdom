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

## Guardrails

- Never break the story bible or skip story beats to chase views.
- No misleading titles: a title must match what's actually in the episode.
- Keep it all-ages, with no shock content.
- Change only one variable at a time, so results mean something.
- Early numbers are tiny and noisy, so don't overreact to single videos.

## Findings log (newest first)

| Date | Finding | Evidence | Action taken |
| --- | --- | --- | --- |
| 2026-11-02 (night) | No clear signal yet: no per-video YouTube rows for Eps 1–3 (Eps 1–2 ~22h old, Ep 3 ~4h; within the 1–2 day lag). Channel has 3 subscribers. | Metricool YTVV query 11-01→11-03 returned 0 rows; YTEV01 = 3 (2026-11-02) | None. Experiment 1 continues (Ep 3 = A; Ep 4 will be first B) |
| 2026-11-02 | Loop started; no analytics yet (YouTube data lags 1–2 days) | Metricool returned no rows | Started Experiment 1 |
