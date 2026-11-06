# Baltimore housing atlas

Finished Codex workshop example: ACS tract counts joined to BNIA's 2020 CSAs and displayed as a vacancy-rate choropleth.

## Run

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open http://127.0.0.1:8000. No build, package installation, API key, or backend is required. Internet access is needed for pinned CDN libraries, fonts, and OpenStreetMap tiles.

The Boundaries button shows the first demo stage; Vacancy shows the completed rollup. Select an area on the map or in the dropdown.

## Data and calculation

2020–2024 ACS five-year estimates, table B25002, downloaded through Census Reporter. All 199 Baltimore city tracts match BNIA's 2020 tract-to-CSA crosswalk. Sum vacant and total housing units separately, then calculate `100 * vacant / total`. Do not average tract percentages.

55 named CSAs contain 295,032 estimated housing units and 39,364 estimated vacant units (13.3%). The 56th polygon, Unassigned -- Jail, has zero housing units and is gray, with no calculated rate. These are survey estimates, not current city Vacant Building Notices or significance tests. Source margins of error remain in data/acs-source.json.

All source URLs and retrieval timestamps are in data/sources.json. Raw counts, crosswalk, boundaries, rollup, and a validation receipt are saved in data/.

Optional data refresh: `python3 prepare-data.py` (requires Python requests). This preparation script is not a server or build step. Review refreshed data before presenting.

## GitHub Pages

Push this repository to the intended GitHub repository, then Settings → Pages → Deploy from a branch → main → / (root). Relative paths support a project subdirectory. This copy has not been published.

## Browser verification

Verified with the static server under /Codex/: 56 map shapes, five vacancy color bins plus the no-rate bin, loaded map tiles, boundary/vacancy switching, and Canton selection (489 / 4,454 = 11.0%). Data preparation reconciles all tract and CSA totals. Bundless 1.0.12's Sucrase runtime is used because the published Acorn runtime failed with this JSX.
