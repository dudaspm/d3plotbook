#!/usr/bin/env python
# coding: utf-8

# # Troubleshooting D3.js Issues

# ## Preface
# 
# I have run into 1000s of issues during my development time with D3.js. This page will be a growing document to express the more common problems and basics of debugging. 

# ## Debugging
# 
# I will provide a perspective from Chrome, but these ideas will also carry through other browsers. 

# ### What is a debugger? 
# 
# There are much better places to learn more about debuggers, but you use them to debug your code at a high level. To be honest, it is mostly used to see errors or warnings (usually, errors). Especially when you expect to see something and that something does not show up. 

# When you have Chrome (or another browser open), and you create your code and...! Nothing happens. Your first stop should be to find the Developer Tools. 
# 
# ```{image} https://raw.githubusercontent.com/dudaspm/ProjectiOn/master/D3Tutorial/Images/debugger1.png
# :alt: Finding the Developer Tools
# :class: debugging
# :width: 500px
# :align: center
# ```
# <br>

# ```{note}
# You can also use the short-cut:
# * Chrome:
#     * Shift + ⌘ + I (on macOS) or Ctrl + Shift + I (on Windows/Linux)
# * Firefox:
#     * Shift + ⌘ + I (on macOS) or Shift + CTRL + I (on Windows/Linux)
# 
# ```

# #### What is this Screen?
# 
# ```{image} https://raw.githubusercontent.com/dudaspm/ProjectiOn/master/D3Tutorial/Images/debugger2.png
# :alt: Finding the Developer Tools
# :class: debugging
# :width: 800px
# :align: center
# ```
# <br>

# There is a lot to unpack in this screen, but we will focus on the Console for our conversation. I would highly recommend learning more about what is available in the Developer Tools, but this is a bit too much for our discussion today. Please, see [Chrome Developer Tools](https://developer.chrome.com/docs/devtools/javascript/) for more information. 

# For now, we will stick with only the debugger located in the Console (highlighted below).
# 
# ```{image} https://raw.githubusercontent.com/dudaspm/ProjectiOn/master/D3Tutorial/Images/debugger3.png
# :alt: Finding the Developer Tools (Console highlighted)
# :class: debugging
# :width: 800px
# :align: center
# ```
# <br>

# In the console, we will see errors pop up when running code. Let's see an example.
# 
# #### Example Error and Developer Tool 

# In[1]:


get_ipython().run_cell_magic('html', '', '<script type="module">\n    \n    someVariable + 2 \n    \n</script>')


# &#8593; Code will not run &#8593;

# Let's take a look at the Console.
# 
# ```{image} https://raw.githubusercontent.com/dudaspm/ProjectiOn/master/D3Tutorial/Images/debugger4.png
# :alt: Finding the Developer Tools (Console highlighted)
# :class: debugging
# :width: 800px
# :align: center
# ```
# <br>
# 
# The error will specify two critical things:
# * What the error is (good for Google Searching)
#     * In this case, "Uncaught ReferenceError: someVariable is not defined."
# * Where the error occurred
#     * In this case, line 3. 
#     
# Now, you may ask yourself, isn't 
# 
# ```javascript
# someVariable + 2 
# ``` 
# 
# on line 3? You would be correct, but our first line tells Jupyter to run HTML code. So, start counting after
# ```python
# %%html

# ### Console Logs
# 
# The next big thing related to the Console or the Debugging Tools, is the ability 

# ## Your Turn

# Create a new cell and run the following code. Then use the Console to see the error and resolve it. 
# 
# ```python
# %%html
# <script type="module">
#     
#     var someVariable = 2 
#     someVariable = someVariable * 2
#     someVariable = somevariable - 1
#     console.log(someVariable)
#     
# </script>
# ```

# In[ ]:




