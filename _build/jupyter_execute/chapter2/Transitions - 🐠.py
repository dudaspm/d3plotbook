#!/usr/bin/env python
# coding: utf-8

# # Transitions - 🐠

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


# ### Starting Graph

# In[2]:


get_ipython().run_cell_magic('html', '', '<div id="gohere1"></div>\n\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    const width = 300\n    const height = 100\n    margin = 40 \n    const dataset = [3, 5, 5, 6, 15, 18]\n    \n    const svg = d3.select("div#gohere1").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n    const x = d3.scaleLinear().range([margin,width-margin]).domain(d3.extent(dataset,(d,i)=> i))\n    \n    svg.selectAll("circle")\n    .data(dataset)\n    .join("circle")\n    .attr("cx", (d,i)=> x(i))\n    .attr("cy", height/2)\n    .attr("r", (d,i)=> d)\n});\n</script>')


# ### Transition

# In[3]:


get_ipython().run_cell_magic('html', '', '<div id="gohere2"></div>\n\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    const width = 300\n    const height = 100\n    margin = 40 \n    const dataset = [3, 5, 5, 6, 15, 18]\n    \n    const svg = d3.select("div#gohere2").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n    const x = d3.scaleLinear().range([margin,width-margin]).domain(d3.extent(dataset,(d,i)=> i))\n    \n    svg.selectAll("circle")\n    .data(dataset)\n    .join("circle")\n    .attr("cx", (d,i)=> x(i))\n    .attr("cy", height/2)\n    .attr("r", 0)\n    .transition()\n    .attr("r", (d,i)=> d)\n});\n</script>')


# ### Duration
# 
# Amount of time the transition takes in ms (1000 ms = 1 second)

# In[4]:


get_ipython().run_cell_magic('html', '', '<div id="gohere3"></div>\n\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    const width = 300\n    const height = 100\n    margin = 40 \n    const dataset = [3, 5, 5, 6, 15, 18]\n    \n    const svg = d3.select("div#gohere3").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n    const x = d3.scaleLinear().range([margin,width-margin]).domain(d3.extent(dataset,(d,i)=> i))\n    \n    svg.selectAll("circle")\n    .data(dataset)\n    .join("circle")\n    .attr("cx", (d,i)=> x(i))\n    .attr("cy", height/2)\n    .attr("r", 0)\n    .transition()\n    .duration(10000)\n    .attr("r", (d,i)=> d)\n});\n</script>')


# ### Delay
# 
# Setting a specific delay on each element based on an amount of time. 

# In[5]:


get_ipython().run_cell_magic('html', '', '<div id="gohere4"></div>\n\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    const width = 300\n    const height = 100\n    margin = 40 \n    const dataset = [3, 5, 5, 6, 15, 18]\n    \n    const svg = d3.select("div#gohere4").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n    const x = d3.scaleLinear().range([margin,width-margin]).domain(d3.extent(dataset,(d,i)=> i))\n    \n    svg.selectAll("circle")\n    .data(dataset)\n    .join("circle")\n    .attr("cx", (d,i)=> x(i))\n    .attr("cy", height/2)\n    .attr("r", 0)\n    .transition()\n    .duration(1000)\n    .delay((d,i)=> i*100)\n    .attr("r", (d,i)=> d)\n});\n</script>')


# ### Easing
# 
# The pattern the transition use. 
# https://observablehq.com/@d3/easing-animations

# In[6]:


get_ipython().run_cell_magic('html', '', '<div id="gohere5"></div>\n\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    const width = 300\n    const height = 100\n    margin = 40 \n    const dataset = [3, 5, 5, 6, 15, 18]\n    \n    const svg = d3.select("div#gohere5").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n    const x = d3.scaleLinear().range([margin,width-margin]).domain(d3.extent(dataset,(d,i)=> i))\n    \n    svg.selectAll("circle")\n        .data(dataset)\n        .join("circle")\n        .attr("cx", (d,i)=> x(i))\n        .attr("cy", height/2)\n        .attr("r", 2)\n        .transition()\n        .duration(1000)\n        .attr("cy", height/3)\n        .transition()\n        .duration(1000) \n        .attr("r", (d,i)=> d)\n});\n</script>')


# Using inputs for transitions. 
# 
# There are a number of different types of [inputs](https://www.w3schools.com/html/html_form_input_types.asp), but we will be covering the following:
# 
# 
# 
# *   Buttons
# *   Radio buttons
# *   Checkboxes
# *   Range
# 

# ### Buttons

# In[7]:


get_ipython().run_cell_magic('html', '', '<input type="button" id="button1" onclick="console.log(\'Hello, Everyone!\')" value="Click the button">')


# ### Radio buttons

# In[8]:


get_ipython().run_cell_magic('html', '  ', '<input type="radio" id="vanilla" name="iceCream" value="vanilla">\n<label for="vanilla">Vanilla</label><br>\n<input type="radio" id="chocolate" name="iceCream" value="chocolate">\n<label for="chocolate">Chocolate</label><br>\n<input type="radio" id="other" name="iceCream" value="other" checked>\n<label for="other">Other</label>')


# In[9]:


get_ipython().run_cell_magic('html', '  ', '<input type="radio" id="vanilla" name="iceCream" value="vanilla" checked>\n<label for="vanilla">Vanilla</label><br>\n<input type="radio" id="chocolate" name="iceCream" value="chocolate">\n<label for="chocolate">Chocolate</label><br>\n<input type="radio" id="other" name="iceCream" value="other">\n<label for="other">Other</label>')


# ### Checkbox
# 

# In[10]:


get_ipython().run_cell_magic('html', '', '<input type="checkbox" id="toppings1" name="toppings1" value="sprinkles" checked>\n<label for="toppings1">Sprinkles</label><br>\n<input type="checkbox" id="toppings2" name="toppings2" value="whippedCream" checked>\n<label for="toppings2">Whipped Cream</label><br>\n<input type="checkbox" id="toppings3" name="toppings3" value="cherry" checked>\n<label for="toppings3">Cherry</label>')


# ### Sliders

# In[11]:


get_ipython().run_cell_magic('html', '', '<input type="range" id="orders" name="orders" min="0" max="10" value="5" step="5" style="width:200px">\n<label for="orders">Number of Orders</label>')


# ### Adding a button

# In[12]:


get_ipython().run_cell_magic('html', '', '<div id="gohere6"></div>\n<input type="button" id="button2" value="Run the Transition!">\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    const width = 300\n    const height = 100\n    margin = 40 \n    const dataset = [3, 5, 5, 6, 15, 18]\n    \n    const svg = d3.select("div#gohere6").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n    const x = d3.scaleLinear().range([margin,width-margin]).domain(d3.extent(dataset,(d,i)=> i))\n    \n    svg.selectAll("circle")\n        .data(dataset)\n        .join("circle")\n        .attr("cx", (d,i)=> x(i))\n        .attr("cy", height/2)\n        .attr("r", 1)\n    \n    // d3.select can select any element on our page\n    d3.select("input#button2")\n        .on("click",function() {\n            console.log("button pushed!")\n        })\n\n\n});\n</script>')


# In[13]:


get_ipython().run_cell_magic('html', '', '<div id="gohere7"></div>\n<input type="button" id="button3" value="Run the Transition!">\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    const width = 300\n    const height = 100\n    margin = 40 \n    const dataset = [3, 5, 5, 6, 15, 18]\n    \n    const svg = d3.select("div#gohere7").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n    const x = d3.scaleLinear().range([margin,width-margin]).domain(d3.extent(dataset,(d,i)=> i))\n    \n    svg.selectAll("circle")\n        .data(dataset)\n        .join("circle")\n        .attr("cx", (d,i)=> x(i))\n        .attr("cy", height/2)\n        .attr("r", 1)\n    \n    // d3.select can select any element on our page\n    d3.select("input#button3")\n        .on("click",function() {\n            // svg.select selects things in the given graph\n            svg.selectAll("circle")\n                .transition()\n                .duration(1000)\n                .delay((d,i)=> i*100)\n                .attr("r", (d,i)=> d)\n        })\n\n});\n</script>')


# In[14]:


get_ipython().run_cell_magic('html', '', '<div id="gohere8"></div>\n<input type="button" id="button4" value="Run the Transition!">\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    const width = 300\n    const height = 100\n    margin = 40 \n    const dataset = [3, 5, 5, 6, 15, 18]\n    \n    const svg = d3.select("div#gohere8").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n    const x = d3.scaleLinear().range([margin,width-margin]).domain(d3.extent(dataset,(d,i)=> i))\n    \n    svg.selectAll("circle")\n        .data(dataset)\n        .join("circle")\n        .attr("cx", (d,i)=> x(i))\n        .attr("cy", height/2)\n        .attr("r", 1)\n    \n    var selected = 1;\n    \n    // d3.select can select any element on our page\n    d3.select("input#button4")\n        .on("click",function() {\n            // svg.select selects things in the given graph\n            if (selected) {\n                svg.selectAll("circle")\n                    .transition()\n                    .duration(1000)\n                    .delay((d,i)=> i*100)\n                    .attr("r", (d,i)=> d)  \n                selected = 0;\n            }\n            else {\n                svg.selectAll("circle")\n                    .transition()\n                    .duration(1000)\n                    .delay((d,i)=> i*100)\n                    .attr("r", (d,i)=> 1)  \n                selected = 1;\n            }\n\n        })\n\n});\n</script>')


# In[ ]:




