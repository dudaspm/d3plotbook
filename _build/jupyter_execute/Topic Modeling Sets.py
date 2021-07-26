#!/usr/bin/env python
# coding: utf-8

# # Topic Modeling Sets

# Some time 

# In[1]:


from IPython.display import  HTML

def load_d3_in_cell_output():
  display(HTML("<script src='https://d3js.org/d3.v6.min.js'></script>"))
get_ipython().events.register('pre_run_cell', load_d3_in_cell_output)


# In[2]:


get_ipython().run_cell_magic('html', '', '<div id="triangle1"></div>\n\n<script type="text/javascript">   \n    var width = 300\n    var height = 300\n    var triangles = 1\n    var dataset = d3.range(triangles*3).map(d=>d)\n    var tri_size = 10\n    \n    var svg = d3.select("div#triangle1").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n        \n    var tri_x = [(tri_size/2), tri_size, 0]\n    var tri_y = [0, tri_size, tri_size]\n    svg.selectAll("circle")\n        .data(d3.range(triangles*3).map(d=>d))\n        .join("circle")\n        .attr("cx", (d,i)=> tri_x[i])\n        .attr("cy", (d,i)=> tri_y[i])\n        .attr("r", 4)\n        .style("fill", "purple")\n        .style("stroke", "black")\n        .style("stroke-width", 3) // reminder, this means 3 pixels\n\n</script>')


# In[3]:


get_ipython().run_cell_magic('html', '', '<div id="triangle2"></div>\n\n<script type="text/javascript">   \n    var width = 300\n    var height = 300\n    var margin = 20\n    var triangles = 1\n    var tri_col = 10\n    var tri_row = 10\n    var tri_size = 10\n    var x = d3.scaleLinear().range([margin , width - margin]).domain([0,tri_col-1])\n    var y = d3.scaleLinear().range([margin , height-margin]).domain([0,tri_row-1])\n    var tri_x = [(tri_size/2), tri_size, 0]\n    var tri_y = [0, tri_size, tri_size]   \n    \n    var svg = d3.select("div#triangle2").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n        \n    var g = svg.selectAll("g")\n        .data(d3.range(tri_col*tri_row).map(d=>d))\n        .join("g")\n        .attr("transform", d => "translate("+(x(d%tri_col))+","+(y(Math.floor(d/tri_col)))+")")\n    g.selectAll("circle")\n        .data(d3.range(triangles*3).map(d=>d))\n        .join("circle")\n        .attr("cx", (d,i)=> tri_x[i])\n        .attr("cy", (d,i)=> tri_y[i])\n        .attr("r", 4)\n        .style("fill", "purple")\n        .style("stroke", "black")\n        .style("stroke-width", 3) // reminder, this means 3 pixels\n\n</script>')


# Topics = 5
# 
# $n = 5$
# 
# $r = 3$
# 
# $\frac{n!}{ r! (n - r)!}$

# In[4]:


get_ipython().run_cell_magic('html', '', '<div id="triangle3"></div>\n\n<script type="text/javascript">   \n    var width = 300\n    var height = 300\n    var margin = 20\n    var fac = n => !(n > 1) ? 1 : fac(n - 1) * n;\n    var n = 4\n    var r = 3 \n    var soup = \'abcdefghijklmnopqrstuvwxyz\'.split(\'\');\n\n    var topics = d3.range(n).map(d=>soup[d])\n    var sets = []\n    for (let i = 0; i < topics.length - 1; i++) {\n        for (let j = i+1; j < topics.length - 1; j++) {\n            for (let k = j+1; k < topics.length; k++) {\n                var temp = []\n                temp.push(topics[i])\n                temp.push(topics[j])\n                temp.push(topics[k])\n                sets.push(temp)\n            }\n        }\n    }\n\n    var triangles = fac(n) / ( fac(r) * fac(n - r) )\n    var tri_col = 10\n    var tri_row = Math.ceil(sets.length/tri_col)\n    var tri_size = 10\n    var x = d3.scaleLinear().range([margin , width - margin]).domain([0,tri_col-1])\n    var y = d3.scaleLinear().range([margin , height-margin]).domain([0,tri_row-1])\n    var tri_x = [(tri_size/2), tri_size, 0]\n    var tri_y = [0, tri_size, tri_size]   \n    var palette = d3.interpolateTurbo\n    var color = d3.scaleLinear().range([0,1]).domain([0,topics.length-1])\n    \n    \n    var svg = d3.select("div#triangle3").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n        \n    var g = svg.selectAll("g")\n        .data(sets)\n        .join("g")\n        .attr("transform", (d,i) => "translate("+(x(i%tri_col))+","+(y(Math.floor(i/tri_col)))+")")\n    g.selectAll("circle")\n        .data(d=>d)\n        .join("circle")\n        .attr("cx", (d,i)=> tri_x[i])\n        .attr("cy", (d,i)=> tri_y[i])\n        .attr("r", 5)\n        .style("fill", d=> palette(color(topics.indexOf(d))))\n        .style("stroke", "black")\n        .style("stroke-width", 1) // reminder, this means 3 pixels\n\n</script>')


# In[5]:


get_ipython().run_cell_magic('html', '', '<div id="triangle4"></div>\n\n<script type="text/javascript">   \n    var width = 300\n    var height = 300\n    var margin = 20\n    var fac = n => !(n > 1) ? 1 : fac(n - 1) * n;\n    var n = 5\n    var r = 3 \n    var soup = \'abcdefghijklmnopqrstuvwxyz\'.split(\'\');\n    var topics = d3.range(n).map(d=>soup[d])\n    var sets = []\n    for (let i = 0; i < topics.length - 1; i++) {\n        for (let j = i+1; j < topics.length - 1; j++) {\n            for (let k = j+1; k < topics.length; k++) {\n                var temp = []\n                temp.push(topics[i])\n                temp.push(topics[j])\n                temp.push(topics[k])\n                sets.push(temp)\n            }\n        }\n    }\n    var triangles = fac(n) / ( fac(r) * fac(n - r) )\n    var tri_col = 10\n    var tri_row = Math.ceil(sets.length/tri_col)\n    var tri_size = 10\n    var x = d3.scaleLinear().range([margin , width - margin]).domain([0,tri_col-1])\n    var y = d3.scaleLinear().range([margin , height-margin]).domain([0,tri_row-1])\n    var tri_x = [(tri_size/2), tri_size, 0]\n    var tri_y = [0, tri_size, tri_size]   \n    var palette = d3.interpolateTurbo\n    var color = d3.scaleLinear().range([0,1]).domain([0,topics.length-1])\n    \n    \n    var svg = d3.select("div#triangle4").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n        \n    var g = svg.selectAll("g")\n        .data(sets)\n        .join("g")\n        .attr("transform", (d,i) => "translate("+(x(i%tri_col))+","+(y(Math.floor(i/tri_col)))+")")\n    g.selectAll("circle")\n        .data(d=>d)\n        .join("circle")\n        .attr("cx", (d,i)=> tri_x[i])\n        .attr("cy", (d,i)=> tri_y[i])\n        .attr("r", 5)\n        .style("fill", d=> palette(color(topics.indexOf(d))))\n        .style("stroke", "black")\n        .style("stroke-width", 1) // reminder, this means 3 pixels\n\n</script>')


# In[6]:


get_ipython().run_cell_magic('html', '', '<div id="triangle5"></div>\n\n<script type="text/javascript">   \n    var width = 300\n    var height = 300\n    var margin = 20\n    var fac = n => !(n > 1) ? 1 : fac(n - 1) * n;\n    var n = 6\n    var r = 3 \n    var soup = \'abcdefghijklmnopqrstuvwxyz\'.split(\'\');\n    var topics = d3.range(n).map(d=>soup[d])\n    var sets = []\n    for (let i = 0; i < topics.length - 1; i++) {\n        for (let j = i+1; j < topics.length - 1; j++) {\n            for (let k = j+1; k < topics.length; k++) {\n                var temp = []\n                temp.push(topics[i])\n                temp.push(topics[j])\n                temp.push(topics[k])\n                sets.push(temp)\n            }\n        }\n    }\n\n    var triangles = fac(n) / ( fac(r) * fac(n - r) )\n    var tri_col = 10\n    var tri_row = Math.ceil(sets.length/tri_col)\n    var tri_size = 10\n    var x = d3.scaleLinear().range([margin , width - margin]).domain([0,tri_col-1])\n    var y = d3.scaleLinear().range([margin , height-margin]).domain([0,tri_row-1])\n    var tri_x = [(tri_size/2), tri_size, 0]\n    var tri_y = [0, tri_size, tri_size]   \n    var palette = d3.interpolateTurbo\n    var color = d3.scaleLinear().range([0,1]).domain([0,topics.length-1])\n    \n    \n    var svg = d3.select("div#triangle5").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n        \n    var g = svg.selectAll("g")\n        .data(sets)\n        .join("g")\n        .attr("transform", (d,i) => "translate("+(x(i%tri_col))+","+(y(Math.floor(i/tri_col)))+")")\n    g.selectAll("circle")\n        .data(d=>d)\n        .join("circle")\n        .attr("cx", (d,i)=> tri_x[i])\n        .attr("cy", (d,i)=> tri_y[i])\n        .attr("r", 5)\n        .style("fill", d=> palette(color(topics.indexOf(d))))\n        .style("stroke", "black")\n        .style("stroke-width", 1) // reminder, this means 3 pixels\n\n</script>')


# In[7]:


get_ipython().run_cell_magic('html', '', '<div id="triangle6"></div>\n\n<script type="text/javascript">   \n    var width = 300\n    var height = 300\n    var margin = 20\n    var fac = n => !(n > 1) ? 1 : fac(n - 1) * n;\n    var n = 7\n    var r = 3 \n    var soup = \'abcdefghijklmnopqrstuvwxyz\'.split(\'\');\n    var topics = d3.range(n).map(d=>soup[d])\n    var sets = []\n    for (let i = 0; i < topics.length - 1; i++) {\n        for (let j = i+1; j < topics.length - 1; j++) {\n            for (let k = j+1; k < topics.length; k++) {\n                var temp = []\n                temp.push(topics[i])\n                temp.push(topics[j])\n                temp.push(topics[k])\n                sets.push(temp)\n            }\n        }\n    }\n    \n    var triangles = fac(n) / ( fac(r) * fac(n - r) )\n    var tri_col = 10\n    var tri_row = Math.ceil(sets.length/tri_col)\n    var tri_size = 10\n    var x = d3.scaleLinear().range([margin , width - margin]).domain([0,tri_col-1])\n    var y = d3.scaleLinear().range([margin , height-margin]).domain([0,tri_row-1])\n    var tri_x = [(tri_size/2), tri_size, 0]\n    var tri_y = [0, tri_size, tri_size]   \n    var palette = d3.interpolateTurbo\n    var color = d3.scaleLinear().range([0,1]).domain([0,topics.length-1])\n    \n    \n    var svg = d3.select("div#triangle6").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n        \n    var g = svg.selectAll("g")\n        .data(sets)\n        .join("g")\n        .attr("transform", (d,i) => "translate("+(x(i%tri_col))+","+(y(Math.floor(i/tri_col)))+")")\n    g.selectAll("circle")\n        .data(d=>d)\n        .join("circle")\n        .attr("cx", (d,i)=> tri_x[i])\n        .attr("cy", (d,i)=> tri_y[i])\n        .attr("r", 5)\n        .style("fill", d=> palette(color(topics.indexOf(d))))\n        .style("stroke", "black")\n        .style("stroke-width", 1) // reminder, this means 3 pixels\n\n</script>')


# Topics = 8

# In[8]:


get_ipython().run_cell_magic('html', '', '<div id="triangle7"></div>\n\n<script type="text/javascript">   \n    var width = 600\n    var height = 200\n    var margin = 20\n    var fac = n => !(n > 1) ? 1 : fac(n - 1) * n;\n    var n = 8\n    var r = 3 \n    var soup = \'abcdefghijklmnopqrstuvwxyz\'.split(\'\');\n    var topics = d3.range(n).map(d=>soup[d])\n    var sets = []\n    for (let i = 0; i < topics.length - 1; i++) {\n        for (let j = i+1; j < topics.length - 1; j++) {\n            for (let k = j+1; k < topics.length; k++) {\n                var temp = []\n                temp.push(topics[i])\n                temp.push(topics[j])\n                temp.push(topics[k])\n                sets.push(temp)\n            }\n        }\n    }\n\n    var triangles = fac(n) / ( fac(r) * fac(n - r) )\n    var tri_col = 10\n    var tri_row = Math.ceil(sets.length/tri_col)\n    var tri_size = 10\n    var x = d3.scaleLinear().range([margin , width - margin]).domain([0,tri_col-1])\n    var y = d3.scaleLinear().range([margin , height-margin]).domain([0,tri_row-1])\n    var tri_x = [(tri_size/2), tri_size, 0]\n    var tri_y = [0, tri_size, tri_size]   \n    var palette = d3.interpolateTurbo\n    var color = d3.scaleLinear().range([0,1]).domain([0,topics.length-1])\n    \n    \n    var svg = d3.select("div#triangle7").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n        \n    var g = svg.selectAll("g")\n        .data(sets)\n        .join("g")\n        .attr("transform", (d,i) => "translate("+(x(i%tri_col))+","+(y(Math.floor(i/tri_col)))+")")\n    g.selectAll("circle")\n        .data(d=>d)\n        .join("circle")\n        .attr("cx", (d,i)=> tri_x[i])\n        .attr("cy", (d,i)=> tri_y[i])\n        .attr("r", 5)\n        .style("fill", d=> palette(color(topics.indexOf(d))))\n        .style("stroke", "black")\n        .style("stroke-width", 1) // reminder, this means 3 pixels\n\n</script>')


# You can see how the complexity increase with the number of topics. Using the slider, change the number of topics to see how much this space increase with the number of topics. 

# In[9]:


get_ipython().run_cell_magic('html', '', '<input type="range" min="3" max="20" value="3" name="topics" oninput="graph(+this.value)">\n<label for="topics">Topics: </label><em id="topics" style="font-style: normal;">3</em>\n<div id="triangle9"></div>\n\n<script type="text/javascript">   \nfunction graph(n) {\n    document.getElementById(\'topics\').innerHTML = n\n    var width = 600\n    var height = 600\n    var margin = 20\n    var fac = n => !(n > 1) ? 1 : fac(n - 1) * n;\n    var r = 3 \n    var soup = \'abcdefghijklmnopqrstuvwxyz\'.split(\'\');\n    var topics = d3.range(n).map(d=>soup[d])\n    var sets = []\n    for (let i = 0; i < topics.length - 1; i++) {\n        for (let j = i+1; j < topics.length - 1; j++) {\n            for (let k = j+1; k < topics.length; k++) {\n                var temp = []\n                temp.push(topics[i])\n                temp.push(topics[j])\n                temp.push(topics[k])\n                sets.push(temp)\n            }\n        }\n    }\n\n    var triangles = fac(n) / ( fac(r) * fac(n - r) )\n    var tri_col = 10\n    var tri_row = Math.ceil(sets.length/tri_col)\n    var tri_size = 10\n    var x = d3.scaleLinear().range([margin , width - margin]).domain([0,tri_col-1])\n    var y = d3.scaleLinear().range([margin , height-margin]).domain([0,tri_row-1])\n    var tri_x = [(tri_size/2), tri_size, 0]\n    var tri_y = [0, tri_size, tri_size]   \n    var palette = d3.interpolateTurbo\n    var color = d3.scaleLinear().range([0,1]).domain([0,topics.length-1])\n    \n    d3.select("div#triangle9").select("svg").remove()\n    var svg = d3.select("div#triangle9").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n        \n    var g = svg.selectAll("g")\n        .data(sets)\n        .join("g")\n        .attr("transform", (d,i) => "translate("+(x(i%tri_col))+","+(y(Math.floor(i/tri_col)))+")")\n    g.selectAll("circle")\n        .data(d=>d)\n        .join("circle")\n        .attr("cx", (d,i)=> tri_x[i])\n        .attr("cy", (d,i)=> tri_y[i])\n        .attr("r", 5)\n        .style("fill", d=> palette(color(topics.indexOf(d))))\n        .style("stroke", "black")\n        .style("stroke-width", 1) // reminder, this means 3 pixels\n}\ngraph(3)\n</script>')


# In[ ]:




