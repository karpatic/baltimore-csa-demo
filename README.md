# Baltimore community atlas

Two static choropleths with shared CSA selection:

- Left: estimated poverty rate from 2020–2024 ACS table B17001.
- Right: open Vacant Building Notice record counts from the city, snapshot dated in the app.

## Run

`python3 -m http.server 8000 --bind 127.0.0.1`

Open http://127.0.0.1:8000. No build, backend, or API key. Internet is needed for pinned CDN libraries, fonts, and OpenStreetMap tiles. Bundless 1.0.12 Sucrase handles React 17 JSX.

Select a CSA on either map or from the dropdown to highlight it on both. Separate legends use percentage bins on the left and notice-count bins on the right. Boundaries-only mode demonstrates the first stage. Maps stack on phones.

## Method

Match 199 Census tract GEOIDs to BNIA's 2020 tract-to-CSA crosswalk. Sum B17001 below-poverty population and poverty-status population separately, then calculate the CSA percentage. Never average tract rates. All 199 tracts matched: 109,292 people below poverty out of a poverty-status population of 553,387. Source margins of error remain in data/acs-source.json. These are survey estimates, not significance tests.

Group city notice records by Neighborhood, match BNIA NSA2020, then sum by CSA2020. All 11,368 notices assigned, no unmatched neighborhoods. Explicitly correct BNIA's Greentown/Bayview typo to Greektown/Bayview. This uses BNIA's neighborhood assignment rather than an exact point-in-polygon spatial join.

Both maps use 55 CSA polygons plus the separate jail area. The jail has no poverty denominator and is gray on that map. Zero counts are colored in the first count bin, distinct from missing data.

Different measures and periods: the maps illustrate patterns but do not establish causation. Notice counts are not vacancy rates, and counts reflect community size.

## Refresh and provenance

All runtime data is saved under data/. Census sources and timestamps are in sources.json; notice provenance and reconciliation are in vbn-counts.json.

Optional preparation (Python requests required):

```
python3 prepare-data.py
python3 prepare-vbn.py
```

These scripts are data preparation, not build steps or servers. They fail on truncated or unmatched sources; inspect refreshed output before presenting. Runtime never requires live data APIs.

## GitHub Pages

Push to the intended repository, then Settings → Pages → Deploy from a branch → main → / (root). Relative paths work in a project subdirectory. Not published.
