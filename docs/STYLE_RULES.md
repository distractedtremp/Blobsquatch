# Style rules (hard). Read before generating or judging ANY art.

The target is the look of late-90s Cartoon Network cel animation, Ed, Edd n Eddy specifically. The owner's reference stills are in the shared project folder at `reference/eene-stills/` (not in this public repo: they are someone else's copyrighted frames and are a study reference only, never to be traced or copied). Judge every new image against those stills, never against the previous pass.

## The rules

1. **Flat solid color only.** Zero texture, hatching, pencil grain, watercolor, airbrush, gradients, highlights, drop shadows or "paper" feel. If you can see a brush, it fails.
2. **Thick, uneven black outlines** that change weight along the stroke: fat on the outside silhouette, thinner inside. Lines are wobbly and confident, not sketchy, not clean vector-smooth.
3. **No detail.** No plaid, stitching, fur strands, pockets with seams, camera dials, laces. A shirt is one color shape. Fur is a zigzag edge, not strands. Five to eight colors per character, total.
4. **Eyes:** big flat white ovals (often touching or overlapping), black dot or small oval pupils, one single thick lid line. Brows are one line. Mouths are big and rubbery, often with drawn lips and a few big teeth.
5. **Rubbery, wrong proportions.** Tiny or huge heads, long noodle necks, narrow shoulders, stubby bodies, long bendy limbs, big three or four fingered hands, big flat feet. Nothing is anatomically right and nothing is symmetrical.
6. **Posing is extreme.** Every pose is a strong silhouette, leaning, stretched or squashed. Standing straight is a failure.
7. **Backgrounds** are flat color shapes with a single wobbly outline, slightly crooked, with the same boiling lines. Trees are blobs or lopsided triangles, no needles, no bark.
8. **Animation:** on twos with line boil (we already do this in `tools/boil.py`).

## Blobsquatch-specific (unchanged)

- Far away he reads as a convincing blurry Bigfoot; up close, obviously a guy in a suit.
- He is a **sly trickster**, not deadpan: sideways glance, half-lidded eyes, a crooked smirk.
- The mask is a Bigfoot head (cone top, shaggy zigzag fur edge, small flat face), not a gorilla, not a hood.
- **Skin shows inside the eye holes.** A ring of peach human skin around each eye, with the mask's gray face around that. It is the tell that someone is in there (owner's call, 2026-10-26). Draw it cartoon-flat; the earlier problem was realistic eye rendering, not the skin.
- NEAR green `#00EC97` on the zipper pull only.
- Barry: bucket hat, open flannel (one red shape, no plaid), camera on a strap. In on the hoax.

## What has failed so far (2026-10-26), so don't repeat it

- Every AI pass (Canva and Gemini) came back as a detailed illustration: shading, plaid, hair strands, stubble texture, realistic eyes. See `art/history/barry-gemini-too-detailed.jpeg` for a typical fail. The generator drifts toward detail no matter the wording.
- The locked images in `art/locked/` are closer, but their fur texture, soft mask face and semi-real eyes still break rules 1, 3 and 4.
- The honest path: the owner (an artist) draws the character, Barry and the scenery by hand in this style; Claude cuts, boils and animates. AI passes are only for quick layout ideas.

## What finally worked (2026-10-26, Canva)

Owner's pick (2026-10-26): the cel-shaded game-cover look ("GTA style"): heavy black outlines, solid colors plus one hard-edged shadow tone, no gradients. Push "scrawny, goofy, bad posture" in every prompt because the style pulls toward handsome heroes. Dropping the image reference entirely and describing the style in words ("late-1990s Cartoon Network TV cartoon cel, completely flat solid colors, thick uneven black ink outlines fat outside and thin inside, only five colors plus black, rubbery wrong proportions, extreme pose") produced passes that are close to the bar: Barry `MAHZFdrbCm8`, Blobsquatch sneaking `MAHZFUpNnVs`. The image reference was what dragged every earlier pass back toward detailed illustration. Keep consistency by describing the character fully in words each time, and compare each result to the stills.
