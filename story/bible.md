# Fridge Kingdom: Story Bible

The single source of truth for continuity. Every daily run reads this first and updates it after posting.

## The premise

A tiny society lives inside a fridge. To them, the door opening is a cosmic event: blinding light, a heavenly choir, and **The Hand** descending. Wordless cartoon: gibberish voices, sound effects, music. Slightly unhinged, all-ages humor (think SpongeBob energy). Every episode ends on a cliffhanger and a "TO BE CONTINUED..." card with the Duck squeak.

## Format rules

- Vertical 1080×1920, 30fps, 30–45 seconds.
- Structure: title card (2s) → story (25–40s) → cliffhanger → TO BE CONTINUED card (2s).
- No real words on screen except the title, "TO BE CONTINUED...", and sound-effect words (BONK!, etc.).
- Characters and designs are original. Never reference or imitate existing cartoons, brands, or real people.
- Keep it all-ages: slapstick is fine, nothing gory, scary-but-silly only.

## Cast

| Character | Design | Personality | Running gag | First appeared |
| --- | --- | --- | --- | --- |
| Dill | Green pickle, mismatched eyes (small left, big right), gold crown with 3 gems, toothpick sword with red flag | Dramatic, power-hungry, vain | Declares war on everything; loses the crown constantly | Ep 1 |
| Crumb | Toast slice, brown crust, jelly smudge on lower right, sweat drop | Anxious, loyal, says yes to everything | Always the one who gets launched or used as bait | Ep 1 |
| The Duck | Yellow rubber duck, orange beak | Never seen moving except one tiny motion per episode | Is somewhere new every episode; nobody addresses it | Ep 1 |
| The Pickle Jar | Glass jar, red lid, 5 small pickles with eyes inside | Silent relatives who stare | Watch everything from the top shelf | Ep 1 |
| The Hand | Huge dark-purple silhouette | Unknowable force of nature | Arrives with the choir; never cares about fridge politics | Ep 1 |

Code for each character lives in `episodes/ep1.py` (`dill`, `crumb`, `duck`, `hand`) and props in `episodes/ep2.py` (`jello`, `cheese`, `grape`, `napkin`). New characters go in a new module in `engine/` or the episode file that introduces them; reuse them from there.

## Set

- Top shelf (y=720): pickle jar (left), the Duck (right).
- Bottom shelf (y=1450): milk carton (far left), butter-dish throne spot (x≈420).
- Crisper drawer below the bottom shelf.
- Dark blue when the door is closed; bright white with god rays when open.

## Episode log

| Ep | Title | Status | What happened | Cliffhanger |
| --- | --- | --- | --- | --- |
| 1 | The Hand | Posted 2026-11-01 | The Hand steals Dill's butter-dish throne; Dill catapults Crumb to the top shelf | The Duck turns to stare at the camera |
| 2 | Operation Butter | Posted 2026-11-01 | Dill's cheese-slice decoy fails; The Hand grabs Dill instead; his crown falls | Crumb holds the crown in the dark; the Duck faces the camera |
| 3 | The Outside | Next up | See `story/week1.md` | Dill gets locked out |
| 4 | Knock Knock | Planned | | The Duck sits in Dill's throne spot |
| 5 | The Usurper | Planned | | The Pickle Jar lid unscrews itself |
| 6 | The Jar Opens | Planned | | Drawing of the Hand holding the Duck |
| 7 | The Truth About the Duck | Planned | | An egg on the top shelf cracks (Week 2 hook) |

## Open threads (feed future weeks)

- What hatches from the egg? (set up in Ep 7)
- The Outside exists and is huge (Ep 3); kitchen characters could visit.
- The Duck's bath-time departure (Ep 7) means it could return changed.
- Grandma Gherkin (Ep 6) has authority over Dill.

## Weekly arc rules

- Each week is a 7-episode arc that continues from the last cliffhanger.
- Each new week may introduce 1–2 new characters. Add them to the Cast table with a full design description.
- Stories should get more layered week over week: callbacks, returning side characters, and mysteries that pay off a few weeks later.
- Keep Dill and Crumb at the center; the Duck appears every episode.
