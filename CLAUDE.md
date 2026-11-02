# Fridge Kingdom: Daily Episode Runbook

This repo runs a wordless animated series posted to YouTube Shorts **twice a day**. Two scheduled runs fire each day (a morning run and an afternoon run). Each run makes and posts exactly ONE new episode for its slot. Follow these steps in order.

The owner (Megha) has given standing approval to post finished episodes publicly without asking first.

## 0. Setup

```bash
pip install pycairo numpy scipy --break-system-packages -q
which ffmpeg   # must exist
```

## 1. Figure out today's episode

1. Read `story/bible.md` (cast, rules, episode log, open threads).
2. Find the lowest-numbered episode in the Episode log whose status is still "Planned" (or that has no row yet). That is this run's episode N. If another run already scheduled episode N (status "Scheduled"), move on to N+1, so two runs never post the same episode.
3. Its script is in the week file that the bible's **Weeks** table lists for N.
4. **If no week covers N yet**, write the next week first. See "Writing a new week" below.

## 2. Animate the episode

1. Write `episodes/epN.py` (video) and `episodes/epN_audio.py` (sound), following the script's timed beats.
2. Reuse existing code: characters in `episodes/ep1.py`, props in `episodes/ep2.py`, title/end cards in `episodes/ep2.py`, the synth library in `engine/audio.py` and `episodes/ep1_audio.py`. Copy the structure of `ep2.py`/`ep2_audio.py` (each script takes an output path; `epN.py OUT.png T` renders one preview frame at time T).
3. New characters or props: write them as functions with an `INK` outline and the same flat style. Add their design to the bible's Cast table.
4. Guard against zero-size shapes: any `scale()` of a value that can reach 0 must be clamped (use `S()` from `ep1.py`), or cairo raises "invalid matrix".

## 3. Check it before posting

1. Render 8–12 preview frames across the episode, combine them into a contact sheet, and LOOK at it.
2. Check: characters fully on screen and large enough to read on a phone, nothing hidden behind props, no broken shapes, the story beats are readable without words, the Duck appears, the cliffhanger lands.
3. Fix and re-check until it would pass a picky viewer. Then render the full episode:

```bash
./render.sh N "Short_Title"     # writes videos/NN_Short_Title.mp4
```

4. Confirm the duration with ffprobe (30–45s) and listen-check the audio isn't silent or clipped (peak level via numpy).

## 4. Publish the video file

1. `git add` the episode code and `videos/NN_*.mp4`, commit, and push to `main`.
2. The public link Metricool needs is:
   `https://raw.githubusercontent.com/m3ghajoshi/fridge-kingdom/main/videos/NN_Short_Title.mp4`
3. Confirm the link returns the video (HTTP 200, content-type video/mp4 or octet-stream, correct size).

## 5. Schedule the post in Metricool

Brand id `7813281`, timezone `America/Los_Angeles`. Use `createScheduledPost`:

- Date: this run's slot, from `story/posting_log.md` → "Current slots" (the morning run takes the morning slot, the afternoon run the afternoon slot). If the slot time has already passed today, schedule 10 minutes from now.
- `providers`: `[{"network": "youtube"}]`. If the brand also has Instagram or TikTok connected (check `getBrandSettings`), add them with `instagramData: {"type": "REEL"}` and `tiktokData: {}`.
- `youtubeData`: `{"title": "<hooky title> | Fridge Kingdom Ep. N", "type": "short", "privacy": "public", "category": "FILM_ANIMATION", "madeForKids": false, "isAiGeneratedContent": false, "tags": ["Fridge Kingdom", "animation", "cartoon", "funny animation", "wordless cartoon"]}`
- `text`: the episode caption from the week file, one line about the episode, "A wordless cartoon from Fridge Kingdom. New episode every day.", a question for comments, then `#FridgeKingdom #animation #cartoon #shorts`.
- `draft: false`, `autoPublish: true`.

The response's `media` URL should switch to `static.metricool.com`. That means Metricool copied the file.

## 6. Clean up and record

1. After Metricool has copied the media, delete `videos/NN_*.mp4` from the repo (keeps the repo small). Keep the episode code.
2. Update `story/bible.md`: set episode N's status to "Scheduled YYYY-MM-DD HH:MM", fill in "What happened" and "Cliffhanger" from what you actually animated, and add any new open threads or characters.
3. Add a row to `story/posting_log.md` (episode, date, time, weekday).
4. Commit and push. If the push is rejected because the other run pushed first, `git pull --rebase` and push again.
4. Send Megha a short note: episode number and title, the scheduled time, and the Metricool planner link from the response.

## Writing a new week

At two posts a day, a week is **14 episodes**. When no week in the bible's Weeks table covers episode N:

1. Re-read the whole bible, especially Open threads and the last cliffhanger.
2. Write `story/weekK.md` (K = next week number): a 14-episode storyline that continues directly from the last cliffhanger, in the same format as `story/week1.md` (a one-line summary and a timed-beat table per episode, the Duck's location, new assets, and a captions table). It can be one long arc or two linked 7-episode arcs.
3. Stay in the Fridge Kingdom universe. You may introduce 1–2 new characters. Give each a full visual design, a personality, and a running gag, and add them to the Cast table.
4. Make the story richer than the week before: pay off at least one older open thread, plant at least one new mystery that pays off in a later week, and give a side character a bigger moment.
5. Add the 14 episodes to the Episode log as "Planned" and a row to the Weeks table.
6. Do the weekly posting-time review (below).
7. Include a short summary of the new week, the new characters, and any slot changes in the note to Megha.

## Posting-time experiments

Megha wants the two daily slots tuned for views, at your discretion. During the new-week step only (not every run):

1. Pull per-episode YouTube views from Metricool analytics (`getAnalyticsAvailableMetrics` for youtube, then `getAnalyticsDataByMetrics`) and record them in `story/posting_log.md`.
2. Check `getBestTimeToPostByNetwork` for youtube.
3. Keep one slot as the control (start: 17:00) and move the other slot to test a new time (start: 10:00). Change at most one slot per week, keep times between 07:00 and 21:00 Pacific, and write the reasoning in the log's "Experiments" section.
4. Episodes are only a few days old when compared, so look for clear differences across several episodes, not single-video noise.

## If something fails

- Rendering crashes: fix the code and retry. Don't post a broken or partial video.
- Push is refused: stop and tell Megha that GitHub push access needs reconnecting.
- Metricool rejects the post: report the exact error to Megha. Don't retry with different settings on your own.
- Never post more than one episode per run.
