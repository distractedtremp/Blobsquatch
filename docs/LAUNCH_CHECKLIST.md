# Launch checklist

Plan: launch the coin and site first. NFTs, airdrop and "Get in the Suit" come after launch, only if the coin gets traction. Timeline below assumes about two weeks of X warm-up before launch day; launching with no audience is the most common way meme coins die.

## Only Guy can do these (in this order)

- [ ] **Accounts.** Make the X account and Telegram group (copy in `LAUNCH_KIT.md`). Turn on 2FA on both.
- [ ] **Domain.** Buy it on Hostinger. Then in Hostinger DNS add: `A` records for `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`, and a `CNAME` for `www` → `distractedtremp.github.io`.
- [ ] **GitHub Pages.** In the repo: Settings → Pages → Source: "GitHub Actions". Then add the domain under "Custom domain" and tick "Enforce HTTPS". Tell Claude the domain so it can add the CNAME file and wire the links.
- [ ] **Wallet.** Make a fresh NEAR wallet for the project (Meteor or HOT). Fund it with enough NEAR for the launch fee plus your own first buy. Write the seed phrase down on paper; never paste it into any chat, including this one.
- [ ] **Venue.** Pick JustHoot or Meme.Cooking (see the audit doc). Open the create-token page once before launch day to see the fee and the fields.
- [ ] **Warm-up.** Post one warm-up post a day from `LAUNCH_KIT.md` for two weeks. Reply to every NEAR account that interacts. Follow and reply to 20 NEAR meme accounts a day.
- [ ] **Launch crew.** Line up at least 20 people who will buy in the first 10 minutes and post about it. DM them the time the day before.
- [ ] **Date.** Pick a weekday, 2 to 4 pm US Eastern, when the NEAR Twitter crowd is awake. Avoid big crypto news days.

## Claude does these

- [x] Site reskinned and in the repo, deploy workflow ready.
- [x] Logos, X banner, token metadata, bios, posts, Telegram copy.
- [ ] Add the CNAME file and real links when Guy sends the domain and handles.
- [ ] Virgin-vs-Chad meme and sticker crops.
- [ ] Short clips of the hero snap and pump dance for X (from `tools/`).
- [ ] After launch: paste the contract address, team wallet and DexScreener pair into the site so the chart drives the pump and dump scenes.
- [ ] After launch: add the buy link to every "Buy $BLOBSQUATCH" button.

## Launch day, step by step

1. Two hours before: post "Barry is loading film." Make sure the site is live and the pinned post is ready.
2. Open the launchpad create page. Paste from `LAUNCH_KIT.md`: name, ticker, description, logo (`brand/logo-masked-512.png`), website, X, Telegram.
3. On Meme.Cooking: set the auction length (1 to 4 hours is a reasonable event), the soft cap, and the team allocation (5%, with a cliff and vesting). On JustHoot: launch, then buy your own first position immediately.
4. Copy the contract address. Send it to Claude and post it on X and Telegram (contract alone in a reply so people can copy it).
5. Ping the launch crew.
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
