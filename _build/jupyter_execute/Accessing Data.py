#!/usr/bin/env python
# coding: utf-8

# # Accessing Data

# In this notebook, we discuss how to access datasets within D3.js. There are two ways to accomplish this in our Jupyter Lab environment. 
# 
# ## d3-fetch
# The most straightforward way is to use [d3-fetch](https://github.com/d3/d3-fetch). 
# 
# **JavaScript**
# ```javascript
# d3.csv("/path/to/file.csv").then((data) => { })
# ```
# 
# ## Python (Pandas) + d3-fetch
# The second way include d3-fetch, but processing the data first in python, saving the file, and then using d3.fetch. Typically, I will use a library called Pandas to do this, as it similar features to d3.js. 
# 
# **Python**
# ```python
# import pandas as pd
# data=pd.read_csv("/path/to/file.csv")
# data.to_csv('newFile.csv', index = False, header=True)
# ```
# **JavaScript**
# ```javascript
# d3.csv("/path/to/newFile.csv").then((data) => { })
# ```
# 
# ### Pros/Cons of Both
# There is little difference between the two, obviously you are adding another step with Python, but you get the added benefit of being able to use all of Python's tools before working with the file. Not to say D3.js does not have these similar capabilities. If anything, I (my preference) think D3.js are a bit better and easier to use, but this not the case for everyone. Let's showcase both. 

# ## Start D3.jsfrom IPython.display import  HTML
# 
# 

# In[1]:


from IPython.display import  HTML

def load_d3_in_cell_output():
  display(HTML("<script src='https://d3js.org/d3.v6.min.js'></script>"))
get_ipython().events.register('pre_run_cell', load_d3_in_cell_output)


# ## Acknowledgement for Data
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

# ## d3-fetch Implementation

# The data we will be using for this exercise is acknowledged above, but the basic idea is this is a weather data for the State College, PA area (near Penn State University). 
# 
# The data preview is:
# * DATE - date in YYYY-MM-DD format
# * DAY - the day (_D format)
# * MONTH - the month (_M format)
# * YEAR - the year (YYYY format)
# * PRCP - the amount of precipitation in inches
# * SNOW - the amount of snow in inches
# * TMAX - the max temperature in F°
# * TMIN - the min temperature in F°
# 
# Here's a print out of the first row of data:

# In[2]:


get_ipython().run_cell_magic('html', '', '<p id="print1"></p>\n<script>\n    d3.csv("https://gist.githubusercontent.com/dudaspm/13174849c09aba7a0716d5fa230ebe95/raw/a4866834185bad7e4a1e1b8f90da76b168eb1361/StateCollege2010-2020_min.csv")\n    .then((data) => \n        document.getElementById("print1").innerHTML = JSON.stringify(data[0])    \n    )\n</script>')


# One thing you can add to this (💥💥AND I STRONGLY RECOMMEND DOING THIS💥💥) is adding 
# ```javascript
# .catch((error) => console.log(error) )
# ```
# 
# Why? because Jupyter does a not so great job of showcasing errors. As much we try and teach ourselves to be perfect coders 🙄. We all make mistakes and too be honest, as much as I love D3.js. One small thing can cause problems. If you have not looked at the troubleshooting section of the notebook, please check it out. It will save you hours of your life in small errors. 

# In[3]:


get_ipython().run_cell_magic('html', '', '<p id="print2"></p>\n<script>\n    d3.csv("https://raw.githubusercontent.com/dudaspm/d3plotbook/main/weather.csv")\n    .then((data) => \n        document.getElementById("print2").innerHTML = JSON.stringify(data[0])    \n    )\n    .catch((error) => console.log(error) )\n</script>')


# ## Python + Pandas + d3-fetch Implementation

# Now this implementation adds an extra step but again, if you want to do more in Python and make the data available to D3.js afterwards. This is where you want to be! 
# 
# Let's do the same steps as above, but this time we will add Pandas. 

# ```{note}
# For those using this notebook in Google Colabs, Pandas is already installed.
# But, for those running this locally or on another system. You may need to install pandas first. 
# You can actually do this in the notebook. Create a new cell (after this one) and run the following:
# 
# *!pip install pandas*
# 
# Here, I'll help with this. The next cell will have this, but it will commented out. Just remove the #.
# 
# ```

# In[4]:


#!pip install pandas


# We need to break this up into three steps. This will allow Jupyter Lab to keep this variable within the notebook and use it internally (instead of writing to file). 
# 
# Also, and most importantly, this works in Google Colab. 
# 
# ### Using Python + Pandas

# Suprisingly, this is much harder than it needs to be. Specifically because I am trying to design this for Jupyter Lab and (the culprit 😈) Google Colab. Google Colab is a fantastic implementation of Jupyter Lab but it has to be locked down a bit more because well, people could do some really bad things if they didn't. So, after months (and I mean months) of searching and trying things, this is my best implementation. 
# 
# Side note, if by chance you figure out a better solution, please let me know! It would make my day 😄
# 
# #### Starting Pandas and Getting the File
# 
# The first step is enabling Pandas in Jupyter Lab and in Python we use import statements for this. Think about imports as extra libraries built using Python to increase what they can do. In this case, [Pandas](https://pandas.pydata.org/) is a great, as they specify, "a fast, powerful, flexible and easy to use open source data analysis and manipulation tool {cite}`reback2020pandas,mckinney-proc-scipy-2010`."

# ```{note}
# When using an external library, like Pandas, we can rename the library (as in this case, pandas to pd). This is a common way to see Pandas being used. This means when I want to use something from this library, I will use pd instead of pandas. 
# ```

# In[5]:


import pandas as pd
data=pd.read_csv("https://raw.githubusercontent.com/dudaspm/d3plotbook/main/weather.csv")


# Obviously, because this is csv, we use 
# ```python
# pd.read_csv
# ```
# Here is a listing of all of Pandas I/Os (input/outputs): https://pandas.pydata.org/docs/reference/io.html

# In[6]:


get_ipython().run_cell_magic('html', '', '<p id="print3"></p>\n<script>\nvar receiver = new BroadcastChannel(\'channel\');\nreceiver.onmessage = (msg) => {\n    var data = d3.csvParse(msg.data.replaceAll(";;;","\\n"))\n    document.getElementById("print3").innerHTML = JSON.stringify(data[0])    \n};\n</script>')


# In[7]:


from IPython.display import display, HTML
d = data.head().to_csv(index=False,line_terminator='\n').replace('\n',';;;')[:-3]
js = """
<script>
var sender = new BroadcastChannel('channel');
var message = '{}'
senderChannel.postMessage(message);
</script>""".format(d)


display(HTML(js))


# 

# In[ ]:




