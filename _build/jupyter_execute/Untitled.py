#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
# URL to https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html
url = 'https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_county_500k.zip'
# get the zip file
r = requests.get(url)
# create a new file called 2018_us_county_500k.zip
f = open('2018_us_county_500k.zip', "wb")
# write the zip from www2.census.gov to this new file
f.write(r.content)
# close the new file 
f.close()


# In[2]:


import requests
import json
url = r'http://ogre.adc4gis.com/convert'
f = open('2018_us_county_500k.zip', "rb")
shp_data = {'upload': f}
print('Calling Ogre to perform shapefile to geoJSON conversion...')
try: 
    r = requests.post(url, files=shp_data)
except:
    print("There was an error with the HTTP request")
    raise
r.raise_for_status()
# close the new file 
f.close()
with open("2018_us_county_500k.json", 'w') as f: 
    f.write(json.dumps(r.json()))
f.close()


# In[ ]:




