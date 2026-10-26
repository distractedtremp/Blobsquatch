# Launch checklist

Plan: launch the coin and site first. NFTs, airdrop and "Get in the Suit" come after launch, only if the coin gets traction.

**Stealth launch (the owner's choice).** No countdown, no pre-launch hype. The coin appears on JustHoot and the X account starts posting the same hour. The warm-up posts in `LAUNCH_KIT.md` become the first two weeks of post-launch posts. Stealth works on a bonding curve (JustHoot) because the curve can sit and get discovered; it does not work on Meme.Cooking, whose auction needs a crowd on a set day. The risk is a silent launch that nobody finds, so the account and Telegram must be live and the posting starts the day of launch, not later.

## Only Guy can do these (in this order)

- [ ] **Accounts.** Make the X account and Telegram group (copy in `LAUNCH_KIT.md`). Turn on 2FA on both.
- [ ] **Domain: blobsquatch.com** (bought on Hostinger). In Hostinger DNS add: `A` records for `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`, and a `CNAME` for `www` → `distractedtremp.github.io`.
- [ ] **GitHub Pages.** The repo is private, and Pages on a free account needs a public repo, so first: repo Settings → General → scroll to "Danger Zone" → Change visibility → Public (the site is public anyway, and nothing secret is in the repo). While there, set the default branch to `main`. Pages creates a `github-pages` environment that only lets the default branch deploy, so if the deploy workflow fails in 3 seconds with no steps, go to Settings → Environments → github-pages → Deployment branches and add `main`. Then Settings → Pages (the repo's own settings, at github.com/distractedtremp/Blobsquatch/settings/pages, not the account-level Pages page) → Source: "GitHub Actions". Then type `blobsquatch.com` under "Custom domain", wait for the DNS check, and tick "Enforce HTTPS". The repo already has the CNAME file.
- [ ] **Wallet.** Make a fresh NEAR wallet for the project (Meteor or HOT). Fund it with enough NEAR for the launch fee plus your own first buy. Write the seed phrase down on paper; never paste it into any chat, including this one.
- [ ] **Venue.** Pick JustHoot or Meme.Cooking (see the audit doc). Open the create-token page once before launch day to see the fee and the fields.
- [ ] **Accounts live before the launch.** X and Telegram exist with the bio, banner and pinned post, even if they have no followers yet.
- [ ] **Date.** Target November 10 to 12, 2026 (a weekday, 2 to 4 pm US Eastern), so the coin has a week of life before GTA 6 lands on November 19 and the sighting-petition bit peaks. See `BRAND_STORY.md`.
- [ ] **The first two weeks after launch.** One post a day from the kit. Reply under every big NEAR account's posts with a blurry photo. Follow and reply to 20 NEAR meme accounts a day. This replaces the warm-up.
- [ ] **Ads.** Skip paid ads at first; replies and memes outperform them for meme coins. If anything, pay a NEAR meme account for one post after the chart has a few days of life.

## Claude does these

- [x] Site reskinned and in the repo, deploy workflow ready.
- [x] Logos, X banner, token metadata, bios, posts, Telegram copy.
- [x] CNAME file, blobsquatch.com, @BlobsquatchNEAR and t.me/blobsquatch wired into the site and kit.
- [ ] Virgin-vs-Chad meme and sticker crops.
- [ ] Short clips of the hero snap and pump dance for X (from `tools/`).
- [ ] NEAR-first copy and the sighting log on the site (draft in `BRAND_STORY.md`, needs Guy's OK).
- [ ] After launch: paste the contract address, team wallet and DexScreener pair into the site so the chart drives the pump and dump scenes.
- [ ] After launch: add the buy link to every "Buy $BLOBSQUATCH" button.

## Launch day, step by step

1. Two hours before: post "Barry is loading film." Make sure the site is live and the pinned post is ready.
2. Open the launchpad create page. Paste from `LAUNCH_KIT.md`: name, ticker, description, logo (`brand/logo-masked-512.png`), website, X, Telegram.
3. On JustHoot: launch, then buy your own first position immediately, before posting the address anywhere. (Meme.Cooking alternative if the plan changes: set the auction length, soft cap and a 5% vested team allocation.)
4. Copy the contract address. Send it to Claude and post it on X and Telegram (contract alone in a reply so people can copy it).
5. Post the first three kit posts over the first hour.
6. Reply to everything for three hours. Quote every meme.
7. Once the pair exists on RHEA or Ref, send Claude the DexScreener link. The site goes live with the chart.
8. Post the "first 100 squatchers" update when it happens.

## After launch (first week)

- Apply for the DexScreener profile update (logo, socials) and CoinGecko / CoinMarketCap listings.
- Ask NEAR ecosystem accounts and NEAR Catalog to list the project.
- Decide the airdrop size from the team allocation and the snapshot date.
- If volume holds for a week, start the NFT collection and "Get in the Suit".

## Not legal advice

Keep the airdrop copy as "nothing is promised." Don't promise returns or a use of proceeds. Get a tax and entity answer from an accountant before revenue comes in.
