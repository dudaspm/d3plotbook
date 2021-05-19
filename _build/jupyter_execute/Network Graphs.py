#!/usr/bin/env python
# coding: utf-8

# # Network Graph

# For this exercise we will be creating a random graph using NetworkX. 
# 
# 
# <cite>
#     Aric A. Hagberg, Daniel A. Schult and Pieter J. Swart, “Exploring network structure, dynamics, and function using NetworkX”, in Proceedings of the 7th Python in Science Conference (SciPy2008), Gäel Varoquaux, Travis Vaught, and Jarrod Millman (Eds), (Pasadena, CA USA), pp. 11–15, Aug 2008
#     </cite>
#     
# https://networkx.org/
# 
# https://networkx.org/documentation/latest/auto_examples/index.html
# 
# We will be using the Barabási–Albert algorithm to create the network
# 
# <cite>
#     A. L. Barabási and R. Albert “Emergence of scaling in random networks”, Science 286, pp 509-512, 1999.
# </cite>
# 
# https://networkx.org/documentation/stable/reference/generated/networkx.generators.random_graphs.barabasi_albert_graph.html?highlight=barabasi#networkx.generators.random_graphs.barabasi_albert_graph
# 
# #### D3.js Force-Directed Graph Notebook: https://observablehq.com/@d3/force-directed-graph 
# 

# In[1]:


get_ipython().run_cell_magic('capture', '', '!pip3 install networkx')


# In[2]:


import networkx as nx
import json

graphsize = 100
nodes = {}
links = {}
Graph = nx.barabasi_albert_graph(graphsize, 1)
j = "" # JSON object
j = j + "{"    
j = j + """\t"nodes": ["""

for n in nx.nodes(Graph):
    nodes[n] = {}
    nodes[n]['name'] = n
for n in nodes:
    j = j + str(json.dumps(nodes[n])) + ",\n"
j = j[:-2]
j = j + "\t],\n"
j = j + """\t"links":[\n"""
for link in nx.edges(Graph):
    links[str(link)] = {}
    links[str(link)]['source'] = link[0]
    links[str(link)]['target'] = link[1]
for l in links:
    j = j + str(json.dumps(links[l])) + ",\n"
j = j[:-2]
j = j + "\t]\n"
j = j + "}"
#print (j)

f = open("network.json", "w")
f.write(j)
f.close()


# ### Start D3.js

# In[3]:


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

# In[4]:


get_ipython().run_cell_magic('html', '', '<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.json(\'network.json\')\n        .then(function(data) {\n            nodes = data.nodes.map(d=> d)\n            console.log(nodes)\n            links = data.links.map(d=> ({source:nodes[d.source], target:nodes[d.target]}))\n            console.log(links)\n        })\n        .catch(function(error){\n        \n        })\n    \n})\n</script>')


# ### Creating the Graph

# In[5]:


get_ipython().run_cell_magic('html', '', '<div id="gohere1"></div>\n\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.json(\'network.json\')\n        .then(function(data) {\n            nodes = data.nodes.map(d=> d)\n            links = data.links.map(d=> ({source:nodes[d.source], target:nodes[d.target]}))\n            const width = 600\n            const height = 600\n\n            const svg = d3.select("div#gohere1").append("svg")\n                .attr("width", width)\n                .attr("height", height)\n\n            const link = svg\n                .selectAll("line.link")\n                .data(links)\n                .join("line")\n                .attr("class", "link")\n                .style("stroke", "#999")\n                .style("stroke-width", ".6px");\n\n            // append the nodes with specified data and style properties\n            const node = svg\n                .selectAll("circle.node")\n                .data(nodes)\n                .join("circle")\n                .attr("class", "node")\n                .attr("r", 5)\n                .style("stroke", "#fff")\n                .style("stroke-width", "1.5px")\n                .style("fill", (d,i)=> (i%2) ? "steelblue" : "purple")\n            \n            // attach titles to nodes, so when the mouse hovers over the nodes it projects the name\n            node.append("title")\n                .text(function(d) { return d.name; });\n        })\n        .catch(function(error){\n        \n        })\n    \n})\n</script>')


# ### Simulation Time

# In[6]:


get_ipython().run_cell_magic('html', '', '<div id="gohere2"></div>\n\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.json(\'network.json\')\n        .then(function(data) {\n            nodes = data.nodes.map(d=> d)\n            links = data.links.map(d=> ({source:nodes[d.source], target:nodes[d.target]}))\n            const width = 600\n            const height = 600\n\n            const svg = d3.select("div#gohere2").append("svg")\n                .attr("width", width)\n                .attr("height", height)\n\n            const link = svg\n                .selectAll("line.link")\n                .data(links)\n                .join("line")\n                .attr("class", "link")\n                .style("stroke", "#999")\n                .style("stroke-width", ".6px");\n\n            // append the nodes with specified data and style properties\n            const node = svg\n                .selectAll("circle.node")\n                .data(nodes)\n                .join("circle")\n                .attr("class", "node")\n                .attr("r", 5)\n                .style("stroke", "#fff")\n                .style("stroke-width", "1.5px")\n                .style("fill", (d,i)=> (i%2) ? "steelblue" : "purple")\n            \n            // attach titles to nodes, so when the mouse hovers over the nodes it projects the name\n            node.append("title")\n                .text(function(d) { return d.name; });\n\n            // this actually adheres the data to the force base layout and starts the layout\n            const simulation = d3.forceSimulation(nodes)\n                .force("link", \n                       d3.forceLink(links).id(d => d.name)\n                       .distance(10)\n                       .strength(1)\n                      )\n                .force("charge", d3.forceManyBody())\n                .force("center", d3.forceCenter(width / 2, height / 2))\n                .on("tick", ticked);            \n            \n            // this is the main mechanism of the force based diagram\n            // which moves the nodes and links from their starting and finishing positions\n            // once it hits equilibrium, it will stop moving the positions\n            function ticked() {\n                svg.selectAll("line.link")\n                    .attr("x1", d => d.source.x )\n                    .attr("y1", d => d.source.y )\n                    .attr("x2", d => d.target.x )\n                    .attr("y2", d => d.target.y )\n                \n                svg.selectAll("circle.node")\n                    .attr("cx", d => d.x)\n                    .attr("cy", d => d.y)\n            };\n        })\n        .catch(function(error){\n        \n        })\n    \n})\n</script>')


# ### Making it move

# In[7]:


get_ipython().run_cell_magic('html', '', '<div id="gohere3"></div>\n\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    \n    d3.json(\'network.json\')\n        .then(function(data) {\n            nodes = data.nodes.map(d=> d)\n            links = data.links.map(d=> ({source:nodes[d.source], target:nodes[d.target]}))\n            const width = 600\n            const height = 600\n\n            const svg = d3.select("div#gohere3").append("svg")\n                .attr("width", width)\n                .attr("height", height)\n\n            const link = svg\n                .selectAll("line.link")\n                .data(links)\n                .join("line")\n                .attr("class", "link")\n                .style("stroke", "#999")\n                .style("stroke-width", ".6px");\n\n            // append the nodes with specified data and style properties\n            const node = svg\n                .selectAll("circle.node")\n                .data(nodes)\n                .join("circle")\n                .attr("class", "node")\n                .attr("r", 5)\n                .style("stroke", "#fff")\n                .style("stroke-width", "1.5px")\n                .style("fill", (d,i)=> (i%2) ? "steelblue" : "purple")\n                .call(d3.drag()\n                      .on("start", dragstarted)\n                      .on("drag", dragged)\n                      .on("end", dragended))\n            \n            // attach titles to nodes, so when the mouse hovers over the nodes it projects the name\n            node.append("title")\n                .text(function(d) { return d.name; });\n\n            // this actually adheres the data to the force base layout and starts the layout\n            const simulation = d3.forceSimulation(nodes)\n                .force("link", \n                       d3.forceLink(links).id(d => d.name)\n                       .distance(d => 0)\n                       .strength(1)\n                      )\n                .force("charge", d3.forceManyBody())\n                .force("center", d3.forceCenter(width / 2, height / 2))\n                .on("tick", ticked);            \n            \n            // this is the main mechanism of the force based diagram\n            // which moves the nodes and links from their starting and finishing positions\n            // once it hits equilibrium, it will stop moving the positions\n            function ticked() {\n                svg.selectAll("line.link").attr("x1", function(d) { return d.source.x; })\n                    .attr("y1", function(d) { return d.source.y; })\n                    .attr("x2", function(d) { return d.target.x; })\n                    .attr("y2", function(d) { return d.target.y; });\n                svg.selectAll("circle.node").attr("cx", function(d) { return d.x; })\n                    .attr("cy", function(d) { return d.y; });\n            };\n            \n\n            function dragstarted(event) {\n                if (!event.active) simulation.alphaTarget(0.3).restart();\n                event.subject.fx = event.subject.x;\n                event.subject.fy = event.subject.y;\n            }\n\n            function dragged(event) {\n                event.subject.fx = event.x;\n                event.subject.fy = event.y;\n            }\n\n            function dragended(event) {\n                if (!event.active) simulation.alphaTarget(0);\n                event.subject.fx = event.x;\n                event.subject.fy = event.y;\n            }            \n            \n        })\n        .catch(function(error){\n        \n        })\n    \n})\n</script>')


# In[ ]:




