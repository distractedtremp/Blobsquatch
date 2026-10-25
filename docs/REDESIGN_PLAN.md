# Redesign plan: the new concept on the existing site

**The principle:** the owner likes the current site's structure, scenes, game and flow. Reskin it to the new concept (a guy in a Bigfoot costume, with Barry in on it) and add the new beats below. **Don't change anything that isn't listed.** Section names refer to `CURRENT_SITE_SPEC.md`. Propose the plan to the owner and get his OK before large rewrites. Keep backups of each version.

## 0. Global

- **Palette:** retire the pink tokens (`--pink` etc.) and the pink "blob" blur color. New brand accents: dark costume brown, rusty brown, charcoal and peach skin, with **NEAR green `#00EC97`** as the one pop color.
  - The night-forest backgrounds, mint `#2EE6A6` UI accents and amber can stay, if they don't fight the brown. Check that the contrast works.
- **The "blob" effect stays:** far away he's a soft blur. Blur him to brown instead of pink.
- **Art:** replace the six pink sprites in `const ART` with cut-outs of the locked images. See `ART_PIPELINE.md` and `CHARACTER_BIBLE.md`.
  - Keep the sprite approach (base64 WebP inside the single HTML file) unless you move to a multi-file build. Ask the owner first.
- **Fix the file skeleton:** add a doctype, `meta charset` and the `[hidden]{display:none!important}` rule if this becomes a standalone deploy. Today it depends on the claude.ai artifact host.
- **Logo:** keep "BLOB" (blurred) plus "SQUATCH", recolored.

## 1. Header and hero copy (§3.1–3.2)

- **h1:** keep "Nobody's gotten a clear picture. Yet." It still works, and now it's ironic.
- **Lede:**
  - Was: "Every photo of Blobsquatch is a pink blur. Barry has been trying to get a clear shot since 1967. Go squatching with him."
  - Proposed: "Every photo of Blobsquatch is a blur. That's on purpose. Barry has been getting a blurry shot since 1967. Go squatching with him."
  - Confirm the wording with the owner.
- Keep the definition line. It's real slang, and it now fits even better.

## 2. Hero canvas scene (§3.3, §5.3–5.5)

Keep the same deep-woods 3D scene, state machine, camera push-in, twig and timings.

| Mode | Current | New |
|---|---|---|
| `rest` | A blurry pink back view paces between trunks. | A blurry **brown** back view (`03-back-walk.jpg`, alternating with its mirror for a 2-frame walk). Same pacing path. |
| `approach` (2.6s push-in) | He gets sharper. | He gets sharper. As he comes into focus the **zipper and green pull** become readable. That's the first giveaway, and it shouldn't show at full blur. |
| `ready`/`minting` | Viewfinder with "Snap a pic." | Same. |
| `twig` (0.55s) | Barry steps on a twig: "snap!" | Same visuals, but now it's Barry's **cue**. Optionally Barry glances at the camera or winks. Keep it subtle. |
| `glance` (0.3s turn, shot at 0.55s) | A face slides into the pink back view. | Swap to **`04-look-back.jpg`**. The camera **flash** fires and lights him up, so his **real human eyes in the mask holes** are unmistakable. This is the big near-miss. Hold a beat so it reads, maybe 0.6–0.9s. Tune it with the owner. |
| `frozen` → Polaroid | Developing pink blob. | Same flow. `renderDeveloping` draws a **brown** blob instead of pink. Title still "Still developing." |

Also:

- **Barry** becomes "in on it": redraw him in the crude style when art exists. Until then, keep the procedural Barry and recolor if needed. His moods (squint, watch, aim, frenzy, sleep) still fit.
- **Hero `aria-label`:** update it, e.g. "Barry and his buddy fake a Bigfoot sighting in a night forest."
- **Fix:** while pump/dump is live, "Go Squatching" is hidden. Let people still start the hero flow, or add a way back.

## 3. Pump and dump (§5.6–5.7)

- **Pump:** see `PUMP_DANCE.md`. Pose-to-pose dance, a bouncing mask showing his chin and face, the mask popping off at k=1, Barry dancing and flashing, plus the existing "PUMPING!", candles and strobe.
- **Dump:** replace the "hiding behind a tree with pink fingertips" gag. The guy **freezes stiff, holding his mask on with both hands** ("they're onto us"), trying to look like a tree or stump. Barry hides the camera behind his back or keeps dozing in the camp chair; the current gag is liked, so ask the owner. Keep the red candles, darkening and the "Wake Barry up" button.
- Mode chips "Normal / Pumping / Dumping" and the note copy stay. Update the note if the dump gag changes.

## 4. NFT section (§3.4)

- Keep the mechanics, numbers and copy structure: 1,967, one per wallet, 3 NEAR or free with 1M+, 1/1/1 split, 3% royalty, #352 "Frame 352", provenance hash, developing Polaroids.
- **Rewrite the traits for the new concept.** The current copy lists fur, tuft, size and expression, which code never draws. The new trait list needs to be decided with the owner. Ideas:
  - giveaways: zipper stuck halfway, sneakers peeking out, wristwatch, price tag, mask crooked;
  - pose, setting and film (keep the existing settings and films: Trail Cam, Night Vision, Disposable, Polaroid);
  - rare: glasses (he never wears them in the suit), mask off;
  - very rare: "true blobsquatch" (totally blurry, keep).
  - Make sure every trait in the copy is actually rendered.
- `renderNFT()` is unused today. It should become the reveal renderer for the new art.

## 5. Game: Snap the Squatch (§6)

Keep all the rules, scoring, focus mechanic, rounds, bears and Barry penalty. Reskin the squatches with the new costume art, blurry far away.

New-concept touches, all optional; propose them first:

- A perfect sharp snap shows the giveaway (zipper or eyes) with a caption like "Clear shot... wait, is that a zipper?"
- An "agile/elusive" tweak: he bolts sooner if you hover too long. This is the owner's stated gameplay reason for agility.

Known bug: a bear can be snapped repeatedly for −50 each time.

## 6. New sections and features (build after the core reskin, with the owner's OK)

1. **"How Bigfoot Is Made":** a crude cutaway diagram of the suit with four labeled parts (stilts, arm extensions, shoulder pads, loose mask). Could also be an "x-ray" on tap or hover over the suit. The art is still needed.
2. **The behind-the-scenes reveal:** at a big milestone (sellout, a market-cap goal or the reveal date), the mask comes off in a photo of Barry and the guy high-fiving, glasses on. It could live in the NFT section or as a special hero state after the milestone.
3. **"Get in the Suit":** a calendar where anyone can pay in $BLOBSQUATCH to put **their own face** in the suit for a day, max 2 days in a row. That day's site Bigfoot uses their face in the eye holes and neck gap; an AI pipeline composites it. Rules:
   - own face only, with a consent checkbox;
   - no minors;
   - manual approval before anything goes live;
   - part of the money goes to buy-and-burn;
   - frame it as buying a feature, not an investment.
   - **No celebrities or real people other than the buyer** (right-of-publicity and AI-likeness laws).
   - Build it as display-only first. Payments need a contract.
4. **Launch meme kit:** "The Virgin Clear Photo vs The Chad Blobsquatch," plus sticker and profile-picture crops of the locked art.

## 7. Checks for every change

- Render screenshots at 1280 and 390 widths, for every hero mode, pump, dump and the game. See `tools/`.
- For motion, record a short video or frame strip and look at consecutive frames.
- Compare the new screenshots against `screenshots/` to confirm nothing else changed.
- Send the owner images or clips to approve. He judges the feel.
