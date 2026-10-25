# The pump dance

## When it plays

The scene is driven by the live chart, the DexScreener 1-hour price change of the pair in `PAIR`. `PAIR` is still empty, because the coin hasn't launched.

- `pct >= 2` and the hero is in `rest` → `scenePump(t, dt, k)` with `k = clamp((pct-2)/8, 0, 1)`. So +2% is k=0, and +10% or more is k=1 (max intensity).
- `pct <= -2` → `sceneDump`.
- Otherwise the normal squatching hero plays.
- The mode chips in the hero let you preview: Normal, +5% (pump, k=.375) and −5% (dump).
- Quirk: while pumping or dumping, the "Go Squatching" button is hidden, so nobody can start the hero flow until the price calms down. Consider fixing this.

## Exactly what plays now (v15, `site/blobsquatch.html` L701)

```js
let ph=0;
function scenePump(t,dt,k){
  drawForest(t,1,0,0,0,false,{noSq:true,candles:'up'}); // dollied-in deep woods + green candles stepping up
  ph+=dt*(4+4*k);                                        // phase speed 4–8 rad/s
  const h=H*.62, x=W*.68+(reduce?0:Math.sin(ph*.5)*W*.03),   // side-to-side sway
        hop=reduce?0:Math.abs(Math.sin(ph))*H*.05;            // bounce
  drawSquatchAt(ctx,DPR,x,H*.985-hop,h,1,t,{arms:'dance',sp:8+6*k,tilt:reduce?0:Math.sin(ph*.5)*.12,happy:true});
  ctx.save();ctx.translate(W*.2,H*1.0);squatcher(ctx,H*.62,t,'frenzy');ctx.restore(); // Barry shooting
  if(!reduce&&((t*4.5)%1)<.08){ctx.fillStyle='rgba(255,250,230,.18)';ctx.fillRect(0,0,W,H)} // strobe ~4.5 Hz
  overlay('PUMPING!',false,false);
}
```

**Blobsquatch's motion**

- Front view, sharp (q=1), 62% of canvas height, standing at the right (x ≈ .68W).
- **Bounce:** `|sin(ph)| × 5% H`, so the feet leave the ground twice per cycle.
- **Sway:** `sin(ph/2) × 3% W`.
- **Body tilt:** `sin(ph/2) × .12 rad`, rocking with the sway.
- **Arms `'dance'`:** both raised overhead at about 2.45 rad, alternating ±.32 rad at `sin(t × sp)` with `sp = 8 + 6k`. It reads as fist pumps, faster on bigger pumps.
- Happy face layer.

**Barry:** in `'frenzy'` mood at the left (.2W). He holds the camera to his eye, jitters, and his flash bursts about 4.5 times a second, in sync with a full-screen strobe.

**Background:** the same night woods as the hero, fully pushed in, plus 9 translucent green candlestick bars stepping up to the right.

**Banner:** "PUMPING!"

Screenshots: `screenshots/pump-1.png`, `pump-2.png`, `pump-mobile.png`.

## History: what the owner liked and didn't

- **v14** (`site/versions/blobsquatch-v14.html`) used the **same choreography**, but Blobsquatch was code-drawn: pink ellipses with stroke arms and a blank "blah" face. The owner found that version **funnier** than v15. The deadpan blankness made it.
- **v15** swapped in sprite art with a sassy/happy face. That was less funny, and the owner dropped "sassy."
- A cutout "rig" attempt with rotating limbs was called **"very bad."** Rotating flat cutouts looks stiff.
- **Lesson:** judge the dance by rendering frame sequences or video (see `tools/rec.js`), not single stills. Be upfront that you can't watch motion directly.
- **Reference vibe:** the two "Pump It" trend videos in the project root:
  - fist pumps overhead;
  - alternating knee raises;
  - jumps;
  - a bend-over head-bang;
  - arm throws.
  - Goofy, high energy, done by regular people, not pro dancers.

## The new pump dance (to build)

**The joke:** they think the hoax worked, so Barry and the guy celebrate. The dancing makes it even more obvious there's a person inside, because the loose mask bobs on his head.

**Approach: pose-to-pose with layered heads.** Don't rotate cut-out limbs.

1. **Body poses.** Generate 3–4 full-body poses in the locked style from `art/locked/02-mask-on-front.jpg`, one per generation:
   - (a) both fists up, left knee raised;
   - (b) both fists up, right knee raised;
   - (c) deep squat with fists at the hips;
   - optional (d) bent over in a head-bang.
   Cycle a→c→b→c on the beat. Code adds squash/stretch on landing, a bounce, a little dust and a light screen shake.
2. **Head stack, drawn separately on top of each body pose:**
   - Bottom layer: **the guy's real head**, cut from `01-mask-held-front.png` and scaled to sit inside the mask.
   - Top layer: **the mask**, cut from `02-mask-on-front.jpg`. It follows the head with a **spring lag**, so it rides up as he lands and drops late as he jumps. At the top of the lag his **chin, mouth and stubble** show below the mask edge. On a crooked bounce, his eyes slide out of line with the eye holes.
   - A suggested spring: `vy += (headY - maskY)·K - vy·D` per frame, with K ≈ 0.25 and D ≈ 0.35, plus a small random tilt kick on each landing. Clamp so the mask never fully clears his head except on a "pop."
3. **Intensity scales with k:**
   - Faster tempo (keep the `4 + 4k` phase rate as the baseline).
   - Bigger hops and bigger mask lag.
   - At **k = 1** (+10% or more), the **mask pops off** every few cycles: it flies up and spins, he grabs it and jams it back on crooked, and for those frames his **whole face** shows. This is one of the "show more of his face" moments the owner asked for.
4. **Stilts:** a slight wobble or teeter on big landings, since he's on stilts inside the suit.
5. **Barry dances too.** He's in on the hoax, so they celebrate together. Keep his camera-flash bursts as the strobe source. Barry needs redrawing in the same crude style first.
6. **Keep:** the "PUMPING!" banner, the green candles, the night woods and the reduced-motion handling (no hop, sway, strobe or mask pop; show one static pose).
7. **Check:** render a short MP4 or frame strip at desktop and mobile sizes, look at consecutive frames, and send them to the owner to confirm the feel.
