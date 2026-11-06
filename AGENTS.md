# Baltimore VBN Map Demo

## What to build

Create a local web app that answers: **How many open vacant building notices are
in each Baltimore Community Statistical Area (CSA)?**

Show the answer on an interactive choropleth: shade each CSA by its notice count.
The main task is joining point locations to boundary polygons. No census data
or forecasts are needed.

## Use these two datasets

- **Open VBN locations:** https://baltegis.baltimorecity.gov/mapping/rest/services/Housing/DHCD_Open_Baltimore_Datasets/FeatureServer/1
- **BNIA CSA boundaries:** https://services1.arcgis.com/mVFRs7NF4iFitgbY/arcgis/rest/services/Community_Statistical_Areas_2020/FeatureServer/0

Inspect the fields and geometry before using them. Fetch all records, including
every page, and put both datasets in the same coordinate system.

## Make it work

- Find which CSA contains each VBN point, then count notices per CSA.
- Preserve source IDs and avoid counting duplicate notices or boundary points twice.
- Account for missing or unmatched points. Keep `Unassigned -- Jail` separate.
- Use a light-to-dark color scale and a legend labeled **Open VBN count**.
- Clicking a CSA should show its name and count. Make zero and missing data distinct.
- Keep the app simple and easy to run locally. Choose libraries as needed.

## Before finishing

Check that all fetched notices are accounted for and that map colors, legend,
and popup counts agree. Show the data sources and retrieval date in the app.
Explain how to run it and mention anything incomplete. Do not publish it.
