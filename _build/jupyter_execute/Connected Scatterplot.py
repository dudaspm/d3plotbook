#!/usr/bin/env python
# coding: utf-8

# # Connected Scatterplot

# Original ObservableHQ notebook: https://observablehq.com/@dudaspm/learning-d3-js-part-4?collection=@dudaspm/d3-in-observablehq

# ### Our Data Set

# In[1]:


import pandas as pd
url="https://gist.githubusercontent.com/dudaspm/e518430a731ac11f52de9217311c674d/raw/4c2f2bd6639582a420ef321493188deebc4a575e/StateCollege2000-2020.csv"
data = []
data=pd.read_csv(url)
data = data.fillna(0) # replace all NAs with 0s
data.to_csv('weather.csv', index = False, header=True)
data.head()


# ### Acknowledgement 
# 
# <cite>Cite as: Menne, Matthew J., Imke Durre, Bryant Korzeniewski, Shelley McNeal, Kristy Thomas, Xungang Yin, Steven Anthony, Ron Ray, Russell S. Vose, Byron E.Gleason, and Tamara G. Houston (2012): Global Historical Climatology Network - Daily (GHCN-Daily), Version 3. CITY:US420020. NOAA National Climatic Data Center. doi:10.7289/V5D21VHZ 02/22/2021. 
# 
# Publications citing this dataset should also cite the following article: Matthew J. Menne, Imke Durre, Russell S. Vose, Byron E. Gleason, and Tamara G. Houston, 2012: An Overview of the Global Historical Climatology Network-Daily Database. J. Atmos. Oceanic Technol., 29, 897-910. doi:10.1175/JTECH-D-11-00103.1. 
# 
# Use liability: NOAA and NCEI cannot provide any warranty as to the accuracy, reliability, or completeness of furnished data. Users assume responsibility to determine the usability of these data. The user is responsible for the results of any application of this data for other than its intended purpose.</cite>
# 
# Links:
# https://data.noaa.gov/onestop/
# 
# https://www.ncdc.noaa.gov/cdo-web/search

# The first step in the process is to take a piece of paper and draw a picture of what you believe the graph will look like. While doing this, I would suggest answering the following questions:
# 
# 1) Is the data continuous or discrete?
#   - For *continuous* we assume the data has a range of values 
#   - For *discrete* we assume the data can be binned
#     - this question can be a challenging first conversation to have, but the basic rule is: can you use a ruler? If so, continuous. If not, discrete.
# 
# 2) Are you interested in *comparing* your data points, or are you looking for a *trend* in your data?
# 
# 3) Which variables are our independent variables or our dependent variables? 
#   - For *independent* this is what we control 
#   - For *dependent* with this control, this is what we are measuring.
# 
# For us, I would say both our continuous, we are interested in the trend of the data, and date is independent and interest in the dependent. So, let's draw this out. 

# ### Start D3.js

# In[2]:


from IPython.display import HTML, Javascript, display

def configure_d3():
    display(Javascript("""
    require.config({
      paths: {
        d3: "https://d3js.org/d3.v6.min"
      }
    })"""))


configure_d3()


# ### Getting the Data into D3.js

# In[3]:


get_ipython().run_cell_magic('html', '', '<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.csv(\'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/us_state_vaccinations.csv\')\n        .then(function(data) {\n            console.log(data[0])\n        })\n        .catch(function(error){\n        \n        })\n    \n})\n</script>')


# ## Filter the Data

# In[4]:


get_ipython().run_cell_magic('html', '', '<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.csv(\'weather.csv\')\n        .then(function(data) {\n            data = data.filter(d=> (d.MONTH=="3") && (d.YEAR=="2020"))\n            console.log(data)\n        })\n        .catch(function(error){\n        \n        })\n    \n})\n</script>')


# ### Mapping the Data

# Now let's convert our data from its original format to an updated format using a function called d3.map(). [d3.map()](https://github.com/d3/d3-collection#maps) is a really nice function that can take your original data and convert it to other formats. Here is a simple example where we have an array of numbers, but we want to re-map them, so the values are multiplied by pi.

# In[5]:


get_ipython().run_cell_magic('javascript', '', 'var justSomeData = [1,2,3,4]\nconst output = justSomeData.map((d,i)=> d * Math.PI)\nelement.text(output)')


# In[6]:


get_ipython().run_cell_magic('javascript', '', 'var justSomeData = [1,2,3,4]\nconst output = justSomeData.map((d,i)=> d + "\\uD83D\\uDC08")\nelement.text(output[0])')


# In[7]:


get_ipython().run_cell_magic('html', '', '<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.csv(\'weather.csv\')\n        .then(function(data) {\n            data = data.filter(d=> (d.MONTH=="3") && (d.YEAR=="2020"))\n            data = data.map(d=> ({"DATE":d.DATE,"TMAX":d.TMAX}))\n            \n            console.log(data)\n            \n        })\n        .catch(function(error){\n        \n        })\n    \n})\n</script>')


# #### Adjusting the data

# In[8]:


get_ipython().run_cell_magic('html', '', '<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.csv(\'weather.csv\')\n        .then(function(data) {\n            data = data.filter(d=> (d.MONTH=="3") && (d.YEAR=="2020"))\n            data = data.map(d=> ({"DATE":d.DATE,"TMAX":+d.TMAX}))\n            \n            console.log(data)\n            \n        })\n        .catch(function(error){\n        \n        })\n    \n})\n</script>')


# Ok, the first step we need a function to convert our date in a way to make it usable in our chart. We can use a built-in function in D3.js called timeParse. timeParse needs to know how the date/time is formatted in our text and then use a specific format (called a specifier string). 
# 
# If we look at our dates we have (for example) "01/2019" or "month/full year". 
# 
# Here is a list of all [specifier strings](https://github.com/d3/d3-time-format#locale_format), and a smaller list for formats that I typically use:
# 
# * **%d** - zero-padded day of the month as a decimal number [01,31]
# * **%H** - hour (24-hour clock) as a decimal number [00,23]
# * **%m** - month as a decimal number [01,12]
# * **%M** - minute as a decimal number [00,59]
# * **%y** - year without century as a decimal number [00,99]
# * **%Y** - year with century as a decimal number, such as 1999
# 
# Meaning, we need a specifier string of "**%m/%Y**" = "**month/full year**"

# In[9]:


get_ipython().run_cell_magic('html', '', '<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.csv(\'weather.csv\')\n        .then(function(data) {\n            const dateConverter = d3.timeParse("%_m/%_d/%Y")\n            data = data.filter(d=> (d.MONTH=="3") && (d.YEAR=="2020"))\n            data = data.map(d=> ({"DATE":dateConverter(d.DATE),"TMAX":+d.TMAX}))\n            console.log(data)\n            \n        })\n        .catch(function(error){\n        \n        })\n    \n})\n</script>')


# ### Layout

# For the artwork itself, we will need a few basic things: a width, height, and margins.

# In[10]:


get_ipython().run_cell_magic('html', '', '<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.csv(\'weather.csv\')\n        .then(function(data) {\n            const width = 600\n            const height = 300\n            const margin = 60 \n            const dateConverter = d3.timeParse("%_m/%_d/%Y")\n            data = data.filter(d=> (d.MONTH=="3") && (d.YEAR=="2020"))\n            data = data.map(d=> ({"DATE":dateConverter(d.DATE),"TMAX":+d.TMAX}))\n            \n        })\n        .catch(function(error){\n        \n        })\n    \n})\n</script>')


# Next, we will need to have a function to scale our date. Again, we are assuming our “date” will be our independent data (the x-axis) and the “interest” our dependent data (y-axis). D3.js has a specific way to scale our time called d3.scaleTime, and for the “interest,” we will use the d3.scaleLinear as we did before.

# In[11]:


get_ipython().run_cell_magic('html', '', '<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.csv(\'weather.csv\')\n        .then(function(data) {\n            const width = 600\n            const height = 300\n            const margin = 60 \n            const dateConverter = d3.timeParse("%_m/%_d/%Y")\n            data = data.filter(d=> (d.MONTH=="3") && (d.YEAR=="2020"))\n            data = data.map(d=> ({"DATE":dateConverter(d.DATE),"TMAX":+d.TMAX}))\n            \n            const xScale = d3.scaleTime().range([margin , width - margin]).domain(d3.extent(data, (d,i) => d.DATE))\n            const yScale = d3.scaleLinear().range([height-margin , margin]).domain(d3.extent(data, (d,i) => d.TMAX))\n            \n            \n        })\n        .catch(function(error){\n        \n        })\n    \n})\n</script>')


# Finally (for now), we will make our function to create the line itself. This will be a function that creates the path from the data. Remember, *DATE is the x* and *TMAX is the y*.`

# In[12]:


get_ipython().run_cell_magic('html', '', '<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.csv(\'weather.csv\')\n        .then(function(data) {\n            const width = 600\n            const height = 300\n            const margin = 60 \n            const dateConverter = d3.timeParse("%_m/%_d/%Y")\n            data = data.filter(d=> (d.MONTH=="3") && (d.YEAR=="2020"))\n            data = data.map(d=> ({"DATE":dateConverter(d.DATE),"TMAX":+d.TMAX}))\n            \n            const xScale = d3.scaleTime().range([margin , width - margin]).domain(d3.extent(data, (d,i) => d.DATE))\n            const yScale = d3.scaleLinear().range([height-margin , margin]).domain(d3.extent(data, (d,i) => d.TMAX))\n            \n            const line = d3.line()\n                .x((d,i)=> xScale(d.DATE)) \n                .y((d,i)=> yScale(d.TMAX)) \n            \n        })\n        .catch(function(error){\n        \n        })\n    \n})\n</script>')


# #### Add our line

# In[13]:


get_ipython().run_cell_magic('html', '', '<div id="gohere1"></div>\n\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.csv(\'weather.csv\')\n        .then(function(data) {\n            const width = 600\n            const height = 300\n            const margin = 60 \n            const dateConverter = d3.timeParse("%_m/%_d/%Y")\n            data = data.filter(d=> (d.MONTH=="3") && (d.YEAR=="2020"))\n            data = data.map(d=> ({"DATE":dateConverter(d.DATE),"TMAX":+d.TMAX}))\n            \n            const xScale = d3.scaleTime().range([margin , width - margin]).domain(d3.extent(data, (d,i) => d.DATE))\n            const yScale = d3.scaleLinear().range([height-margin , margin]).domain(d3.extent(data, (d,i) => d.TMAX))\n            \n            const line = d3.line()\n                .x((d,i)=> xScale(d.DATE)) \n                .y((d,i)=> yScale(d.TMAX)) \n            \n            const svg = d3.select("div#gohere1").append("svg")\n                .attr("width", width)\n                .attr("height", height)\n\n            svg.selectAll("path")\n                .data([data])\n                .join("path")\n                .attr("d", function(d,i) { return line(d) })\n                .style("stroke", "green" )\n                .style("stroke-width", 3) \n                .style("fill", "none")\n            \n        })\n        .catch(function(error){\n        \n        })\n    \n})\n</script>')


# #### Adding our Circles

# In[14]:


get_ipython().run_cell_magic('html', '', '<div id="gohere2"></div>\n\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.csv(\'weather.csv\')\n        .then(function(data) {\n            const width = 600\n            const height = 300\n            const margin = 60 \n            const dateConverter = d3.timeParse("%_m/%_d/%Y")\n            data = data.filter(d=> (d.MONTH=="3") && (d.YEAR=="2020"))\n            data = data.map(d=> ({"DATE":dateConverter(d.DATE),"TMAX":+d.TMAX}))\n            \n            const xScale = d3.scaleTime().range([margin , width - margin]).domain(d3.extent(data, (d,i) => d.DATE))\n            const yScale = d3.scaleLinear().range([height-margin , margin]).domain(d3.extent(data, (d,i) => d.TMAX))\n            \n            const line = d3.line()\n                .x((d,i)=> xScale(d.DATE)) \n                .y((d,i)=> yScale(d.TMAX)) \n            \n            \n            const svg = d3.select("div#gohere2").append("svg")\n                .attr("width", width)\n                .attr("height", height)\n\n             svg.selectAll("circle")\n                .data(data)\n                .join("circle")\n                .attr("cx", (d,i)=> xScale(d.DATE))\n                .attr("cy", (d,i)=> yScale(d.TMAX))\n                .attr("r", 5) \n                .style("fill", "none")\n                .style("stroke", "black" )\n                .style("stroke-width", 3) \n            \n            svg.selectAll("path")\n                .data([data])\n                .join("path")\n                .attr("d", function(d,i) { return line(d) })\n                .style("stroke", "green" )\n                .style("stroke-width", 3) \n                .style("fill", "none")\n            \n\n            \n        })\n        .catch(function(error){\n        \n        })\n    \n})\n</script>')


# That's it! That is all the code we need to make the artwork. Now, we probably want to add an axis for our x and y values. Let's see how that will look within our code.
# 
# The x-axis will need to have the axis label at the bottom of the axis. This is pretty straight-forward by using the axisBottom() function to make the axis text on the bottom. The scale of our axis (the smallest, largest, and the labels in-between) will be based on our x values or scaleTime() values. So, set this as our scale. 

# In[15]:


get_ipython().run_cell_magic('html', '', '<div id="gohere3"></div>\n\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.csv(\'weather.csv\')\n        .then(function(data) {\n            const width = 600\n            const height = 300\n            const margin = 60 \n            const dateConverter = d3.timeParse("%_m/%_d/%Y")\n            data = data.filter(d=> (d.MONTH=="5") && (d.YEAR=="2020"))\n            data = data.map(d=> ({"DATE":dateConverter(d.DATE),"TMIN":+d.TMIN}))\n            \n            const xScale = d3.scaleTime().range([margin , width - margin]).domain(d3.extent(data, (d,i) => d.DATE))\n            const yScale = d3.scaleLinear().range([height-margin , margin]).domain(d3.extent(data, (d,i) => d.TMIN))\n            \n            const line = d3.line()\n                .x((d,i)=> xScale(d.DATE)) \n                .y((d,i)=> yScale(d.TMIN)) \n            \n            \n            const svg = d3.select("div#gohere3").append("svg")\n                .attr("width", width)\n                .attr("height", height)\n            \n            \n            const xAxis = d3.axisBottom().scale(xScale).tickFormat(d3.timeFormat("%d"))\n            \n            svg.append("g")\n                .attr("class", "axis")\n                .attr("transform", "translate(0," + (height-margin) + ")")\n                .call(xAxis) \n            \n            svg.selectAll("path.temp")\n                .data([data])\n                .join("path")\n                .attr("d", function(d,i) { return line(d) })\n                .attr("class", "temp")\n                .style("stroke", "green" )\n                .style("stroke-width", 3) \n                .style("fill", "none")\n            \n            svg.selectAll("circle")\n                .data(data)\n                .join("circle")\n                .attr("cx", (d,i)=> xScale(d.DATE))\n                .attr("cy", (d,i)=> yScale(d.TMIN))\n                .attr("r", 5)\n            \n        })\n        .catch(function(error){\n        \n        })\n    \n})\n</script>')


# The y-axis will need to have the axis label to the left. Again, straight-forward, axisLeft(), and the scaling is based on our y values or scaleLinear() values. 

# In[16]:


get_ipython().run_cell_magic('html', '', '<div id="gohere4"></div>\n\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.csv(\'weather.csv\')\n        .then(function(data) {\n            const width = 600\n            const height = 300\n            const margin = 60 \n            const dateConverter = d3.timeParse("%_m/%_d/%Y")\n            data = data.filter(d=> (d.MONTH=="5") && (d.YEAR=="2020"))\n            data = data.map(d=> ({"DATE":dateConverter(d.DATE),"TMAX":+d.TMIN}))\n            \n            const xScale = d3.scaleTime().range([margin , width - margin]).domain(d3.extent(data, (d,i) => d.DATE))\n            const yScale = d3.scaleLinear().range([height-margin , margin]).domain(d3.extent(data, (d,i) => d.TMAX))\n            \n            const line = d3.line()\n                .x((d,i)=> xScale(d.DATE)) \n                .y((d,i)=> yScale(d.TMAX)) \n            \n            \n            const svg = d3.select("div#gohere4").append("svg")\n                .attr("width", width)\n                .attr("height", height)\n            \n            \n            const xAxis = d3.axisBottom().scale(xScale).tickFormat(d3.timeFormat("%d"))\n            \n            svg.append("g")\n                .attr("class", "axis")\n                .attr("transform", "translate(0," + (height-margin) + ")")\n                .call(xAxis) \n            \n            \n            const yAxis = d3.axisLeft().scale(yScale).tickFormat((d,i) => d + "°")\n            \n            svg.append("g")\n                .attr("class", "axis")\n                .attr("transform", "translate(" + margin + ",0)")\n                .call(yAxis)  \n            \n            svg.selectAll("path.temp")\n                .data([data])\n                .join("path")\n                .attr("d", function(d,i) { return line(d) })\n                .attr("class", "temp")\n                .style("stroke", "green" )\n                .style("stroke-width", 3) \n                .style("fill", "none")\n            \n            svg.selectAll("circle")\n                .data(data)\n                .join("circle")\n                .attr("cx", (d,i)=> xScale(d.DATE))\n                .attr("cy", (d,i)=> yScale(d.TMAX))\n                .attr("r", 5)\n            \n        })\n        .catch(function(error){\n        \n        })\n    \n})\n</script>')


# In[ ]:




