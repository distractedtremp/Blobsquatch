# Blobsquatch ($BLOBSQUATCH) — project guide for Claude Code

Read this first, then the file in `docs/` that matches the task. This folder is the handoff from a long Cowork (claude.ai) design session. Everything decided there is written down here; nothing else carries over.

## What this is

A memecoin on the NEAR blockchain, **$BLOBSQUATCH**, with:

- a one-page website with an interactive canvas hero scene;
- a chart-reactive pump and dump scene;
- an arcade game, "Snap the Squatch";
- a 1,967-piece NFT collection.

A **blobsquatch** is real Bigfoot-hunter slang for a blurry photo that's supposedly Bigfoot. The project's joke grew from that.

## Current status (read carefully)

- **The website is `index.html` at the repo root** (static, no build step; sprites in `img/sq/`). It has been reskinned from the old pink Bigfoot to the costume guy, animated pose to pose "on twos" with line boil (see `tools/boil.py`). `site/versions/` keeps v14 and v15 for reference.
- **The concept:** Blobsquatch is now a regular guy in a cheap brown Bigfoot costume, faking Bigfoot sightings with his buddy Barry. The character art is locked in `art/locked/`, in a crude "MS Paint degen meme" style.
- **Next job:** rebuild the site around the new concept. Follow `docs/REDESIGN_PLAN.md`, and keep everything else about the current site the same unless the plan says otherwise.

## File map

| Path | What |
|---|---|
| `docs/STYLE_RULES.md` | **Hard art style rules (read before any art work).** Flat color, thick uneven outlines, no detail, rubbery proportions. |
| `docs/PROJECT_BRIEF.md` | The coin, NFTs, launch, story and copy lines. The "why" behind everything. |
| `docs/CHARACTER_BIBLE.md` | The locked character: rules, palette, style, the locked images and their Canva links, plus what's still needed. |
| `docs/CURRENT_SITE_SPEC.md` | An exact spec of the current site: every section with copy verbatim, state machine, every scene, the game, a function index with line numbers, and quirks. |
| `docs/PUMP_DANCE.md` | The exact current pump dance, and the new bouncing-mask dance design. |
| `docs/REDESIGN_PLAN.md` | A scene-by-scene plan for the new-concept site. |
| `docs/ART_PIPELINE.md` | How the art is made: AI image prompts that worked, rules that prevent drift, and how sprites are cut and embedded. |
| `docs/HISTORY.md` | How the concept evolved and what was rejected and why. Read it before suggesting a "new" idea. |
| `docs/OPEN_QUESTIONS_AND_RISKS.md` | Undecided items and legal/IP flags. |
| `site/blobsquatch.html` | The live site file (v15), exactly as published. It has no doctype; see the spec. |
| `site/blobsquatch-standalone.html` | The same site wrapped so it opens directly in a browser. |
| `site/versions/blobsquatch-v14.html` | The previous version, with a code-drawn blank-faced blob. Its pump dance is the one the owner found funniest. |
| `screenshots/` | 26 screenshots of the current site in every state (hero, pump, dump, game, NFTs). |
| `art/locked/` | The locked new-concept character images. |
| `art/history/` | Rejected or superseded art, kept for reference only. It includes the realistic costume version that proved the concept, the gorilla-mask and too-big-shoulders versions, and the old pink master. |
| `tools/` | Playwright screenshot/recording scripts and the Python sprite-cutting scripts used to build v15. Their paths are hard-coded from the old workspace, so update them before running. |
| `PUMP IT ...mp4`, `Pump it up ...mp4` | The owner's reference videos for the "Pump It" trend dance, the vibe for the pump scene. |
| Loose `.jpg`/`.png` in the root | The owner's own downloads of the locked art. Don't move or delete them. |

## How to work with the owner (Guy)

- **Keep replies short and to the point.** He doesn't read long responses.
- **For bigger changes, propose a plan first and wait for his OK.**
- **Be honest.** Flag weak ideas and push back constructively. Don't just agree.
- **Research before building.** For example, check whether a name or token already exists.
- **Think answers through** so the logic is consistent. Don't answer fast and contradict yourself later.
- **He wants to focus on the creative work.** Create and organize files yourself; don't ask him to move things.
- **You are not a lawyer.** Flag legal, IP, securities and tax questions as such.
- **He can't see what you see.** When you judge animation, render frames or video and say plainly what you can and can't verify.
- **Never delete anything outside this project.**

## Hard rules for the art and the site

1. **The core meme:** from far away he's a convincing, blurry Bigfoot; up close it's obviously a guy in a costume. Every element must serve that and read instantly. If it doesn't, cut it.
2. **Style:** crude MS Paint degen meme with thick wobbly black outlines and flat fills. No realistic rendering, no cheesy crypto props (no Pepe, apes, laser eyes, Monster cans or coins), no other people's IP.
3. **NEAR green `#00EC97` appears only on the zipper pull,** the one bright color on him. Never use the NEAR "N" logo.
4. **The mask is a Bigfoot head, not a gorilla:** a tall cone top, shaggy fur framing a small flat face, a small flat nose.
5. **When generating AI images, never edit an edit.** Each edit degrades the image (dark colors, halos, soft lines). Generate fresh from a locked reference, and change one thing per prompt.
6. **Barry is the photographer and is in on the hoax.** Barry is NOT Blobsquatch's name. Blobsquatch has no personal name.
