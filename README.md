# Coleman's Aerial Solutions (CAS) website

A single-page site with a drone fly-in intro, gallery, packages, a live
Australia-wide fly zones map, and a booking form. No build step: Cloudflare
Pages serves the files as they are.

## What's in here

| File / folder | What it is |
|---|---|
| `index.html` | The whole site |
| `site-config.js` | Your email, phone, Instagram, form and map keys. **Edit this.** |
| `works.json` | The list of photos and videos in the gallery |
| `images/` | Your photos and videos (see `images/README.txt`) |
| `data/airspace.js` | No-fly zone data from openAIP |
| `scripts/refresh-airspace.py` | Re-downloads the zone data every few months |

## Put it online (same setup as FinchSnaps)

1. **GitHub:** create a new repository, e.g. `CheekyDoe/CAS`.
   Click **uploading an existing file** and drag in everything from this
   folder (keep the folder structure). Commit.
2. **Cloudflare:** Workers & Pages → Create → Pages → **Connect to Git** →
   pick the `CAS` repo.
   - Framework preset: **None**
   - Build command: *(leave empty)*
   - Build output directory: `/`
   Save and deploy. You get a link like `cas.pages.dev`.
3. **Domain (optional):** buy one (e.g. `colemansaerial.com.au`), then in the
   Pages project → **Custom domains** → add it and follow the DNS steps.

Every time you push a change to GitHub, Cloudflare updates the site in about a minute.

## Set up the extras

- **Booking form → your inbox:** make a free form at formspree.io, copy its ID
  (the part after `/f/`), paste it into `formspree` in `site-config.js`.
  Without it, the form falls back to "copy this message".
- **Satellite view on the map:** free account at maptiler.com → API keys →
  paste into `maptilerKey`. In MapTiler, restrict the key to your domain.
- **Your own drone in the animations:** add a transparent PNG of your drone
  (facing right) to `images/` and set `droneImage: "images/drone.png"`.

## Add photos and videos

1. Drop files into `images/`.
2. Add an entry for each one in `works.json` (examples in `images/README.txt`).
3. Push to GitHub.

Set `"hero": true` on one photo to use it as the big background at the top.

## Keep the no-fly zones fresh

Every few months (or after big airspace changes):

```
pip install shapely
OPENAIP_KEY=your_openaip_key python3 scripts/refresh-airspace.py
```

Then push `data/airspace.js`. Make a new openAIP key for this, and don't
commit the key itself.

## Map and data credits (keep these)

- Street map: OpenFreeMap / OpenMapTiles / © OpenStreetMap contributors (added automatically)
- Airspace: openAIP, CC BY-NC 4.0
- The map is a guide only, not for navigation. Check a CASA-verified app
  (e.g. OpenSky) before every flight.
