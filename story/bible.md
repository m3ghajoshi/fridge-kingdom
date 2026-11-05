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
| Crumb | Toast slice, brown crust, jelly smudge on lower right, sweat drop; top-right crust corner snapped off in Ep 5 (`crumb_notched` in `episodes/ep5.py`) | Anxious, loyal, says yes to everything | Always the one who gets launched or used as bait | Ep 1 |
| The Duck | Yellow rubber duck, orange beak; since Ep 5 wears an orange-red crimped bottle-cap crown (`cap_crown` in `episodes/ep5.py`), now tilted | Never seen moving except one tiny motion per episode | Is somewhere new every episode; nobody addresses it | Ep 1 |
| The Pickle Jar | Glass jar, red lid, 5 small pickles with eyes inside | Silent relatives who stare | Watch everything from the top shelf | Ep 1 |
| The Hand | Huge dark-purple silhouette | Unknowable force of nature | Arrives with the choir; never cares about fridge politics | Ep 1 |
| Grandma Gherkin | Tiny, ancient, hunched olive-green pickle with wrinkle lines, round gold spectacles, bushy white brows, a white garlic-clove bun, lavender shawl with white dots (doubles as a parachute), crooked wooden cane (`grandma` in `episodes/ep6.py`) | Stern matriarch of the Jar; surprisingly fast and springy for her age | Bonks Dill with her cane whenever he gets grandiose | Ep 6 |
| The Jar Pickles | Five small dark-green pickles with bumps: plain, mustache, red bowtie (tallest), sprout on head (smallest), freckles (`pickle_kid(c, x, y, k)` in `episodes/ep6.py`, k=0..4) | Move as one; loyal to whoever Grandma bows to | March everywhere in a line to a tiny drum | Ep 1 (jar), Ep 6 (out) |
| Wilt | Wilted lettuce leaf: pale yellow-green crinkly leaf, white rib with veins, browning edges, floppy top that hangs over, half-lidded sad eyes, small frown (`wilt` in `episodes/ep6.py`) | Melancholy, gentle, long-time resident of the crisper drawer | Sighs and pats anyone sad with its floppy top | Ep 6 |
| Peep | Tiny chick: round pale-lemon fluffy body with a scalloped fluff outline, three-feather tuft poking up, huge glossy black eyes with white shines, pink cheeks, small orange triangle beak, stubby wings, orange twig feet; wears the top half of its eggshell as a tilted helmet (`peep`, `shell_half` in `episodes/ep8.py`; moods happy/love/proud/blink/chirp/sneeze/shock/hungry, wings down/flap/salute/hug) | Fearless, chaotic, always hungry; imprinted on Crumb | Copies whatever the last character did, in miniature (and usually better) | Ep 8 |
| Chip | Small ice cube: pale-blue translucent rounded cube, white frost highlights, one trapped air-bubble freckle, shy little eyes, wobbly mouth, constant puff of frosty breath | Shy, polite, homesick; scared of whatever rules the freezer | Melts a little whenever someone is nice to him; Crumb mops him up | Ep 15 (planned) |

Code for each character lives in `episodes/ep1.py` (`dill`, `crumb`, `duck`, `hand`) and props in `episodes/ep2.py` (`jello`, `cheese`, `grape`, `napkin`). New characters go in a new module in `engine/` or the episode file that introduces them; reuse them from there.

## Set

- Fridge door outside with climbable magnets, handle, door-swing geometry (`fridge_door`, Ep 4 `episodes/ep4.py`); eggs, shells, yolk, toothpick spear also in `ep4.py`. Dill now has `arm="reach"` (both arms up) and `arm="pound"` (knocking fist).
- Kitchen (Ep 3, `episodes/ep3.py`): cream tiled wall with window, teal cabinets, butcher-block counter (edge at x=2000), blue/white checker floor, cutting board + plate, orange mug, giant spoon, striped sugar bowl, sprinkles, fridge exterior with magnets and handle (`fridge_front`).

- Top shelf (y=720): pickle jar (left), the Duck (right).
- Bottom shelf (y=1450): milk carton (far left), butter-dish throne spot (x≈420).
- Crisper drawer below the bottom shelf.
- Dark blue when the door is closed; bright white with god rays when open.

## Weeks

| Week | Episodes | File | Storyline |
| --- | --- | --- | --- |
| 1 | 1–7 | `story/week1.md` | The War on The Hand |
| 2 | 8–21 | `story/week2.md` | The Egg (8–14) + The Frozen North (15–21) |

From week 2 on, each week is 14 episodes (two posts a day).

## Episode log

| Ep | Title | Status | What happened | Cliffhanger |
| --- | --- | --- | --- | --- |
| 1 | The Hand | Posted 2026-11-01 | The Hand steals Dill's butter-dish throne; Dill catapults Crumb to the top shelf | The Duck turns to stare at the camera |
| 2 | Operation Butter | Posted 2026-11-01 | Dill's cheese-slice decoy fails; The Hand grabs Dill instead; his crown falls | Crumb holds the crown in the dark; the Duck faces the camera |
| 3 | The Outside | Scheduled 2026-11-02 17:00 (variant A: title card first; 40s) | The Hand drops Dill onto a plate in the giant kitchen; a sandwich is built around him and he's pinched onto the tomato; he dives out as the top slice slams, zips down a giant spoon, PINGs off a sugar bowl, skids through sprinkles, somersaults off the counter to a heroic floor landing, and races the slowly closing fridge door | The door slams; Dill BONKs flat against it and peels off. Inside in the dark, Crumb is admiring himself in the crown when three knocks sound; the Duck (top shelf front edge) turns toward the door |
| 4 | Knock Knock | Scheduled 2026-11-03 10:00 (variant B: cold open; 39.6s) | Cold open on a split screen: outside, red-faced Dill pounds the door; inside, Crumb (wearing the crown) jumps and screams at every knock. Crumb shuttles six eggs into a wobbly pyramid wall and hides behind it with a toothpick spear (the Duck perches on top of the egg wall for a moment; nobody notices). Dill climbs the door magnets (banana, star, pizza); the pizza magnet slides all the way down with him (clunk, sad trombone). He climbs again, leaps to the handle and strains (HNNNG). The Hand grabs the handle above him and swings the door open; Dill is flung inside like a wrecking ball, CRACKs through the egg wall and flattens Crumb. Both yolky; they hug; Crumb hands back the crown and Dill puts it on with great dignity (sword raised). | Door closes. Dill turns to his throne spot: the Duck is sitting exactly there, then slowly turns its head to the camera |
| 5 | The Usurper | Scheduled 2026-11-03 17:00 (variant A: title card first; 39.4s) | The Duck sits on Dill's throne spot wearing a crimped orange bottle-cap crown. Yolky Dill trembles, steams and points (thought bubble: duck, crossed out). Staring contest: Dill's eyes water, his big eye twitches, he BLINKs first and topples backwards (THUD). Dance-off: Dill flails to a funky bassline; the Duck does nothing; a cricket chirps. Dill charges with his sword, leaps onto the Duck, BOINGs off it like a trampoline and CRASHes into the milk carton (milk splashes), sliding down dizzy. Crumb snaps off his own top-right crust corner (CRUNCH, tiny ow), sets it before the Duck as a gift and bows deeply. Silence. The Duck squeaks once; its cap crown tilts. Dill and Crumb scream, run in circles, and dive behind a big jello (far right of bottom shelf), peeking over it. | Top shelf: the Pickle Jar lid turns by itself, click by click, rising and showing a gap of light |
| 6 | The Jar Opens | Scheduled 2026-11-04 10:00 (variant B: cold open; 40s) | Cold open: the Pickle Jar lid POPs off and clatters onto the top shelf. Five little pickles hop out and march along the top shelf, then step off the edge and BOING off the jello onto the bottom shelf; ancient Grandma Gherkin climbs out last, hobbles fast with her cane and parachutes down on her lavender shawl. Dill leaps out from behind the jello beaming with open arms (hearts, sparkles); the pickles march right past him (record scratch) and bow to the Duck, which slowly nods back. Dill hops in front for a rallying speech (bubble: crown over a pickle army); when he leans down smugly toward Grandma, she springs up and BONKs his head with her cane (slide whistle; he squashes, dizzy). The pickles carry him flat overhead like a parade float, Grandma leading like a drum major, and toss him into the crisper drawer (SHHHK, THUNK). Crumb, still peeking over the jello, waves a tiny teary goodbye (sad trombone). In the dim drawer Dill slumps in tears; Wilt, a wilted lettuce leaf, flops its top over and pats his back three times. | Dill notices a doodle scratched into the drawer wall: the Hand holding the Duck (with its bottle-cap crown), surrounded by hearts. Close-up: Dill's eyes go huge; DUN DUN DUNNN |
| 7 | The Truth About the Duck | Scheduled 2026-11-04 17:00 (variant A: title card first; 40.3s) | In the crisper drawer, Wilt bends its floppy top down and SPROINGs Dill back up to the shelf; he lands behind the jello next to Crumb. Dill acts out the doodle (thought bubble: the Hand holding the Duck, hearts), then the plan (bubble: the Duck squeaking, the Hand coming). Crumb gulps and salutes, then tiptoes behind the bowing pickles to spy music, freezing when Grandma peeks (spectacle glint) and when the bowtie pickle peeks. Dill gives a thumbs-up from behind the door seal (grey rubber gasket at the right edge). The door opens (choir); as the Hand descends, Crumb leaps onto the Duck: a huge echoing SQUEEEAK; the Hand freezes. Crumb tumbles off to the left. The Hand gently scoops up the Duck and carries it away trailing hearts; the pickles GASP. A dreamy vignette shows the Duck's silhouette (with its cap) bobbing in a steaming bathtub, hearts rising. The Hand returns Dill's butter dish, now with a big bite out of the butter (CLUNK). Door closes (THUD). Dill leaps from the door seal over everyone onto his throne, sword raised; fanfare and confetti; the pickles and Grandma bow to him (Grandma raises her cane); Crumb sits crying happy tears. Music stops. | Camera drifts up to the top shelf in the dark: a lone egg (next to the jar lid) wobbles, CRACK!, CRACK!, and two tiny eyes peek out of the crack; "peep" |
| 8 | It Hatched | Scheduled 2026-11-05 10:00 (variant B: cold open; 38.2s) | Cold open: the top-shelf egg (beside the fallen jar lid) wobbles, CRACKs twice and POPs; Peep tumbles out and the top half of the shell lands on its head as a helmet (clink); it blinks and peeps, then hops out of the bottom shell. Dill and Crumb haul themselves up over the top shelf's front edge, huffing. Dill strides up and poses with his sword; Peep peeks right past him at Crumb, eyes turn to hearts (record scratch), runs over and hugs Crumb's leg (Crumb: "?"). Copycat: Crumb steps, Peep steps; Crumb hops, Peep hops higher; Crumb salutes, Peep salutes with a wing. Sulking Dill marches back and poses again; Peep hops onto his head, PECK PECK, the crown flips off and lands on Peep, who hops down and poses like Dill while Dill steams. Dill lunges, Peep darts away, Dill BONKs into Crumb and they topple into a pile (Crumb dizzy at the bottom); Peep sits on top, crowned. They spring up; a soap bubble drifts in from the right with a tiny reflection of the Duck (with its cap crown) in bath foam; it pops on Peep's beak; A-CHOO, the crown flies back onto Dill. | Peep's tummy RUMBLEs; it turns to Dill. Close-up: Peep's beak wide open, drooling, eyes glinting; Dill shocked, gulp; DUN DUN DUNNN |
| 9 | Feeding Time | Planned | | |
| 10 | Hide the Chick | Planned | | |
| 11 | Wilt's Secret | Planned | | |
| 12 | Peep Learns to Fly | Planned | | |
| 13 | Knock From Above | Planned | | |
| 14 | The Duck Is Back | Planned | | |
| 15 | Something Is Melting | Planned | | |
| 16 | The Ice Cube | Planned | | |
| 17 | The Expedition Plan | Planned | | |
| 18 | The Squeak Strategy | Planned | | |
| 19 | The Frozen North | Planned | | |
| 20 | The Ice King's Shadow | Planned | | |
| 21 | Thaw | Planned | | |

## Open threads (feed future weeks)

- What hatched from the egg: Peep (Ep 8), a chick that imprinted on Crumb. RESOLVED.
- The Outside exists and is huge (Ep 3); kitchen characters could visit.
- The Duck's bath-time departure (Ep 7) means it could return changed.
- Grandma Gherkin (Ep 6) has authority over Dill.
- The fridge door's outside has magnets (banana, star, pizza) and a handle, already shown in Ep 3 for Ep 4's climb.
- Crumb secretly enjoyed wearing the crown (Ep 3); he gave it back in Ep 4.
- The pizza magnet now sits at the bottom of the fridge door (Ep 4).
- How did the Duck get from the top shelf to the egg wall to the throne spot in the dark? (Ep 4)
- Where did the Duck's bottle-cap crown come from? (Ep 5)
- Crumb is missing a corner (Ep 5); his snapped-off corner sits as an offering in front of the Duck.
- Dill has a new left-pointing arm (`arm="point_l"`) and a dance pose (`arm="flail"`) in `ep1.py`.
- A big jello now sits at the far right of the bottom shelf (Dill and Crumb's hiding spot, Ep 5).

- Who scratched the doodle of the Hand holding the Duck (with hearts) into the crisper drawer wall, and when? (Ep 6)
- The Jar pickles and Grandma Gherkin now serve the Duck; the Jar is open and its lid lies on the top shelf (Ep 6).
- Dill is stuck in the crisper drawer with Wilt (Ep 6); Crumb is alone outside with the pickles.
- Crumb's snapped-off corner (the gift) was left in front of the Duck (Ep 6 still shows it until the parade).
- Dill has a new `mood="sad"` in `ep1.py` (Ep 6).

- The Duck is gone: the Hand took it to a steaming bathtub (Ep 7). It's the Hand's beloved bath toy. Will it come back, and changed?
- Something with two tiny eyes is hatching from an egg on the top shelf, beside the fallen jar lid (Ep 7).
- Dill's butter-dish throne came back with a big bite out of the butter (Ep 7). Who (or what) took the bite?
- The pickles and Grandma now bow to Dill (Ep 7). How long will that last?
- Wilt helped Dill escape and is still alone in the crisper drawer (Ep 7).
- Squeaking the Duck summons/attracts the Hand (Ep 7): a rule the characters now know.
- Ep 7 assets in `episodes/ep7.py`: `door_seal`, `butter_dish_bitten`, `cracking_egg` (crack/gap/eyes), `thumbs_up`, `confetti`, `the_duck(x, y, sx, sy)`, bathtub `vignette`.

- Peep is hungry and eyeing Dill (Ep 8 cliffhanger); Ep 9 feeding montage follows.
- Peep wears the top of its eggshell as a helmet; the bottom half of the shell sits on the top shelf at x≈900 (Ep 8).
- The Duck, still away at bath time, appeared as a reflection inside a soap bubble that drifted in through the door seal (Ep 8).
- Week 2 plants: tapping from the ceiling vent and a crowned "Ice King" shadow in the freezer (pays off Week 3); a second Duck frozen in an ice block (Eps 19–21).
- Ep 8 assets in `episodes/ep8.py`: `peep`, `shell_half`, `fluff_path`, `soap_bubble` (with the Duck's reflection), `pop_burst`, `crown_flight`.

## Weekly arc rules

- Each week is a 7-episode arc that continues from the last cliffhanger.
- Each new week may introduce 1–2 new characters. Add them to the Cast table with a full design description.
- Stories should get more layered week over week: callbacks, returning side characters, and mysteries that pay off a few weeks later.
- Keep Dill and Crumb at the center; the Duck appears every episode.
