#!/usr/bin/env python
# coding: utf-8

# # Making a Map

# Let's talk about making a map in D3. D3 is GREAT for making maps and it pretty straightforward to do so. 
# 
# Let's create a [choropleth map](https://en.wikipedia.org/wiki/Choropleth_map#:~:text=A%20choropleth%20map%20(from%20Greek,each%20area%2C%20such%20as%20population) for PA.
# 
# > A really good resource for this: https://observablehq.com/@floledermann/drawing-maps-from-geodata-in-d3

# In[1]:


from IPython.display import  HTML

def load_d3_in_cell_output():
  display(HTML("<script src='https://d3js.org/d3.v6.min.js'></script>"))
get_ipython().events.register('pre_run_cell', load_d3_in_cell_output)


# ## Data (Shapefiles)

# ### Acknowledgement
# <cite>Bureau, US Census. “Cartographic Boundary Files - Shapefile.” The United States Census Bureau, https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html. Accessed 25 May 2021.<cite> {cite}`bureau_cartographic_nodate`

# In[2]:


import requests
# URL to https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html
url = 'https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_county_20m.zip'
# get the zip file
r = requests.get(url)
# create a new file called 2018_us_county_500k.zip
f = open('cb_2018_us_county_20m.zip', "wb")
# write the zip from www2.census.gov to this new file
f.write(r.content)
# close the new file 
f.close()


# The way we need to get this zip file to ogre.adc4gis.com is to use a POST. Thanks to Rob Story's Github file for providing much of the details here {cite}`rob_story_shapefile_nodate`

# In[3]:


import requests
import json
url = r'http://ogre.adc4gis.com/convert'
f = open('cb_2018_us_county_20m.zip', "rb")
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
with open("cb_2018_us_county_20m.json", 'w') as f: 
    f.write(json.dumps(r.json(),sort_keys=True, indent=4,separators=(',', ': ')))
print("File is ready, called: cb_2018_us_county_20m.json")


# ### Let's look at our data
# 
# This is a basic "read-in" function for D3.js, specifically, for JSON. 
# 
# For this function, d3.js uses [Promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises) to make sure we get our file first, then tell the program what we are going to do with this file (using *.then*) and if it does go as planned, an error (using *.catch*). This is important to understand because your data is not available **outside** of the promise. 
# 
# For the purposes of viewing the structure of a typical geo(json) file. I made a mini-version. Here is the structure of these files.
# 

# In[4]:


get_ipython().run_cell_magic('html', '', '<em>Preview of the JSON file</em>\n<pre id="output1"></pre>\n<br>\n<p> As you can see, the structure of this document contains a FeatureCollection and each <em>Feature</em> is a reference to a county. Let\'s take a look at the first county.</p>\n<hr>\n<em>The first feature (or location)</em>\n<pre id="output2"></pre>\n<br>\n<p>For each county we have two sets of data. The <em>geometry</em> and the <em>properties</em>. \nThe <em>geometry</em> reflects all the latitudes and longitudes to create a single county. \nThink of this as "Connect the Dots" and all the dots connected form the shape (or polygon) of each county.\nBelow, we focus on the properties. \n</p>\n<hr>\n<em>The properties of the first feature (or location)</em>\n<pre id="output3"></pre>\n<br>\n<p> The <em>properties</em> are the meta-data of each county. As an example, the <em>Name</em> is Bladen. \nThere are a couple we need to point out for later but are also helpful for understanding shapefiles in general. \nThis being the <em>FIPS</em> or the Federal Information Processing Standards. \nLook at the <em>STATEFP</em> for the county, this is 37, meaning North Carolina. Here is a list of the <a href="https://www.nrcs.usda.gov/wps/portal/nrcs/detail/?cid=nrcs143_013696">State FIPS</a>.\nNow the <em>COUNTYFP</em>, is the FIPS of the that specific county within North Carolina. \nFinally, you might see this information combined, like the <em>GEOID</em>. \nThe <em>GEOID</em> is 37017 or Bladen, North Carolina. \n</p>\n\n<script type="text/javascript">   \n    \n    d3.json("cb_2018_us_county_20m-mini.json")\n        .then(function(us) {        \n            d3.select("pre#output1").text(JSON.stringify(us,null,\' \'))\n            d3.select("pre#output2").text(JSON.stringify(us["features"][0],null,\' \'))\n            d3.select("pre#output3").text(JSON.stringify(us["features"][0]["properties"],null,\' \'))\n        })\n        .catch(function(error){\n            console.log(error)\n        })\n\n</script>')


# ```{admonition} Common Question
# :class: tip
# Why do we need a FIPS number if the name is available?
# ```

# ```{admonition} Answer!
# :class: tip
# Sometimes people use different names for different locations. Example: New York and New York State. 
# Both are correct, but would look different based on the data. Instead, we can use FIPS 36. 
# Also, there might be inconsistencies based on what is capitalized and what is not. North Dakota is not the same as north dakota. 
# ```

# ## Creating the [Projection](https://github.com/d3/d3-geo#azimuthal-projections) for the US

# In[5]:


get_ipython().run_cell_magic('html', '', '<div id="map1"></div>\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.json("https://gist.githubusercontent.com/dudaspm/89da9e990236d2bc73a3a6ee00c18bb6/raw/055b78a9d016873c36e28872ab6a4d85d0be858e/usCounties.json")\n        .then(function(us) {\n            const width = 800\n            const height = 600\n            const margin = 0\n            // Create the Mercator Projection\n            projectionUS = d3.geoMercator().fitExtent([[margin, margin], [width - margin, height - margin]], us)\n            // Create a function to generate our paths (counties)\n            pathGeneratorUS = d3.geoPath().projection(projectionUS)\n            \n            const svg = d3.select("div#map1").append("svg")\n                .attr("width", width)\n                .attr("height", height)\n            \n            // construct the element\n            svg.selectAll("path")\n                .data(us.features)\n                .join("path")\n                .attr(\'d\', pathGeneratorUS)\n                .attr(\'fill\', \'none\')\n                .attr(\'stroke\', \'#999999\')\n                .attr(\'stroke-width\', \'2\')\n            \n        })\n        .catch(function(error){\n            console.log(error)\n        })\n    \n})\n</script>')


# This is a county map for the entire US. Let's focus on just Pennsylvania. 
# To do this, we need to filter to PA's data. 
# 
# If we take a look at the data. The data contains a stateFP for the [FIPS for each state](https://www.bls.gov/respondents/mwr/electronic-data-interchange/appendix-d-usps-state-abbreviations-and-fips-codes.htm).
# 
# For PA it is 42. 

# In[6]:


get_ipython().run_cell_magic('html', '', '<div id="map2"></div>\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.json("https://gist.githubusercontent.com/dudaspm/89da9e990236d2bc73a3a6ee00c18bb6/raw/055b78a9d016873c36e28872ab6a4d85d0be858e/usCounties.json")\n        .then(function(us) {\n            const width = 800\n            const height = 600\n            const margin = 0\n            // filter data to only PA\n            pa = ({type:"FeatureCollection", features:us.features.filter(d=> d.properties.STATEFP==42)})\n            \n            // Create the Mercator Projection\n            projectionPA = d3.geoMercator().fitExtent([[margin, margin], [width - margin, height - margin]], pa)\n            // Create a function to generate our paths (counties)\n            pathGeneratorPA = d3.geoPath().projection(projectionPA)\n            \n            const svg = d3.select("div#map2").append("svg")\n                .attr("width", width)\n                .attr("height", height)\n            \n            // construct the element\n            svg.selectAll("path")\n                .data(pa.features)\n                .join("path")\n                .attr(\'d\', pathGeneratorPA)\n                .attr(\'fill\', \'white\')\n                .attr(\'stroke\', \'#999999\')\n                .attr(\'stroke-width\', \'2\')\n                .append("title")\n                .text(d=> JSON.stringify(d.properties,null,\'\\t\'))\n                \n            \n        })\n        .catch(function(error){\n            console.log(error)\n        })\n    \n})\n</script>')


# Let's get some data to add to our map. 
# 
# Example is from [Los Angeles Times Data and Graphics Department](https://observablehq.com/@datadesk/u-s-households-without-internet-access-by-county?collection=@datadesk/u-s-census-data)
# 
# An example of using data from the Data Desk's open-source [census-data-downloader](https://github.com/datadesk/census-data-downloader)

# In[7]:


get_ipython().run_cell_magic('html', '', '<div id="output3"></div>\n<div id="output4"></div>\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.csv("https://raw.githubusercontent.com/datadesk/census-data-downloader/613e69f6413d917a6db60186e5ddf253e722dcfd/data/processed/acs5_2017_internet_counties.csv")\n        .then(function(census) {\n            d3.select("div#output4").text(JSON.stringify(census[0],null,\'\\t\'))\n            \n        })\n        .catch(function(error){\n            console.log(error)\n        })\n    \n})\n</script>')


# So, based on our data we have a state and a county code (like above). Let's use this data to see the percentage of internet access per county in PA. 

# In[8]:


get_ipython().run_cell_magic('html', '', '<div id="map3"></div>\n<div id="legend1"></div>\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.json("https://gist.githubusercontent.com/dudaspm/89da9e990236d2bc73a3a6ee00c18bb6/raw/055b78a9d016873c36e28872ab6a4d85d0be858e/usCounties.json")\n        .then(function(us) {\n        d3.csv("https://raw.githubusercontent.com/datadesk/census-data-downloader/613e69f6413d917a6db60186e5ddf253e722dcfd/data/processed/acs5_2017_internet_counties.csv")\n            .then(function(census) {\n                const width = 800\n                const height = 600\n                const margin = 0\n                // filter data to only PA\n                pa = ({type:"FeatureCollection", features:us.features.filter(d=> d.properties.STATEFP==42)})\n\n                // Adding our census data\n                census = census.filter(d=> d.state==42)\n                censusObject = {}\n                census.forEach(d=> censusObject[d.county] = (+d.total_no_internet/+d.universe))\n                \n                // create our color\n                palette = d3.interpolatePurples\n                color = d3.scaleLinear().range([0,1]).domain(d3.extent(census,d=> (+d.total_no_internet/+d.universe)))\n                \n                // Create the Mercator Projection\n                projectionPA = d3.geoMercator().fitExtent([[margin, margin], [width - margin, height - margin]], pa)\n                // Create a function to generate our paths (counties)\n                pathGeneratorPA = d3.geoPath().projection(projectionPA)\n\n                const svg = d3.select("div#map3").append("svg")\n                    .attr("width", width)\n                    .attr("height", height)\n\n                console.log(censusObject)\n                // construct the element\n                svg.selectAll("path").append(\'path\')\n                    .data(pa.features)\n                    .join("path")\n                    .attr(\'d\', pathGeneratorPA)\n                    .attr(\'fill\', d=> palette(color(censusObject[d.properties.COUNTYFP])))\n                    .attr(\'stroke\', \'#999999\')\n                    .attr(\'stroke-width\', \'2\')\n                    .append("title")\n                    .text(d=> "Location: "+d.properties.NAME+"\\nData: "+censusObject[d.properties.COUNTYFP])\n\n            })\n            .catch(function(error){\n                console.log(error)\n            })\n\n                \n            \n        })\n        .catch(function(error){\n            console.log(error)\n        })\n    \n})\n</script>')


# In[9]:


get_ipython().run_cell_magic('html', '', '\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.csv("https://raw.githubusercontent.com/datadesk/census-data-downloader/613e69f6413d917a6db60186e5ddf253e722dcfd/data/processed/acs5_2017_internet_counties.csv")\n        .then(function(census) {\n            const width = 800\n            const height = 100\n            const margin = 40 \n            census = census.filter(d=> d.state==42)\n            palette = d3.interpolatePurples\n            x = d3.scaleLinear().range([margin,width-margin]).domain(d3.extent(census,d=> (+d.total_no_internet/+d.universe)))\n            \n            const svg = d3.select("div#legend1").append("svg")\n                .attr("width", width)\n                .attr("height", height)\n            \n            \n            const xAxis = d3.axisBottom().scale(x)\n            \n            svg.append("g")\n                .attr("class", "axis")\n                .attr("transform", "translate(0," + (height-margin) + ")")\n                .call(xAxis) \n\n            svg.append("text")\n                .attr("x", width/2)\n                .attr("y", height-5)\n                .style("text-anchor", "middle")\n                .text("No Internet/All Data (%)")\n                       \n            \n            const num = 20\n            const values = d3.range(1,num)\n            \n            const coloring = d3.scaleLinear().range([0,1]).domain(d3.extent(values))\n            var defs = svg.append("defs")\n            var linearGradient = defs.append("linearGradient")\n                .attr("id", "linear-gradient1") \n\n            linearGradient.selectAll("stop").data(values).join("stop")\n                .attr("offset", d=> d/num)\n                .attr("stop-color", d=>palette(coloring(d)) )\n            svg.append("rect")\n                .attr("x", margin)\n                .attr("y", (height-margin)-50)\n                .attr("width", (width-margin)-(margin))\n                .attr("height", 50)\n                .style("fill", "url(#linear-gradient1)")\n\n            \n        })\n        .catch(function(error){\n            console.log(error)\n        })\n    \n})\n</script>')


# In[ ]:




