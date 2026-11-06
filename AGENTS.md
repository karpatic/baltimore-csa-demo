# Baltimore: two maps, two stories

Build a polished static app with two CSA choropleths side by side:
- **Left:** Census poverty rate, 2020–2024 ACS.
- **Right:** city open Vacant Building Notice counts, dated snapshot.

## Demo stages

Complete one stage, demonstrate it, then wait for the presenter to continue.
1. **Map:** show 2020 CSA boundaries, neutral fills, names, and attribution.
2. **City records:** join neighborhood notice counts to CSAs; add a count choropleth.
3. **Census:** roll tract poverty counts up to CSAs; show poverty on the left and notices on the right.
4. **Polish:** shared area selection, separate legends, responsive layout, saved data, GitHub Pages readiness.

If a working app already exists, preserve it and improve only the requested stage.

## Stack

Use Bundless, React 17, Leaflet 1.9.4, and pinned CDNs. No build step or backend.
- Import map: `react` → `https://esm.sh/react@17.0.2/es2022/react.mjs`; `react-dom` → `https://esm.sh/react-dom@17.0.2/es2022/react-dom.mjs`.
- Load `./App.jsx` as `text/jsx`, then `https://unpkg.com/bundlessdev@1.0.12/dist/bundless.sucrase.min.js` as a module. Use `ReactDOM.render`.
- Include Leaflet CSS. Use OpenStreetMap tiles with attribution; no map API key.
- Serve only with `python3 -m http.server 8000 --bind 127.0.0.1`.

## Sources

- CSA shapes: https://services1.arcgis.com/mVFRs7NF4iFitgbY/arcgis/rest/services/Community_Statistical_Areas_2020/FeatureServer/0
- City notices: https://baltegis.baltimorecity.gov/mapping/rest/services/Housing/DHCD_Open_Baltimore_Datasets/FeatureServer/1
- Neighborhood → CSA: https://services1.arcgis.com/mVFRs7NF4iFitgbY/arcgis/rest/services/NSA2020_to_CSA2010_and_CSA2020_Crosswalk/FeatureServer/0
- Tract → CSA: https://services1.arcgis.com/mVFRs7NF4iFitgbY/arcgis/rest/services/Tract2020_to_CSA2020/FeatureServer/0
- ACS poverty counts: https://api.censusreporter.org/1.0/data/show/acs2024_5yr?table_ids=B17001&geo_ids=140%7C05000US24510

Download ACS with a project-specific User-Agent, such as `BaltimoreCSAWorkshop/1.0 (educational demo)`. Use saved snapshots in the browser, not API keys.
ArcGIS: append `/query`; use `where=1=1`, `outFields=*`, `f=json`. Shapes use `f=geojson&outSR=4326`. Retrieve all pages.

## Two joins

**Notices:** group city records by `Neighborhood`, count `OBJECTID`, match crosswalk `NSA2020`, then sum by `CSA2020`. Trim/case-normalize names; explicitly correct `Greentown/Bayview` to `Greektown/Bayview`. This is BNIA's neighborhood assignment, not an exact point-in-polygon join.

**Poverty:** strip `14000US` from Census Reporter geography keys; match the remaining 11-digit string to `GEOID_Tract_2020`. Group by `Community_Statistical_Area_2020`; match polygon `CSA2020`.
- `B17001001`: population with poverty status determined.
- `B17001002`: people below poverty.
- **CSA rate = 100 × summed below-poverty population / summed poverty-status population.** Never average tract percentages.

## Finish clearly

- Keep 55 CSAs and the separate `Unassigned -- Jail` area. Distinguish zero, missing data, and zero denominators.
- Check duplicate/unmatched joins and reconcile totals. Preparation matched 199 tracts and 11,368 notices; refreshed counts may change.
- Label units, periods, and numeric legend breaks. Poverty is an estimate; notices are counts. Different periods and community sizes matter. Do not imply causation.
- Save public data and source URLs/dates in `data/`. Retain Census margins of error; avoid significance claims.
- Test selection, both maps, mobile layout, and subdirectory hosting in a browser.
- Use root `index.html` and relative paths. Commit each working stage. Prepare Pages from `main` at `/`; publish only when asked.
