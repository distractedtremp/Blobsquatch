# Launch checklist

Plan: launch the coin and site first. NFTs, airdrop and "Get in the Suit" come after launch, only if the coin gets traction.

**Stealth launch (the owner's choice).** No countdown, no pre-launch hype. The coin appears on JustHoot and the X account starts posting the same hour. The warm-up posts in `LAUNCH_KIT.md` become the first two weeks of post-launch posts. Stealth works on JustHoot because the pool can sit and get discovered (there is no bonding curve; see launch day, step 3); it does not work on Meme.Cooking, whose auction needs a crowd on a set day. The risk is a silent launch that nobody finds, so the account and Telegram must be live and the posting starts the day of launch, not later.

## Only Guy can do these (in this order)

- [x] **Download the art keepers.** Done 2026-10-26 (Remote Control session); they are in `art/candidates/clean-meme/`.
- [ ] **Go or no on the new art.** Look at the preview PR and the clips in the shared folder under `launch/v2/`. On "go" Claude merges and the site, logo and kit switch to the new set; the X profile picture is then the new `brand/logo-masked-512.png`.
- [x] **X account.** @BlobsquatchNEAR exists (2026-10-26). Turn on 2FA. Leave the profile picture alone until the face is final; Claude will say when.
- [ ] **Telegram group.** t.me/blobsquatch, copy in `LAUNCH_KIT.md`. Turn on 2FA.
- [x] **Domain: blobsquatch.com** (Hostinger). DNS set 2026-10-26, live over HTTPS.
- [x] **GitHub Pages.** Public repo, Pages on GitHub Actions, blobsquatch.com with HTTPS.
- [ ] **Default branch.** Settings → General → set the default branch to `main`. Then Settings → Environments → github-pages → Deployment branches → add `main`. Until then merges do not auto-deploy and Claude redeploys by hand after each one.
- [ ] **Wallet.** Make a fresh NEAR wallet for the project (Meteor, HOT or Intear). Fund it with enough NEAR for the launch fee plus your own first buy, and keep at least 0.1 NEAR spare for gas and storage (first-time token storage costs about 0.00125 NEAR). Write the 12-word seed phrase down on paper; never paste it into any chat, including this one.
- [x] **Venue: JustHoot** (decided 2026-10-26; Meme.Cooking stays the fallback).
- [ ] **Dry run.** Open JustHoot's create-token page once before launch day to see the fee and the fields. Do not submit. Note whether it says the pool's LP is locked or burned; nobody's public guide says, so the site and kit now say "whole supply in the pool" instead of "liquidity locked". If the page confirms a lock, tell Claude and the word goes back in.
- [ ] **Accounts live before the launch.** X and Telegram carry the bio, banner and pinned post, even with no followers yet.
- [ ] **Profile picture.** After the "go", upload `brand/logo-masked-512.png` (new face) to X. Only then; X limits changes.
- [ ] **Date.** Target November 10 to 12, 2026 (a weekday, 2 to 4 pm US Eastern), so the coin has a week of life before GTA 6 lands on November 19 and the sighting-petition bit peaks. See `BRAND_STORY.md`.
- [ ] **The first two weeks after launch.** One post a day from the kit. Reply under every big NEAR account's posts with a blurry photo. Follow and reply to 20 NEAR meme accounts a day. This replaces the warm-up.
- [ ] **Ads.** Skip paid ads at first; replies and memes outperform them for meme coins. If anything, pay a NEAR meme account for one post after the chart has a few days of life.

## Claude does these

- [x] Site reskinned and in the repo, deploy workflow ready.
- [x] Logos, X banner, token metadata, bios, posts, Telegram copy.
- [x] CNAME file, blobsquatch.com, @BlobsquatchNEAR and t.me/blobsquatch wired into the site and kit.
- [x] Logo, stickers, banner and meme templates redone in the clean-meme style (`tools/brand.py`, waiting in the preview PR).
- [ ] Virgin-vs-Chad meme.
- [x] Short clips of the hero snap and pump dance for X (re-recorded with the new art; shared folder `launch/v2/`).
- [x] NEAR-first copy and the sighting log on the site (live 2026-10-26; the tally is the `SIGHTINGS` constant in `index.html`, update it by hand from the #BlobsquatchForGTA6 count).
- [ ] After launch: paste the contract address, team wallet and DexScreener pair into the site so the chart drives the pump and dump scenes.
- [ ] After launch: add the buy link to every "Buy $BLOBSQUATCH" button.

## Launch day, step by step

1. Two hours before: post "Barry is loading film." Make sure the site is live and the pinned post is ready.
2. Open the launchpad create page. Paste from `LAUNCH_KIT.md`: name, ticker, description, logo (`brand/logo-masked-512.png`), website, X, Telegram.
3. On JustHoot: launch, then buy your own first position immediately, before posting the address anywhere. How JustHoot works (checked 2026-10-26 on neartrade.lol's guide; confirm the fee on the create page): there is no bonding curve. The whole launch supply goes into a pool as one-sided liquidity, so the token trades from its first block on RHEA. Trackers move it to "Final Stretch" once about a quarter of the launch supply is bought (price about 1.8x launch), then to "Trading" on volume. So the first buys set the chart; a stealth launch needs your own first buy plus the first posts in the same hour. (Meme.Cooking alternative if the plan changes: set the auction length, soft cap and a 5% vested team allocation.)
4. Copy the contract address. Send it to Claude and post it on X and Telegram (contract alone in a reply so people can copy it).
5. Post the first three kit posts over the first hour.
6. Reply to everything for three hours. Quote every meme.
7. Once the pair exists on RHEA or Ref, send Claude the DexScreener link. The site goes live with the chart.
8. Post the "first 100 squatchers" update when it happens.

## After launch (first week)

- Apply for the DexScreener profile update (logo, socials) and CoinGecko / CoinMarketCap listings.
- Ask NEAR ecosystem accounts and NEAR Catalog to list the project.
- Decide the airdrop size (from what the team bought at launch; JustHoot mints no team allocation) and the snapshot date.
- If volume holds for a week, start the NFT collection and "Get in the Suit".

## Not legal advice

Keep the airdrop copy as "nothing is promised." Don't promise returns or a use of proceeds. Get a tax and entity answer from an accountant before revenue comes in.
