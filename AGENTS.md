# Baltimore Census Map Demo

Build an attractive, entirely static pair of side-by-side choropleths of poverty rate and open vacant-building notice counts by Baltimore Community Statistical Area (CSA).
Use 2020–2024 ACS poverty estimates on the left and a dated city open-VBN count snapshot on the right. Keep measures, periods, and legends distinct.

## Work in stages
1. Load the 2020 CSA polygons on a Leaflet map. Neutral fills, names, attribution, fit Baltimore.
2. Fetch ACS B17001 tract poverty counts and BNIA's 2020 tract-to-CSA crosswalk. Join and shade CSAs by poverty percentage, then add a second notice-count choropleth using the neighborhood crosswalk. Include legend, selection details, and clear missing-data states.
3. Save public data snapshots with source URLs and dates. Finish a polished responsive app that works on GitHub Pages.

Start Stage 1 only, show it, and wait for the presenter to request the next stage.

## Stack
Use Bundless for React 17/JSX, Leaflet 1.9.4, and pinned CDN dependencies.
Follow https://bundless.dev/usage.html. Use ReactDOM.render and a ref/effect for Leaflet.
Import map: react -> https://esm.sh/react@17.0.2/es2022/react.mjs and react-dom -> https://esm.sh/react-dom@17.0.2/es2022/react-dom.mjs.
Load App.jsx using a text/jsx script and https://unpkg.com/bundlessdev@1.0.12/dist/bundless.sucrase.min.js as a module.
No bundler, build step, backend, proxy, or API keys in the app.
Run only `python3 -m http.server 8000 --bind 127.0.0.1`.

## Data
- Census table: https://data.census.gov/table/ACSDT5Y2024.B17001?g=050XX00US24510$1400000
- Key-free Census Reporter mirror: https://api.censusreporter.org/1.0/data/show/acs2024_5yr?table_ids=B17001&geo_ids=140%7C05000US24510
- Crosswalk: https://services1.arcgis.com/mVFRs7NF4iFitgbY/arcgis/rest/services/Tract2020_to_CSA2020/FeatureServer/0
- Polygons: https://services1.arcgis.com/mVFRs7NF4iFitgbY/arcgis/rest/services/Community_Statistical_Areas_2020/FeatureServer/0

Download the mirror during preparation using a project-specific User-Agent, for example `BaltimoreCSAHousingWorkshop/1.0 (educational static map demo)`. Save the public response; the browser should use local snapshots. Official Census API currently requires a key.
ArcGIS: append /query, where=1=1, outFields=*, f=json; polygons use f=geojson and outSR=4326. Fetch all pages if limited.

## Join correctly
Census Reporter geography keys are `14000US` plus the 11-digit tract GEOID. Match that GEOID to crosswalk `GEOID_Tract_2020`. Keep IDs as strings.
Group by `Community_Statistical_Area_2020`; match polygon `CSA2020`.
B17001 fields: B17001001 population for whom poverty status is determined; B17001002 people below poverty (mirror spelling).
Sum counts first. CSA poverty percent = 100 * sum(below poverty) / sum(poverty-status population). Never average tract percentages.
These sources have 199 matching tracts and 56 areas: 55 named CSAs plus `Unassigned -- Jail`. Keep jail separate from ordinary CSA summaries. Preserve null/negative sentinel values as missing, not zero. Zero denominator means no rate. Match city Neighborhood to crosswalk NSA2020, then group by CSA2020. Normalize whitespace/case; explicitly correct Greentown/Bayview to Greektown/Bayview. This is a neighborhood assignment, not an exact spatial point join. Reconcile assigned plus unmatched notices to the source count. Show zero separately from missing.
Show period, source, and that these are survey estimates with uncertainty. Poverty and notice counts have different units and dates. Do not imply causation or compare color intensity as a shared numerical scale. Counts reflect area size too. Link selection across both maps; provide separate numeric legends; stack maps on phones. Do not average medians or invent precision; retain source margins of error and avoid significance claims.

## Finish
Reconcile tract and CSA totals, report unmatched/duplicate IDs, verify polygon names and zero/missing states. Test in a browser at root and a project subdirectory.
Use relative asset paths and root index.html. Keep data in data/ with provenance. No SPA rewrites.
Commit each working stage. Prepare GitHub Pages from main at /; publish only when asked.

## City notice-count sources
- Open VBNs: https://baltegis.baltimorecity.gov/mapping/rest/services/Housing/DHCD_Open_Baltimore_Datasets/FeatureServer/1
- Neighborhood crosswalk: https://services1.arcgis.com/mVFRs7NF4iFitgbY/arcgis/rest/services/NSA2020_to_CSA2010_and_CSA2020_Crosswalk/FeatureServer/0
For quick counts query groupByFieldsForStatistics=Neighborhood, outFields=Neighborhood, returnGeometry=false and outStatistics=[{"statisticType":"count","onStatisticField":"OBJECTID","outStatisticFieldName":"notice_count"}]. Fetch all pages if limited. Check returnCountOnly=true separately and preserve source counts and unmatched rows. Save dated snapshots; no runtime API dependency.
