# Blobsquatch site: current-state spec

Source of truth: `site/blobsquatch.html` (957 lines, 229,486 bytes, last modified Oct 21). This document describes that file exactly as it is. Line numbers (`L123`) refer to that file. Screenshots are in `../screenshots/` (see section 11).

---

## 1. Overview

**What it is.** A one-page meme-coin site for **$BLOBSQUATCH**, a pre-launch NEAR memecoin. The joke: Blobsquatch is a pink Bigfoot that only ever shows up in blurry photos. "Barry the Squatcher", a hiker-photographer, has been trying to get a clear shot since 1967. That's a nod to the 1967 Patterson-Gimlin film and its famous "Frame 352". The page has:
- an interactive hero scene ("Go Squatching", which ends in "Snap a pic" and mints an NFT),
- a chart-reactive mode: PUMPING / DUMPING scenes driven by the DexScreener 1h price change,
- an NFT explainer with four "still developing" Polaroids,
- a Duck-Hunt-style canvas game, "Snap the Squatch",
- Squatcher Stash (community fund) receipts,
- tokenomics and how-to-buy,
- a footer disclaimer.

**Tech.**
- Plain HTML + one `<style>` + one classic `<script>`. No framework, no build step and no external JS libraries.
- All graphics are **Canvas 2D**. The character art is six embedded WebP sprites (base64 in `const ART`, L316). Everything else is drawn procedurally: Barry, the bear, trees, ferns, sky and moon.
- Fonts come from Google Fonts (L2-3): `Bagel Fat One` (display), `Rubik` 400/500/600/700 (body) and `VT323` (camera/monospace).
- Network calls:
  - Google Fonts.
  - DexScreener, only when `PAIR` is non-empty. It is empty right now.
  - `GAME_LOG_URL` POST, only when it is set and a wallet is connected. It is empty right now.
- Persistence: `localStorage['snapSquatchBest']` (best game score) only.

**File structure (single file).**
| Lines | Content |
|---|---|
| 1 | `<title>Blobsquatch</title>` |
| 2-3 | Google Fonts preconnect + stylesheet |
| 4-154 | `<style>` (tokens, layout, components, media queries) |
| 156-301 | `<div class="wrap">` (all page DOM) |
| 303-957 | `<script>` |
| 304-311 | helpers (`$`, `reduce`, `DPRx`, `lerp`, `clamp`, `sm`, `fmt`, `FONT_D`) |
| 313-348 | Blobsquatch sprite rig (`P`, `ART`, `SPR`, `squatch()`) |
| 316 | **`const ART={...}` (about 153 KB single line of base64 WebP)** |
| 350-443 | Barry the Squatcher (`Q`, `camera`, `squatcher`, `sleeper`) |
| 445-486 | legacy flat scenery (mostly dead code) + shared draw helpers |
| 487-615 | hero stage: canvas, 3D "deep woods", state machine `S` |
| 617-698 | Go Squatching / Snap a pic / NFT mint + Polaroid rendering |
| 700-721 | PUMP and DUMP scenes |
| 723-746 | chart input (DexScreener), main `frame()` loop |
| 748-751 | film grain, Copy buttons |
| 753-947 | Snap the Squatch game |
| 949-956 | wallet connect for score logging |

**Document skeleton quirk (important).** The file has **no `<!doctype>`, `<html>`, `<head>`, `<body>` or `<meta charset>`**. It is meant to be wrapped by a host (claude.ai Artifact publishing adds the skeleton). It also **depends on a host rule `[hidden]{display:none!important}`**. Several hidden elements set their own `display`: `.btn/button` → inline-block, `.snapBox` → grid, `.mintPol`/`.gover` → flex, `.polaroid` → grid, `.modes` → flex. Without that rule, the browser's built-in `[hidden]` style loses and all those overlays show at once. Non-ASCII glyphs (· − … ▮ ▯ ˈ ɑ ● °) need UTF-8.

**How to run locally.** Wrap it as the existing helper scripts do:
```html
<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<style>[hidden]{display:none!important}body{margin:0}</style><body> …file contents… </body>
```
Open it in a browser, or load it in Playwright with `page.setContent(wrap)`. In the sandbox Google Fonts is blocked. The screenshots served the same three families from npm `@fontsource/*` packages via `context.route(/fonts\.googleapis\.com/)`. The script is `tools/spec_shots.js`.

---

## 2. Design tokens

### CSS custom properties (`:root`, L6-13)
| Token | Value | Meaning |
|---|---|---|
| `--night` | `#0C1A1C` | page background, topbar bg, h1 `em` text |
| `--panel` | `#13282A` | panels, number cards, contract chips |
| `--line` | `#2B4A46` | borders, dividers, chip borders |
| `--fog` | `#E8F0EA` | main text, ghost button, dictionary card bg |
| `--muted` | `#9FB8B0` | secondary text |
| `--pink` | `#FF6FB1` | Blobsquatch / primary buttons / headings accents |
| `--pink-deep` | `#D94E8E` | (declared, unused) |
| `--pink-ink` | `#2B0D1C` | text/border on pink buttons, `.dict` text |
| `--amber` | `#FFC65C` | camera light, status text, focus outline, HUD values |
| `--near` | `#2EE6A6` | mint = NEAR; banner bg, h1 `em` bg, focus lock |
| `--shadow` | `#030809` | hard offset shadows |
| `--display` | `"Bagel Fat One","Arial Rounded MT Bold",system-ui,sans-serif` | |
| `--body` | `"Rubik","Trebuchet MS",system-ui,sans-serif` | |
| `--cam` | `"VT323",ui-monospace,Menlo,monospace` | |
| `color-scheme` | `dark` | (no light theme exists) |

The design comment (L5) reads: "One night palette; hot pink is Blobsquatch, mint means NEAR, amber is camera light."

### Hard-coded CSS colors
`.stage`/`.cam` bg `#0A1430`; `.gamebox` bg `#06101A`; `.dict .pron/.pos/.ex` `#5B4A52`; `.camui` text `#F4F4EC`; `.rec` `#FF4D4D`; `.polaroid` paper `#F6F3EA`; polaroid caption `#2A2A2A`; overlays `rgba(4,10,14,.78)` (snapBox small), `.45` (mintPol), `.62` (gover); game key hints `rgba(232,240,234,.55)`.

### JS palettes
- `P` (L315), Blobsquatch: pink `#FDACCD`, rose `#E480A6` (used for the fingertips in the dump scene), deep `#C8608C`, eye `#3A1230`. Only `rose` is used.
- `Q` (L350), Barry: hat `#C9B27C`, band `#6E5F3B`, skin `#E3AE86`, skin2 `#C98F68`, jacket `#55673A`, jacket2 `#45542F`, plaid `#E3A93C`, pants `#7E6E52`, boot `#2A221B`, ink `#0B1112`, cam `#1A1D1F`, lens `#5A8796`, chair `#2F6B5A`, metal `#8C979A`.
- Bear (L803): `#7A5236` body, `#5A3B26` dark, `#C79B72` muzzle, `#1A0F0A` nose/eyes.
- Deep-woods 3D shading (L524): `FOG=[30,58,68]`, `LIT=[236,240,228]`. Trunk `[46,37,30]`, fern `[30,74,44]`/`[24,62,38]`, log `[58,44,32]`, moss `[46,92,52]`, log end `[88,66,46]`.
- Sky `#081226`→`#16343E`, moon `#F3EBC8`, ground `#1A3530`→`#0B1912`, canopy `#0A1C1A`/`#0E2620`/`#12302A`, foreground ferns `#0C2216`/`#0F2A1B`, twig `#8A6040`.
- Canvas text outline `#071012` (`bigText`). Pop colors: `#FF8A8A` (penalty), `#FFB59A` (blobsquatch), `#2EE6A6` (clear), `#FFC65C` (blurry), `#E8F0EA` (missed), `#FFB3D3` ("HA HA!").

### Type scale
- body 17px/1.55 Rubik
- `.logo` 30px Bagel (23px ≤560px), with `small` VT323 18px muted (hidden ≤560px)
- `h1` Bagel 400 `clamp(40px,8vw,84px)` lh 1
- `h2` Bagel `clamp(30px,5vw,46px)` lh 1.05
- `.lede` 19px; `.sub` muted, max 62ch; `.note` 14px muted
- buttons Bagel 18px, letter-spacing .3px
- `.num span` VT323 19px uppercase .06em; `.num b` Bagel 26px pink; `.num p` 15px
- `.panel b.t` Bagel 22px pink
- `.dict .word` Bagel `clamp(30px,5vw,44px)` (defined but there is no `.dict` element)
- `.defn` 17px muted, with `b` Bagel 22px fog, `.pron` VT323 19px
- HUD VT323 `clamp(14px,2.4vw,22px)`
- canvas display font `FONT_D='"Bagel Fat One", sans-serif'`; canvas mono `VT323, monospace`

### Components
- **Buttons** (`.btn, button`, L26-29): pink bg, pink-ink text, 3px pink-ink border, radius 14px, padding 7px 16px, `box-shadow:4px 4px 0 var(--shadow)`, transition transform .08s. `:active` translates (3px,3px) and the shadow shrinks to 1px 1px. `:focus-visible` gets a 3px amber outline, offset 3px. `.ghost` is transparent with a fog border and fog text.
- **Panels** `.panel`: panel bg, 2px line border, radius 18px, padding 14px 16px, grid gap 8px.
- **Number card** `.num`: same as a panel, gap 2px.
- **Contract chip** `.ca`: flex, panel bg, 2px line border, radius 14px, padding 10px 12px, margin-top 14px. Label VT323 19px uppercase muted, `code` 15px wraps anywhere, Copy button 15px with no shadow. `.cachip` max-width 560px.
- **Stage** `.stage`: relative, 3px line border, radius 24px, overflow hidden, `aspect-ratio:16/10`, bg `#0A1430`, shadow 8px 8px 0.
- **Polaroid**: `#F6F3EA` paper, padding 8px 8px 6px, shadow `0 8px 24px rgba(0,0,0,.5)`, rotate(-3deg). Canvas `clamp(72px,20vw,170px)` square, caption VT323. `.big`: canvas and caption `clamp(110px,26vw,240px)`. `.ex` (NFT grid): rotations -2°, 1.5°, -1°, 2.5° for children 1-4; canvas 100% wide; figcaption VT323 16px centered, `white-space:pre-line`.
- **Chip** `.modes .chip`: Rubik 600 15px, pill, transparent, 2px line border, no shadow. `[aria-pressed="true"]` is pink with pink-ink text and border.
- Animations: `.go` → `bob` 1.6s ease-in-out infinite (translate 0 → -4px → 0). `.develop` → `develop` 3.2s ease-out both: 0% `brightness(2.2) saturate(0) blur(6px)` opacity .35, 60% `brightness(1.2) saturate(.6) blur(1px)` opacity .9, 100% no filter, opacity 1.

### Layout
`.wrap` max-width 1040px, centered, `padding-inline:16px`, `padding-block:0 64px`, grid gap 44px. `section{scroll-margin-top:80px}`.

---

## 3. Page sections in DOM order (verbatim copy)

Everything sits in `<div class="wrap">` (L156).

### 3.1 `header.topbar` (L157-162)
Sticky: `top:env(safe-area-inset-top,0px)`, z 20, flex space-between, `--night` bg, padding-block 12px, 2px `--line` bottom border.
- `.logo`: `<span class="b">BLOB</span>` (pink, `filter:blur(1.4px)`) + `<span class="s">SQUATCH</span>` (pink, sharp) + `<small>on NEAR</small>`.
- `<nav class="links" aria-label="Blobsquatch links">` holds one `a.btn href="#buy"`: **"Buy<span class="full"> $BLOBSQUATCH</span>"**. At ≤560px `.full` is hidden, so the button reads **"Buy"**, at 15px with padding 4px 10px.

### 3.2 `section.hero` (L164-170), no id
- `h1`: **"Nobody's gotten a <span class="blur">clear picture</span>. Yet."** ("clear picture" is pink with blur 3px; the CSS also styles `h1 em` mint-highlighted, but there is no `em`.)
- `p.defn`: **`<b><span class="b">blob</span>·squatch</b> <span class="pron">/ˈblɑbˌskwɑtʃ/</span> <i>noun.</i> A blurry photo someone swears is Bigfoot.`** ("blob" blurred 1.6px.)
- `p.lede`: **"Every photo of Blobsquatch is a pink blur. Barry has been trying to get a clear shot since 1967. Go squatching with him."**
- `.ctas`: `a.btn href="#buy"` **"Buy $BLOBSQUATCH"** and `a.btn.ghost href="#game"` **"Play Snap the Squatch"**.
- `.ca.cachip`: label **"Contract"**, `code#caTop` **"Posted at launch"**, `button.copyBtn data-target="caTop"` **"Copy"**.

### 3.3 `section.stagebox#spot` (L172-188): the hero canvas
`.stage#stage` contains:
- `canvas#c`, `aria-label="Barry the Squatcher sneaks up on Blobsquatch in a night forest"`.
- `div.banner#banner` (hidden). An absolute mint pill at top 5%, centered, rotated -3deg, Bagel `clamp(20px,4.4vw,40px)`, 3px shadow-colored border, radius 12px. JS shows it with the text **"PUMPING!"** during the pump scene only.
- `button.stagebtn.go#goBtn` (hidden): **"Go Squatching"**. Bottom 6%, centered, `clamp(16px,3vw,22px)`, bobbing. Shown only in `rest` mode of the squatching scene.
- `a.btn.stagebtn#wake href="#buy"` (hidden): **"Wake Barry up"**. Shown only in the dump scene.
- `div.snapBox#snapBox` (hidden; bottom 5%, centered grid, gap 6px, max 92% wide):
  - `button#snapBtn` **"Snap a pic"**
  - `<small>` **"Mints your Blobsquatch NFT · 3 NEAR · free if you hold 1M+ $BLOBSQUATCH"**, styled as a dark pill.
  - Shown in modes `ready` and `minting`.
- `div.mintPol#mintPol` (hidden; inset 0, z 3, flex center, `rgba(4,10,14,.45)` scrim):
  - `.polaroid.big` with `canvas#nftCv` 360×360 (`aria-label="Your Blobsquatch NFT photo"`) and `span#nftCap`.
  - `.gtext` with `b#nftTitle` **"Still developing."** (pink Bagel `clamp(20px,5vw,44px)`), `span#nftMsg`, and `button#backWoods` **"Back to the woods"**.
  - Shown 450ms after the photo is taken.

Below the stage:
- `p.stagenote`: **"Going squatching is free. Snapping a pic mints your Blobsquatch NFT, and it develops later. <a href="#nft">How the NFTs work</a>"** (link in pink).
- `div.modes#preview role="group" aria-label="Preview the chart modes"`: `<span>Preview the chart:</span>` followed by three `button.chip`s: **"Normal"** (`data-pct="0"`, `aria-pressed="true"`), **"Pumping"** (`data-pct="5"`), **"Dumping"** (`data-pct="-5"`). The whole group is hidden once live DexScreener data arrives.
- `p.note`: **"At launch the scene follows the real $BLOBSQUATCH chart. Up 2% in the last hour, they both lose it. Down 2%, Blobsquatch hides and Barry dozes off."**
- `p.status#claimStatus role="status"`: amber, empty by default. Messages are listed in §4.4.

### 3.4 `section#nft` (L190-228)
- `h2` **"1,967 Polaroids. One per wallet."**
- `p.sub` **"Every Blobsquatch NFT is a photo from your own sighting, and there's more than one blobsquatch out there. Fur, tuft, size, expression, pose, setting and film are picked when you mint, so no two shots are the same."**
- `.pols` (`aria-label="Example Blobsquatch NFTs"`, 4 columns, 2 at ≤760px, gap 18px): four `figure.polaroid.ex`, each with a `canvas` 300×300 and an empty `figcaption` that JS fills (see `EXAMPLES`):
  1. "#352 · 1 of 1\nStill developing"
  2. "#0120\nStill developing"
  3. "#0954\nStill developing"
  4. "#1967\nStill developing"
- `p.note` **"Every Polaroid stays undeveloped until the reveal. Nobody's gotten a clear picture. Yet."**
- `.duo` (2 columns, 1 at ≤760px):
  - Panel 1, `b.t` **"How to get one"**:
    - `ol.plain`:
      1. "Tap **Go Squatching**. It's free."
      2. "When you're close, tap **Snap a pic** and approve the mint in your NEAR wallet."
      3. "Your Polaroid starts developing. That's your NFT."
    - `ul.rules`:
      - "**3 NEAR**, or free if your wallet holds 1,000,000+ $BLOBSQUATCH."
      - "One per wallet. 1,967 in total."
      - "Polaroids develop when all 1,967 are minted, or on the reveal date, whichever comes first."
      - "Before the mint opens, we post a fingerprint of the final art (a provenance hash), so nobody can rig who gets the rare ones."
      - "#352 is a one of one, "Frame 352," named for the film's famous look-back frame."
  - Panel 2, `b.t` **"Where your 3 NEAR goes"**:
    - `ul.split`:
      - "**1 NEAR** buys $BLOBSQUATCH on the open market and burns it."
      - "**1 NEAR** goes to the Squatcher Stash."
      - "**1 NEAR** goes to the creator."
    - `p.note` (margin 0): "Resales pay a 3% royalty: 1% buys and burns $BLOBSQUATCH, 1% goes to the Squatcher Stash and 1% to the creator. Every burn is posted in Field notes with its transaction."
    - `p.note` (margin 0): "Traits: fur, tuft, expression, size, pose, setting and film, plus a very rare, completely blurry "true blobsquatch.""
- `.ctas`: `a.btn href="#spot"` **"Go Squatching"**.

### 3.5 `section#game` (L230-250)
- `h2` **"Snap the Squatch"**
- `p.sub` **"Blobsquatch are hiding in the trees, and there's more than one. Keep one in your crosshair until the focus ring locks, then snap. Far shots pay the most but take the longest to focus. Snap too soon and all you get is a blobsquatch. Don't photograph bears. Or Barry."**
- `div.gamebox#gameBox tabindex="0"`. 16/10, radius 22px, bg `#06101A`, `touch-action:none`, no user-select, amber focus ring. `aria-label`: **"Snap the Squatch game. Move to aim and click to take a photo. On a phone, hold to focus and let go to snap. Arrow keys aim and space snaps."**
  - `canvas#gcv`. Gets `cursor:none` while the box has class `.playing`.
  - `div.gover#gOver` (visible at load; inset 0, z 2, flex, scrim `.62`):
    - `.polaroid#pol` (hidden) with `canvas#polCv` 360×360 and `span#polCap`.
    - `.gtext`:
      - `b#gTitle` **"Snap the Squatch"** (pink Bagel `clamp(20px,6vw,54px)`)
      - `span#gMsg` **"Hover to focus, click to snap. On a phone, hold to focus and let go to snap."**
      - `button#gPlay` **"Play"**
  - `div.ghud` (VT323, top 8px, values amber): `<span>RND <b id="gRound">1</b> · SEEN <b id="gSight">0/10</b> · CLEAR <b id="gClear">0/4</b></span>` and `<span>FILM <b id="gFilm">▮▮▮</b> · SCORE <b id="gScore">0</b> · BEST <b id="gBest">0</b></span>`. It has no z-index, so it renders under the `.gover` scrim (dimmed) when the overlay is up.
- `.wallet`: `button.ghost#wConnect` **"Connect NEAR wallet"**, `span#wStatus` **"Connect a NEAR wallet to log your scores."**
- `p.note` **"Any future airdrop would go to wallets that also hold $BLOBSQUATCH. Nothing is promised."**

### 3.6 `section#stash` (L252-277)
- `h2` **"Squatcher Stash"**
- `p.sub` **"The community's fund. It starts with 1% of the supply, and it collects 1 NEAR from every NFT mint plus 1% of every NFT resale."**
- `.nums.three` (`aria-label="Receipts"`, 3 columns, 1 at ≤640px):
  - **Raised from mints**: `b#rRaised` "0 NEAR", "Every paid mint, counted from the chain."
  - **Burned**: `b#rBurned` "0", "$BLOBSQUATCH bought on the open market and burned."
  - **Stash balance**: `b#rStash` "0 NEAR", "What the Squatcher Stash holds right now."
  - These are static placeholders. No JS writes them.
- `p.note` **"Receipts go live at launch and update from the chain."**
- `.duo`:
  - Panel **"What it pays for"**: `ul.rules`:
    - "Prizes for top Snap the Squatch players."
    - "Marketing and contests."
    - "Art for new NFT traits and seasons."
    - Then `p.note`: "Down the road, Blobsquatch might get a say in how it's spent."
  - Panel `.notes` **"Field notes"**: `div.empty` (dashed border): "Every Stash payment and every burn gets logged here with a link to the transaction. The first entry lands at launch."
- `.ca`: **"Stash wallet"**, `code#stashAddr` "Posted at launch", Copy.

### 3.7 `section#buy` (L279-295)
- `h2` **"Get $BLOBSQUATCH"**
- `.nums` (4 columns; 2 at ≤820px; 1 at ≤420px):
  - **Total supply**: **1 billion**. "1,000,000,000 $BLOBSQUATCH. No more can ever be made, and every NFT mint burns some."
  - **Airdrop**: **Coming**. "A share of the supply goes to active NEAR wallets. The size and snapshot are posted before launch."
  - **Liquidity**: **Locked**. "Launch liquidity goes into a NEAR pool and the LP is locked. No presale, and 0% buy or sell tax."
  - **Team**: **5%, locked**. "It unlocks on a public schedule, so you can see every token before it moves. A separate 1% seeds the Squatcher Stash."
- `ol.plain.buysteps`:
  1. "Get a NEAR wallet, like Meteor, HOT, or MyNearWallet."
  2. "Buy some NEAR and send it to your wallet."
  3. "Open the Blobsquatch launch, or paste the contract into a NEAR swap. Links go up at launch."
  4. "Swap for $BLOBSQUATCH. You're a Squatcher."
- `.ca` **"Contract"** `code#ca` "Posted at launch" + Copy.
- `.ca` **"Team wallet"** `code#dev` "Posted at launch" + Copy.

### 3.8 `footer` (L297-300)
14px muted, max 74ch.
- "$BLOBSQUATCH is a meme token for fun, with no intrinsic value and no expectation of financial return. Not financial advice. Blobsquatch is a fan of NEAR and isn't affiliated with or endorsed by the NEAR Foundation."
- "No clear photos of Bigfoot were taken in the making of this site."

**Tokenomics as stated on the page:**
- 1,000,000,000 total supply, fixed.
- Airdrop to active NEAR wallets (size TBD).
- LP locked, no presale, 0% tax.
- Team 5%, locked on a public unlock schedule.
- Stash seeded with 1% of supply.
- NFT: 1,967 supply, one per wallet, 3 NEAR or free with ≥1M tokens. The 3 NEAR splits 1/1/1 to burn, Stash and creator.
- 3% resale royalty, split 1/1/1 the same way.
- #352 is the 1/1 "Frame 352".
- Very rare "true blobsquatch" trait, which is fully blurry.
- Reveal: all minted, or the reveal date, whichever comes first.
- Provenance hash posted before mint.

There is no roadmap and no FAQ section.

---

## 4. JavaScript architecture

### 4.1 Helpers (L304-311)
- `$=id=>document.getElementById(id)`
- `reduce` = `prefers-reduced-motion: reduce`, read **once at load** (not live).
- `DPRx()` = `min(1.5, devicePixelRatio)`. All canvases cap DPR at 1.5.
- `lerp`, `clamp`.
- `sm(x)` = cosine ease `.5-.5cos(πx)` on clamped x.
- `fmt` = rounded `toLocaleString('en-US')`.
- `FONT_D`.

### 4.2 Global constants and config
| Name | Line | Value | Notes |
|---|---|---|---|
| `SQ_CX, SQ_FT, SQ_HM` | 318 | 440, 1166, 1025 | sprite-space center x, feet y, height (1166-141) |
| `PIV_L, PIV_R` | 318 | [176,640], [704,640] | shoulder pivots (sprite space) |
| `HEADCLIP` | 319 | Path2D `M224,505 C232,380 300,230 485,146 C610,215 690,330 700,505 L705,610 L220,610 Z` | head silhouette clip used for the look-back face |
| `HZ` | 455 | .6 | horizon for legacy `scenery()` (dead) |
| `EYE, FOV, SQZ, CLEAR_X, DOLLY, SQ_H` | 511 | 1.35, .9, 14, .1, 9.2, 2.5 | deep-woods 3D camera |
| `NFT_SUPPLY` | 627 | 1967 | |
| `MINT_PRICE` | 627 | `'3 NEAR'` | |
| `FREE_HOLD` | 627 | `'1M+'` | |
| `REVEAL_DATE` | 627 | `''` | e.g. `'Dec 1'` once set; changes the `nftMsg` text |
| `POSES` | 631 | Glance Left, Glance Right, Mid-Stride, Wave, Startled | NFT traits |
| `SETTINGS` | 631 | Night, Dawn Fog, Snow, Rain, Campfire | |
| `FILMS` | 631 | Polaroid, Trail Cam, Disposable, Night Vision | |
| `EXAMPLES` | 689 | ids 352/120/954/1967 + captions | |
| `PAIR` | 725 | `''` | DexScreener NEAR pair address (Ref Finance pool) |
| `PUMP, DUMP` | 726 | 2, -2 | % change over the last hour |
| `LAYERS` | 761 | see §6 | game depth layers |
| `SIGHTS` | 766 | 10 | sightings per round |
| `NEED(r)` | 766 | `min(3+r, 8)` | clear shots needed |
| `GAME_LOG_URL` | 951 | `''` | POST `{account, score, at}` |

**Wallet hook** (comment L619-626). At launch the host page defines:
```js
window.BLOBSQUATCH_WALLET = {
  signIn: async () => accountId,
  mint:   async () => ({ tokenId, traits:{ pose, setting, film, ultra } })
}
```
The comments say the contract enforces: max 1,967, one per wallet, 3 NEAR, free at 1M+ held, the 1/1/1 split, #352 as the 1/1, 3% royalties, undeveloped until sold out or `REVEAL_DATE`, and a provenance hash.

### 4.3 Mutable globals
- `ctx, W, H, DPR`: hero canvas context and CSS size.
- `bgCache`: legacy, filled only by the dead `bg()`; cleared on resize.
- `off/ox`: shared offscreen canvas for `soft()`.
- `S`: hero state.
- `account` (wallet id or null).
- `ph`: pump dance phase.
- `pct`: current 1h % change, from preview chips or DexScreener.
- `live`: true once DexScreener returned a number.
- `last`: frame timestamp.
- `grain`: 160×160 noise canvas with alpha 26/255.
- `GW, GH, GD, gBg, gTrees`: game canvas size and cached art.
- `G`: game state.
- `tmpC`: capture scratch canvas.
- `gLast, gt`: game clock.
- `armed`: game box has focus.

### 4.4 Hero state object `S` (L504)
`S={mode:'rest', t:0, glance:0, frozen:null, flash:0, nft:null}`
- `mode`: `rest | approach | ready | minting | twig | glance | frozen`
- `t`: seconds in the current mode. `setMode(m)` sets the mode and resets `t=0`. `t` only advances inside `sceneSquatching`, so it stops during pump/dump.
- `glance`: 0..1 head-turn amount. Persists into `frozen`. Reset to 0 by "Back to the woods" or a chip click.
- `frozen`: canvas snapshot (from `freezeFrame()`).
- `flash`: 1 → 0 white flash overlay in frozen mode.
- `nft`: `{id, pose, setting, film, ultra, preview}` for the shot.

**Transitions:**
| From | Trigger | To | Side effects |
|---|---|---|---|
| `rest` | click `#goBtn` (only works in `rest`) | `approach` | status "Shh. Sneaking up on him…" |
| `approach` | `S.t >= 2.6` s | `ready` | |
| `ready` | click `#snapBtn`, no `window.BLOBSQUATCH_WALLET` | `twig` | `S.nft=randomNFT()` (preview:true); status "Preview. At launch, this connects your NEAR wallet and mints your NFT." |
| `ready` | click `#snapBtn`, wallet present | `minting` | status "Connecting your wallet…", then `connect()`, then "Approve the mint in your wallet: 3 NEAR, or free if you hold 1M+ $BLOBSQUATCH.", then `await mint()` |
| `minting` | mint resolves | `twig` | `S.nft={id:r.tokenId,...r.traits,preview:false}`; status cleared |
| `minting` | mint/connect throws | `ready` | status = the error message if it matches `/sold out\|already/i`, else "Nothing was minted. Tap Snap a pic to try again." |
| `twig` | `S.t >= .55` s | `glance` | |
| `glance` | `S.t >= .55` s (`shoot`) | `frozen` | frame drawn with flash lighting; `S.frozen=freezeFrame()`; `S.flash=1`; `setTimeout(showNFT,450)` |
| `frozen` | click `#backWoods` | `rest` | hide `#mintPol`, `glance=0`, `frozen=null`, status cleared |
| any non-rest | click a preview chip | `rest` | same reset as Back to the woods |

**Scene selection each frame** (`frame()`, L736-744):
- if `pct>=2 && S.mode==='rest'` → `scenePump`, intensity `k=clamp((pct-2)/8,0,1)`
- else if `pct<=-2 && S.mode==='rest'` → `sceneDump`, `k=clamp((-2-pct)/8,0,1)`
- else → `sceneSquatching`

`dt` is capped at .05s. So pump and dump replace the rest state only. A chart move during an approach or mint does not interrupt it. While pumping or dumping, the Go button is hidden, so **you cannot start squatching until the chart calms** (or a user clicks Normal while chips are visible).

**Overlay control** `overlay(txt,go,wk)` sets the banner text and hidden state, `goBtn.hidden=!go` and `wake.hidden=!wk`. `snapBox.hidden` is set directly in `sceneSquatching` (visible in ready/minting). In the pump and dump scenes `snapBox` is not touched; it stays hidden because they only run in rest.

### 4.5 Status messages (`say()` → `#claimStatus`), verbatim
- "Shh. Sneaking up on him…"
- "Preview. At launch, this connects your NEAR wallet and mints your NFT."
- "Connecting your wallet…"
- "Approve the mint in your wallet: 3 NEAR, or free if you hold 1M+ $BLOBSQUATCH."
- "Nothing was minted. Tap Snap a pic to try again." (or the raw error message when it contains "sold out" or "already")
- "" (cleared)

### 4.6 Wallet and score logging
- `connect()` (L630): returns the cached `account`, or `await BLOBSQUATCH_WALLET.signIn()`. On success it sets `#wStatus` to `Connected: ${account}. Your scores are logged.`.
- `#wConnect` click: with no hook → "Wallet connect turns on at launch."; on failure → "Couldn't connect. Try again from your wallet app."
- `logPlay(score)`: only on game over, only if `account && GAME_LOG_URL`. Sends `POST JSON {account, score, at: Date.now()}` and ignores errors.

### 4.7 Copy buttons (L751)
Each `.copyBtn` copies `$(data-target).textContent` through `navigator.clipboard`. The label becomes "Copied". If the clipboard is unavailable, it selects the text instead. The label goes back to "Copy" after 1500ms either way. Right now this copies "Posted at launch".

### 4.8 Live price (L723-733)
`pull()`: if `PAIR` is set, it fetches `https://api.dexscreener.com/latest/dex/pairs/near/${PAIR}` and reads `(d.pair || d.pairs[0]).priceChange.h1`. If that is a number: `pct=h1`, and on the first success `live=true` and `#preview` is hidden. Errors are swallowed. It runs once at load, then every 60,000ms.

**Fallback:** if `PAIR` is empty or a fetch fails, `pct` stays at its last value (0 by default, or the chip choice). The chips are the only manual control. There is no other price source.

---

## 5. Canvas scenes and animation

### 5.1 Blobsquatch sprite rig
`ART` (L316) maps keys to `{x,y,w,h,src}` in a **sprite coordinate space about 880 wide**, the master art's px. `src` is base64 WebP, stored at about 72% scale. The `_meta` key holds `pivL:[176,640,72]` and `pivR:[704,640,72]`; the third number is 72, which matches the 72% storage scale. `_meta` itself is unused (the pivots are hard-coded in `PIV_L/PIV_R`).

| Key | x,y,w,h (sprite space) | Stored px | Use |
|---|---|---|---|
| `armL` | 43,565,209,466 | 150×336 | left arm, rotates about `PIV_L` |
| `armR` | 629,565,209,466 | 150×336 | right arm, rotates about `PIV_R` |
| `front` | 105,141,671,1028 | 483×740 | body facing the viewer, face baked in |
| `back` | 105,141,671,1028 | 483×740 | body from behind |
| `face` | 273,313,345,299 | 248×215 | neutral face; used only for the look-back over `back` |
| `faceHappy` | 273,313,345,299 | 248×215 | happy face drawn over `front` |

At load, `SPR[k]=new Image()` is created from each `src`, then `src` is deleted from `ART` (L317). `spr(g,k)` draws a sprite at its box once loaded. `sprPart` draws a sub-rectangle (in sprite space) with an offset. `armAt(g,k,pivot,ang)` rotates a sprite about a pivot.

**`squatch(g, h, t, o)`** (L325) draws him with feet at (0,0), `h` px tall. Scale `s=h/1025`, then translate `(-440, -1166 + bob/s)`. Options:
- `bob`: vertical offset in px (negative = up).
- `tilt`: rotation in rad about the sprite point (440,727), roughly the belly.
- `arms`:
  - `'dance'`: `aL=2.45+.32·sin(t·sp)`, `aR=2.45-.32·sin(t·sp)` (arms overhead, pumping alternately).
  - `'up'`: both 2.5.
  - `'wave'`: right arm `2.55+.28·sin(9t)`, left arm 0.
  - `'none'`: no arms drawn.
  - Anything else (e.g. `'down'`) with `walk:true` → swing `sw=.09·sin(5t)` (aL=sw, aR=-sw). Otherwise 0.
  - Angle 0 means hanging; larger values rotate up and out. The left arm rotates by `+aL`, the right by `-aR` (mirror).
- `back`: draw `back` + arms. Then if `glance>0`: clip to `HEADCLIP` and draw `face` translated by `off = gside·((1-gl)·230 + 95·gl)`, horizontally squashed `sx=.55+.27·gl` about x=445. The face slides in from the side of the head as he looks over his shoulder. `gside` -1 means he looks to the viewer's left (the hero uses -1).
- else: `front`. With `splay`, add a foot: `sprPart(front, 465,1068,230,102)` shifted +175px x, so a foot pokes out from behind the tree. Then arms, then `faceHappy` if `happy`.

**`soft(g,dpr,x,y,w,h,q,fn)`** (L478) is the blur mechanic. It renders `fn` into the shared offscreen canvas at resolution `max(.03,q)·dpr` and upscales with high-quality smoothing, so a low `q` gives a pink blob. **`drawSquatchAt(g,dpr,x,feet,h,q,t,o)`** wraps `squatch` in a `1.25h × 1.2h` soft box.

### 5.2 Barry the Squatcher: `squatcher(g,h,t,mood)` (L360)
Procedural, feet at (0,0), facing right, `h` = total height. Structure:
- Legs: pants strokes, width `.085h`, from hip `-.44h`.
- Boots: ellipses.
- Body: translate to the hip, then rotate (`squint` +.12 rad lean, `elated` -.05).
- Back arm (jacket2), torso rounded rect (jacket) with a plaid collar triangle, center seam and pocket.
- Head circle at `hy=-.49h` above the hip, r `.095h`; nose; ear (skin2); stubble ellipse.
- Bucket hat (crown rect + brim ellipse + band).
- Face per mood, front arm per mood.
- `camera(g,x,y,s)` (L352): body + top plate + lens barrel `#5A8796` + highlight, facing right.

Moods:
| Mood | Where used | Look |
|---|---|---|
| `squint` | hero `rest` | leaning in; hand flat over brow as a visor; squint lines; flat mouth; camera on chest strap |
| `watch` | hero `approach`; game Barry | neutral dot eye + brow, small smile; camera on chest strap; back arm hanging |
| `aim` | hero `ready/minting/twig/glance` | camera raised to eye (`camera` at `(.12h, hy-.005h)`, size .085h); open half-circle mouth; both arms up holding it |
| `frenzy` | pump scene | same as aim + horizontal jitter `sin(45t)·.006h` + camera flash bursts: a cream circle at `(.08h, hy-.075h)` r .06h whenever `(4.5t)%1 < .18`, fading |
| `elated` | **unused** | jump `|sin 7t|·.05h`, camera held overhead, big white eye, open mouth |
| `sleep` | dump scene | `sleeper()`: metal camp chair with green `#2F6B5A` seat/back; legs stretched out; torso reclined -.35 rad; camera on belly; head breathing `sin(1.6t)·.006h`; small open mouth; hat tipped over the eyes (rotated .35); dangling arm |

Reduced motion turns off the jump, jitter, frenzy flash and breathing.

### 5.3 Hero "deep woods" 3D scene (`drawForest`, L551)
A tiny perspective world. `P3(x,y,z,camZ)` gives: `d=z-camZ`, `f=H·FOV/d`, `screen=(W/2 + x·f, H·.48 + (EYE-y)·f)`. The camera dollies `camZ = DOLLY·k` (k: 0 → 1). Blobsquatch stands at `z=SQZ=14`, `SQ_H=2.5` units tall. At rest, `d=14` and he is about 0.16·H tall. At k=1, `d=4.8` and he is about 0.47·H tall.

`FOREST` (L512) is generated with a seeded Park-Miller PRNG (seed 21, `s=s·16807 % 2147483647`):
- **Trunks**: two framing trunks `{x:-1.3,z:13.2,w:.5}` and `{x:1.55,z:13.0,w:.55}`, plus 90 random ones: `z∈[1.8,39.8]`, `x∈±(3.5+z·.5)`, `w∈[.22,.64]`. Skipped if `z<14 && |x-.1|<1.15` (keeps the line of sight open) or `12.6≤z<16.5 && |x-.1|<1.9` (the clearing).
- **Ferns**: 140 at `z∈[1,31]`, `x∈±(2.5+z·.45)`, size `.3–.85`, skipped in the approach corridor (`9.5<z<14.5 && |x-.1|<1`). Plus 5 ferns around his feet at z≈13.4–13.9.
- **Canopy**: 260 leaf ellipses at `x∈[0,1]`, `y=r^1.8·.2` (top 20%), with a moon gap at x .66–.86, y<.17.

Draw order:
1. `forestBackdrop`: sky gradient `#081226→#16343E` over the top 50%; moon `#F3EBC8` at (.76W, .1H) r .045H; ground `#1A3530→#0B1912` from .48H; fog band `rgba(40,70,80,.55)` across .3–.62H.
2. Optional `candles(up|down)`.
3. Painter's sort, farthest z first:
   - **trunks**: rect from the top down to the ground point, plus a flared root, shaded by `shade()`; within 14 units, dark grooves and a cool rim light.
   - **ferns**: 7 ellipse fronds each.
   - **moonbeam** at z 14.6: additive trapezoid from the top (`gx+W·.1`) down to the clearing, plus a ground pool ellipse.
   - **log** at z 3.2, spanning x -2.8 to -0.3, 0.5 tall, with moss and a cut end.
   - **Blobsquatch** at z 14.
4. `forestCanopy(k)` scales by `1+.08k`, so the zoom-in pushes leaves outward.
5. Optional dark overlay `rgba(0,4,8,o.dark)`.

`shade(base,d,FL)`: fog mix `clamp((d-2)/24)·.9` toward `FOG`. With flash `FL`, things nearer than 7 units are lit toward `LIT` (`FL·(1-d/7)·.8`).

Blobsquatch inside the forest: `q = lerp(.13, 1, k^1.4)`, so he is blurry far away and sharp up close. He is drawn with `back:true, walk, bob, glance, gside:-1`. Walking bob is `|sin(t·(k>.5?3:5))|·h·.025` when `S.glance===0` and motion is allowed. When the flash fires there is an additive glow on him. The function returns the box `{x,y,h}` for the viewfinder.

### 5.4 `sceneSquatching(t,dt)` (L581), per mode
- **frozen**: blit `S.frozen`; flash overlay `rgba(255,252,235,S.flash)` with `S.flash -= dt·2.2` (about 0.45s); hide all buttons and the snapBox; return.
- `k`: `rest` 0; `approach` `sm(S.t/2.6)` (cosine ease over **2.6s**); otherwise 1.
- **Wander**: at rest he paces between trunks, `x = .1 + sin(.22t)·3.1` world units (about a 28.5s cycle). `sqx = lerp(wanderX, .1, k)` slides him into the clearing as you close in. With reduced motion he stays at .1.
- **glance**: `S.glance = min(1, S.t/.3)` (a 0.3s head turn). At `S.t >= .55` it shoots.
- **Barry** (foreground): height `rh=.62H`, at x `.15W`, feet `1.07H - creep`, where `creep=|sin(6·S.t)|·.012H` during approach (a sneaking bob). Mood: rest `squint`, approach `watch`, else `aim`.
- On the shoot frame: an additive radial flash from (.3W, H), r .7H, alpha .35, and the forest is drawn with `FL=1`.
- `foreFerns(t,k,creep·.6)`: four big black-green ferns at fx/fy/size: (.06,1.04,.24), (.22,1.06,.2), (.92,1.05,.26), (.78,1.08,.18) ×W/H. Sway `sin(1.3t)·.05` rad.
- **Twig** (in twig and glance modes): a broken brown twig at `(bx+rh·.2, .975H)`, size .05H. In `twig` only, add three amber crack lines and the canvas text **"snap!"** (Bagel, amber `#FFC65C`, rotated -.12, size .045H) above it.
- **Viewfinder** (ready/minting/twig/glance): white L-brackets around his body (half-width .42h, from y-1.08h to y-.02h, arm .12h) and a mint `#2EE6A6` focus square on his head (center y-.82h, half-size .07h).
- At the end of each frame: `overlay('', mode==='rest', false)` (the Go button shows only in rest), and the snapBox shows in ready/minting.

**Timeline after "Snap a pic"** (preview path): twig 0.55s → glance (head turns over 0.3s, shot at 0.55s) → frozen flash (about 0.45s) → Polaroid overlay appears at +450ms → CSS develop animation 3.2s.

### 5.5 Photo and developing Polaroid
- `freezeFrame()` copies the hero canvas at device resolution.
- `showNFT()` (L691) uses `n = S.nft || randomNFT()` and calls `renderDeveloping(#nftCv, n.id)`. Caption: `Blobsquatch #${id padded to 4}` (e.g. "Blobsquatch #1781"). Message: `It develops when all 1,967 are minted or on the reveal date, whichever comes first.`. If `REVEAL_DATE` is set, "on the reveal date" becomes `on ${REVEAL_DATE}`. Preview mints add ` (Preview.)`. It restarts the `.develop` class (skipped under reduced motion) and unhides `#mintPol`. The title stays "Still developing."
- `renderDeveloping(c, seed)` (L677) draws an undeveloped Polaroid:
  - a milky gradient `#A9A596→#C9C4B4→#8F8B7C`;
  - 5 faint vertical "trunk" bands `rgba(40,52,46,.22)`;
  - one soft pink radial blob (position and size from the seeded hash `nh()`);
  - a milk haze, film grain and a vignette.
  - It is deterministic per id.
- `randomNFT()` returns `{id:1..1967 random, pose, setting, film random, ultra: 3% chance, preview:true}`.
- `renderNFT(c, n)` (L651) is **defined but never called**. It is the future revealed photo: the same deep woods (no Blobsquatch, k=1) drawn into the square, then Blobsquatch at .66Z tall, feet .97Z, x .52Z, using `poseOpts`:
  - Glance Left/Right → back view, glance 1, gside -1/+1.
  - Mid-Stride → back view walking.
  - Wave → front, waving, happy.
  - Startled → arms up, happy.
  - `ultra` (true blobsquatch) → drawn through `soft()` at q .07, a total blur.
  - Settings:
    - Dawn Fog: peach sky tint + low fog.
    - Snow: white ground wash + 70 flakes.
    - Rain: darken + 90 streaks.
    - Campfire: orange additive glow at the bottom-left + 3 flames.
  - Films:
    - Trail Cam: desaturate, multiply `#DCE6D6`, text "CAM 03  47°F" bottom-left.
    - Night Vision: desaturate, multiply `#7CFF9A`, text "IR ●" top-left, heavier vignette.
    - Disposable: multiply `#FFE2B8`, orange date stamp "'67 10 14" bottom-right.
    - Polaroid: no treatment.
  - Then grain and a vignette. See `nft-renderNFT-trait-grid.jpg`.
  - Traits in copy that the renderer does **not** implement: fur, tuft, size, expression. They are not in `POSES/SETTINGS/FILMS`.
- `drawExamples()` renders the four `.polaroid.ex` canvases with `renderDeveloping(id)` and sets their captions. It runs at +60ms and again on `document.fonts.ready`. It no-ops if the hero `W` is 0.

### 5.6 PUMP scene (`scenePump(t,dt,k)`, L701). Trigger: `pct >= 2` in rest
- Background: `drawForest(t,1,0,0,0,false,{noSq:true,candles:'up'})`. That is the fully dollied-in woods (k=1), no back-view Blobsquatch, and green candles.
- `candles(up)`: 12 slots, bars i=2..10, alpha .2, `#2EE6A6`. Each bar is .36 of the slot wide, height `.06H + sin(1.7i)·.015H`, with a wick. The base rises `H·.5 - (i-2)·.03H`, a staircase going up to the right.
- Phase `ph += dt·(4 + 4k)` rad/s. With chip +5%, k = .375, so the rate is 5.5 rad/s.
- **Blobsquatch dance**:
  - Front view, sharp (q=1), happy face, height `.62H`.
  - x `= .68W + sin(ph·.5)·.03W` (side-to-side sway).
  - Feet at `.985H - hop`, with `hop=|sin(ph)|·.05H` (bouncing).
  - Arms `'dance'` with `sp = 8 + 6k` (both arms raised about 2.45 rad, ±.32 rad alternating at `sin(t·sp)`).
  - Body `tilt = sin(ph·.5)·.12` rad.
- **Barry**: `frenzy` at (.2W, feet 1.0H), height .62H.
- Strobe: whenever `(4.5t)%1 < .08`, a full-frame `rgba(255,250,230,.18)` flash. That is about 4.5 Hz, in sync with Barry's camera flashes.
- `overlay('PUMPING!', false, false)`: the mint banner shows "PUMPING!"; Go and Wake are hidden.
- Reduced motion: no sway, hop, tilt or strobe. The arms still move, because `squatch` dance arms are not gated.

### 5.7 DUMP scene (`sceneDump(t,dt,k)`, L710). Trigger: `pct <= -2` in rest
- Background: the forest at k=1, `noSq`, `candles:'down'` (red `#FF6B6B` bars stepping down from .18H), `dark:.3` overlay.
- **Blobsquatch hiding**: at `tx=.69W`, feet .94H, height .55H. Front view, `splay:true` (foot sticking out to the right), `arms:'none'`. He is then covered by a tree trunk `#2A2019` of width `.66h`, centered on tx, from `feet-.95H` to the feet. The trunk has five bark stripes `#352920`. Three rose `#E480A6` fingertip ellipses peek around the trunk's right edge at heights `feet-h·(.6, .645, .69)`. Net effect: only the fingertips and one foot are visible.
- **Barry dozing**: `squatcher(...,'sleep')` at (.24W, .99H), height .6H.
- **Zs**: `2 + round(3k)` letters "z" (3 at -5%). Each drifts on `p=(.4t + i/n)%1`: x `.27W + p·.07W`, y `.5H - p·.3H`, size `H·(.045 + .012i)`, alpha `1-p`, color `#E8F0EA`, Bagel with dark outline. Reduced motion freezes them at p=.4.
- `overlay('', false, true)` shows **"Wake Barry up"** (a link to `#buy`).

### 5.8 Legacy, unused hero code
`SCN`, `PAL` (normal/pump/dump flat palettes), `pine()` (also used by the game), `scenery()`, `bg()`, `bgCache`, `stars()`, `flies()` and `burst()` are the flat-forest scene from earlier versions. Only `pine` is still called (game art). `bg`, `stars`, `flies`, `burst` and `scenery` are never invoked.

---

## 6. The game: "Snap the Squatch" (L753-947)

**Concept** (comment L754-756): "Duck-Hunt-style photo game. Blobsquatch peeks and dashes between trees at three distances. Keep him in the crosshair to focus (far takes longest), then snap. Points = distance value × focus. Snap with no focus and you get a BLOBSQUATCH (10 pts). Bears and Barry cost points."

### 6.1 World
`buildGameArt()` caches the art on resize:
- sky `#081226→#1E4A52` down to the horizon `.56GH`;
- 55 deterministic stars;
- a moon glow and moon `#F3EBC8` at (.8W, .13H) r .05H;
- a distant pine row `#12303A`;
- ground `#14301F→#09170F`;
- a soft shadow ellipse per layer.

Each layer's trees are cached on their own canvas: bark rect + grooves + a highlight, and for FAR/MID a pine crown. NEAR trunks run off the top of the frame.

`LAYERS` (y and h are fractions of GH; tree x are fractions of GW):
| Layer | base y | actor h | pts | focus time `ft` | min blur `q` | trees x | bark / crown |
|---|---|---|---|---|---|---|---|
| FAR | .60 | .12 | 200 | 1.0 s | .18 | .1 .27 .44 .6 .76 .92 | `#22302B` / `#173229` |
| MID | .79 | .26 | 100 | .55 s | .42 | .13 .38 .63 .88 | `#2C2A22` / `#163A2B` |
| NEAR | 1.05 | .50 | 50 | .25 s | .80 | .03 .97 | `#30261D` / `#12301F` |

`lay(i)` gives `y=base·GH`, `hh=h·GH`, trunk width `tw = hh·.9` (FAR/MID) or `hh·.8` (NEAR). NEAR feet sit below the frame, since base is 1.05.

Draw order per frame: background, then for each layer far → near: the actor if it is on that layer (or the laughing squatch on MID), then that layer's trees. That is how actors hide behind trunks. Then Barry, viewfinder corners, pops, crosshair and flash.

### 6.2 Actors
`makeActor(kind)`:
- Layer: squatch FAR 32% / MID 40% / NEAR 28%; bear FAR 50% / MID 50%.
- Speed scale `rs = 1 + (round-1)·.18`.
- Starts at a random tree and gets 2–4 moves. Each move is a 55% **peek** (or always a peek when the layer has fewer than 2 trees): `{out:.22/rs, hold:(1.1–1.6)/rs, inn:.2/rs}`. Otherwise it is a **dash** to a different tree.
- It always ends with a dash offscreen to the nearer side (`-.15` or `1.15`).
- Peek side (`sideFor`): trees with x < .2 peek right, x > .8 peek left, the rest are random.

Peek motion: `pk` eases 0 → 1 (sm) → hold → 0. The actor's x is `tree + side·(tw·.55·pk)/GW`. He leans with `tilt = side·.12`.

Dash: duration `max(.15, |Δx|·GW / (hh·3·rs·(fast?1.8:1)))`, which is about 3 body-heights per second. Running uses `walk:true` and bob `|sin 12t|·.04h`.

Blobsquatch in the game uses the **front** sprite. `happy` is on once snapped or while laughing. Arms: `'up'` when laughing, otherwise none set, which means they hang or swing.

Bear (`bear(g,h)`) is a brown seated bear, drawn at `.85·hh`.

### 6.3 Hit testing
- `onActor`: x within `±.34h` of the actor, y within `[L.y-1.02h, L.y]`, and **not occluded**. Any trunk of the same or a nearer layer covers it when x is inside the trunk and y is above that layer's ground line.
- `onBarry`: Barry is `h=.62GH`, x from `fx-.16h` to `fx+.2h`, and `y > 1.1GH - 1.02h` (about the lower 53% of the screen).

### 6.4 Focus mechanic
Each frame, focus rises when there is an unsnapped actor (bear included), the aim is on it, and focusing is allowed (`input !== 'touch'` or the finger is held): `focus = min(1, focus + dt/ft)`. Otherwise it decays at `2.5/s`.

The actor is rendered with `q = lerp(L.q, 1, focus)` only while aimed at; otherwise it stays at the layer's base blur.

Crosshair:
- a ring of radius `lerp(.075GH, .022GH, focus)`, amber `#FFC65C`, turning mint `#2EE6A6` at focus ≥ 1;
- **"LOCK"** (VT323, .045GH) appears below it at lock;
- four white corner brackets (s=.06GH) and a 12px center cross.
- The OS cursor is hidden while playing.

### 6.5 Snapping (`doSnap`)
A snap needs `state==='play'`, cooldown 0 and film > 0. Each snap:
- uses one film; sets cooldown **0.45s**; flashes (`rgba(255,252,235,.7·flash)`, decays 3/s).
- Checks, in order:
  1. **Barry hit** (checked first, even if he is behind the target): score `max(0, score-50)`, pop **"That's Barry. −50"** `#FF8A8A`.
  2. **Unsnapped actor hit**:
     - Bear: −50 (floored at 0), **"That's a bear. −50"**. The bear is not marked snapped and does not flee, so you can be penalized repeatedly.
     - Squatch with focus `s`:
       - `s < .3` → **10 pts, "BLOBSQUATCH"** `#FFB59A`
       - otherwise `pts = round(L.pts·s/10)·10`. The label is **"CLEAR SHOT!"** `#2EE6A6` if `s ≥ .85` (and `clear++`), else **"BLURRY"** `#FFC65C`.
       - The pop reads `${label} +${pts}`. Then `capture()`, `snapped=true`, and `flee()`, which replaces the remaining moves with a fast (1.8×) dash out.
  3. Otherwise **"Missed"** `#E8F0EA`.
- If film reaches 0 and the squatch was not snapped, it flees.
- Pops float up `.08GH` and fade over 1.1s. They use Bagel at .05GH, x clamped to [.18W, .82W].

`capture(a,s,pts,label)` keeps only the round's best shot: it skips if `roundBest.pts >= pts`. It crops a square of side `min(GH, max(1.5h, .3GH))` around the actor (center y `L.y - .55h`), clamped to the canvas. It downsamples to `max(4, round(360·lerp(.05,1,s)))` px and upscales to 360, so focus controls the blur. The capture comes from the canvas after the actors, trees and Barry are drawn but **before** the crosshair and pops, so the photo is clean.

### 6.6 Round flow
- `startPlay(fresh)`:
  - fresh → round 1, score 0; otherwise round++ with the score kept.
  - Resets sight, clear, roundBest, actor, laugh and pops; `gap=.9`s; Barry timer `7–13s`; focus 0; film 3.
  - Centers the aim if unset, sets `state='play'`, hides the overlay and the Polaroid, adds `.playing`.
- Main loop:
  - with an actor: step it; when it is done, call `endSighting`.
  - with a laugh: run it for **1.4s**.
  - otherwise `gap -= dt`. When the gap hits 0: if `sight >= 10` → `roundEnd()`, else `startGameSighting()`.
- `startGameSighting()`: film = **3 per sighting**, focus 0. It is a **bear decoy with 22% chance** if `sight>0` and the previous one was not a decoy.
- `endSighting(a)`: only squatch sightings count (`sight++`); bears don't. If the squatch escaped unsnapped, a **laugh** follows: a happy squatch with arms up peeks from one of the first four MID trees. The canvas text **"HA HA!"** (`#FFB3D3`, rotated -.05) appears above it, animated at 3× speed. Then `gap=.7`s.
- **Barry** cameo: when `barryT` runs out he walks from `fx=-.15` to `1.2` at `.22·GW/s` (about 6.1s). He is drawn huge in the foreground (`.62GH`, feet at 1.1GH, mood `watch`, bob `|sin 7t|·.01GH`). Next appearance after `12–20s`.
- `roundEnd()`: `need = min(3+round, 8)` (R1 4, R2 5, R3 6, R4 7, R5+ 8).
  - Shows the best-shot Polaroid (`#pol`, caption **`Best shot: ${label} +${pts}`**) if any.
  - Removes `.playing`.
  - Saves best: if `score > best` → update `#gBest` and `localStorage.snapSquatchBest`.
  - Cleared (`clear >= need`): `state='round'`, title **`Round ${n} cleared!`**, message **`${clear} clear shots. Score ${score}.`**, button **"Next round"**.
  - Failed: `state='over'`, `logPlay(score)`, title **"Game over"**, message **`You needed ${need} clear shots and got ${clear}. Score ${score}.`**, button **"Play again"**.
- `#gPlay` click: focus the box, then `startPlay(G.state !== 'round')`.
- HUD (`hud()`): `RND n · SEEN s/10 · CLEAR c/need` | `FILM ▮▮▯` (▮ per remaining film, ▯ per used) `· SCORE · BEST`.
- `G.best` loads from localStorage at start (try/catch).

### 6.7 Controls
- **Mouse**: pointermove aims (sets `input='mouse'`); pointerdown snaps (`snapReq`, handled in the next frame).
- **Touch/pen**: pointerdown (`preventDefault`, pointer capture) starts holding, and focus only builds while holding. Moving drags the aim. **Releasing snaps** at the release point. pointercancel stops holding.
- **Keyboard** (only while `#gameBox` has focus, `armed`): arrow keys move the aim at `.6·GW` px/s (and set `input='key'`). Space/Enter snaps while playing. Blur clears the held keys. Clicking the canvas focuses the box (`preventScroll`).
- The game **pauses** (no update or draw) while `#gameBox` is off-screen (IntersectionObserver).

### 6.8 `G` state object (L767)
`state ('ready'|'play'|'round'|'over'), round, sight, clear, score, best, film, cool, flash, focus, aim{x,y}, keys{}, holding, input ('mouse'|'touch'|'key'), actor, gap, barry ({fx}|null), barryT, laugh ({t,a}|null), pops[], snapReq, paused, roundBest ({pts,label,img}|null), lastDecoy`.

---

## 7. NFT, mint, tokenomics, roadmap, FAQ
See §3.4 (NFT copy), §3.6 (Stash), §3.7 (tokenomics/buy), §4.2 and §4.4 (mint constants and flow), and §5.5 (rendering). There is no roadmap or FAQ section. The Stash numbers (`#rRaised`, `#rBurned`, `#rStash`) and the addresses (`#caTop`, `#ca`, `#dev`, `#stashAddr`) are static placeholders with no JS wiring.

---

## 8. Responsive, reduced motion, accessibility

**Breakpoints:**
- ≤820px: `.closer` 1 column (unused); `.nums` 2 columns.
- ≤760px: `.duo` 1 column; `.pols` 2 columns.
- ≤640px: `.nums.three` 1 column.
- ≤560px:
  - logo 23px, "on NEAR" hidden;
  - links gap 10px, no wrap;
  - topbar button 15px, padding 4px 10px, smaller shadow, text "Buy";
  - `.soon` hidden (no such element).
- ≤520px: `.snapBox` bottom 3%, gap 3px; button 14px, padding 3px 12px; small text 10px.
- ≤480px: `.gtext button` 15px.
- ≤420px: `.nums` 1 column.

Fluid `clamp()` sizes are used for h1/h2, banner, stage button, overlays, Polaroids and HUD. The stage and game keep 16:10. At 390px there is **no horizontal overflow** (verified). Canvases re-measure on `resize` (`size()`, `gsize()`) and cap DPR at 1.5. The game art cache rebuilds on resize. The example Polaroids are fixed 300px canvases scaled by CSS.

**Reduced motion** (`reduce`, read once at load):
- CSS: no `.go` bob, no button transitions.
- JS:
  - no Blobsquatch wander (fixed at center), no walk bob or arm swing in the hero;
  - no approach creep, no fern sway;
  - no Barry jump, jitter, frenzy flash or breathing;
  - no pump sway, hop, tilt or strobe (the dance arms still move);
  - frozen Zs;
  - no Polaroid `.develop` animation.
- The camera dolly, the shot flash, and everything in the game are **not** reduced.

**Accessibility:**
- `aria-label` on the hero canvas, NFT canvas, NFT example group, preview chip group (with `aria-pressed` on chips), receipts group, nav and game box.
- The game box is focusable (`tabindex=0`) with a visible amber focus ring and full keyboard play.
- `#claimStatus` has `role="status"`.
- Buttons have a `:focus-visible` amber outline.
- `scroll-margin-top:80px` keeps the sticky header from covering anchors.
- Gaps: canvas content (banner text aside) is not exposed to assistive tech. `#gMsg` and the HUD have no live region. "PUMPING!" is a visual-only div with no role.

---

## 9. Function index
| Line | Function | Purpose |
|---|---|---|
| 304 | `$` | getElementById |
| 306 | `DPRx` | DPR capped at 1.5 |
| 307 | `lerp` | linear interpolation |
| 308 | `clamp` | clamp |
| 309 | `sm` | cosine ease 0..1 |
| 310 | `fmt` | integer with thousands separators |
| 320 | `spr` | draw one ART sprite at its sprite-space box |
| 321 | `sprPart` | draw a sub-rect of a sprite with an offset (splayed foot) |
| 323 | `armAt` | draw an arm sprite rotated about a pivot |
| 325 | `squatch` | draw Blobsquatch (front/back, arms, glance face, tilt, bob) |
| 351 | `rr` | rounded-rect path (falls back to rect) |
| 352 | `camera` | draw Barry's camera |
| 360 | `squatcher` | draw Barry in a mood |
| 421 | `sleeper` | Barry asleep in a camp chair |
| 459 | `pine` | 3-tier pine tree (game backdrop; legacy scenery) |
| 461 | `scenery` | legacy flat forest (unused) |
| 473 | `candles` | translucent green/red candlestick staircase |
| 478 | `soft` | low-res render + upscale = blur |
| 483 | `drawSquatchAt` | Blobsquatch through `soft()` |
| 484 | `bigText` | outlined Bagel canvas text |
| 485 | `burst` | comic starburst (unused) |
| 489 | `size` | resize hero canvas |
| 491 | `bg` | cached legacy scenery (unused) |
| 492 | `stars` | twinkling stars (unused) |
| 493 | `flies` | fireflies (unused) |
| 496 | `overlay` | banner text + Go/Wake visibility |
| 506 | `setMode` | set `S.mode`, reset `S.t` |
| 507 | `freezeFrame` | snapshot the hero canvas |
| 525 | `P3` | 3D → screen projection |
| 526 | `shade` | fog + flash color mix |
| 527 | `drawTrunk` | 3D trunk |
| 532 | `drawFern` | 3D fern |
| 536 | `drawLog` | the mossy log at z 3.2 |
| 540 | `drawBeam` | moonbeam + ground pool |
| 544 | `forestBackdrop` | sky, moon, ground, fog band |
| 550 | `forestCanopy` | leaf canopy (zooms with k) |
| 551 | `drawForest` | full 3D woods with depth sorting; returns the squatch box |
| 571 | `foreFerns` | foreground ferns |
| 576 | `viewfinder` | brackets + head focus square |
| 581 | `sceneSquatching` | hero state machine render/update |
| 630 | `connect` | wallet sign-in (cached) |
| 633 | `randomNFT` | preview NFT traits |
| 649 | `poseOpts` | pose trait → `squatch` options |
| 651 | `renderNFT` | revealed NFT photo (currently unused) |
| 677 | `renderDeveloping` | undeveloped Polaroid |
| 690 | `drawExamples` | fill the 4 example Polaroids |
| 691 | `showNFT` | show the mint Polaroid overlay |
| 701 | `scenePump` | pump scene |
| 710 | `sceneDump` | dump scene |
| 732 | `pull` | DexScreener 1h change |
| 736 | `frame` | hero rAF loop + scene selection |
| 759 | `gsize` | resize game canvas |
| 771 | `hud` | update HUD text |
| 775 | `sideFor` | peek side for a tree |
| 776 | `makeActor` | build a squatch/bear move script |
| 786 | `nextMove` | advance the move script |
| 787 | `flee` | replace the remaining moves with a fast exit |
| 788 | `stepActor` | update peek/dash |
| 795 | `actorH` | actor height (bear .85) |
| 796 | `occluded` | trunk occlusion test |
| 797 | `onActor` | actor hit test |
| 799 | `onBarry` | Barry hit test |
| 802 | `bear` | draw the bear |
| 815 | `buildGameArt` | cache game background and tree layers |
| 833 | `drawActorAt` | draw the actor with focus blur |
| 840 | `pop` | add a floating score text |
| 844 | `capture` | save the best photo crop of the round |
| 854 | `doSnap` | resolve a snap |
| 869 | `startGameSighting` | spawn the next actor |
| 870 | `endSighting` | count the sighting; spawn the laugh |
| 872 | `showPolaroid` | show the best shot on the overlay |
| 873 | `roundEnd` | cleared / game over |
| 879 | `startPlay` | start a round |
| 885 | `showOver` | set overlay title/msg/button |
| 888 | `gframe` | game rAF loop |
| 936 | `setAim` | pointer → aim |
| 956 | `logPlay` | POST score |

Anonymous handlers: the goBtn click (L634), snapBtn click (L635), backWoods (L646), chips (L728), copy buttons (L751), pointer/keyboard (L937-945), gPlay (L946), wConnect (L952). Self-invoking builders: `SCN` (L446), `FOREST` (L512), `grain` (L749).

---

## 10. Known quirks and TODOs
1. **Needs the host `[hidden]{display:none!important}` rule** and a UTF-8 doctype wrapper (§1). Standalone, the overlays all show.
2. Launch placeholders are still empty:
   - `PAIR=''` (no live chart);
   - `REVEAL_DATE=''`;
   - `GAME_LOG_URL=''`;
   - no `window.BLOBSQUATCH_WALLET` (mint runs in preview mode);
   - contract, team and stash addresses read "Posted at launch";
   - Stash receipts are hard-coded 0 with no chain fetch.
3. During live pump or dump the Go Squatching button is hidden, so users **cannot start the hero flow** until the price calms. Once live, the preview chips are hidden too.
4. `renderNFT` (revealed art with traits) is never called. The mint overlay always shows the developing blob. The copy advertises fur, tuft, size and expression traits that no code renders. `ultra` exists only at 3% random in preview.
5. The preview NFT id is random 1–1967 each time (it may collide with #352, the 1/1).
6. Dead code: `SCN`, `PAL`, `HZ`, `scenery`, `bg`/`bgCache`, `stars`, `flies`, `burst`, the `elated` mood, `P.pink/deep/eye`, `--pink-deep`, ART `_meta`. Unused CSS: `.camui`, `.rec`, `.big` (non-polaroid), `.row`, `.bar`, `.controls`, `.tag`, `.gkeys`, `.closer`, `.cam`, `.dict*`, `.preview label/output/input`, `details.preview`, `.soon`, `h1 em`.
7. Game: a bear can be photographed repeatedly for −50 each, since it is never marked snapped. Barry is hit-tested before the target, so snapping a squatch in front of Barry costs 50. Focus also builds on bears. The HUD sits under the overlay scrim.
8. `reduce` is read once; changing the OS setting needs a reload. The game ignores reduced motion.
9. `drawExamples` silently does nothing if the hero canvas had zero width when it ran (e.g. a hidden tab at load). The example Polaroids never redraw on resize (they don't need to; CSS scales them).
10. `S.t` freezes during pump/dump (those scenes don't call `sceneSquatching`).
11. The `mint()` error path shows raw contract messages only when they contain "sold out" or "already".
12. With fonts unavailable the canvas text falls back to sans/monospace. The canvas draws text before `document.fonts.ready` without re-rendering cached game art. The game's art has no text, so only live text is affected, and it redraws each frame.

---

## 11. Screenshots (`../screenshots/`)
All captures use the wrapper from §1 with locally served Google-font equivalents (identical families). Desktop is 1280×900; mobile is 390×844. States were forced where noted.

| File | What |
|---|---|
| `01-desktop-full.jpg` | full page, 1280 wide |
| `02-mobile-full.jpg` | full page, 390 wide |
| `hero-rest.png` | `rest`: far blurry Blobsquatch walking away, Barry squinting, "Go Squatching" |
| `hero-approach.png` | `approach` at S.t=1.3s (mid dolly), Barry in `watch` |
| `hero-ready.png` | `ready`: sharp back view in the clearing, viewfinder, "Snap a pic" + mint note |
| `hero-twig.png` | `twig`: broken twig + "snap!" |
| `hero-glance.png` | `glance`: face turned over his shoulder (gside -1) |
| `hero-photo-developing.png` | `frozen` + `#mintPol` about 1.5s in (develop animation running) |
| `hero-photo-developed.png` | `frozen` + `#mintPol` after the animation; caption "Blobsquatch #NNNN", "(Preview.)" |
| `pump-1.png`, `pump-2.png` | pump scene (chip +5%): two dance moments, "PUMPING!" banner, green candles |
| `dump.png` | dump scene (chip -5%): hiding behind the tree (fingers + foot), Barry asleep, Zs, "Wake Barry up" |
| `hero-mobile-rest.png`, `hero-mobile-ready.png` | hero on mobile (the snapBox note wraps) |
| `pump-mobile.png`, `dump-mobile.png` | chart scenes on mobile |
| `nft-examples.png` | the four "Still developing" example Polaroids |
| `nft-renderNFT-trait-grid.jpg` | 8 renders from the unused `renderNFT` (poses × settings × films, last is `ultra`) |
| `game-start.png` | game intro overlay |
| `game-playing.png` | in play, actor peeking |
| `game-focus-lock.png` | forced MID-layer peek, crosshair locked (mint ring + LOCK), actor sharp |
| `game-snap-pop.png` | "CLEAR SHOT! +100" pop, film ▮▮▯ |
| `game-round-cleared.png` | "Round 1 cleared!" with the best-shot Polaroid |
| `game-over.png` | "Game over" (round 2, forced) |
| `game-barry.png` | Barry walking across the foreground |
| `game-mobile-start.png` | game overlay on mobile |
