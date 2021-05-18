#!/usr/bin/env python
# coding: utf-8

# # Making a Map

# Let's talk about making a map in D3. D3 is GREAT for making maps and it pretty straightforward to do so. 
# 
# Let's create a [choropleth map](https://en.wikipedia.org/wiki/Choropleth_map#:~:text=A%20choropleth%20map%20(from%20Greek,each%20area%2C%20such%20as%20population) for PA.
# 
# > A really good resource for this: https://observablehq.com/@floledermann/drawing-maps-from-geodata-in-d3

# In[1]:


from IPython.display import HTML, Javascript, display

def configure_d3():
    display(Javascript("""
    require.config({
      paths: {
        d3: "https://d3js.org/d3.v6.min"
      }
    })"""))


configure_d3()


# ## Let's look at our data

# In[2]:


get_ipython().run_cell_magic('html', '', '<div id="output1"></div>\n<div id="output2"></div>\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.json("https://gist.githubusercontent.com/dudaspm/89da9e990236d2bc73a3a6ee00c18bb6/raw/055b78a9d016873c36e28872ab6a4d85d0be858e/usCounties.json")\n        .then(function(us) {\n            d3.select("div#output1").text(\'{"type":"FeatureCollection", "features": []}\')\n            d3.select("div#output2").text(JSON.stringify(us["features"][0],null,\'\\t\'))\n            \n        })\n        .catch(function(error){\n            console.log(error)\n        })\n    \n})\n</script>')


# ## Creating the [Projection](https://github.com/d3/d3-geo#azimuthal-projections) for the US

# In[3]:


get_ipython().run_cell_magic('html', '', '<div id="map1"></div>\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.json("https://gist.githubusercontent.com/dudaspm/89da9e990236d2bc73a3a6ee00c18bb6/raw/055b78a9d016873c36e28872ab6a4d85d0be858e/usCounties.json")\n        .then(function(us) {\n            const width = 800\n            const height = 600\n            const margin = 0\n            // Create the Mercator Projection\n            projectionUS = d3.geoMercator().fitExtent([[margin, margin], [width - margin, height - margin]], us)\n            // Create a function to generate our paths (counties)\n            pathGeneratorUS = d3.geoPath().projection(projectionUS)\n            \n            const svg = d3.select("div#map1").append("svg")\n                .attr("width", width)\n                .attr("height", height)\n            \n            // construct the element\n            svg.selectAll("path")\n                .data(us.features)\n                .join("path")\n                .attr(\'d\', pathGeneratorUS)\n                .attr(\'fill\', \'none\')\n                .attr(\'stroke\', \'#999999\')\n                .attr(\'stroke-width\', \'2\')\n            \n        })\n        .catch(function(error){\n            console.log(error)\n        })\n    \n})\n</script>')


# This is a county map for the entire US. Let's focus on just Pennsylvania. 
# To do this, we need to filter to PA's data. 
# 
# If we take a look at the data. The data contains a stateFP for the [FIPS for each state](https://www.bls.gov/respondents/mwr/electronic-data-interchange/appendix-d-usps-state-abbreviations-and-fips-codes.htm).
# 
# For PA it is 42. 

# In[4]:


get_ipython().run_cell_magic('html', '', '<div id="map2"></div>\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.json("https://gist.githubusercontent.com/dudaspm/89da9e990236d2bc73a3a6ee00c18bb6/raw/055b78a9d016873c36e28872ab6a4d85d0be858e/usCounties.json")\n        .then(function(us) {\n            const width = 800\n            const height = 600\n            const margin = 0\n            // filter data to only PA\n            pa = ({type:"FeatureCollection", features:us.features.filter(d=> d.properties.STATEFP==42)})\n            \n            // Create the Mercator Projection\n            projectionPA = d3.geoMercator().fitExtent([[margin, margin], [width - margin, height - margin]], pa)\n            // Create a function to generate our paths (counties)\n            pathGeneratorPA = d3.geoPath().projection(projectionPA)\n            \n            const svg = d3.select("div#map2").append("svg")\n                .attr("width", width)\n                .attr("height", height)\n            \n            // construct the element\n            svg.selectAll("path")\n                .data(pa.features)\n                .join("path")\n                .attr(\'d\', pathGeneratorPA)\n                .attr(\'fill\', \'white\')\n                .attr(\'stroke\', \'#999999\')\n                .attr(\'stroke-width\', \'2\')\n                .append("title")\n                .text(d=> JSON.stringify(d.properties,null,\'\\t\'))\n                \n            \n        })\n        .catch(function(error){\n            console.log(error)\n        })\n    \n})\n</script>')


# Let's get some data to add to our map. 
# 
# Example is from [Los Angeles Times Data and Graphics Department](https://observablehq.com/@datadesk/u-s-households-without-internet-access-by-county?collection=@datadesk/u-s-census-data)
# 
# An example of using data from the Data Desk's open-source [census-data-downloader](https://github.com/datadesk/census-data-downloader)

# In[5]:


get_ipython().run_cell_magic('html', '', '<div id="output3"></div>\n<div id="output4"></div>\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.csv("https://raw.githubusercontent.com/datadesk/census-data-downloader/613e69f6413d917a6db60186e5ddf253e722dcfd/data/processed/acs5_2017_internet_counties.csv")\n        .then(function(census) {\n            d3.select("div#output4").text(JSON.stringify(census[0],null,\'\\t\'))\n            \n        })\n        .catch(function(error){\n            console.log(error)\n        })\n    \n})\n</script>')


# So, based on our data we have a state and a county code (like above). Let's use this data to see the percentage of internet access per county in PA. 

# In[6]:


get_ipython().run_cell_magic('html', '', '<div id="map3"></div>\n<div id="legend1"></div>\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.json("https://gist.githubusercontent.com/dudaspm/89da9e990236d2bc73a3a6ee00c18bb6/raw/055b78a9d016873c36e28872ab6a4d85d0be858e/usCounties.json")\n        .then(function(us) {\n        d3.csv("https://raw.githubusercontent.com/datadesk/census-data-downloader/613e69f6413d917a6db60186e5ddf253e722dcfd/data/processed/acs5_2017_internet_counties.csv")\n            .then(function(census) {\n                const width = 800\n                const height = 600\n                const margin = 0\n                // filter data to only PA\n                pa = ({type:"FeatureCollection", features:us.features.filter(d=> d.properties.STATEFP==42)})\n\n                // Adding our census data\n                census = census.filter(d=> d.state==42)\n                censusObject = {}\n                census.forEach(d=> censusObject[d.county] = (+d.total_no_internet/+d.universe))\n                \n                // create our color\n                palette = d3.interpolatePurples\n                color = d3.scaleLinear().range([0,1]).domain(d3.extent(census,d=> (+d.total_no_internet/+d.universe)))\n                \n                // Create the Mercator Projection\n                projectionPA = d3.geoMercator().fitExtent([[margin, margin], [width - margin, height - margin]], pa)\n                // Create a function to generate our paths (counties)\n                pathGeneratorPA = d3.geoPath().projection(projectionPA)\n\n                const svg = d3.select("div#map3").append("svg")\n                    .attr("width", width)\n                    .attr("height", height)\n\n                console.log(censusObject)\n                // construct the element\n                svg.selectAll("path").append(\'path\')\n                    .data(pa.features)\n                    .join("path")\n                    .attr(\'d\', pathGeneratorPA)\n                    .attr(\'fill\', d=> palette(color(censusObject[d.properties.COUNTYFP])))\n                    .attr(\'stroke\', \'#999999\')\n                    .attr(\'stroke-width\', \'2\')\n                    .append("title")\n                    .text(d=> "Location: "+d.properties.NAME+"\\nData: "+censusObject[d.properties.COUNTYFP])\n\n            })\n            .catch(function(error){\n                console.log(error)\n            })\n\n                \n            \n        })\n        .catch(function(error){\n            console.log(error)\n        })\n    \n})\n</script>')


# In[7]:


get_ipython().run_cell_magic('html', '', '\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.csv("https://raw.githubusercontent.com/datadesk/census-data-downloader/613e69f6413d917a6db60186e5ddf253e722dcfd/data/processed/acs5_2017_internet_counties.csv")\n        .then(function(census) {\n            const width = 800\n            const height = 100\n            const margin = 40 \n            census = census.filter(d=> d.state==42)\n            palette = d3.interpolatePurples\n            x = d3.scaleLinear().range([margin,width-margin]).domain(d3.extent(census,d=> (+d.total_no_internet/+d.universe)))\n            \n            const svg = d3.select("div#legend1").append("svg")\n                .attr("width", width)\n                .attr("height", height)\n            \n            \n            const xAxis = d3.axisBottom().scale(x)\n            \n            svg.append("g")\n                .attr("class", "axis")\n                .attr("transform", "translate(0," + (height-margin) + ")")\n                .call(xAxis) \n\n            svg.append("text")\n                .attr("x", width/2)\n                .attr("y", height-5)\n                .style("text-anchor", "middle")\n                .text("No Internet/All Data (%)")\n                       \n            \n            const num = 20\n            const values = d3.range(1,num)\n            \n            const coloring = d3.scaleLinear().range([0,1]).domain(d3.extent(values))\n            var defs = svg.append("defs")\n            var linearGradient = defs.append("linearGradient")\n                .attr("id", "linear-gradient1") \n\n            linearGradient.selectAll("stop").data(values).join("stop")\n                .attr("offset", d=> d/num)\n                .attr("stop-color", d=>palette(coloring(d)) )\n            svg.append("rect")\n                .attr("x", margin)\n                .attr("y", (height-margin)-50)\n                .attr("width", (width-margin)-(margin))\n                .attr("height", 50)\n                .style("fill", "url(#linear-gradient1)")\n\n            \n        })\n        .catch(function(error){\n            console.log(error)\n        })\n    \n})\n</script>')


# In[ ]:




