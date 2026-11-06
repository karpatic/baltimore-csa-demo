from pathlib import Path
import json,requests,datetime,subprocess
dest=Path(__file__).resolve().parent; data=dest/'data';data.mkdir(exist_ok=True)
base='https://services1.arcgis.com/mVFRs7NF4iFitgbY/arcgis/rest/services/'
polyu=base+'Community_Statistical_Areas_2020/FeatureServer/0'
polys=requests.get(polyu+'/query',params={'where':'1=1','outFields':'CSA2020','outSR':4326,'f':'geojson'},timeout=30).json()
assert len(polys['features'])==56 and not polys.get('exceededTransferLimit')
cw=[x['attributes'] for x in requests.get(base+'Tract2020_to_CSA2020/FeatureServer/0/query',params={'where':'1=1','outFields':'*','returnGeometry':'false','f':'json'},timeout=30).json()['features']]
raw=requests.get('https://api.censusreporter.org/1.0/data/show/acs2024_5yr',params={'table_ids':'B25002','geo_ids':'140|05000US24510'},headers={'User-Agent':'BaltimoreCSAHousingWorkshop/1.0 (educational static map demo)'},timeout=30).json(); tracts={}; grouped={}
for row in cw:
 geoid=row['GEOID_Tract_2020']; name=row['Community_Statistical_Area_2020']; v=raw['data']['14000US'+geoid]['B25002']['estimate'];total=v['B25002001'];vacant=v['B25002003'];occupied=v['B25002002']
 assert all(isinstance(n,(int,float)) and n>=0 for n in [total,vacant,occupied]) and total==vacant+occupied
 tracts[geoid]={'CSA2020':name,'total':total,'vacant':vacant,'occupied':occupied}
 g=grouped.setdefault(name,{'total':0,'vacant':0,'occupied':0,'tracts':0});g['total']+=total;g['vacant']+=vacant;g['occupied']+=occupied;g['tracts']+=1
assert set(grouped)=={f['properties']['CSA2020'] for f in polys['features']}
for g in grouped.values():g['rate']=100*g['vacant']/g['total'] if g['total'] else None
sources={'retrieved':datetime.datetime.now(datetime.timezone.utc).isoformat(),'period':'2020–2024 ACS five-year estimates','census_table':'https://data.census.gov/table/ACSDT5Y2024.B25002?g=050XX00US24510$1400000','census_metadata':'https://api.census.gov/data/2024/acs/acs5/groups/B25002.html','data_mirror':'https://api.censusreporter.org/1.0/data/show/acs2024_5yr?table_ids=B25002&geo_ids=140|05000US24510','crosswalk':base+'Tract2020_to_CSA2020/FeatureServer/0','boundaries':polyu,'note':'Census Reporter mirrors Census ACS estimates. Request using a project-specific User-Agent. Official Census API currently requires a key. No keys needed at runtime.'}
for name,obj in [('csa.geojson',polys),('tract-crosswalk.json',cw),('acs-tracts.json',tracts),('csa-housing.json',grouped),('sources.json',sources)]: (data/name).write_text(json.dumps(obj,separators=(',',':')))
(data/'acs-source.json').write_text(json.dumps(raw,separators=(',',':')))
report={'matched_tracts':len(tracts),'unmatched_tracts':0,'mapped_areas':len(grouped),'named_csas':55,'total_housing_units':sum(g['total'] for g in grouped.values()),'vacant_housing_units':sum(g['vacant'] for g in grouped.values()),'zero_denominator_areas':[k for k,g in grouped.items() if g['rate'] is None]};(data/'validation.json').write_text(json.dumps(report,indent=2));print(report)
