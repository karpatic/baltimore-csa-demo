"""Refresh public notice counts and BNIA neighborhood assignments, not a server."""
from pathlib import Path
import requests,json,datetime
D=Path(__file__).resolve().parent/'data'
SOURCE='https://baltegis.baltimorecity.gov/mapping/rest/services/Housing/DHCD_Open_Baltimore_Datasets/FeatureServer/1'
CROSS='https://services1.arcgis.com/mVFRs7NF4iFitgbY/arcgis/rest/services/NSA2020_to_CSA2010_and_CSA2020_Crosswalk/FeatureServer/0'
def query(url,params):
 r=requests.get(url+'/query',params={**params,'f':'json'},timeout=45);r.raise_for_status();j=r.json()
 if 'error' in j:raise RuntimeError(j['error'])
 assert not j.get('exceededTransferLimit'), 'Query truncated'
 return j
cw=query(CROSS,{'where':'1=1','outFields':'NSA2020,CSA2020','returnGeometry':'false'})
rows=query(SOURCE,{'where':'1=1','outFields':'Neighborhood','returnGeometry':'false','groupByFieldsForStatistics':'Neighborhood','outStatistics':json.dumps([{'statisticType':'count','onStatisticField':'OBJECTID','outStatisticFieldName':'notice_count'}])})
total=query(SOURCE,{'where':'1=1','returnCountOnly':'true'})['count']
norm=lambda s:(s or '').strip().casefold()
lookup={}
for f in cw['features']:
 a=f['attributes'];key=norm(a['NSA2020']);name=a['CSA2020'];name='Greektown/Bayview' if name=='Greentown/Bayview' else name
 assert key not in lookup or lookup[key]==name
 lookup[key]=name
names={f['properties']['CSA2020'] for f in json.loads((D/'csa.geojson').read_text())['features']}
counts={name:0 for name in names};unmatched=[]
for f in rows['features']:
 a=f['attributes'];name=lookup.get(norm(a['Neighborhood']))
 if name not in counts:unmatched.append(a)
 else:counts[name]+=a['notice_count']
assert sum(counts.values())+sum(a['notice_count'] for a in unmatched)==total
assert not unmatched,unmatched
result={'counts':counts,'total':total,'unmatched':unmatched,'retrieved':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':SOURCE,'crosswalk':CROSS,'method':'City Neighborhood matched to BNIA NSA2020, grouped by CSA2020. Neighborhood assignment, not point-in-polygon. Explicit Greentown/Bayview typo alias.'}
for name,obj in [('vbn-counts.json',result),('vbn-neighborhoods.json',rows),('neighborhood-crosswalk.json',cw)]: (D/name).write_text(json.dumps(obj,separators=(',',':')))
print(json.dumps({'total':total,'assigned':sum(counts.values()),'unmatched':len(unmatched),'areas':len(counts)}))
