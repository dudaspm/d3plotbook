#!/usr/bin/env python
# coding: utf-8

# # Getting Started

# ## From the Top!

# ### Why am I here?

# You are here to learn about D3.js, which is a data visualization library, and how to use D3.js in Jupyter. The skills learned in here can easily be translated outside of Jupyter, but this is the simplist way to get started with D3.js.

# If you are interested in how to do this for observablehq.com, here is a link to that discussion: https://observablehq.com/@dudaspm/learning-d3-part-1?collection=@dudaspm/d3-in-observablehq

# ### Who should be here?

# This is meant to be an introduction to D3 (and a little bit of introduction to Jupyter). I am focused on helping people who have little to no programming experence. I may use a technical term here and there, but my goal is to create analogies whenever I can and include some technical terms to make searching for more details accessible.

# ### Who am I?

# I am teacher and D3 user for about 10 years, back when we used to call it [Protovis](http://vis.stanford.edu/papers/protovis). Even before that I was using SVG, XSLT, XPath, and XML to make interactive graphs (note, don't worry about looking these up, this type of development is REALLY old and outdated). 
# 
# I am very passionate about helping people increase their visual literacy, or simply, using data to tell better visual stories.

# ## Let's start

# ### Our easel

# <img src="https://upload.wikimedia.org/wikipedia/commons/a/ae/Tripod_easel.jpg" alt="an easel" width="200"/>

# <cite>File:Tripod easel.jpg. (2019, January 24). Wikimedia Commons, the free media repository. Retrieved 14:27, June 1, 2020 from https://commons.wikimedia.org/w/index.php?title=File:Tripod_easel.jpg&oldid=336282573.</cite>

# When you want to create artwork, you need something to draw on. For this anology, I will be calling this the easel.

# ### Our paint

# <img src="https://upload.wikimedia.org/wikipedia/commons/0/04/Oil_painting_palette.jpg" alt="a palette" width="200"/>

# <cite>File:Oil painting palette.jpg. (2017, September 27). Wikimedia Commons, the free media repository. Retrieved 14:30, June 1, 2020 from https://commons.wikimedia.org/w/index.php?title=File:Oil_painting_palette.jpg&oldid=260097528.</cite>

# Now before you get our easel ready, we need to pick a type of paint or art medium (water colors, markers, finger paints). Well in this analogy we are choosing D3 as our art medium. So, let's start by declaring, in our notebook, that we will be using D3.

# I DECLARE I WANT TO USE D3!

# No, no...close... but we need to do this in a way that tells the notebook you want to use the D3.js. 

# ### (Required First Step) Enabling D3 in Jupyter Lab/Google Colab

# In[16]:


from IPython.display import  HTML

def load_d3_in_cell_output():
  display(HTML("<script src='https://d3js.org/d3.v6.min.js'></script>"))

get_ipython().events.register('pre_run_cell', load_d3_in_cell_output)


# The example below should output a blue circle. If so, everything is working properly! If not, please make sure to run the "Required First Step."

# ### Both Colab and Jupyter Lab will be able to run the following example

# In[17]:


get_ipython().run_cell_magic('html', '', '<div id="example1"></div>\n\n<script type="text/javascript">   \n    var width = 300\n    var height = 100\n    \n    var svg = d3.select("div#example1").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n\n    var circle = svg.append("circle")\n        .attr("cx", 150)\n        .attr("cy", 50)\n        .attr("r", 20)\n        .style("fill", "blue")\n        .style("stroke", "black")\n\n</script>')


# ### Our canvas

# <cite>File:Splined Canvas.jpg. (2015, October 11). Wikimedia Commons, the free media repository. Retrieved 14:38, June 1, 2020 from https://commons.wikimedia.org/w/index.php?title=File:Splined_Canvas.jpg&oldid=175318221.</cite>

# The next analogy we need to consider is the canvas for our art work. I need to be a bit careful here, if you have a bit of visualization background, especially online. You may have heard of a programming langauge called Canvas. This is not that Canvas. For the sake of simplicity, I will be using the lower case "canvas" to reference the supporting medium for our D3.js art.

# Let's start talking about what is needed to create the canvas. We basically need to know two things: 
# 
# * Height of the canvas
# * Width of the canvas
# 
# In the image below, I am assuming the width of canvas will be 600 (600 pixels) and height will be 400 (400 pixels).

# <img  src='https://raw.githubusercontent.com/dudaspm/ProjectiOn/master/D3Tutorial/Images/intro_2.PNG'  width="300" />

# In[18]:


get_ipython().run_cell_magic('html', '', '<div id="example2"></div>\n\n<script type="text/javascript">   \n    var width = 600\n    var height = 400\n    \n    var svg = d3.select("div#example2").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n\n</script>')


# Let's walk through this...
# 
# Variable types, as the name suggests, are the types of variables you can have in Javascript. For now, we will use one type: var or var(iable). This means the variable will available throughout our code. 
# 
# Variables we will need:
# * Well the first two are pretty straight forward, we need our canvas to have a width and height. So...
#   * var width = 600
#     * or in human words... our variable called "width" will be 600.
#   * var height = 400 
#     * or in human words... our variable called "height" will be 400.
# * and this one is bit more difficult, but we need to our canvas to be these values
#   * var svg = d3.select("div#example2").append("svg").attr("width", width).attr("height", height)
#     * we're going to talk more about d3.select and d3.selectAll later, but for now you can assume that we are selecting the given cell (our easel) that we are in and adding our canvas of width (600) and height (400) to it`

# TA DA! You did! You made your first "canvas" in the art of D3.js!

# ### Our shapes

# There are number of shapes we can add to our canvas, but for now we will focus on one of those shapes. Here is a listed of the available [shape types](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Basic_Shapes).

# Our first shape we will add is a circle. A circle requires 3 things: its x position (cx), its y position (cy), and a radius (r). Here is an example mock-up for a circle at position (160, 280) and radius 80.

# <img
#   src='https://raw.githubusercontent.com/dudaspm/ProjectiOn/master/D3Tutorial/Images/circle_1.PNG'
#   width="300" />

# To do this, we take our canvas and *append*, well, a circle. Considering a circle needs a cx, cy, and r, we will add those as attr(ibutes). Which gets us...

# In[19]:


get_ipython().run_cell_magic('html', '', '<div id="example3"></div>\n\n<script type="text/javascript">   \n    var width = 600\n    var height = 400\n    \n    var svg = d3.select("div#example3").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n    svg.append("circle")\n        .attr("cx", 160)\n        .attr("cy", 280)\n        .attr("r", 80)\n</script>')


# I want to point out something that may look confusing. Some may notice that circle appears to be lower than expected. That is because in HTML (the structure of webpages), the 0,0 point is in the top left (figure 2 below) and not the bottom left (figure 1 below). Just something to be mindful of moving forward.

# <table>
# <tr>
# <td>
# <img
#   src='https://raw.githubusercontent.com/dudaspm/ProjectiOn/master/D3Tutorial/Images/corner_1.PNG'
#   width="200" />
# </td>
# <td>
# <img
#   src='https://raw.githubusercontent.com/dudaspm/ProjectiOn/master/D3Tutorial/Images/corner_2.PNG'
#   width="200" />
# </td>
# </tr>
# <tr>
# <td>
# Figure 1 - </br>How most assume an X,Y coordinate would look.
# </td>
# <td>
# Figure 2 - </br>How it is done in HTML and thus, D3.js
# </td>
# </tr>
# </table>

# To create the actual graph from above, we need to take advantage of the height variable to do so. 

# In[20]:


get_ipython().run_cell_magic('html', '', '<div id="example4"></div>\n\n<script type="text/javascript">   \n    var width = 600\n    var height = 400\n    \n    var svg = d3.select("div#example4").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n    svg.append("circle")\n        .attr("cx", 160)\n        .attr("cy", height - 280)\n        .attr("r", 80)\n\n</script>')


# There we go!

# Your turn: Create a new easel and canvas. On the canvas, add 3 circles to your canvas at different places and of different sizes.

# In[21]:


get_ipython().run_cell_magic('html', '', '<div id="example5"></div>\n\n<script type="text/javascript">   \n    var width = 600\n    var height = 400\n    \n    var svg = d3.select("div#example5").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n    // YOUR CODE HERE //\n\n</script>')


# Your turn: Create a new easel and canvas. On the canvas, add a rectangle to your canvas at different places and of different sizes.
# 
# To help, here is an SVG Rectangle
# ```html
# <svg width="600" height="400">
#   <rect x="10" y="10" width="30" height="30" />
# </svg>
# ```

# In[22]:


get_ipython().run_cell_magic('html', '', '<div id="example6"></div>\n\n<script type="text/javascript">   \n    var width = 600\n    var height = 400\n    \n    var svg = d3.select("div#example6").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n    // YOUR CODE HERE //\n\n</script>')

