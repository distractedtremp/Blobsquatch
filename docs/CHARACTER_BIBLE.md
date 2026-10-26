# Character bible: Blobsquatch (new concept, locked)

## Who he is

A regular, fictional guy in his 30s wearing a cheap brown Bigfoot costume, faking Bigfoot sightings with his buddy Barry.

- **No personal name.** He's just "Blobsquatch." **Barry** is the photographer, not him.
- **From far away** he must pass as a classic Bigfoot. **Up close** it's obviously a costume.
- **Personality (updated 2026-10-26):** a trickster. He is fooling people and enjoying it, so the face reads sly and a little devious: half-lidded eyes, pupils in a sideways glance, angled brows, a crooked smirk, in the way a scheming 90s-cartoon character would. **Not bored, not deadpan, not angry.** Zero shame ("yeah, it's me, so what"). Not sassy, not sad, not gross or disheveled.
- **Face style:** flat and heavy-outlined like the body. Big flat white cartoon eye ovals with dot pupils and a thick lid line. No realistic eyes, no skin tint around the eyes, no stubble texture (a few pen dots at most). The soft airbrushed mask face and semi-real eyes in the current locked images read as uncanny and are being replaced.
- **His only "special" traits:** NEARsighted (glasses off under the mask) and agile/elusive (he can't let you get close).

## Locked images (`art/locked/`)

| File | What | Canva media ID | Notes |
|---|---|---|---|
| `01-mask-held-front.png` | **Master.** Front view, mask off, held under his left arm, his gloved hand at the mask's chin. | `MAHZDdSCJV8`; this file has a manual fix | The face, smirk and proportions reference. The forehead mark was hand-fixed to a soft light-pink line. On Canva the original still has the harsh red line, so use this file, not Canva. |
| `02-mask-on-front.jpg` | Front view, mask worn, his real human eyes in the eye holes, a stubbly chin sliver at the neck gap. | `MAHY8OOSQ6k` | Base for the pump dance and dump. The arms touch his sides at the top, so the dance is pose-to-pose; don't rig the arms. |
| `03-back-walk.jpg` | Walking straight away from the viewer, mid-stride. | `MAHZDjq5VAU` | Hero shot. The zipper runs down his back with a green pull. Mirror it horizontally for the other stride, so two frames make a walk cycle. The lifted back foot is bigger because it's closer to the camera, which is correct. |
| `04-look-back.jpg` | Walking away at a three-quarter angle, head turned back over his shoulder. | `MAHZDvEPt9c` | The snap moment. His eyes peek through the mask holes with skin showing. Zipper visible. |

Canva links have the form `https://www.canva.com/M/<ID>`. The owner's own downloads of 02–04 are also loose in the project root with long auto-generated names. They're the same images.

**Lineage (reference only, don't use as masters):**

- `MAHY78CiSoA`: the degen master before the mask was redrawn.
- `MAHY7_wty0c`: before the mask became Bigfoot-shaped (it was a gorilla mask, rejected).
- `MAHY4QurcpI`: the semi-realistic painted version that proved the concept ("nailed it"). Its style was rejected as too realistic. It's saved as `art/history/costume-realistic-lookback.png`.

## Design spec

**Proportions**

- His real head is about 1/7–1/8 of total height when the mask is off. 1/12 was too small, 1/4.5 too big.
- He stands on short hidden stilts, so the suit is a bit taller than a man, with longer legs and longer arms.
- The shoulders are broad, padded and **sloping down from the neck** like a classic Bigfoot. They are not humps rising above his chin (that was rejected as looking like a fridge in football pads).
- Bulky barrel chest, sturdy thick legs (not thin tubes), very big rubber feet, big rubber gloves.

**Suit**

- Flat dark brown fill (sampled around `#483621` / `#42301E`) with crude zigzag fur edges.
- Visible stitched seams at the wrists, ankles and where the mask meets the suit.
- A dark gray neck-hole ring.
- Gloves and feet are dark charcoal rubber (`#373736`).
- **No hood.** A hood was tried and rejected because it looked flimsy.

**Zipper**

- Runs down the middle of the back from the neck to the waist, with visible teeth.
- **Bright NEAR-green pull `#00EC97`**, the only bright color on him. From the front, the pull peeks over his right shoulder at the back of the neck.
- Why green: cheap costume zippers come in random colors, so nobody asks why. "You had to be NEAR" means close enough to see the zipper.

**Mask: a separate piece, not a hood**

- **A Bigfoot head, not a gorilla:**
  - a tall pointed cone top (sagittal crest);
  - shaggy fur covering the cheeks and jaw, so only a small bare charcoal-gray face patch shows;
  - a sloping heavy brow;
  - a small flat nose with tiny nostrils and no snout or muzzle;
  - a thin straight mouth.
- Its expression is dopey and slightly pensive.
- Bigger than his head; it sits low on his shoulders when worn, giving the classic no-neck look.
- Loose fit, so it bobs, slips crooked and can pop off.
- **Worn:** his real eyes are visible in the eye holes (white eyeballs, small pupils, heavy half-closed lids), with peach skin around them.
- **Off:** the eye holes are empty black holes.
- **Held:** under his left arm like an astronaut's helmet, his gloved hand cupping its chin. It's a happy accident that the mask looks like it's thinking; keep it.

**His face (mask off)**

- Short messy brown hair, flattened and sweaty from the mask.
- A **soft light-pink line across his forehead** where the mask pressed, like a hat dent. Not a red cut.
- Light stubble, heavy half-closed eyelids, a slight smug half-smile.
- Sweat drops on his forehead and temples only, **never under the eyes** (they read as tears).
- Light skin, around `#F3CCAA`.

**Style**

- Crude MS Paint internet-meme drawing, in the spirit of the Virgin-vs-Chad memes, without copying Chad.
- Thick wobbly black outlines, flat paint-bucket fills, almost no shading, no gradients or texture.
- It should look low-effort but bold and readable at profile-picture size.
- **Not allowed:**
  - realistic or painterly rendering;
  - cheesy crypto references (no Pepe, Bored Ape, laser eyes, Monster cans, charts on his body or coins);
  - other people's IP or trademarks;
  - looking dirty, sad or homeless.

**Palette (whole brand)**

- **Suit:** dark brown, plus rusty-brown accents if needed.
- **Gloves and feet:** charcoal rubber.
- **Skin:** peach.
- **The only pop color:** NEAR green `#00EC97`.
- The current site's night-forest palette works well with this. The old pink palette (`#FF3FA4`, `#FFA6D2`, `#FDACCD`) is retired.

**Dark on dark:** a dark brown suit in a dark night forest nearly disappears from far away. That's good for the blob meme, but the reveal needs light, and the **camera flash** provides it. Up-close giveaways must show in the flash frame.

## Still needed (art)

1. **Pump-dance poses** in the mask-on style: both fists up with the left knee raised; the same with the right knee; a deep squat. Generate fresh from `02-mask-on-front.jpg`, one pose per generation.
2. **Dump pose:** frozen stiff, both gloved hands holding his mask down on his head.
3. **The guy's head alone, aligned with the mask-on front,** to sit under the mask layer for the bounce reveal. You can cut it from `01-mask-held-front.png` and scale it.
4. **Barry** redrawn in the same crude style. Currently he's procedural canvas art in an old flat style: bucket hat, plaid collar, jacket, camera, stubble. He's "in on it."
5. **Behind-the-scenes reveal:** Barry and the guy high-fiving, mask off, glasses on.
6. **The cutaway diagram "How Bigfoot Is Made":** the suit split open showing short stilts strapped to his shoes, arm extensions (his real hands end at the costume's elbows), foam shoulder pads and the loose mask. Four parts only.
7. **NFT trait art** for the new concept.
8. **Long term:** a human artist redraw. AI-only images are generally not copyrightable in the US, so a human-made version is needed to really own the brand. Not legal advice.
