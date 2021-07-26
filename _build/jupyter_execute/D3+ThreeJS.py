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

# In[2]:


get_ipython().run_cell_magic('html', '', '<p id="preview"></p>\n<script>\n    var data = d3.range(11).map(d=>0)\n    var points = d3.range(100).map(d=> Math.round(d3.randomNormal(.5, .1)(d)*10))\n    var rolledData = d3.rollup(points,v => v.length, d => d)\n    \n    for (let [key, value] of rolledData) {\n        data[key] = value\n    }\n    document.getElementById("preview").innerHTML = data \n</script>')


# In[3]:


get_ipython().run_cell_magic('html', '', '<p id="preview2"></p>\n<script>\n    var data = d3.range(10).map(d=> d3.randomNormal(.5, .1)(d))\n    data = data.map(d=> Math.round(d*10))\n    data = data.sort((a, b) => a - b)\n    document.getElementById("preview2").innerHTML = data\n    \n    \n    \n</script>')


# In[4]:


get_ipython().run_cell_magic('html', '', '<div id="oneD1"></div>\n<script>\n    var squares = 10\n    var size = width/(squares-1)\n    var data = d3.range(squares).map(d=> d3.randomNormal(.5, .1)(d))\n    data = data.map(d=> Math.round(d*10))\n    data = data.sort((a, b) => a - b)\n    \n    var width = 400\n    var height = 400\n    var margin = 20 \n    var svg = d3.select("div#oneD1").append("svg")\n        .attr("width", width)\n        .attr("height", height)            \n\n    var x = d3.scaleLinear().range([0, width]).domain(d3.extent(data,(d,i) => i))\n    \n    var palette = d3.interpolateReds\n    var color = d3.scaleLinear().range([0,1]).domain([0,10])\n\n    var xAxis = d3.axisBottom().scale(x)\n    svg.append("g")\n        .attr("class", "axis")\n        .attr("transform", "translate(0," + (height-margin) + ")")\n        .call(xAxis) \n\n    svg.append("text")\n        .attr("x", width/2)\n        .attr("y", height-5)\n        .style("text-anchor", "middle")\n        .text("Index")\n\n    svg.selectAll("rect").data(data)\n        .join("rect")\n        .attr("x", (d,i)=>x(i))\n        .attr("y",(d,i)=>(height/2))\n        .attr("width",size)\n        .attr("height", size)\n        .style("stroke-width", 2) \n        .style("stroke","white")\n        .style("fill", d => palette(color(d)))\n        \n    svg.append("line")\n        .attr("x1", 0)\n        .attr("y1", height/2)\n        .attr("x2", width)\n        .attr("y2", height/2)\n        .style("stroke-width", 5) \n        .style("stroke","black")\n    \n</script>')


# In[5]:


get_ipython().run_cell_magic('html', '', '<div id="oneD2"></div>\n<script>\n    var squares = 10\n    var size = width/(squares-1)\n    var data = d3.range(squares).map(d=> d3.randomNormal(.5, .1)(d))\n    data = data.map(d=> Math.round(d*10))\n    data = data.sort((a, b) => a - b)\n    \n    var width = 400\n    var height = 400\n    var margin = 20 \n    var svg = d3.select("div#oneD2").append("svg")\n        .attr("width", width)\n        .attr("height", height)            \n\n    var x = d3.scaleLinear().range([0, width]).domain(d3.extent(data,(d,i) => i))\n    \n    var palette = d3.interpolateReds\n    var color = d3.scaleLinear().range([0,1]).domain([0,10])\n\n    var xAxis = d3.axisBottom().scale(x)\n    svg.append("g")\n        .attr("class", "axis")\n        .attr("transform", "translate(0," + (height-margin) + ")")\n        .call(xAxis) \n\n    svg.append("text")\n        .attr("x", width/2)\n        .attr("y", height-5)\n        .style("text-anchor", "middle")\n        .text("Index")\n\n    svg.selectAll("rect").data(data)\n        .join("rect")\n        .attr("x", (d,i)=>x(i))\n        .attr("y",(d,i)=>(height/2)-(size/2))\n        .attr("width",size)\n        .attr("height", size)\n        .style("stroke-width", 2) \n        .style("stroke","white")\n        .style("fill", d => palette(color(d)))\n        \n    svg.append("line")\n        .attr("x1", 0)\n        .attr("y1", height/2)\n        .attr("x2", width)\n        .attr("y2", height/2)\n        .style("stroke-width", 5) \n        .style("stroke","black")\n    \n</script>')


# In[6]:


get_ipython().run_cell_magic('html', '', '<div id="twoD1"></div>\n<script>\n    var squares = 10\n    var size = width/(squares-1)\n    var data = d3.range(squares*squares).map(d=> d3.randomNormal(.5, .1)(d))\n    data = data.map(d=> Math.round(d*10))\n    data = data.sort((a, b) => a - b)\n    \n    var width = 400\n    var height = 400\n    var margin = 20 \n    var svg = d3.select("div#twoD1").append("svg")\n        .attr("width", width)\n        .attr("height", height)            \n\n    var x = d3.scaleLinear().range([0, width]).domain(d3.extent(data,(d,i) => i))\n    var y = d3.scaleLinear().range([0, height]).domain(d3.extent(data,(d,i) => i))\n    \n    var palette = d3.interpolateReds\n    var color = d3.scaleLinear().range([0,1]).domain([0,10])\n\n    var xAxis = d3.axisBottom().scale(x)\n    svg.append("g")\n        .attr("class", "axis")\n        .attr("transform", "translate(0," + (height-margin) + ")")\n        .call(xAxis) \n    var yAxis = d3.axisLeft().scale(y)\n    svg.append("g")\n        .attr("class", "axis")\n        .attr("transform", "translate(" + margin + ",0)")\n        .call(yAxis)\n\n    svg.selectAll("rect").data(data)\n        .join("rect")\n        .attr("x", (d,i)=>x(i))\n        .attr("y",(d,i)=>(height/2)-(size/2))\n        .attr("width",size)\n        .attr("height", size)\n        .style("stroke-width", 2) \n        .style("stroke","white")\n        .style("fill", d => palette(color(d)))\n        \n    svg.append("line")\n        .attr("x1", 0)\n        .attr("y1", height/2)\n        .attr("x2", width)\n        .attr("y2", height/2)\n        .style("stroke-width", 5) \n        .style("stroke","black")\n    svg.append("line")\n        .attr("x1", width/2)\n        .attr("y1", 0)\n        .attr("x2", width/2)\n        .attr("y2", height)\n        .style("stroke-width", 5) \n        .style("stroke","black")\n</script>')


# In[7]:


get_ipython().run_cell_magic('html', '', '<div id="twoD2"></div>\n<script>\n    var squares = 10\n    var size = width/(squares-1)\n    var data = d3.range(squares*squares).map(d=> d3.randomNormal(.5, .1)(d))\n    data = data.map(d=> Math.round(d*10))\n    data = data.sort((a, b) => a - b)\n    \n    var width = 400\n    var height = 400\n    var margin = 20 \n    var svg = d3.select("div#twoD2").append("svg")\n        .attr("width", width)\n        .attr("height", height)            \n\n    var x = d3.scaleLinear().range([0, width]).domain([0,squares])\n    var y = d3.scaleLinear().range([0, height]).domain([0,squares])\n    \n    var palette = d3.interpolateReds\n    var color = d3.scaleLinear().range([0,1]).domain([0,10])\n\n    var xAxis = d3.axisBottom().scale(x)\n    svg.append("g")\n        .attr("class", "axis")\n        .attr("transform", "translate(0," + (height-margin) + ")")\n        .call(xAxis) \n    var yAxis = d3.axisLeft().scale(y)\n    svg.append("g")\n        .attr("class", "axis")\n        .attr("transform", "translate(" + margin + ",0)")\n        .call(yAxis)\n\n    svg.selectAll("rect").data(data)\n        .join("rect")\n        .attr("x", (d,i)=>x(i))\n        .attr("y",(d,i)=>(height/2)-(size/2))\n        .attr("width",size)\n        .attr("height", size)\n        .style("stroke-width", 2) \n        .style("stroke","white")\n        .style("fill", d => palette(color(d)))\n        \n    svg.append("line")\n        .attr("x1", 0)\n        .attr("y1", height/2)\n        .attr("x2", width)\n        .attr("y2", height/2)\n        .style("stroke-width", 5) \n        .style("stroke","black")\n    svg.append("line")\n        .attr("x1", width/2)\n        .attr("y1", 0)\n        .attr("x2", width/2)\n        .attr("y2", height)\n        .style("stroke-width", 5) \n        .style("stroke","black")\n</script>')


# In[8]:


get_ipython().run_cell_magic('html', '', '<div id="twoD3"></div>\n<script>\n    var squares = 10\n    var size = width/(squares-1)\n    var data = d3.range(squares*squares).map(d=> d3.randomNormal(.5, .1)(d))\n    data = data.map(d=> Math.round(d*10))\n    data = data.sort((a, b) => a - b)\n    \n    var width = 400\n    var height = 400\n    var margin = 20 \n    var svg = d3.select("div#twoD3").append("svg")\n        .attr("width", width)\n        .attr("height", height)            \n\n    var x = d3.scaleLinear().range([0, width]).domain([0,squares])\n    var y = d3.scaleLinear().range([0, height]).domain([0,squares])\n    \n    var palette = d3.interpolateReds\n    var color = d3.scaleLinear().range([0,1]).domain([0,10])\n\n    var xAxis = d3.axisBottom().scale(x)\n    svg.append("g")\n        .attr("class", "axis")\n        .attr("transform", "translate(0," + (height-margin) + ")")\n        .call(xAxis) \n    var yAxis = d3.axisLeft().scale(y)\n    svg.append("g")\n        .attr("class", "axis")\n        .attr("transform", "translate(" + margin + ",0)")\n        .call(yAxis)\n\n    d3.range(0,squares).forEach(function(dx) {\n        d3.range(0,squares).forEach(function(dy) {\n            i = (dy*10) + dx\n            svg.append("rect")\n                .attr("x", x(dx) )\n                .attr("y", y(dy) )\n                .attr("width",size)\n                .attr("height", size)\n                .style("stroke-width", 2) \n                .style("stroke","white")\n                .style("fill", palette(color(data[i])) )\n\n        })\n    })\n        \n    svg.append("line")\n        .attr("x1", 0)\n        .attr("y1", height/2)\n        .attr("x2", width)\n        .attr("y2", height/2)\n        .style("stroke-width", 5) \n        .style("stroke","black")\n        \n    svg.append("line")\n        .attr("x1", width/2)\n        .attr("y1", 0)\n        .attr("x2", width/2)\n        .attr("y2", height)\n        .style("stroke-width", 5) \n        .style("stroke","black")\n</script>')


# In[9]:


get_ipython().run_cell_magic('html', '', '<p id="data"></p>\n<div id="output"></div>\n<script type="module">\n    import * as THREE from \'https://threejs.org/build/three.module.js\';\n    import { OrbitControls } from \'https://threejs.org/examples/jsm/controls/OrbitControls.js\';\n    d3.text("https://gist.githubusercontent.com/dudaspm/2c78fe8deab29c0ac2c9d9c4ab9cdc25/raw/dc8ba78fa08e26e908ff6b5a01b265e278f57539/toyData.simulations.csv")\n    .then((input) => {\n        console.log(input)\n        var data = []\n        data = input.split("\\n")\n        data.map((d,i)=>+d)\n        document.getElementById("data").innerHTML = JSON.stringify(data[0])   \n        var height = 700\n        var width = 700\n        \n        var palette = d3.interpolateReds\n        var color = d3.scaleLinear().domain(d3.extent(data)).range([0,1])\n        var squares = 10\n        let renderer = new THREE.WebGLRenderer({antialias: true});\n        renderer.setSize(width, height);\n        renderer.setPixelRatio(devicePixelRatio);\n        var scene = new THREE.Scene();\n        var camera = new THREE.PerspectiveCamera(\n            45, // Field of view\n            height / width, // Aspect ratio\n            0.1, // Near\n            10000 // Far\n        );\n        console.log(camera)\n  var controls = new OrbitControls(camera, renderer.domElement);\n\n  controls.addEventListener("change", () => renderer.render(scene, camera));\n    camera.position.x = 0;\n  camera.position.y = 0;\n  camera.position.z = 2000;\n  var cubes = new THREE.Object3D();\n  scene.add( cubes );\n  var x = d3.scaleLinear().range([-width/2,width/2]).domain([0,squares-1])\n  var y = d3.scaleLinear().range([-width/2,width/2]).domain([0,squares-1])\n  var z = d3.scaleLinear().range([-width/2,width/2]).domain([0,squares-1])\n  var counter = 0;\n  d3.range(0,squares).forEach(function(dx) {\n    d3.range(0,squares).forEach(function(dy) {\n      d3.range(0,squares).forEach(function(dz) {\n        //console.log(x(dx), y(dy),z(dz), width/(squares-1));\n        if (data[counter]>.5) {\n          var size = width/(squares-1)\n          var geometry = new THREE.BoxGeometry(size,size,size);\n          if (data[counter]>.5) {\n            var material = new THREE.MeshBasicMaterial({color: palette(color(data[counter])), transparent : false, opacity:.3});\n          }\n          else {\n            var material = new THREE.MeshBasicMaterial({color: palette(color(data[counter])), transparent : true, opacity:.1});\n          }\n          var cube = new THREE.Mesh(geometry, material);\n          cube.position.x = x(dx);\n          cube.position.y = y(dy);\n          cube.position.z = z(dz);\n          cubes.add(cube);\n          \n        }\n        counter++;\n      })\n    })\n  })\n  \n \n  try {\n    while (true) {\n      renderer.render(scene, camera);\n      return document.getElementById("output").appendChild( renderer.domElement )\n    }\n  } finally {\n    renderer.dispose();\n  }\n    })\n    .catch((error) => console.log(error) )\n</script>')


# In[10]:


get_ipython().run_cell_magic('html', '', '<div id="output2"></div>\n<script type="module">\n    import * as THREE from \'https://threejs.org/build/three.module.js\';\n    import { OrbitControls } from \'https://threejs.org/examples/jsm/controls/OrbitControls.js\';\n    import { GLTFExporter } from \'https://threejs.org/examples/jsm/exporters/GLTFExporter.js\';\n    d3.text("https://gist.githubusercontent.com/dudaspm/2c78fe8deab29c0ac2c9d9c4ab9cdc25/raw/dc8ba78fa08e26e908ff6b5a01b265e278f57539/toyData.simulations.csv")\n    .then((input) => {\n        console.log(input)\n        var data = []\n        data = input.split("\\n")\n        data.map((d,i)=>+d)\n        document.getElementById("data").innerHTML = JSON.stringify(data[0])   \n        var height = 700\n        var width = 700\n        \n        var palette = d3.interpolateReds\n        var color = d3.scaleLinear().domain(d3.extent(data)).range([0,1])\n        var squares = 10\n        let renderer = new THREE.WebGLRenderer({antialias: true});\n        renderer.setSize(width, height);\n        renderer.setPixelRatio(devicePixelRatio);\n        var scene = new THREE.Scene();\n        var camera = new THREE.PerspectiveCamera(\n            45, // Field of view\n            height / width, // Aspect ratio\n            0.1, // Near\n            10000 // Far\n        );\n        console.log(camera)\n  var controls = new OrbitControls(camera, renderer.domElement);\n\n  controls.addEventListener("change", () => renderer.render(scene, camera));\n    camera.position.x = 0;\n  camera.position.y = 0;\n  camera.position.z = 2000;\n  var cubes = new THREE.Object3D();\n  scene.add( cubes );\n  var x = d3.scaleLinear().range([-width/2,width/2]).domain([0,squares-1])\n  var y = d3.scaleLinear().range([-width/2,width/2]).domain([0,squares-1])\n  var z = d3.scaleLinear().range([-width/2,width/2]).domain([0,squares-1])\n  var counter = 0;\n  d3.range(0,squares).forEach(function(dx) {\n    d3.range(0,squares).forEach(function(dy) {\n      d3.range(0,squares).forEach(function(dz) {\n        //console.log(x(dx), y(dy),z(dz), width/(squares-1));\n        if (data[counter]>.5) {\n          var size = width/(squares-1)\n          var geometry = new THREE.BoxGeometry(size,size,size);\n          if (data[counter]>.5) {\n            var material = new THREE.MeshBasicMaterial({color: palette(color(data[counter])), transparent : false, opacity:.3});\n          }\n          else {\n            var material = new THREE.MeshBasicMaterial({color: palette(color(data[counter])), transparent : true, opacity:.1});\n          }\n          var cube = new THREE.Mesh(geometry, material);\n          cube.position.x = x(dx);\n          cube.position.y = y(dy);\n          cube.position.z = z(dz);\n          cubes.add(cube);\n          \n        }\n        counter++;\n      })\n    })\n  })\n        function exportGLTF( input ) {\n\n            const gltfExporter = new GLTFExporter();\n\n\n            gltfExporter.parse( input, function ( result ) {\n                console.log(result)\n\n                if ( result instanceof ArrayBuffer ) {\n\n                    saveArrayBuffer( result, \'scene.glb\' );\n\n                } else {\n\n                    const output = JSON.stringify( result, null, 2 );\n                    console.log( output );\n                    saveString( output, \'scene.gltf\' );\n\n                }\n\n            } );\n\n        }\n        function saveArrayBuffer( buffer, filename ) {\n\n            save( new Blob( [ buffer ], { type: \'application/octet-stream\' } ), filename );\n\n        }\n\t\t\tconst link = document.createElement( \'a\' );\n\t\t\tlink.style.display = \'none\';\n\t\t\tdocument.body.appendChild( link );\n\t\t\tfunction save( blob, filename ) {\n\n\t\t\t\tlink.href = URL.createObjectURL( blob );\n\t\t\t\tlink.download = filename;\n\t\t\t\tlink.click();\n\n\t\t\t\t// URL.revokeObjectURL( url ); breaks Firefox...\n\n\t\t\t}\n\t\t\tfunction saveString( text, filename ) {\n\n\t\t\t\tsave( new Blob( [ text ], { type: \'text/plain\' } ), filename );\n\n\t\t\t}\n        exportGLTF( cubes )\n  try {\n    while (true) {\n      renderer.render(scene, camera);\n      return document.getElementById("output").appendChild( renderer.domElement )\n    }\n  } finally {\n    renderer.dispose();\n  }\n    })\n    .catch((error) => console.log(error) )\n</script>')


# In[ ]:




