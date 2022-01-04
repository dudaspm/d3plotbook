#!/usr/bin/env python
# coding: utf-8

# # Bar Charts

# ### Data

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
# 
# Bostock, M., Ogievetsky, V., & Heer, J. (2011). D³ data-driven documents. *IEEE transactions on visualization and computer graphics*, 17(12), 2301-2309.

# In[12]:


from IPython.display import HTML, Javascript, display

def configure_d3():
    display(Javascript("""
    require.config({
      paths: {
        d3: "https://d3js.org/d3.v6.min"
      }
    })"""))


configure_d3()


# ### Group

# In[13]:


get_ipython().run_cell_magic('html', '', '<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.csv(\'weather.csv\')\n        .then(function(data) {\n            const dateConverter = d3.timeParse("%_m/%_d/%Y")\n            const daysOfTheWeek = d3.timeFormat("%a")\n            data = data.map(d=> ({"DATE":dateConverter(d.DATE),"PRCP":+d.PRCP}))\n            console.log(d3.group(data, d => daysOfTheWeek(d.DATE)))\n        })\n        .catch(function(error){\n        \n        })\n    \n})\n</script>')


# ### Rollup

# In[14]:


get_ipython().run_cell_magic('html', '', '<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.csv(\'weather.csv\')\n        .then(function(data) {\n            const dateConverter = d3.timeParse("%_m/%_d/%Y")\n            const daysOfTheWeek = d3.timeFormat("%a")\n            data = data.map(d=> ({"DATE":dateConverter(d.DATE),"PRCP":+d.PRCP}))\n            console.log(d3.rollup(data, v => d3.mean(v, d => d.PRCP), k => daysOfTheWeek(k.DATE)))\n        })\n        .catch(function(error){\n        \n        })\n    \n})\n</script>')


# ### ScaleBand

# In[15]:


get_ipython().run_cell_magic('html', '', '\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    const someData = [0,4,14,20,30,31,42,50,59,62]\n    tryingScaleBands = d3.scaleBand().range([0,100]).domain(d3.extent(someData))\n    d3.select("div#graph1").text(someData.map(d=>tryingScaleBands(d))) \n})\n</script>\n<div id="graph1"></div>')


# In[16]:


get_ipython().run_cell_magic('html', '', '\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    const someData = [0,4,14,20,30,31,42,50,59,62]\n    tryingScaleBands = d3.scaleBand().range([0,100]).domain(someData.map(d=>d))\n    d3.select("div#graph2").text("list length: "+(someData.length)+"   scaleBand output: "+someData.map(d=>tryingScaleBands(d))) \n})\n</script>\n<div id="graph2"></div>')


# This makes a bit more sense. As you can see, this is evenly spacing all of our data based on the maximum range (100) minus the minimal range value (0), then dividing this by the size (the number of values) in the list. Or...

# $$
# \frac{(\text{maximum range value} - \text{minimum range value})}{\text{total number in the array}} = \frac{(100-0)}{10}
# $$

# scaleBand() has a couple of neat features that can help with bar chart design. Two in particular are called scaleBand().bandwidth and scaleBand().padding.
# * scaleBand().bandwidth - will give you the distance between points in scaleBand(). Meaning, it will be perfect for our bar charts, because we will be using rectangles for our bars.
# * scaleBand().padding - increases the padding between each bar.
# 
# Here is a graph showing the use of scaleBand() and using scaleBand().bandwidth to create the width of the rectangles.

# ![learning-d3-js-part-5-bar-chart.svg](attachment:learning-d3-js-part-5-bar-chart.svg)

# The figure below maps out 10 values and padding for 0 to 1. 0 indicating no padding and 1 meaning 100% padding (or no rectangle at all). Notice how values and the axis get evenly spaced based on the padding as well.

# ![learning-d3-js-part-5-bar-chart_2.svg](attachment:learning-d3-js-part-5-bar-chart_2.svg)

# Creating the rectangles themselves is another significant change from the line chart. With rectangles, you need 4 components:

# 
#   <span style="color:#008ec4">svg</span>.append(<span style="color:#008ec4">"g"</span>).selectAll(<span style="color:#008ec4">"rect"</span>)
# <br>&nbsp;&nbsp;.data(<span style="color:#008ec4">data</span>)
# <br>&nbsp;&nbsp;.join(<span style="color:#008ec4">"rect"</span>)
# <br>the x position (as it relates to the date)
# <br>&nbsp;&nbsp;.attr(<span style="color:#008ec4">"x"</span>, (d,i)=>x(<span style="color:#008ec4">d</span>.day)) 
# <br>the y position (as it relates to the interest), NOTE it is NOT the x-axis
# <br>&nbsp;&nbsp;.attr(<span style="color:#008ec4">"y"</span>,(d,i)=>y(<span style="color:#008ec4">d</span>.avg))
# <br>the width, which we talked about in regards to using the bandwidth
# <br>&nbsp;&nbsp;.attr(<span style="color:#008ec4">"width"</span>,<span style="color:#008ec4">x</span>.bandwidth)
# <br>this one is a bit, well, weird. I will explain below. 
# <br>&nbsp;&nbsp;.attr(<span style="color:#008ec4">"height"</span>, d => <span style="color:#008ec4">y</span>(0) - <span style="color:#008ec4">y</span>(<span style="color:#008ec4">d</span>.avg))
# <br>&nbsp;&nbsp;.style(<span style="color:#008ec4">"stroke-width"</span>, 2) 
# <br>&nbsp;&nbsp;.style(<span style="color:#008ec4">"stroke"</span>,<span style="color:#008ec4">"black"</span>)
# <br>&nbsp;&nbsp;.style(<span style="color:#008ec4">"fill"</span>, <span style="color:#008ec4">"steelblue"</span>)
# 

# OK, let's talk about height. The weirdness stems from our 0,0 being in the top-left corner of the screen. Meaning, when we create a rectangle and add a ''height,'' it goes down and not up. 
# 
# Here is an example of a rectangle that starts in the middle of the box. When we add height, it goes down. You may think, well, can I use a negative height? The answer is no. What does this mean? Continue below.

# ![learning-d3-js-part-5-bar-chart_4.svg](attachment:learning-d3-js-part-5-bar-chart_4.svg)

# This how we get the following. We first need to recall that the y is 
# <br>
# .attr(<span style="color:#008ec4">"y"</span>,(d,i)=>y(<span style="color:#008ec4">d</span>.avg))
# <br>
# This is NOT the x-axis, but the position of the actual value at that given avg.
# <br><br>
# Next, we take the maximum height value from our y scaleLinear().
# <br>
# 
# y = <span style="color:#008ec4">d3</span>.scaleLinear().range([<span style="color:#008ec4">height</span>-<span style="color:#008ec4">margin</span>.bottom , <span style="color:#008ec4">margin</span>.top]).domain([<span style="color:#008ec4">0,d3.max(backToList, (d,i) => d.avg)</span>])
# 
# <br><br>
# The largest value is (<span style="color:#008ec4">height</span>-<span style="color:#008ec4">margin</span>.bottom) or in another words, the smallest index in our y scaleLinear() ( <span style="color:#008ec4">y</span>(0))
# Last part we need to remember that we are starting at y(<span style="color:#008ec4">d</span>.interest) and we trying to get back to the x-axis. Meaning, we need to subtract out <span style="color:#008ec4">y</span>(<span style="color:#008ec4">d</span>.avg)
# <br><br>
# 
# We can write out the height two different ways:
# <br>
# 
# 
# .attr(<span style="color:#008ec4">"height"</span>, d => <span style="color:#008ec4">y</span>(0) - <span style="color:#008ec4">y</span>(<span style="color:#008ec4">d</span>.avg))
# 
# <br>
# OR
# <br>
# 
# 
# .attr(<span style="color:#008ec4">"height"</span>, d => (<span style="color:#008ec4">height</span>-<span style="color:#008ec4">margin</span>.bottom) - <span style="color:#008ec4">y</span>(<span style="color:#008ec4">d</span>.avg))
# 
# <br>
# My choice? 
# .attr(<span style="color:#008ec4">"height"</span>, d => (<span style="color:#008ec4">height</span>-<span style="color:#008ec4">margin</span>.bottom) - <span style="color:#008ec4">y</span>(<span style="color:#008ec4">d</span>.avg))
# <br> because this will be true no matter what the minimal value is for y. It is constant.

# Map - JavaScript | MDN. https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map. Accessed 9 Apr. 2021.
# 

# In[17]:


get_ipython().run_cell_magic('html', '', '<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.csv(\'weather.csv\')\n        .then(function(data) {\n            const dateConverter = d3.timeParse("%_m/%_d/%Y")\n            const daysOfTheWeek = d3.timeFormat("%a")\n            data = data.map(d=> ({"DATE":dateConverter(d.DATE),"PRCP":+d.PRCP}))\n            const nestedData = d3.rollup(data, v => d3.mean(v, d => d.PRCP), d => daysOfTheWeek(d.DATE))\n            console.log(nestedData)\n            var backToList = []\n            for (let [key, value] of nestedData) {\n                console.log(key + \' = \' + value)\n                backToList.push({"day":key,"avg":value})\n            }\n            console.log(backToList)     \n        \n            \n        })\n        .catch(function(error){\n        \n        })\n    \n})\n</script>')


# ### Graph

# In[18]:


get_ipython().run_cell_magic('html', '', '<div id="graph3"></div>\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.csv(\'weather.csv\')\n        .then(function(data) {\n            const dateConverter = d3.timeParse("%_m/%_d/%Y")\n            const daysOfTheWeek = d3.timeFormat("%a")\n            data = data.map(d=> ({"DATE":dateConverter(d.DATE),"PRCP":+d.PRCP}))\n            const nestedData = d3.rollup(data, v => d3.mean(v, d => d.PRCP), k => daysOfTheWeek(k.DATE))\n            var backToList = []\n            for (let [key, value] of nestedData) {\n                backToList.push({"day":key,"avg":value})\n            } \n            const width = 600\n            const height = 300\n            const margin = 60 \n            const svg = d3.select("div#graph3").append("svg")\n                .attr("width", width)\n                .attr("height", height)            \n            \n            const x = d3.scaleBand().range([margin , width - margin]).domain(backToList.map(d=>d.day)).padding(0)\n            const y = d3.scaleLinear().range([height-margin , margin]).domain([0,d3.max(backToList, (d,i) => d.avg)])\n            \n            const xAxis = d3.axisBottom().scale(x)\n            svg.append("g")\n                .attr("class", "axis")\n                .attr("transform", "translate(0," + (height-margin) + ")")\n                .call(xAxis) \n\n            svg.append("text")\n                .attr("x", width/2)\n                .attr("y", height-5)\n                .style("text-anchor", "middle")\n                .text("Days of the Week")\n            \n            const yAxis = d3.axisLeft().scale(y)\n            svg.append("g")\n                .attr("class", "axis")\n                .attr("transform", "translate(" + margin + ",0)")\n                .call(yAxis)\n\n            svg.append("text")\n                .attr("transform", "rotate(-90,15,"+(height/2)+")")\n                .attr("x", 15)\n                .attr("y", height/2)\n                .style("text-anchor", "middle")\n                .text("Average Rainfall (inches)")\n\n            svg.append("g").selectAll("rect")\n                .data(backToList)\n                .join("rect")\n                .attr("x", (d,i)=>x(d.day))\n                .attr("y",(d,i)=>y(d.avg))\n                .attr("width",x.bandwidth)\n                .attr("height", d => (height-margin) - y(d.avg))\n                .style("stroke-width", 2) \n                .style("stroke","black")\n                .style("fill", "steelblue")\n                .append("title")\n                .text(d=>d.avg)\n            \n        })\n        .catch(function(error){\n        \n        })\n    \n})\n</script>')


# In[ ]:




