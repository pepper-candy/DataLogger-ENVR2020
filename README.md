# ENVR 2020 Field Data Logger

Mobile-first, dark-mode logger for field measurements. **All records stay on this device** (browser `localStorage`). There are no accounts, no analytics, and no upload.

Usability on a phone in the dark, often offline on a mountain, is the priority.

## Two ways to use it

### A. GitHub Pages (recommended for GPS)

Live app: **https://pepper-candy.github.io/DataLogger-ENVR2020/**

If that URL 404s, a repo admin should open **Settings → Pages** and set Source to **GitHub Actions** (workflow: `.github/workflows/pages.yml`). After the first successful run on `main`, the URL above serves the app.

1. Open that URL **once** while you still have signal (it is HTTPS).
2. Optional: browser menu → **Add to Home Screen**.
3. After that first visit, you can reopen it (or the home-screen icon) **offline** on the mountain.

GPS and clipboard work more reliably here than in a downloaded file.

### B. Single-file HTML (no install)

Download **[ENVR2020_field_log.html](./ENVR2020_field_log.html)** from this repository and open it in the phone browser. It is self-contained (no CDN, no extra files).

Android Chrome often **blocks geolocation on `file://`**. If the locate button does nothing, type coordinates by hand, or use the Pages URL (opened once with signal) instead.

Direct download (after this repo is on `main`):  
https://github.com/pepper-candy/DataLogger-ENVR2020/raw/main/ENVR2020_field_log.html

## On the phone

- **Location** — tap the compact switch in the title bar to cycle High 山頂 → Mid 山腰 → Urban 路邊. Each site has its own colour. Last choice is remembered.
- Fill **any** of: 5 lux, 5 wind degrees, temp, humidity, latitude, longitude, elevation, Laser / Photo. You do not need every field.
- **Record Now** is enabled when any measurement or checkbox has a value. Location alone (and empty lat/long) is not enough.
- Record Now logs **device local time with UTC offset**, then keeps location + GPS/elevation (same site) and clears the round fields.
- **Copy** (clipboard icon) copies the *current* form as short plain text for WhatsApp etc. Copy does not save a record by itself.
- **Locate** (pin to the right of lat / long / m) asks the phone for a high-accuracy fix and fills empty coordinate/elevation boxes only — it never overwrites values you already typed.
- **Download** (top right) exports **all cached records** as `ENVR2020_field_log.csv`.

## CSV → ArcGIS Pro

The file is UTF-8 **with BOM**. Coordinates are WGS84 decimal degrees in columns named `Latitude` and `Longitude`. Also included: `Elevation_m`, `Time` (ISO 8601 with offset), `Location`, `Lux1`…`Lux5`, `Lux_mean` (filled when at least one lux value exists), `Wind_deg1`…`Wind_deg5`, `Wind_mean` (filled when at least one wind value exists), `Temp_C`, `Humidity_pct`, `Laser`, `Photo` (yes/no).

## GPS altitude

Phone GPS altitude is **approximate ellipsoid height**, not orthometric / map elevation. If you have a Garmin or other measured elevation, treat that as official and type it in the `m` box.

## Hidden clear

There is no visible delete button (so it cannot be tapped by accident in the dark). To wipe cached records on this browser:

1. Press **Record Now** **10 times in a row** (successful saves).
2. Then **press and hold Record Now for 2 seconds**.

A brief confirmation appears. A single accidental long-press does **not** clear anything.

## Privacy

Records never leave the phone unless you copy text or download the CSV yourself.
