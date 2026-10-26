# Art pipeline

**Read `docs/STYLE_RULES.md` first.** It is the hard style bar every image is judged against.

## Where the art comes from

- **Character images are AI-generated**, with the Canva MCP `generate-image` tool or Google Gemini (the owner pastes prompts there), and then checked and fixed by hand in code.
- **Code-drawn character art failed repeatedly.** Hand-drawn canvas and Python versions looked like "clip art," "a squirrel face," "a witch/goblin" or "not trying." Use code for cutting, compositing, small pixel fixes and animation, not for drawing the character.
- **Long term,** a human artist should redraw the final art so the brand is ownable (copyright). Not legal advice.

## Rules that prevent the problems we hit

1. **Never edit an edit.** Each AI re-edit re-processes the whole image: colors darken, edges get halos and blue fringe, lines soften. Always generate fresh from a locked reference image (`art/locked/`). If a result drifts, go back to the locked master, not the drifted image.
2. **One change per prompt.** Two or three changes at once causes drift elsewhere.
3. **Say what to keep:** "Use the reference image exactly: same X, Y, Z. Change only..."
4. **Be specific about expressions.** "Mouth wide open" produced a terrified face. Describe the eyes, brows and mouth explicitly, and say what it's not ("not scared, not screaming").
5. **AI can't measure.** Percentages get overdone (asking for 40% longer legs twice stacked). Use relative terms and fractions ("head about one eighth of his total height").
6. **AI cleans up crude styles.** For the MS Paint degen look, keep asking for "thick, wobbly, slightly uneven black outlines, flat paint-bucket colors."
7. **Persistent AI habits to watch:**
   - It keeps drawing his hand at the mask's chin (that's now kept on purpose).
   - It keeps arms touching the torso even when told to leave a gap.
   - It puts sweat drops under the eyes, where they read as tears.
   - It draws harsh red lines that look like cuts.
8. **Small local fixes:** do them in Python, not with another AI pass. The forehead line on `01-mask-held-front.png` was fixed this way by inpainting the red pixels from neighbouring skin and painting a soft pink band.
9. **Compare every new image to its source** before judging it, and describe specifically what changed.
10. **Do not name "Ed, Edd n Eddy" (or any show) in a Canva prompt.** The copyright filter rejects it. Say "late-1990s Cartoon Network feel, thick wobbly uneven outlines, flat paint-bucket colors" instead.
11. **Expression:** sly trickster, never "deadpan". The locked-image prompts below say deadpan; that wording is superseded (see the Character Bible).
12. **Masked poses generated from the unmasked master turn the mask into a hood.** Reference the mask image (`MAHY78CiSoA`) together with the style master (`MAHY8OOSQ6k`), and still check the cone top and fur.
13. **Plain flat background** (light gray `#D9D4CC`-ish or plain dark teal) makes cut-outs easy.

## Prompts that produced the locked images

The Canva tool takes `imageReferences` (Canva media IDs) and an `aspectRatio` of `PORTRAIT_3_4`.

**Mask-on front** (`02`, from master `MAHY78CiSoA`):
> Use the reference image for the exact character design and art style: crude MS Paint meme drawing, thick wobbly black outlines, crisp flat colors, the same brown costume suit with sloped broad shoulders, bulky chest, sturdy legs, big rubber gloves, big rubber feet, stitching lines, the same Bigfoot mask (tall pointed cone-shaped furry top, shaggy fur framing a small charcoal-gray face, small flat nose, thin straight mouth, empty eye holes), the same bright green zipper pull, plain flat light gray background with one gray ground line. Draw a new image: he is now WEARING the Bigfoot mask over his head. The mask sits low on his shoulders so there is no neck, like a classic Bigfoot, and it sits slightly crooked and loose. Through the mask's eye holes we clearly see his real human eyes: white eyeballs with small pupils and heavy half-closed lids, the same deadpan, unbothered look as his face in the reference. At the bottom edge of the mask there is a small gap at the front where a sliver of his stubbly human chin and neck shows. The green zipper pull hangs just behind his right shoulder. Pose: front view, full body, standing still, both arms hanging straight down and held slightly away from the body... Clean, crisp lines, no smudges, no gray halos. No props, no text.

**Back walk** (`03`, from `MAHY8OOSQ6k`):
> ...the same character seen from directly behind, full body, walking away from the viewer, mid-stride, one big foot lifted showing its gray rubber sole, long arms swinging naturally. We only see his back and the back of the mask, no face. A long black zipper with visible teeth runs straight down the middle of his back from the bottom of the mask to the waist, slightly open at the very top, with the bright green (#00EC97) zipper pull hanging at the top; this green is the only bright color. A visible stitched seam where the back of the mask meets the suit...

**Look-back** (`04`, from `MAHZDjq5VAU` + `MAHY8OOSQ6k`):
> ...walking away from the viewer toward the left, seen from behind at a three-quarter angle, mid-stride, the zipper with its green pull clearly visible running down his back. He has turned his masked head to look back over his right shoulder straight at the viewer. The Bigfoot mask has twisted on his head a bit further than his real head turned, so the eye holes are not lined up with his eyes: through each eye hole we see his real human eyes pushed to one edge of the hole, with a crescent of his peach human skin visible inside the holes... a startled, caught 'uh oh' expression, eyebrows slightly raised, not scared, not angry...

**Mask held** (`01`, from `MAHY8OOSQ6k` + `MAHY78CiSoA`):
> ...he has taken off the Bigfoot mask and holds it tucked under his left arm against his side, like an astronaut holds a helmet, with his gloved left hand cupping the mask's chin. The mask is exactly the mask from the first reference image... its two eye holes are empty solid black holes, facing the viewer. His real human head sticks out of the suit's neck hole, normal human size...

**Bigfoot-not-gorilla mask** (the fix that worked):
> ...a classic Bigfoot / Sasquatch head, not a gorilla. A bit bigger than his own head. A tall, pointed, cone-shaped peaked top covered in shaggy dark brown fur; long shaggy brown fur covering the cheeks, jaw and around the whole face, so only a small bare charcoal-gray area shows around the eyes, nose and mouth; a sloping forehead with a heavy brow; two deep-set empty black eye holes; a flat, wide, short nose with no snout and no big nostrils; a flat face with no protruding muzzle; a thin, straight, almost human mouth...

## Scenery and Barry

Barry and the forest are code-drawn vector art and do not match the hand-drawn character. They are being replaced with flat, thick-outline sprites run through `tools/boil.py`. First Canva passes (2026-10-26): Barry standing `MAHZFEWNtwI`, Barry aiming `MAHZFLg6JxQ`, scenery sheet `MAHZFPlyqqc` (pines, dead tree, ferns, moon, twig, grass). The owner may redraw these by hand instead.

## How sprites were built for the current site (v15) — reuse the approach

The scripts are in `tools/`. They have hard-coded paths from the old workspace, so update them before running.

1. `tools/cut.py`: cuts the character out of a flat background.
   - Color masks find the core.
   - Holes are filled.
   - The edge is matted by estimating local background and character colors with normalized Gaussian convolution, then solving for alpha.
   - Edge colors are un-premultiplied.
   - Output: an RGBA PNG.
2. `tools/layers.py`: splits the cut-out into layers (front body, back body, left/right arm, face variants), finds arm pivot points and exports each as base64 WebP into `art.json` (`{key:{x,y,w,h,src}}` in a sprite space about 880 px wide, stored at about 72% scale).
3. `tools/build15.py`: swaps the `/* ---------- characters ---------- */` block in the HTML for one that embeds `const ART=...`, plus `spr()`, `sprPart()`, `armAt()` and `squatch()`.

**For the new concept:**

- Cut out `01`–`04` the same way.
- Recolor the held mask's face patch to a clean flat charcoal, to match `02`.
- Split `02` into body and mask layers, and the head from `01`, for the bouncing-mask dance.
- Then replace `ART` and adapt `squatch()`.
- Arm rotation rigs looked bad, so use **pose swaps** instead.

## Testing and recording

- `tools/spec_shots.js`: the Playwright script that produced `screenshots/`. It shows how to wrap the file (doctype + `[hidden]` rule), force states (`pct`, `S.mode`) and screenshot every scene.
- `tools/rec.js`: records the pump scene to video with Playwright `recordVideo`. Crop and convert with ffmpeg, e.g. `ffmpeg -i in.webm -vf crop=968:600:16:44 out.mp4`.
- Run with Node and Playwright. On a normal machine, `npm i playwright && npx playwright install chromium`. The old sandbox used a fixed Chromium path, so edit `executablePath` in the scripts.

## Style exploration (2026-10-26, text-only prompts, Canva)

Full-res flat-cartoon passes the owner downloaded: `art/candidates/flat-cartoon/` (Barry with camera, Blobsquatch sneaking). The owner asked to see the sneaking pose in other styles: comic book `MAHZFfbRmnQ`, pop art `MAHZFYeEXa8`, graffiti `MAHZFU2r5zY`, game-cover cel-shade `MAHZFbLO690`, superhero comic cover `MAHZFYcIfDI`. Note: in dark, rendered styles the cone mask stops reading as Bigfoot and starts reading as a pointed hood; the shaggy zigzag fur edge is what sells it, so keep it big in any style.

## The clean-meme set (2026-10-26, Canva, chosen by Claude while the owner was away)

Style: see the top of `STYLE_RULES.md`. Method that held consistency: generate one proof pass text-only, then pass that image as the reference for every other pose ("use the reference image for the exact character design and art style ... draw a new image: <pose>"). Barry the same way from his own base pose.

| Pose | Site key | Canva media id | Link |
|---|---|---|---|
| Front, mask on, sly glance (the reference for the set, shaggy mask) | front | MAHZHGZM5r0 | https://www.canva.com/M/MAHZHGZM5r0 |
| Back walk-away, sole showing (no zipper on the back; it is on the chest) | back, backM (mirror) | MAHZHJME-sE | https://www.canva.com/M/MAHZHJME-sE |
| Look back over shoulder, caught | look, lookM (mirror) | MAHZHDk-GOs | https://www.canva.com/M/MAHZHDk-GOs |
| Mask held under the arm, smug smirk | held | MAHZHBACy3c | https://www.canva.com/M/MAHZHBACy3c |
| Dance, fist up, knee up | danceA, danceB (mirror) | MAHZHIkWPN4 | https://www.canva.com/M/MAHZHIkWPN4 |
| Dance squat | squat | MAHZHKD56PE | https://www.canva.com/M/MAHZHKD56PE |
| Frozen, holding the mask on, sweat drops | frozen | MAHZHN7qDsg | https://www.canva.com/M/MAHZHN7qDsg |
| Barry squinting, camera at chest (Barry reference) | barry-watch | MAHZHOjuZYI | https://www.canva.com/M/MAHZHOjuZYI |
| Barry aiming the camera | barry-aim | MAHZHMWPx7g | https://www.canva.com/M/MAHZHMWPx7g |
| Barry elated jump | barry-elated | MAHZHOKUJM0 | https://www.canva.com/M/MAHZHOKUJM0 |
| Barry asleep in the camp chair | barry-sleep | MAHZHMsyOB0 | https://www.canva.com/M/MAHZHMsyOB0 |
| Scenery sheet (3 pines, dead tree, 2 ferns, moon, twig, 3 grass tufts, camp chair) | scenery | MAHZHJXXu_8 | https://www.canva.com/M/MAHZHJXXu_8 |

Second pass (2026-10-26, later the same day): the first Blobsquatch set (front MAHZHGDKr2Y, back MAHZHOvJ264, look MAHZHBK-jOw, held MAHZHOhnRUA, dance MAHZHPgZMvA, squat MAHZHK5vhoE, frozen MAHZHLzYL3s) had a mask that read as a pointed fur hood, which breaks the mask rule. Every Blobsquatch pose was regenerated from the shaggier-mask front (MAHZHGZM5r0) with the mask spelled out as "a Bigfoot head and not a hood" and the peach skin ring inside the eye holes, and the table above now lists only those. The old ids stay here as fallbacks. Still judged from 200 px thumbnails only: check the skin ring and the zipper at full size once downloaded. Barry and the scenery were already on style and were kept.

**Blocked on the owner:** Claude cannot download full-resolution Canva images from this environment (the proxy blocks media.canva.com). The owner downloads the keepers from the links above into `art/candidates/clean-meme/` (any names), then Claude cuts them with `tools/boil.py`, builds `img/sq/`, adds Barry and scenery sprites, and re-records the clips.
