# BNIA Data Lab

## Goal

Build an interactive choropleth of Baltimore's Community Statistical Areas
(CSAs), shaded by vacant building notice (VBN) count. Discover the public data,
join individual VBN points to CSA boundary polygons, and calculate the counts.
The spatial join is the main demonstration. Do not add census comparisons or
trend projections.

## Data discovery

Start with the public portals:

- Open Baltimore: https://data.baltimorecity.gov/
- BNIA mapping: https://mapping-bniajfi.opendata.arcgis.com/
- BNIA Vital Signs: https://vital-signs-bniajfi.hub.arcgis.com/

Candidate services to inspect and verify before using:

- Individual VBN locations: https://baltegis.baltimorecity.gov/mapping/rest/services/Housing/DHCD_Open_Baltimore_Datasets/FeatureServer/1
- CSA boundaries: https://services1.arcgis.com/mVFRs7NF4iFitgbY/arcgis/rest/services/Community_Statistical_Areas_2020/FeatureServer/0

Check the publisher, schema, geometry, and dates. Use individual location records,
not an already summarized citywide or tract-level table. Fetch every query page.
Record source URLs and retrieval dates with the downloaded data.

## Implementation

- Explain your approach briefly, then build a working local application.
- Prefer a lightweight browser app. Use libraries when they help.
- Preserve raw source data and IDs; keep calculations separate from display code.
- Put points and polygons in the same coordinate reference system before joining.
- Handle points on polygon boundaries explicitly. Never count a point twice.
- Inspect duplicate notice and property IDs. Clearly label whether totals count
  notices or unique buildings.
- Keep unmatched points, missing coordinates, and ambiguous assignments visible
  in a reconciliation summary. Keep `Unassigned -- Jail` separate from named CSAs.
- Show each CSA's name and count when selected. Include a sequential color legend
  with numeric breaks. Distinguish zero counts from missing data.
- Label the map as counts, not a vacancy rate. Do not invent a denominator.
- Keep the application local. Do not publish or modify existing websites.

## Checks

- Reconcile fetched records with the service count and check pagination.
- Test known inside, outside, and boundary points.
- After any documented deduplication, assigned totals plus exceptions must equal
  the input total.
- Verify that map colors, legend ranges, and selected-CSA counts agree.
- Confirm the application loads locally and explain how to run it.

## Handoff

Summarize what works, what you checked, and what remains incomplete. Keep these
instructions current if the project changes.
