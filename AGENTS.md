# Baltimore VBN Map Demo

## Goal

Build a small, attractive web app showing **open vacant building notices by
Baltimore Community Statistical Area (CSA)**. Use BNIA's neighborhood-to-CSA
crosswalk to join the counts to the map. Counts are notices, not vacancy rates.

Work one stage at a time. Start with Stage 1 only. Show the working result and
let the presenter request the next stage. Keep each stage easy to explain.

## Stack: Bundless and static files

Use **Bundless** for the React/JSX UI and **Leaflet 1.9.4** for the map. Load
libraries from version-pinned CDNs where possible, including Leaflet's CSS.
Follow the browser bootstrap in https://bundless.dev/usage.html:

```html
<script type="importmap">
{"imports": {
  "react": "https://esm.sh/react@17.0.2/es2022/react.mjs",
  "react-dom": "https://esm.sh/react-dom@17.0.2/es2022/react-dom.mjs"
}}
</script>
<div id="react-root"></div>
<script src="./App.jsx" type="text/jsx"></script>
<script src="https://unpkg.com/bundlessdev@1.0.12/dist/bundless.acorn.min.js" type="module"></script>
```

Use `ReactDOM.render` with this React 17 setup. A small React component can own
a Leaflet map through a ref and effect; React-Leaflet is not required.

No Vite, bundler, build step, backend, API proxy, or server-side rendering.
The development server is only:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

## Data: three sources

These are ArcGIS layers/tables. Append `/query` to retrieve records.

- **CSA polygons (2020):** https://services1.arcgis.com/mVFRs7NF4iFitgbY/arcgis/rest/services/Community_Statistical_Areas_2020/FeatureServer/0
- **Open VBNs:** https://baltegis.baltimorecity.gov/mapping/rest/services/Housing/DHCD_Open_Baltimore_Datasets/FeatureServer/1
- **Neighborhood crosswalk:** https://services1.arcgis.com/mVFRs7NF4iFitgbY/arcgis/rest/services/NSA2020_to_CSA2010_and_CSA2020_Crosswalk/FeatureServer/0

For polygons, query `where=1=1`, `outFields=CSA2020`, `outSR=4326`, and
`f=geojson`. For the crosswalk, request `NSA2020,CSA2020`, `returnGeometry=false`,
and `f=json`. Use the **CSA2020** column, not CSA2010.

For the quickest demo, request VBN counts grouped by `Neighborhood`: use
`groupByFieldsForStatistics=Neighborhood`, `outFields=Neighborhood`, `f=json`,
and this JSON value for `outStatistics`:

```json
[{"statisticType":"count","onStatisticField":"OBJECTID","outStatisticFieldName":"notice_count"}]
```

Also query `returnCountOnly=true` for the source total. Fetch all result pages
when a query is limited; never assume the first response is complete.

## Stages

### 1. Get the CSA map working

Show a Baltimore basemap with the CSA polygons, a short title, and clickable CSA
names. Fit the view to Baltimore and include map attribution. Keep every CSA the
same neutral color. No VBN fetching or choropleth calculations yet.

### 2. Join the counts and make the choropleth

Join VBN `Neighborhood` to crosswalk `NSA2020`, then sum `notice_count` by
crosswalk `CSA2020`. Match that result to polygon `CSA2020`.

Trim/case-normalize names for matching while retaining original display names.
One verified source typo needs an explicit alias: **Greentown/Bayview →
Greektown/Bayview**. Do not guess other matches. Show unmatched records separately.
Keep `Unassigned -- Jail` separate from the 55 named CSAs.

Shade CSAs with a light-to-dark count scale. Add numeric legend breaks and show
each CSA's name and count on selection. Distinguish zero from missing data.
Explain that this uses BNIA's neighborhood assignment; it is not an exact
point-in-polygon count where neighborhoods cross CSA boundaries.

### 3. Make it ready for GitHub Pages

Keep the finished app entirely static, with `index.html` at the repository root.
Use relative paths such as `./App.jsx` and `./data/csa.geojson` so it also works
under a GitHub Pages project subdirectory. Avoid root-relative paths and SPA
routes that need a server rewrite.

Save the fetched polygons, crosswalk, and grouped counts as small public JSON
snapshots in `data/`, with source URLs and retrieval dates. The app should load
these snapshots without needing a live API or secret. Keep CDN dependencies.
Show a clear error if data cannot load.

## Finish each stage

Run it with the static server and check the browser. After Stage 2, assigned
counts plus exceptions must equal the VBN source total; every named CSA should
have a count or an explicit missing state. Check colors, legend, and popups.
Before handoff, test the site beneath a subdirectory as well as at the root.

Commit each working stage. Summarize what works and how to run it. At the end,
explain how to enable GitHub Pages from `main` at `/`. Prepare for hosting;
publish only if the presenter asks. Do not add census comparisons or forecasts.
