#!/usr/bin/env python
# coding: utf-8

# # Styles, Scales, and Shapes

# ## Styles and Shapes

# *Styling* - The styling is handled through something call CSS (Cascading Style Sheets), but we can specifically handle this within our D3.js code. Here is a list of typical style changes. 
# * fill - the color inside the shape
# * stroke - the border of the shape
# * opacity - the transparency of the shape
# * Note: there are more combinations, but these are the basics and covers a good amount of styling.
# 
# *Shapes* - At this point, we have been using circles primarily for out designs. There are few other shapes we need to cover and what is needed to draw these.
# * Circles ("circle") - cx, cy, r
# * Rectangles ("rect") - x, y, width, height
# * Line ("line") - x1, y1, x2, y2
# * Text ("text") - x, y
# * Paths ("path") - these are by far the most complicate shapes, and will require further discussion throughout these notebooks
# * Note: There are ellipse, polylines, and polygons, but these are RARELY used in D3.js
# . 

# First things, first... Let's bring back our last project for Part 2.

# In[1]:


from IPython.display import  HTML

def load_d3_in_cell_output():
  display(HTML("<script src='https://d3js.org/d3.v6.min.js'></script>"))
get_ipython().events.register('pre_run_cell', load_d3_in_cell_output)


# ```javascript
# var dataset = [3, 5, 5, 6, 15, 18]
# ```

# In[2]:


get_ipython().run_cell_magic('html', '', '<div id="gohere1"></div>\n\n<script type="text/javascript">   \n    var width = 300\n    var height = 300\n    var dataset = [3, 5, 5, 6, 15, 18]\n    \n    var svg = d3.select("div#gohere1").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n  svg.selectAll("circle")\n    .data(dataset)\n    .join("circle")\n    .attr("cx", (d,i)=> i*30)\n    .attr("cy", (d,i)=> height - (i*20))\n    .attr("r", (d,i)=> d)\n</script>')


# In the above example, we used .attr(ibute) for the attributes of the given shape. We can use another function called .style() to add the CSS styling directly to the shape.
# 
# For our first example, we make these *purple circles with a black border that is 3 px in width*

# In[3]:


get_ipython().run_cell_magic('html', '', '<div id="gohere2"></div>\n\n<script type="text/javascript">   \n    var width = 300\n    var height = 300\n    var dataset = [3, 5, 5, 6, 15, 18]\n    \n    var svg = d3.select("div#gohere2").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n  svg.selectAll("circle")\n    .data(dataset)\n    .join("circle")\n    .attr("cx", (d,i)=> i*30)\n    .attr("cy", (d,i)=> height - (i*20))\n    .attr("r", (d,i)=> d)\n    .style("fill", "purple")\n    .style("stroke", "black")\n    .style("stroke-width", 3) // reminder, this means 3 pixels\n\n</script>')


# **Your Turn** - Create the 6 circles with the stroke: blue, stroke-width: 5px, and fill: lightgrey

# In[4]:


get_ipython().run_cell_magic('html', '', '<div id="gohere3"></div>\n\n<script type="text/javascript">   \n    var width = 300\n    var height = 300\n    var dataset = [3, 5, 5, 6, 15, 18]\n    \n    var svg = d3.select("div#gohere3").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n  svg.selectAll("circle")\n    .data(dataset)\n    .join("circle")\n    .attr("cx", (d,i)=> i*30)\n    .attr("cy", (d,i)=> height - (i*20))\n    .attr("r", (d,i)=> d)\n    .style("fill", "lightgrey")\n    .style("stroke", "blue")\n    .style("stroke-width", 5) // reminder, this means 3 pixels\n</script>')


# Again, the cool thing about D3.js is that we can use the data to style as well. Here is the same plot, but the stroke-width will be the value of our data set.

# In[5]:


get_ipython().run_cell_magic('html', '', '<div id="gohere4"></div>\n\n<script type="text/javascript">   \n    var width = 300\n    var height = 300\n    var dataset = [3, 5, 5, 6, 15, 18]\n    \n    const svg = d3.select("div#gohere4").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n    svg.selectAll("circle")\n        .data(dataset)\n        .join("circle")\n        .attr("cx", (d,i)=> i*30)\n        .attr("cy", (d,i)=> height - (i*20))\n        .attr("r", (d,i)=> d)\n        .style("fill", "purple")\n        .style("stroke", "black")\n        .style("stroke-width", (d,i) => i) \n</script>')


# ### Color Scales

# For the most part, this is not very helpful. One way to make this more useful is to use color based on our data, or in other words, the darker the color, the larger the value. 
# 
# To implement this, I would HIGHLY suggest visit [color-scales](https://github.com/d3/d3-scale-chromatic). As mentioned in the article, the color scales were created using Cynthia A. Brewer’s [ColorBrewer](https://colorbrewer2.org/). ColorBrewer was designed to help designers find color-blind safe and print and copier safe color palette. ColorBrewer is my (and several other programming languages) “go-to” color palette.

# For this, I will be choosing the Sequential (Single Hue) - Purple color. For these color palettes, they are expecting a value between 0 to 1, where 0 is the far-left of the color palette, the far-right is 1.

# ![purple.PNG](https://raw.githubusercontent.com/dudaspm/d3plotbook/main/purple.PNG)

# For now, to get our values between 0 and 1. I will take the largest value in our array (dataset, which is 18) and divide all of our values by this. Meaning, 3 will become 3/18, 5 will be 5/18 and so on.

# In[6]:


get_ipython().run_cell_magic('html', '', '<div id="gohere5"></div>\n\n<script type="text/javascript">   \n\n    var width = 300\n    var height = 300\n    var dataset = [3, 5, 5, 6, 15, 18]\n    var palette =  d3.interpolatePurples\n    \n    var svg = d3.select("div#gohere5").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n    svg.selectAll("circle")\n        .data(dataset)\n        .join("circle")\n        .attr("cx", (d,i)=> i*30)\n        .attr("cy", (d,i)=> height - (i*20))\n        .attr("r", (d,i)=> d)\n        .style("fill", (d,i) => palette(d/18))\n        .style("stroke", "black")\n        .style("stroke-width", 2) \n\n</script>')


# Cool! We have some color! Though, we want to setup a way for our data to fit the 0 to 1 range withOUT needing us to manaully adding the largest value. There is a way to do this using [scaling](https://github.com/d3/d3-scale). Scaling allows use to create a range of values based on our data set. There are multiple types of scaling.For continuous data, or data with numeric values (Linear, Power, Log, Identity, Time, Radial). There are types of scaling, but for now we will focus on these.

# ### Scale Linear (d3.scaleLinear)

# Let's start by creating a scaling function called between0and1. To do this we will need two things:
# * the **.domain()** which is the lowest and highest number that will be given to the function. This is usually the smallest number in our array or 3, and largest number, 18. 
# * the **.range()** is the range of values we want to map to, as in we want all numbers to be within 0 to 1. 
# 
# Our smallest number (3), will be mapped 0 and our largest number (18) mapped to 1.

# In[7]:


get_ipython().run_cell_magic('html', '', '<figure>\n<video width="480" height="240" controls muted >\n  <source src="https://github.com/dudaspm/d3plotbook/blob/main/Styles_Scales_Shapes_video.mp4?raw=true" type=video/mp4>\n</video>\n  <figcaption>(No Audio) Figure showing how are list [5,3,16,5,6,18] maps to the domain and range [0,1]</figcaption>\n</figure>')


# In[8]:


get_ipython().run_cell_magic('html', '', '<p id="printout1"></p>\n<script>\nvar dataset = [5, 3, 16, 5, 6, 18]\nvar between0and1 = d3.scaleLinear().range([0,1]).domain([3,18])\ndocument.getElementById("printout1").innerHTML = between0and1(18)\n</script>')


# Again, though, we are still manually putting these values into our boundries. That's why there are built in functions to help AUTOMAGICALLY find the lowest and highest values in an array. 
# * **d3.max()** - finds the max value in the array
# * **d3.min()** - finds the min value in the array
# * **d3.extent()** - finds both the min and max values in an array

# In[9]:


get_ipython().run_cell_magic('html', '', '<p id="printout2"></p>\n<script>\nvar dataset = [5, 3, 16, 5, 6, 18]\ndocument.getElementById("printout2").innerHTML = d3.min(dataset)\n</script>')


# In[10]:


get_ipython().run_cell_magic('html', '', '<p id="printout3"></p>\n<script>\nvar dataset = [5, 3, 16, 5, 6, 18]\ndocument.getElementById("printout3").innerHTML = d3.max(dataset)\n</script>')


# In[11]:


get_ipython().run_cell_magic('html', '', '<p id="printout4"></p>\n<script>\nvar dataset = [5, 3, 16, 5, 6, 18]\ndocument.getElementById("printout4").innerHTML = d3.extent(dataset)\n</script>')


# In[12]:


get_ipython().run_cell_magic('html', '', '<div id="gohere6"></div>\n\n<script type="text/javascript">   \n    var width = 300\n    var height = 300\n    var dataset = [5, 3, 16, 5, 6, 18]\n    var palette =  d3.interpolateInferno\n    var color = d3.scaleLinear().range([0,1]).domain(d3.extent(dataset))\n    \n    var svg = d3.select("div#gohere6").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n \n    svg.selectAll("circle")\n        .data(dataset)\n        .join("circle")\n        .attr("cx", (d,i)=> i*30)\n        .attr("cy", (d,i)=> height - (i*20))\n        .attr("r", (d,i)=> d)\n        .style("fill", "lightgrey" )\n        .style("stroke", (d,i) => palette(color(d)) )\n        .style("stroke-width", 5) \n</script>')


# <p>So, when to use d3.extent or d3.min/d3.max? This is a good example of this case. Right now, </p>
# 
# 
# ```javascript
# const color = d3.scaleLinear().range([0,1]).domain(d3.extent(dataset))
# ```
# 
# 
# <p>assumes that our lowest number, 3, is mapped to 0. Though, in some cases, we want 0 to be mapped to 0. Meaning we should use</p> 
# 
# 
# ```javascript
# const color = d3.scaleLinear().range([0,1]).domain([0,d3.max(dataset)])
# ```

# In[13]:


get_ipython().run_cell_magic('html', '', '<div id="gohere7"></div>\n\n<script type="text/javascript">   \n    var width = 300\n    var height = 300\n    var dataset = [5, 3, 16, 5, 6, 18]\n    var palette =  d3.interpolatePurples\n    var color = d3.scaleLinear().range([0,1]).domain([0,d3.max(dataset)])\n    \n    var svg = d3.select("div#gohere7").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n \n    svg.selectAll("circle")\n        .data(dataset)\n        .join("circle")\n        .attr("cx", (d,i)=> i*30)\n        .attr("cy", (d,i)=> height - (i*20))\n        .attr("r", (d,i)=> d)\n        .style("fill", (d,i) => palette(color(d)) )\n        .style("stroke", "black")\n        .style("stroke-width", 2) \n\n</script>')


# ## Shapes

# ### Rectangles

# In[14]:


get_ipython().run_cell_magic('html', '', '<div id="gohere8"></div>\n\n<script type="text/javascript">   \n    var width = 300\n    var height = 300\n    var dataset = [5, 3, 16, 5, 6, 18]\n    var palette =  d3.interpolatePurples\n    var color = d3.scaleLinear().range([0,1]).domain([0,d3.max(dataset)])\n    \n    var svg = d3.select("div#gohere8").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n \n    svg.selectAll("rect")\n    .data(dataset)\n    .join("rect")\n    .attr("x", (d,i)=> d*5)\n    .attr("y", (d,i)=> height - (i*20))\n    .attr("width", 20)\n    .attr("height", 20)\n    .style("fill", (d,i) => palette(color(d)) )\n    .style("stroke", "black")\n    .style("stroke-width", 2) \n    .style("stroke-width", 2) \n</script>')


# For rectangles, the x,y is the origin of the rectangle (again in the top-lefthand corner). Right now, we are missing a rectangle, well, not missing it, it just off the canvas. For data point 3, index 0, the x position is 15, and the y position is the height. Meaning, we need to correct this. Also, we are not using the space very well. This was true with our circles, but let's see if we can fix this issue here as well. The best way to do this is to create margins. For now, let's just set a margin of 30. 30 on the top, bottom, left, and right. We will do this using the scaleLinear function for both the x and y axis.

# In[15]:


get_ipython().run_cell_magic('html', '', '<div id="gohere9"></div>\n\n<script type="text/javascript">   \n\n    var width = 300\n    var height = 300\n    var margin = 30 // Add my margin\n    var dataset = [5, 3, 16, 5, 6, 18]\n    var palette =  d3.interpolatePurples\n    var color = d3.scaleLinear().range([0,1]).domain([0,d3.max(dataset)])\n  \n    var svg = d3.select("div#gohere9").append("svg")\n        .attr("width", width)\n        .attr("height", height)    \n    \n    // Use the margin to create an x domain and range\n    var x = d3.scaleLinear().range([margin,width-margin]).domain(d3.extent(dataset)) \n\n    // Use the margin to create an y domain and range\n    var y = d3.scaleLinear().range([height-margin,margin]).domain([0,dataset.length-1])   \n\n    svg.selectAll("rect")\n        .data(dataset)\n        .join("rect")\n        .attr("x", (d,i)=> x(d))\n        .attr("y", (d,i)=> y(i))\n        .attr("width", 20)\n        .attr("height", 20)\n        .style("fill", (d,i) => palette(color(d)) )\n        .style("stroke", "black")\n        .style("stroke-width", 2) \n\n</script>')


# ### Text

# Next, we add some text next to our boxes. For the most part, we will be using the same code as our rectangles. Let's take a look.

# In[16]:


get_ipython().run_cell_magic('html', '', '<div id="gohere10"></div>\n\n<script type="text/javascript">   \n    var width = 300\n    var height = 300\n    var margin = 30 // Add my margin\n    var dataset = [5, 3, 16, 5, 6, 18]\n    var palette =  d3.interpolatePurples\n    var color = d3.scaleLinear().range([0,1]).domain([0,d3.max(dataset)])\n  \n    var svg = d3.select("div#gohere10").append("svg")\n        .attr("width", width)\n        .attr("height", height)    \n    \n    // Use the margin to create an x domain and range\n    var x = d3.scaleLinear().range([margin,width-margin]).domain(d3.extent(dataset)) \n\n    // Use the margin to create an y domain and range\n    var y = d3.scaleLinear().range([height-margin,margin]).domain([0,dataset.length-1])   \n\n    svg.selectAll("rect")\n        .data(dataset)\n        .join("rect")\n        .attr("x", (d,i)=> x(d))\n        .attr("y", (d,i)=> y(i))\n        .attr("width", 20)\n        .attr("height", 20)\n        .style("fill", (d,i) => palette(color(d)) )\n        .style("stroke", "black")\n        .style("stroke-width", 2) \n    \n    // adding in the text \n    svg.selectAll("text")\n        .data(dataset)\n        .join("text")\n        .attr("x", (d,i)=> x(d))\n        .attr("y", (d,i)=> y(i))\n        .text((d,i) => "x: "+d+" y: "+i)\n</script>')


# Adding in the text, the only additional piece we need to add is what the .text() will be. In this case, I am again using the data to add specific data related text to the screen. If we take a particular look at this function, we can see how we used both text and data together.

# <code>.text((d,i) => <span style="color:#008ec4">"x: "</span>+<span style="color:#005f87">d</span>+<span style="color:#008ec4">" y: "</span>+<span style="color:#005f87">i</span>)</code>

# Using the "x: ", the plus sign (+), and d will combine or concatenate the two to make one string

# The last thing that needs to be adjusted is the fact that both the rectangle and the text occupy the same x,y coordinate, which means they overlap a bit. Also, the text for our last rectangle is off the canvas. So, let's adjust both of these.

# In[17]:


get_ipython().run_cell_magic('html', '', '<div id="gohere11"></div>\n\n<script type="text/javascript">   \n    var width = 300\n    var height = 300\n    var margin = 30 // Add my margin\n    var dataset = [5, 3, 16, 5, 6, 18]\n    var palette =  d3.interpolatePurples\n    var color = d3.scaleLinear().range([0,1]).domain([0,d3.max(dataset)])\n  \n    var svg = d3.select("div#gohere11").append("svg")\n        .attr("width", width)\n        .attr("height", height)    \n    \n    // Use the margin to create an x domain and range\n    var x = d3.scaleLinear().range([margin,width-margin]).domain(d3.extent(dataset)) \n\n    // Use the margin to create an y domain and range\n    var y = d3.scaleLinear().range([height-margin,margin]).domain([0,dataset.length-1])   \n\n    svg.selectAll("rect")\n        .data(dataset)\n        .join("rect")\n        .attr("x", (d,i)=> x(d))\n        .attr("y", (d,i)=> y(i))\n        .attr("width", 20)\n        .attr("height", 20)\n        .style("fill", (d,i) => palette(color(d)) )\n        .style("stroke", "black")\n        .style("stroke-width", 2) \n    \n    // adding in the text \n    svg.selectAll("text")\n        .data(dataset)\n        .join("text")\n        .attr("x", (d,i)=> x(d))\n        // moving our text up a bit (subtracting 5 pixels)\n        .attr("y", (d,i)=> y(i)-5)\n        .text((d,i) => "x: "+d+" y: "+i)\n</script>')


# ### Lines

# Next, we have lines. Lines are similar to circles, rectangles, and text. You need a starting x,y, and similar to the rectangle you need secondary dimension (width/height), whereas lines need an ending x,y position. I think there can be a misconception about lines, based on “line graphs.” Line graphs (as seen below) look like a single line but fluctuations here and there when a better way to think about lines independent of one another. Paths (talked about next) are where we will be able to think about one, continuous line.

# <table>
# <tr>
# <td>
# <img
#   src='https://raw.githubusercontent.com/dudaspm/ProjectiOn/master/D3Tutorial/Images/linechart1.PNG'
#   width="200" />
# </td>
# <td>
# <img
#   src='https://raw.githubusercontent.com/dudaspm/ProjectiOn/master/D3Tutorial/Images/linechart2.PNG'
#   width="200" />
# </td>
# </tr>
# <tr>
# <td>
# Figure 1 - </br>How you might assume the line shape would work.
# </td>
# <td>
# Figure 2 - </br>How the line shape actually works.
# </td>
# </tr>
# </table>

# In[18]:


get_ipython().run_cell_magic('html', '', '<div id="gohere12"></div>\n\n<script type="text/javascript">   \n    var width = 300\n    var height = 300\n    var margin = 30 // Add my margin\n    var dataset = [5, 3, 16, 5, 6, 18]\n    var palette =  d3.interpolatePurples\n    var color = d3.scaleLinear().range([0,1]).domain([0,d3.max(dataset)])\n  \n    var svg = d3.select("div#gohere12").append("svg")\n        .attr("width", width)\n        .attr("height", height)    \n    \n    // Use the margin to create an x domain and range\n    var x = d3.scaleLinear().range([margin,width-margin]).domain(d3.extent(dataset)) \n\n    // Use the margin to create an y domain and range\n    var y = d3.scaleLinear().range([height-margin,margin]).domain([0,dataset.length-1])   \n\n    // update this to select the lines, then join (or add) lines.\n    svg.selectAll("line")\n        .data(dataset)\n        .join("line")\n        // lines require x1,y1 (where the line starts) and x2,y2 (where the lines end)\n        .attr("x1", (d,i)=> x(d))\n        .attr("y1", (d,i)=> y(i))\n        .attr("x2", (d,i)=> x(d)+10)\n        .attr("y2", (d,i)=> y(i)+10)\n        // to change the color of the line we need to update the stroke, not the fill. \n        .style("stroke", (d,i) => palette(color(d)) )\n        .style("stroke-width", 10) \n\n</script>')


# To create a line chart from these lines would require several changes. Here is an example of how to do it, but there is a MUCH simpler way using paths, which we will talk about in a second.

# In[19]:


get_ipython().run_cell_magic('html', '', '<div id="gohere13"></div>\n\n<script type="text/javascript">   \n    var width = 300\n    var height = 300\n    var margin = 30 // Add my margin\n    var dataset = [5, 3, 16, 5, 6, 18]\n    var palette =  d3.interpolatePurples\n    var color = d3.scaleLinear().range([0,1]).domain([0,d3.max(dataset)])\n  \n    var svg = d3.select("div#gohere13").append("svg")\n        .attr("width", width)\n        .attr("height", height)    \n    \n    // Use the margin to create an x domain and range\n    var x = d3.scaleLinear().range([margin,width-margin]).domain(d3.extent(dataset)) \n\n    // Use the margin to create an y domain and range\n    var y = d3.scaleLinear().range([height-margin,margin]).domain([0,dataset.length-1])   \n\n    // update this to select the lines, then join (or add) lines.\n    svg.selectAll("line")\n        .data(dataset.slice(0, -1))\n        .join("line")\n        .attr("x1", (d,i)=> x(d))\n        .attr("y1", (d,i)=> y(i))\n        // we then need to end our line with the next data point.\n        // that\'s why we use (i+1) and why we cutoff the last position in our array\n        .attr("x2", (d,i)=> x(dataset[i+1]))\n        .attr("y2", (d,i)=> y(i+1))\n        .style("stroke", "black" ) // changing this back, as not all the data points (and colors) will be represented\n        .style("stroke-width", 10) \n</script>')


# As you can see, this is not the most elegant way to handle creating a line.

# ### Paths

# Finally, we have paths. Up to this point, we have been focusing on the idea "for each data point, we create a shape or object." Paths require multiple data points to create the shape/object. We can use a function to create our line. We can either do this in a new (separate) cell or in with the code itself. Let's build it in our design. 

# In[20]:


get_ipython().run_cell_magic('html', '', '<div id="gohere14"></div>\n\n<script type="text/javascript">   \n    var width = 300\n    var height = 300\n    var margin = 30 // Add my margin\n    var dataset = [5, 3, 16, 5, 6, 18]\n    var palette =  d3.interpolatePurples\n    var color = d3.scaleLinear().range([0,1]).domain([0,d3.max(dataset)])\n  \n    var svg = d3.select("div#gohere14").append("svg")\n        .attr("width", width)\n        .attr("height", height)    \n    \n    // Use the margin to create an x domain and range\n    var x = d3.scaleLinear().range([margin,width-margin]).domain(d3.extent(dataset)) \n\n    // Use the margin to create an y domain and range\n    var y = d3.scaleLinear().range([height-margin,margin]).domain([0,dataset.length-1])   \n\n    // this is our function to create the line, where the x is based on the d(ata) and the y on the i(ndex)\n    var line = d3.line()\n        .x((d,i)=> x(d)) \n        .y((d,i)=> y(i)) \n\n    svg.selectAll("path")\n        .data([dataset])\n        .join("path")\n        .attr("d", line)\n        .style("stroke", "black" )\n        .style("stroke-width", 10) \n        .style("fill", "none") // SPECIAL NOTE HERE: we set the fill to "none" because a path will have a fill color\n\n</script>')


# In[ ]:




