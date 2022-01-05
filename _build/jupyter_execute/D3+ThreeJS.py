#!/usr/bin/env python
# coding: utf-8

# # D3.js + Three.js → Aero Adobe

# We are looking at connecting D3.js + Three.js. A common question I would receive when leading discussions or courses would be 
# 
# >"Can I create 3D graphs with D3.js?" 
# 
# My response would be 
# 
# >"D3 is only 2D, to do 3D you need to use Three, but you can use D3 in Three." 
# 
# Partly as a joke, but mostly because its true. So, this is what this notebook is trying to showcase, coupling d3.js and three.js. Remember, D3 stands for Data Driven Documents and it does an excellent job of creating a means to format data to be used in three.js. 
# 
# The output for this will be a *.gltf* file or a GL Transmission Format file, which is used in blender or Adobe Aero.
# 
# Even though we will be using three.js we will be using the three.js [modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules). So, as always...

# In[1]:


from IPython.display import  HTML

def load_d3_in_cell_output():
  display(HTML("<script src='https://d3js.org/d3.v6.min.js'></script>"))
get_ipython().events.register('pre_run_cell', load_d3_in_cell_output)


# ## Our Data 
# 
# For our project, we are going to create a 3D cube and with values from a 2D normal distribution. To create our data, we can use 
# ```javascript
# d3.randomNormal(mu, sigma)
# ``` 
# 
# the *mu* value or the mean (μ) 
# 
# and
# 
# the *sigma* is the standard deviation (σ)
# 
# Let's create a 2D version of this only in d3.js. 

# ### Generating the Values (and Sorting)
# 
# To simply generate the data, we used  
# ```javascript
# d3.randomNormal()
# ```
# 
# with μ = .5 and σ = .1
# 
# Using 
# 
# ```javascript
# d3.range(10).map(d=>d)
# ```
# 
# we run the random normal distribution 10 times and create the first data source.  We then sort the data using
# 
# ```javascript
# data.sort((a, b) => a - b)
# ```
# 
# and print it to the 
# 
# ```html
# <p></p>
# ```

# In[2]:


get_ipython().run_cell_magic('html', '', '<p id="preview1"></p>\n<script>\n    var data = d3.range(10).map(d=> d3.randomNormal(.5, .1)(d))\n    data = data.map(d=> Math.round(d*10))\n    data = data.sort((a, b) => a - b)\n    document.getElementById("preview1").innerHTML = data\n    \n    \n    \n</script>')


# We will busing this data method for the majority of this conversation, but ulitimately we need to count occurances (and not just enumerate them). So, data set 2 will be
# 
# ### Histogram of the Random Normal Distribution
# 
# All d3.randomNormal() is doing is producing a random value based on the μ  and σ provide. The bell curve (that we are used to seeing) is a histogram of those values. Meaning, if we are given
# 
# 3,4,4,4,5,5,5,6,6,7
# 
# We could produce the following table of data
# 
# <table>
#     <tr><th>values</th><th>counts</th></tr>
#     <tr><td>0</td><td>0</td></tr>
#     <tr><td>1</td><td>0</td></tr>
#     <tr><td>2</td><td>0</td></tr>
#     <tr><td>3</td><td>1</td></tr>
#     <tr><td>4</td><td>3</td></tr>
#     <tr><td>5</td><td>3</td></tr>
#     <tr><td>6</td><td>2</td></tr>
#     <tr><td>7</td><td>1</td></tr>
#     <tr><td>8</td><td>0</td></tr>
#     <tr><td>9</td><td>0</td></tr>
# </table>

# To do this in D3.js we can use a built in function called 
# 
# ```javascript
# d3.rollup(data, values to rollup, count of values)
# ```

# In[3]:


get_ipython().run_cell_magic('html', '', '<p id="preview2rollup"></p>\n<p id="preview2"></p>\n<script>\n    var data = d3.range(11).map(d=>0)\n    var points = d3.range(100).map(d=> Math.round(d3.randomNormal(.5, .1)(d)*10))\n    var rolledData = d3.rollup(points,v => v.length, d => d)\n    \n    s = "Keys: " + [...rolledData.keys()] + "<br>Values:" + [...rolledData.values()]\n    \n    document.getElementById("preview2rollup").innerHTML = s\n    for (let [key, value] of rolledData) {\n        data[key] = value\n    }\n    \n    s = "Index: " + d3.range(11) + "<br>Values:" + data\n    \n    document.getElementById("preview2").innerHTML = s \n</script>')


# Let's create a visualization to help see how mu and sigma affect these histograms. 
# 
# #### Visualizing the Histogram

# In[4]:


get_ipython().run_cell_magic('html', '', '<input type="range" id="sigmahist" name="sigmahist" min="2" max="10" value="2" oninput="updateSigmaHist(this.value)">\n<label for="sigmahist">Sigma σ - Standard Deviation</label>\n<p id="sigmahist">0.1</p>\n\n<input type="range" id="meanhist" name="meanhist" min="0" max="10" oninput="updateMuHist(this.value)">\n<label for="meanhist">mu μ - Mean</label> \n<p id="meanhist">.5</p>\n\n<div id="histogram"></div>\n\n<script>\n    var sigmahist = .1\n    var meanhist = .5\n    var data = d3.range(11).map(d=>0)\n    var points = d3.range(100).map(d=> Math.round(d3.randomNormal(meanhist, sigmahist)(d)*10))\n    var rolledData = d3.rollup(points,v => v.length, d => d)\n    \n    for (let [key, value] of rolledData) {\n        data[key] = value\n    }\n    var widthHist = 400\n    var heightHist = 300\n    var marginHist = 40 \n    var svg = d3.select("div#histogram").append("svg")\n        .attr("width", widthHist)\n        .attr("height", heightHist)            \n\n    var xHist = d3.scaleLinear().range([marginHist, widthHist-marginHist]).domain(d3.extent(d3.range(11)))\n    var yHist = d3.scaleLinear().range([heightHist-marginHist, marginHist]).domain([0,50])\n    \n    var palette = d3.interpolateReds\n    var color = d3.scaleLinear().range([0,1]).domain([0,50])\n\n    var xAxisHist = d3.axisBottom().scale(xHist)\n    svg.append("g")\n        .attr("class", "xaxis")\n        .attr("transform", "translate(0," + (heightHist-marginHist) + ")")\n        .call(xAxisHist) \n        \n    svg.append("text")\n        .attr("x", widthHist/2)\n        .attr("y", heightHist-5)\n        .style("text-anchor", "middle")\n        .text("Indices")\n        \n    var yAxisHist = d3.axisLeft().scale(yHist)\n    svg.append("g")\n        .attr("class", "yaxis")\n        .attr("transform", "translate(" + marginHist + ",0)")\n        .call(yAxisHist)\n        \n    svg.append("text")\n        .attr("transform", "rotate(-90,15,"+(heightHist/2)+")")\n        .attr("x", 15)\n        .attr("y", heightHist/2)\n        .style("text-anchor", "middle")\n        .text("Count")\n        \n    var radius = 20\n    svg.selectAll("rect").data(data)\n        .join("rect")\n        .attr("class", "hist")\n        .attr("x",(d,i)=> xHist(i)-(radius/2))\n        .attr("y",(d,i)=> yHist(d)-(radius/2))\n        .attr("rx",radius/4)\n        .attr("width", radius)\n        .attr("height", radius)\n        .style("stroke","darkgrey")\n        .style("fill",(d,i)=> palette(color(d)))\n\n    function updateSigmaHist(s){\n        sigmahist = +s/20\n        d3.select("p#sigmahist").text(sigmahist)\n        updateGraphHist()\n    }\n    \n    function updateMuHist(m){\n        meanhist = +m/10\n        d3.select("p#meanhist").text(meanhist)\n        updateGraphHist()\n    }\n    \n    function updateGraphHist() {\n        var points = d3.range(100).map(d=> Math.round(d3.randomNormal(meanhist, sigmahist)(d)*10))\n        var rolledData = d3.rollup(points,v => v.length, d => d)\n        \n        data = d3.range(11).map(d=> 0)\n        for (let [key, value] of rolledData) {\n            data[key] = value\n        }\n        data = data.filter((d,i) => (i>=0) && (i<=10))\n        console.log(data)\n        d3.selectAll("rect.hist").data(data)\n            .transition()\n            .attr("y",(d,i)=> yHist(d)-(radius/2))\n            .style("fill",(d,i)=> palette(color(d)))\n    }\n</script>')


# As you can see, you how the bell-shaped curve can flucate around the mu and sigma values.

# ## Creating the 2D Shape
# 
# Our 2D shape 

# In[5]:


get_ipython().run_cell_magic('html', '', '<div id="oneD1"></div>\n<script>\n    var squares = 10\n    var size = width/(squares-1)\n    var data = d3.range(11).map(d=>0)\n    var points = d3.range(100).map(d=> Math.round(d3.randomNormal(.5, .1)(d)*10))\n    var rolledData = d3.rollup(points,v => v.length, d => d)\n    \n    for (let [key, value] of rolledData) {\n        data[key] = value\n    }\n    \n    var width = 400\n    var height = 400\n    var margin = 20 \n    var svg = d3.select("div#oneD1").append("svg")\n        .attr("width", width)\n        .attr("height", height)            \n\n    var x = d3.scaleLinear().range([0, width]).domain(d3.extent(data,(d,i) => i))\n    \n    var palette = d3.interpolateReds\n    var color = d3.scaleLinear().range([0,1]).domain([0,10])\n\n    var xAxis = d3.axisTop().scale(x)\n    svg.append("g")\n        .attr("class", "axis")\n        .attr("transform", "translate(0," + (height) + ")")\n        .call(xAxis) \n\n    svg.append("text")\n        .attr("x", width/2)\n        .attr("y", height-5)\n        .style("text-anchor", "middle")\n        .text("Index")\n\n    svg.selectAll("rect").data(data)\n        .join("rect")\n        .attr("x", (d,i)=>x(i))\n        .attr("y",(d,i)=>(height/2))\n        .attr("width",size)\n        .attr("height", size)\n        .style("stroke-width", 2) \n        .style("stroke","white")\n        .style("fill", d => palette(color(d)))\n        \n    svg.append("line")\n        .attr("x1", 0)\n        .attr("y1", height/2)\n        .attr("x2", width)\n        .attr("y2", height/2)\n        .style("stroke-width", 5) \n        .style("stroke","black")\n    \n</script>')


# In[6]:


get_ipython().run_cell_magic('html', '', '<div id="oneD2"></div>\n<script>\n    var squares = 10\n    var size = width/(squares-1)\n    var data = d3.range(11).map(d=>0)\n    var points = d3.range(100).map(d=> Math.round(d3.randomNormal(.5, .1)(d)*10))\n    var rolledData = d3.rollup(points,v => v.length, d => d)\n    \n    for (let [key, value] of rolledData) {\n        data[key] = value\n    }\n    \n    var width = 400\n    var height = 400\n    var margin = 20 \n    var svg = d3.select("div#oneD2").append("svg")\n        .attr("width", width)\n        .attr("height", height)            \n\n    var x = d3.scaleLinear().range([0, width]).domain(d3.extent(data,(d,i) => i))\n    \n    var palette = d3.interpolateReds\n    var color = d3.scaleLinear().range([0,1]).domain([0,10])\n\n    var xAxis = d3.axisTop().scale(x)\n    svg.append("g")\n        .attr("class", "axis")\n        .attr("transform", "translate(0," + (height) + ")")\n        .call(xAxis) \n\n    svg.append("text")\n        .attr("x", width/2)\n        .attr("y", height-5)\n        .style("text-anchor", "middle")\n        .text("Index")\n\n    svg.selectAll("rect").data(data)\n        .join("rect")\n        .attr("x", (d,i)=>x(i))\n        .attr("y",(d,i)=>(height/2))\n        .attr("width",size)\n        .attr("height", size)\n        .style("stroke-width", 2) \n        .style("stroke","white")\n        .style("fill", d => palette(color(d)))\n        \n    svg.append("line")\n        .attr("x1", 0)\n        .attr("y1", height/2)\n        .attr("x2", width)\n        .attr("y2", height/2)\n        .style("stroke-width", 5) \n        .style("stroke","black")\n    \n</script>')


# In[7]:


get_ipython().run_cell_magic('html', '', '<div id="twoD2"></div>\n<script>\n    var squares = 10\n    var size = width/(squares-1)\n    var data = d3.range(11).map(d=>0)\n    var points = d3.range(100).map(d=> Math.round(d3.randomNormal(.5, .1)(d)*10))\n    var rolledData = d3.rollup(points,v => v.length, d => d)\n    \n    for (let [key, value] of rolledData) {\n        data[key] = value\n    }\n    \n    var width = 400\n    var height = 400\n    var margin = 20 \n    var svg = d3.select("div#twoD2").append("svg")\n        .attr("width", width)\n        .attr("height", height)            \n\n    var x = d3.scaleLinear().range([0, width]).domain([0,squares])\n    var y = d3.scaleLinear().range([0, height]).domain([0,squares])\n    \n    var palette = d3.interpolateReds\n    var color = d3.scaleLinear().range([0,1]).domain([0,10])\n\n    var xAxis = d3.axisTop().scale(x)\n    svg.append("g")\n        .attr("class", "axis")\n        .attr("transform", "translate(0," + (height) + ")")\n        .call(xAxis) \n    var yAxis = d3.axisRight().scale(y)\n    svg.append("g")\n        .attr("class", "axis")\n        .attr("transform", "translate(" + 0 + ",0)")\n        .call(yAxis)\n\n    svg.selectAll("rect").data(data)\n        .join("rect")\n        .attr("x", (d,i)=>x(i))\n        .attr("y",(d,i)=>(height/2)-(size/2))\n        .attr("width",size)\n        .attr("height", size)\n        .style("stroke-width", 2) \n        .style("stroke","white")\n        .style("fill", d => palette(color(d)))\n        \n    svg.append("line")\n        .attr("x1", 0)\n        .attr("y1", height/2)\n        .attr("x2", width)\n        .attr("y2", height/2)\n        .style("stroke-width", 5) \n        .style("stroke","black")\n    svg.append("line")\n        .attr("x1", width/2)\n        .attr("y1", 0)\n        .attr("x2", width/2)\n        .attr("y2", height)\n        .style("stroke-width", 5) \n        .style("stroke","black")\n</script>')


# In[8]:


get_ipython().run_cell_magic('html', '', '<div id="twoD3"></div>\n<script>\n    var squares = 10\n    var size = width/(squares-1)\n    var data = d3.range(squares*squares).map(d=>0)\n    var points = d3.range(squares*squares*squares).map(d=> Math.round(d3.randomNormal((squares*squares)/20, (squares*squares)/100)(d)*10))\n    var rolledData = d3.rollup(points,v => v.length, d => d)\n    \n    for (let [key, value] of rolledData) {\n        data[key] = value\n    }\n    \n    var width = 400\n    var height = 400\n    var margin = 20 \n    var svg = d3.select("div#twoD3").append("svg")\n        .attr("width", width)\n        .attr("height", height)            \n\n    var x = d3.scaleLinear().range([0, width]).domain([0,squares])\n    var y = d3.scaleLinear().range([0, height]).domain([0,squares])\n    \n    var palette = d3.interpolateReds\n    var color = d3.scaleLinear().range([0,1]).domain([0,10])\n\n    var xAxis = d3.axisTop().scale(x)\n    svg.append("g")\n        .attr("class", "axis")\n        .attr("transform", "translate(0," + (height) + ")")\n        .call(xAxis) \n    var yAxis = d3.axisRight().scale(y)\n    svg.append("g")\n        .attr("class", "axis")\n        .attr("transform", "translate(" + 0 + ",0)")\n        .call(yAxis)\n\n    d3.range(0,squares).forEach(function(dy) {\n        d3.range(0,squares).forEach(function(dx) {\n            i = (dy*10) + dx\n            svg.append("rect")\n                .attr("x", x(dx) )\n                .attr("y", y(dy) )\n                .attr("width",size)\n                .attr("height", size)\n                .style("stroke-width", 2) \n                .style("stroke","white")\n                .style("fill", palette(color(data[i])) )\n\n        })\n    })\n        \n    svg.append("line")\n        .attr("x1", 0)\n        .attr("y1", height/2)\n        .attr("x2", width)\n        .attr("y2", height/2)\n        .style("stroke-width", 5) \n        .style("stroke","black")\n        \n    svg.append("line")\n        .attr("x1", width/2)\n        .attr("y1", 0)\n        .attr("x2", width/2)\n        .attr("y2", height)\n        .style("stroke-width", 5) \n        .style("stroke","black")\n</script>')


# In[9]:


get_ipython().run_cell_magic('html', '', '<input type="range" id="sd" name="sd" min="0" max="20" oninput="updateSigma(this.value)">\n<label for="sd">Sigma σ - Standard Deviation</label>\n<p id="sd">10</p>\n\n<input type="range" id="mean" name="mean" min="20" max="70" oninput="updateMu(this.value)">\n<label for="mean">mu σ - Mean</label> \n<p id="mean">50</p>\n\n<div id="twoD3Sums"></div>\n<script>\n    var squares = 10\n    var size = width/(squares-1)\n    var sigma = 10\n    var mu = (squares*squares)/2\n    var points = d3.range(1000).map(d=> d3.randomNormal(mu, sigma)(d))\n    points = points.map(d=> Math.round(d))\n    var data = d3.range(squares*squares).map(d=>0)\n    var rolledData = d3.rollup(points,v => v.length, d => d)\n\n    for (let [key, value] of rolledData) {\n        data[key] = value\n    }\n    var width = 400\n    var height = 400\n    var margin = 20 \n    var svg = d3.select("div#twoD3Sums").append("svg")\n        .attr("width", width)\n        .attr("height", height)            \n\n    var x = d3.scaleLinear().range([0, width]).domain([0,squares])\n    var y = d3.scaleLinear().range([0, height]).domain([0,squares])\n    \n    var palette = d3.interpolateReds\n    var color = d3.scaleLinear().range([0,1]).domain([0,10])\n\n    var xAxis = d3.axisTop().scale(x)\n    svg.append("g")\n        .attr("class", "axis")\n        .attr("transform", "translate(0," + (height) + ")")\n        .call(xAxis) \n    var yAxis = d3.axisRight().scale(y)\n    svg.append("g")\n        .attr("class", "axis")\n        .attr("transform", "translate(" + 0 + ",0)")\n        .call(yAxis)\n\n    d3.range(0,squares).forEach(function(dy) {\n        d3.range(0,squares).forEach(function(dx) {\n            i = (dy*10) + dx\n            svg.append("rect")\n                .attr("class","twod")\n                .attr("x", x(dx) )\n                .attr("y", y(dy) )\n                .attr("width",size)\n                .attr("height", size)\n                .style("stroke-width", 2) \n                .style("stroke","white")\n                .style("fill", palette(color(data[i])) )\n\n        })\n    })\n        \n    svg.append("line")\n        .attr("x1", 0)\n        .attr("y1", height/2)\n        .attr("x2", width)\n        .attr("y2", height/2)\n        .style("stroke-width", 5) \n        .style("stroke","black")\n        \n    svg.append("line")\n        .attr("x1", width/2)\n        .attr("y1", 0)\n        .attr("x2", width/2)\n        .attr("y2", height)\n        .style("stroke-width", 5) \n        .style("stroke","black")\n        \n\n    function updateSigma(s){\n        sigma = +s\n        d3.select("p#sd").text(sigma)\n        updateGraph()\n    }\n    \n    function updateMu(m){\n        mu = +m\n        d3.select("p#mean").text(mu)\n        updateGraph()\n    }\n    \n    function updateGraph() {\n        console.log(sigma,mu)\n        points = d3.range(1000).map(d=> d3.randomNormal(mu, sigma)(d))\n        points = points.map(d=> Math.round(d))\n        data = d3.range(squares*squares).map(d=>0)\n        rolledData = d3.rollup(points,v => v.length, d => d)\n\n        for (let [key, value] of rolledData) {\n            data[key] = value\n        }\n            svg.selectAll("rect.twod").data(data)\n                .style("fill", (d,i)=>palette(color(data[i])) )\n    }\n</script>')


# ## Creating the 3D Shape

# In[10]:


get_ipython().run_cell_magic('html', '', '<div id="three1"></div>\n<script type="module">\n    import * as THREE from \'https://threejs.org/build/three.module.js\';\n    import * as d3 from "https://cdn.skypack.dev/d3@7";\n    import { OrbitControls } from \'https://threejs.org/examples/jsm/controls/OrbitControls.js\';\n\n    var squares = 10\n    var sigma = 100\n    var mu = (squares*squares*squares)/2\n    var points = d3.range(10000).map(d=> d3.randomNormal(mu, sigma)(d))\n    points = points.map(d=> Math.round(d))\n    var data = d3.range(squares*squares*squares).map(d=>0)\n    var rolledData = d3.rollup(points,v => v.length, d => d)\n    for (let [key, value] of rolledData) {\n        data[key] = value\n    }\n    \n    var height = 400\n    var width = 400\n\n    var palette = d3.interpolateReds\n    var color = d3.scaleLinear().domain(d3.extent(data)).range([0,1])\n\n    let renderer = new THREE.WebGLRenderer({antialias: true});\n    renderer.setSize(width, height);\n    renderer.setPixelRatio(devicePixelRatio);\n    var scene = new THREE.Scene();\n    var camera = new THREE.PerspectiveCamera(\n        45, // Field of view\n        height / width, // Aspect ratio\n        0.1, // Near\n        3000 // Far\n    );\n\n    var controls = new OrbitControls(camera, renderer.domElement)\n\n    controls.addEventListener("change", () => renderer.render(scene, camera))\n    camera.position.x = 0;\n    camera.position.y = 0;\n    camera.position.z = 1000;\n    var cubes = new THREE.Object3D();\n    scene.add( cubes );\n    var x = d3.scaleLinear().range([-width/2,width/2]).domain([0,squares-1])\n    var y = d3.scaleLinear().range([-width/2,width/2]).domain([0,squares-1])\n    var z = d3.scaleLinear().range([-width/2,width/2]).domain([0,squares-1])\n    var counter = 0;\n    console.log(data)\n\n    d3.range(0,squares).forEach(function(dx) {\n        d3.range(0,squares).forEach(function(dy) {\n            d3.range(0,squares).forEach(function(dz) {\n                //console.log(data[counter])\n                if (data[counter]>10) {\n                    var size = width/(squares-1)\n                    var geometry = new THREE.BoxGeometry(size,size,size);\n                    var material = new THREE.MeshBasicMaterial({color: palette(color(data[counter])), transparent : true, opacity:color(data[counter])})\n                    var cube = new THREE.Mesh(geometry, material);\n                    cube.position.x = x(dx);\n                    cube.position.y = y(dy);\n                    cube.position.z = z(dz);\n                    cubes.add(cube);\n\n                }\n            counter++;\n            })\n        })\n    })\n    document.getElementById("three1").appendChild( renderer.domElement )\n    var render = function () {\n        requestAnimationFrame( render );\n\n\n\n        // Render the scene\n    renderer.render(scene, camera);\n    };\n\nrender();\n\n</script>')


# In[ ]:





# In[11]:


get_ipython().run_cell_magic('html', '', '<input type="button" id="exportButton" value="Export GLTF">\n<br>\n<input type="range" id="sd2" name="sd2" min="20" max="200" value="50">\n<label for="sd2">Sigma σ - Standard Deviation</label>\n<p id="sd2">50</p>\n\n<input type="range" id="mean2" name="mean2" min="200" max="700" value="500">\n<label for="mean2">mu σ - Mean</label> \n<p id="mean2">500</p>\n<div id="threeDOutput"></div>\n<script type="module">\n    \n    import * as THREE from \'https://threejs.org/build/three.module.js\';\n    import { OrbitControls } from \'https://threejs.org/examples/jsm/controls/OrbitControls.js\';\n    import { GLTFExporter } from \'https://threejs.org/examples/jsm/exporters/GLTFExporter.js\';\n    var cubes = new THREE.Object3D();\n    var sigma = 50\n    var mu = (squares*squares*squares)/2\n    function createGraph() {\n        var squares = 10\n\n        var points = d3.range(1000).map(d=> d3.randomNormal(mu, sigma)(d))\n        points = points.map(d=> Math.round(d))\n        var data = d3.range(squares*squares*squares).map(d=>0)\n        var rolledData = d3.rollup(points,v => v.length, d => d)\n        for (let [key, value] of rolledData) {\n            data[key] = value\n        }\n\n        var height = 400\n        var width = 400\n\n        var palette = d3.interpolateReds\n        var color = d3.scaleLinear().domain(d3.extent(data)).range([0,1])\n\n        let renderer = new THREE.WebGLRenderer({antialias: true});\n        renderer.setSize(width, height);\n        renderer.setPixelRatio(devicePixelRatio);\n        var scene = new THREE.Scene();\n        var camera = new THREE.PerspectiveCamera(\n            45, // Field of view\n            height / width, // Aspect ratio\n            0.1, // Near\n            3000 // Far\n        );\n\n        var controls = new OrbitControls(camera, renderer.domElement)\n\n        controls.addEventListener("change", () => renderer.render(scene, camera))\n        camera.position.x = 0;\n        camera.position.y = 0;\n        camera.position.z = 1000;\n        cubes = new THREE.Object3D();\n        scene.add( cubes );\n        var x = d3.scaleLinear().range([-width/2,width/2]).domain([0,squares-1])\n        var y = d3.scaleLinear().range([-width/2,width/2]).domain([0,squares-1])\n        var z = d3.scaleLinear().range([-width/2,width/2]).domain([0,squares-1])\n        var counter = 0;\n        console.log(data)\n\n        d3.range(0,squares).forEach(function(dx) {\n            d3.range(0,squares).forEach(function(dy) {\n                d3.range(0,squares).forEach(function(dz) {\n\n                    if (data[counter]>=1) {\n                        var size = width/(squares-1)\n                        var geometry = new THREE.BoxGeometry(size,size,size);\n                        var material = new THREE.MeshBasicMaterial({color: palette(color(data[counter])), transparent : true, opacity:color(data[counter])})\n                        var cube = new THREE.Mesh(geometry, material);\n                        cube.position.x = x(dx);\n                        cube.position.y = y(dy);\n                        cube.position.z = z(dz);\n                        cubes.add(cube);\n\n                    }\n                counter++;\n                })\n            })\n        })\n        document.getElementById("threeDOutput").appendChild( renderer.domElement )\n        \n        var render = function () {\n            requestAnimationFrame( render );\n            renderer.render(scene, camera);\n        };\n        \n        render();\n    }\n    function exportGLTF( input ) {\n        const gltfExporter = new GLTFExporter();\n        gltfExporter.parse( input, function ( result ) {\n            if ( result instanceof ArrayBuffer ) {\n                saveArrayBuffer( result, \'scene.glb\' );\n            } \n            else {\n                const output = JSON.stringify( result, null, 2 );\n                saveString( output, \'scene.gltf\' );\n\n            }\n        })\n    }\n    function saveArrayBuffer( buffer, filename ) {\n        save( new Blob( [ buffer ], { type: \'application/octet-stream\' } ), filename );\n    }\n    const link = document.createElement( \'a\' );\n    link.style.display = \'none\';\n    document.body.appendChild( link );\n    function save( blob, filename ) {\n        link.href = URL.createObjectURL( blob );\n        link.download = filename;\n        link.click();\n\n    }\n    function saveString( text, filename ) {\n        save( new Blob( [ text ], { type: \'text/plain\' } ), filename )\n    }\n    \n    createGraph();\n\n    document.querySelector(\'input#exportButton\').addEventListener(\'click\', function(){exportGLTF(cubes)})\n    document.querySelector(\'input#mean2\').addEventListener(\'change\', function(){updateMu2(this.value)})\n    document.querySelector(\'input#sd2\').addEventListener(\'change\', function(){updateSigma2(this.value)})\n    function updateSigma2(s){\n        sigma = +s\n        d3.select("p#sd2").text(sigma)\n        d3.select("#threeDOutput").select("*").remove()\n        createGraph()\n    }\n    \n    function updateMu2(m){\n        mu = +m\n        d3.select("p#mean2").text(mu)\n        d3.select("#threeDOutput").select("*").remove()\n        createGraph()\n    }\n    \n</script>')


# In[ ]:




