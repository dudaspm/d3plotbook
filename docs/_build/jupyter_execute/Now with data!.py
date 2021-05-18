#!/usr/bin/env python
# coding: utf-8

# # Now with data!

# Now that we know how to make a basic graph, we should focus on what makes D3 so special: its ability to connect data to visualizations. D3 actually stands for Data Driven Documents, meaning that data should inform the visual artifact or the document.
# 
# [ObservableHQ version](https://observablehq.com/@dudaspm/learning-d3-js-part-2?collection=@dudaspm/d3-in-observablehq)

# ### Introduction to Arrays

# In[1]:


get_ipython().run_cell_magic('javascript', '', 'var groceryList = []')


# Note, what we did was create a variable or a named piece of code. Something that can vary (hence its name, variable). Variables must be one continous string of letters/numbers. So, instead of **grocery list**, I called it **groceryList**. Why the capitalization? because it makes it easier to separate out the words in the name. As in, **grocerylist** vs. **groceryList**. We have a fun name for this: camel case. <img src="https://upload.wikimedia.org/wikipedia/commons/c/c8/CamelCase_new.svg" alt="camel case" width="100"/>

# <cite>File:CamelCase new.svg. (2020, April 15). Wikimedia Commons, the free media repository. Retrieved 15:25, June 3, 2020 from https://commons.wikimedia.org/w/index.php?title=File:CamelCase_new.svg&oldid=411544943.</cite>

# Now to add to our array, we need to **push** some data into it. What, thats not how you usually put things in other things? By pushing it? OK, the naming is a bit weird, but we need to push data into our groceryList.

# In[2]:


get_ipython().run_cell_magic('javascript', '', 'var groceryList = []\ngroceryList.push("apples")\ngroceryList.push("bananas")\ngroceryList.push("coffee")\nelement.text(groceryList)')


# ### Referencing parts of our array.

# With our lists, we can access the data we put into them by using a numeric reference. Like saying, this is first on the list, second on the list, and so on. Unfortunately, this is where it gets a little weird. Where we expect to see that ordering would be 1, 2, 3, etc. it actually starts at 0. So, it's 0, 1, 2, etc...
# 
# So, to access let's say "banana". We would use position 1 or index 1 to access this element. Here is our array written out:
# 

# <img src="https://raw.githubusercontent.com/dudaspm/ProjectiOn/master/D3Tutorial/Images/array1.PNG" alt="an easel" width="200"/>

# In[3]:


get_ipython().run_cell_magic('javascript', '', 'var groceryList = ["apples","bananas","coffee"]\nelement.text(groceryList[1])')


# I want to access "apple".

# In[4]:


get_ipython().run_cell_magic('javascript', '', 'var groceryList = ["apples","bananas","coffee"]\nelement.text(groceryList[0])')


# Another way to create an array is just to list out the items or elements in array. 
# 
# Here is an example:

# In[5]:


get_ipython().run_cell_magic('javascript', '', 'const listOfThings = ["item1", 42, 3.14, ["pb","j"]]\nelement.text(listOfThings[0])')


# In[6]:


get_ipython().run_cell_magic('javascript', '', 'const listOfThings = ["item1", 42, 3.14, ["pb","j"]]\nelement.text(listOfThings[2])')


# In[7]:


get_ipython().run_cell_magic('javascript', '', 'const listOfThings = ["item1", 42, 3.14, ["pb","j"]]\nelement.text(listOfThings[3])')


# ### Arrays to Artwork

# For our array to artwork, we will be working with some data. For this I will be using some integer (or whole numbers).

# In[8]:


get_ipython().run_cell_magic('javascript', '', 'const drawingCircles = [3, 5, 5, 6, 15, 18]\nvar table = ""\ntable+="<table style=\'width:100px;\'>"\ntable+="<tr><td>index</td><td>element</td></tr>"\ndrawingCircles.forEach((d,i)=> table+="<tr><td>"+i+"</td><td>"+d+"</td></tr>")\ntable+="</table>"  \nelement.append(table)')


# Let's copy and paste our code from our previous notebook for creating a circle

# In[9]:


from IPython.display import HTML, Javascript, display

def configure_d3():
    display(Javascript("""
    require.config({
      paths: {
        d3: "https://d3js.org/d3.v6.min"
      }
    })"""))


configure_d3()


# #### Enabling D3 in Google Colab
# 
# ```javascript
# from IPython.display import  HTML
# 
# def load_d3_in_cell_output():
#   display(HTML("<script src='https://d3js.org/d3.v6.min.js'></script>"))
# get_ipython().events.register('pre_run_cell', load_d3_in_cell_output)
# ```

# NOTE: Do use this code in Google Colab, you have to remove the 
# 
# ```javascript 
# require(['d3'], function (d3) {}) 
# ```

# ### In Jupyter

# In[10]:


get_ipython().run_cell_magic('html', '', '<div id="gohere1"></div>\n\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    const width = 600\n    const height = 400\n    \n    const svg = d3.select("div#gohere1").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n    svg.append("circle")\n        .attr("cx", 160)\n        .attr("cy", 280)\n        .attr("r", 80)\n});\n</script>')


# ### In Google Colab
# 
# ```html
# %%html
# <div id="gohere1"></div>
# 
# <script type="text/javascript">   
#     const width = 600
#     const height = 400
#     
#     const svg = d3.select("div#gohere1").append("svg")
#         .attr("width", width)
#         .attr("height", height)
#     
#     svg.append("circle")
#         .attr("cx", 160)
#         .attr("cy", 280)
#         .attr("r", 80)
# </script>
# ```

# Now we need to add our data to our artwork, which will allow us to create 6 circles from our 6 data points.

# There are 3 things we need to add to our code to connect the data to the shapes.
# 1. **.selectAll("circle")** - This is probably one of the most confusing parts of D3.js. I have spent many hours trying to figure how best to describe what is going on here. The basic concept is this; because we want to create circles based on our data, logically, we need to know how many circles do we originally have on our canvas and then compare this to our data. The best analogy I can come up with is imagine cooking with a friend and having that friend ask you to put 6 cloves of garlic into the bowl. A pretty standard question you might ask is "how many did you add already?" Because you don't want to add more than what is neccessary. This is what is going on here, you want to add 6 circles, so you need to ask, "how many do I have so far?"
# 
# 2. **.data(drawingCircles)** - This is where we add the data. The function, or the way we bring in the data, is called **.data()** and our data is called **drawingCircles**. **REALLY IMPORTANT** that the data you bring in *has to be* an array. Hence why we spent all that time talking and learning about arrays 😃
# 
# 3. **.join("circle")** - This last step tells d3.js what you want to add to our canvas. In this case, we want to add a circle. In our next notebook, we will discuss the other types we can use in D3.js.

# To simplify these steps, let's create a 3 piece set of actions:
# 1. Observe (the original scene) - **.selectAll()**
# 2. Collect (the data we need to update) - **.data()**
# 3. Update (the shape with this data) - **.join()**

# In[11]:


get_ipython().run_cell_magic('html', '', '<div id="gohere2"></div>\n\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    const drawingCircles = [3, 5, 5, 6, 15, 18]\n    const width = 600\n    const height = 400\n    \n    const svg = d3.select("div#gohere2").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n    // Observe\n    svg.selectAll("circle")\n    // Collect\n        .data(drawingCircles)\n    // Update\n        .join("circle")\n        .attr("cx", 160)\n        .attr("cy", 280)\n        .attr("r", 80)\n});\n</script>')


# We did it! We made 6 circles! You might be wondering why you only see 1 circle here. Well, logically, if you draw 6 circles all on top of each other of the same radius. This is what you would see. 
# 
# Let's try using the data to make the circles unique.
# 
# To do this, we need to change the way we use the **.attr()**. Specifically, use these in conjunction with our data to make unique circles based on our data. Here is an example:
# 
# * .attr("r", 80) becomes .attr("r", (d,i) => d) this is called [arrow function expression](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions) or using an arrow to indicate a function or action taking place. You may notice that we are "shooting" two things -- the letter *d* and *i*. The *d* references the d(ata) and the *i* the i(ndex). So, if we want to change the radius based on the data, we would use the d value and if you wanted to use the index, you would use the i.
# 
# Let's change the radius based on the d(ata) and the cx value based on the i(ndex).

# Also, let's show this using two different methods.
# 
# 1. using a tradition JavaScript function
# 
# 2. using an arrow function 

# #### Traditional JavaScript function

# In[12]:


get_ipython().run_cell_magic('html', '', '<div id="traditional"></div>\n\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    const drawingCircles = [3, 5, 5, 6, 15, 18]\n    const width = 600\n    const height = 200\n    \n    const svg = d3.select("div#traditional").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n    // Observe\n    svg.selectAll("circle")\n          // Collect\n        .data(drawingCircles)\n          // Update\n        .join("circle")\n        .attr("cx", \n          function(d,i) {\n            return i*20\n          }\n        )\n        .attr("cy", 100)\n        .attr("r",\n          function(d,i) {\n            return d\n          }\n        )\n});\n</script>')


# #### Arrow JavaScript function

# In[13]:


get_ipython().run_cell_magic('html', '', '<div id="arrow"></div>\n\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    const drawingCircles = [3, 5, 5, 6, 15, 18]\n    const width = 600\n    const height = 400\n    \n    const svg = d3.select("div#arrow").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n    // Observe\n    svg.selectAll("circle")\n          // Collect\n        .data(drawingCircles)\n         // Update\n        .join("circle")\n        .attr("cx", (d,i) => i*20)\n        .attr("cy", 280)\n        .attr("r", (d,i) => d)\n});\n</script>')


# As you can see, I used the i(ndex) and multiplied it by 20 to help create more spacing. This shows you the power of D3.js, the data is dictating the drawing (maybe they should use this for D3 acronym instead 😆).
# 
# Knowing this, let's making a drawing that looks like a plot of points with a positive slope (meaning the points are heading up as you move left to right.

# In[14]:


get_ipython().run_cell_magic('html', '', '<div id="gohere3"></div>\n\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    const drawingCircles = [3, 5, 5, 6, 15, 18]\n    const width = 600\n    const height = 400\n    \n    const svg = d3.select("div#gohere3").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n    // Observe\n    svg.selectAll("circle")\n    // Collect\n        .data(drawingCircles)\n    // Update\n        .join("circle")\n        .attr("cx", (d,i) => i*30)\n        .attr("cy", (d,i) => i*20)\n        .attr("r", (d,i) => d)\n});\n</script>')


# So, in this example, the points are heading down the hill. Remember from before, the (0,0) position is in the top-left, not the bottom-left. With this in mind, we can use the **height** to draw these.

# In[15]:


get_ipython().run_cell_magic('html', '', '<div id="gohere4"></div>\n\n<script type="text/javascript">   \nrequire([\'d3\'], function (d3) {\n    const drawingCircles = [3, 5, 5, 6, 15, 18]\n    const width = 600\n    const height = 400\n    \n    const svg = d3.select("div#gohere4").append("svg")\n        .attr("width", width)\n        .attr("height", height)\n    \n    // Observe\n    svg.selectAll("circle")\n    // Collect\n        .data(drawingCircles)\n    // Update\n        .join("circle")\n        .attr("cx", (d,i) => i*30)\n        .attr("cy", (d,i) => height - (i*20))\n        .attr("r", (d,i) => d)\n    \n    \n});\n</script>')


# Your turn: Create a new array with random numbers in it (how many and the order does not matter). Then create circles with that array.

# In[ ]:




