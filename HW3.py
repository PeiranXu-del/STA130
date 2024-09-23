#!/usr/bin/env python
# coding: utf-8

# 1. Use fig.add[h/v]line()_ and fig.add[h/v]rect()_ to mark, respspectively, location (mean and median) and scale (range, interquartile range, and a range defined by two standard deviations away from the mean in both directions) of flipper_length_mm for each species onto plotly histograms of flipper_length_mm for each species in the penguins dataset

# In[1]:


import pandas as pd
import plotly.express as px
import seaborn as sns
penguins = sns.load_dataset('penguins')

for species in penguins['species'].unique():
    df = penguins[penguins['species'] == species]
    fig = px.histogram(df, x='flipper_length_mm', nbins=30, title=f'{species} Flipper Lengths')
    
    mean_val = df['flipper_length_mm'].mean()
    median_val = df['flipper_length_mm'].median()
    
    q1 = df['flipper_length_mm'].quantile(0.25)
    q3 = df['flipper_length_mm'].quantile(0.75)
    iqr = q3 - q1

    std_dev = df['flipper_length_mm'].std()
    mean_plus_2std = mean_val + 2 * std_dev
    mean_minus_2std = mean_val - 2 * std_dev
    
    fig.add_vline(x=mean_val, line_dash="dash", line_color="blue", annotation_text="mean")
    fig.add_vline(x=median_val, line_dash="dash", line_color="green", annotation_text="median")
    
    fig.add_vrect(x0=q1, x1=q3, fillcolor="blue", opacity=0.2, line_width=0)
    
    fig.add_vrect(x0=mean_minus_2std, x1=mean_plus_2std, fillcolor="red", opacity=0.2, line_width=0)
    
    
    fig.show()


# 2. Transition your ChatBot session from the previous problem to repeat the previous problem, but this time using seaborn kernel density estimation (KDE) plots to produce the desired figures organized in row of three plots

# In[2]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from seaborn import load_dataset
import numpy as np
# Load the penguins dataset
df = load_dataset('penguins')

# Drop rows with missing values in flipper_length_mm column
df = df.dropna(subset=['flipper_length_mm'])
species_list = df['species'].unique()

fig = make_subplots(rows=len(species_list), cols=1, subplot_titles=species_list)

for i, species in enumerate(species_list):
    species_df = df[df['species'] == species]
    
    # Calculate statistics
    mean_val = species_df['flipper_length_mm'].mean()
    median_val = species_df['flipper_length_mm'].median()
    std_val = species_df['flipper_length_mm'].std()
    min_val = species_df['flipper_length_mm'].min()
    max_val = species_df['flipper_length_mm'].max()
    q1 = species_df['flipper_length_mm'].quantile(0.25)
    q3 = species_df['flipper_length_mm'].quantile(0.75)
    
    # Create histogram for species
    hist = px.histogram(species_df, x='flipper_length_mm', nbins=30, title=species)
    
    # Add mean and median lines
    fig.add_vline(x=mean_val, line=dict(color="blue", dash="dash"), row=i+1, col=1)
    fig.add_vline(x=median_val, line=dict(color="green", dash="dash"), row=i+1, col=1)
    
    # Add range (min to max)
    fig.add_vrect(x0=min_val, x1=max_val, fillcolor="lightgrey", opacity=0.3, row=i+1, col=1)
    
    # Add IQR (Q1 to Q3)
    fig.add_vrect(x0=q1, x1=q3, fillcolor="orange", opacity=0.4, row=i+1, col=1)
    
    # Add 2 standard deviation range
    fig.add_vrect(x0=mean_val - 2*std_val, x1=mean_val + 2*std_val, fillcolor="red", opacity=0.2, row=i+1, col=1)
    
    fig.add_trace(hist.data[0], row=i+1, col=1)

# Update layout
fig.update_layout(height=600 * len(species_list), width=900, showlegend=False)
fig.show()


# 3. Search online for some images of box plots, histograms, and kernel density estimators (perhaps for the same data set); describe to a ChatBot what you think the contrasting descriptions of these three "data distribution" visualization methods are; and then see if the ChatBot agrees and what "pros and cons" list of these three "data distribution" visualization methods your ChatBot can come up with; finally, describe your preference for one or the other and your rationale for this preference

# Boxplot:
# 
# Boxplot shows the distribution of data, with special emphasis on five numbers: minimum, first quartile (Q1), median (Q2), third quartile (Q3), and maximum. It can also help identify outliers. Through boxplots, we can intuitively see the distribution range of data, central tendency, and whether there is data deviation.
# Histogram:
# 
# Histogram divides data into multiple intervals (or bins) to show the frequency or quantity of data in each interval. This method can well show the distribution shape and concentration area of ​​data, and control the display details by adjusting the interval size.
# Kernel Density Estimation (KDE):
# 
# KDE is a smoothed histogram that assigns a probability density to each data point through a kernel function to show the probability density curve of continuous data. It is smoother than a histogram and has no clear "column interval", so it is more suitable for showing the continuous distribution characteristics of data.
# 
# Boxplot	- Concise summary of distribution
# - Highlights outliers
# - Good for comparisons	- No insight into distribution shape
# - Limited detail
# - No granularity
# 
# Histogram	- Shows distribution shape
# - Displays frequency
# - Adjustable bin size	- Dependent on bin size
# - Can be choppy
# - Not ideal for small datasets
# 
# KDE	- Smooth representation
# - No binning issues
# - Good for small datasets	- Bandwidth sensitivity
# - Doesn't show actual counts
# - Harder to interpret for some

# 4.Run the code below and look at the resulting figure of distrubutions and then answer the following questions
# 
# Which datasets have similar means and similar variances
# 
# Which datasets have similar means but quite different variances
# 
# Which datasets have similar variances but quite different means
# 
# Which datasets have quite different means and quite different variances

# In[3]:


from scipy import stats
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

n = 1500
data1 = stats.uniform.rvs(0, 10, size=n)
data2 = stats.norm.rvs(5, 1.5, size=n)
data3 = np.r_[stats.norm.rvs(2, 0.25, size=int(n/2)), stats.norm.rvs(8, 0.5, size=int(n/2))]
data4 = stats.norm.rvs(6, 0.5, size=n)

fig = make_subplots(rows=1, cols=4)

fig.add_trace(go.Histogram(x=data1, name='A', nbinsx=30, marker=dict(line=dict(color='black', width=1))), row=1, col=1)
fig.add_trace(go.Histogram(x=data2, name='B', nbinsx=15, marker=dict(line=dict(color='black', width=1))), row=1, col=2)
fig.add_trace(go.Histogram(x=data3, name='C', nbinsx=45, marker=dict(line=dict(color='black', width=1))), row=1, col=3)
fig.add_trace(go.Histogram(x=data4, name='D', nbinsx=15, marker=dict(line=dict(color='black', width=1))), row=1, col=4)

fig.update_layout(height=300, width=750, title_text="Row of Histograms")
fig.update_xaxes(title_text="A", row=1, col=1)
fig.update_xaxes(title_text="B", row=1, col=2)
fig.update_xaxes(title_text="C", row=1, col=3)
fig.update_xaxes(title_text="D", row=1, col=4)
fig.update_xaxes(range=[-0.5, 10.5])

for trace in fig.data:
    trace.xbins = dict(start=0, end=10)
    
# This code was produced by just making requests to Microsoft Copilot
# https://github.com/pointOfive/stat130chat130/blob/main/CHATLOG/wk3/COP/SLS/0001_concise_makeAplotV1.md

fig.show() # USE `fig.show(renderer="png")` FOR ALL GitHub and MarkUs SUBMISSIONS


# (1) Which datasets have similar means and similar variances?
# Datasets B and D: Both distributions are centered around similar means (around 5-6) and have similar variances. Both are relatively narrow, indicating that their distributions are close and that their overall spreads are similar.
# 
# (2)Which datasets have similar means but very different variances?
# Datasets B and C: Both datasets appear to have their central values ​​(means) in a similar region, around 5. However, dataset C shows more variation (it is a mixture of two distributions, with one cluster around 2 and the other around 8), indicating that the variance is much larger than dataset B, which is tightly concentrated around its mean.
# 
# (3)Which datasets have similar variances but very different means?
# Datasets A and D: The means of these two distributions are very different - dataset A is evenly distributed over a wide range (mean around 5), while dataset D is normally distributed with a smaller range around 6. Nevertheless, the variance ranges of both are relatively similar, despite their different shapes (uniform vs. normal).
# 
# (4)Which datasets have very different means and variances?
# Datasets A and C: Dataset A is uniformly distributed between 0 and 10, so its variance is relatively high, and its mean is around 5. On the other hand, dataset C is bimodal, with clusters around 2 and 8, which results in a larger variance and a different mean. Therefore, both their means and variances are different.

# 5. Start a new ChatBot session to explore the general relationship between the mean and median and "right" and "left" skewness (and why this is); what the following code does and how it works; and then explain (in your own words) the relationship between the mean and median and "right" and "left" skewness and what causes this, using and extending the code to demonstrate your explanation through a sequence of notebook cells.

# In[6]:


from scipy import stats
import pandas as pd
import numpy as np

#scipy.stats: This module contains a wide range of probability distributions and statistical functions.
#pandas: Useful for handling data structures like DataFrames.
#numpy: Provides functions for numerical operations such as generating arrays and computing quantiles.


sample1 = stats.gamma(a=2, scale=2).rvs(size=1000)

#stats.gamma(a=2, scale=2): This creates a gamma distribution with shape parameter a=2 and scale parameter scale=2.
#.rvs(size=1000): Generates 1000 random values (sample) from this gamma distribution. Since the gamma distribution is positively skewed, this sample will exhibit right skewness (longer right tail).

fig1 = px.histogram(pd.DataFrame({'data': sample1}), x="data")

# USE `fig1.show(renderer="png")` FOR ALL GitHub and MarkUs SUBMISSIONS

#This line creates a histogram of sample1, using Plotly Express (px), plotting the values in the sample.
#fig1.show(renderer="png") is a suggestion for how to visualize this histogram when submitting to platforms like GitHub or MarkUs, likely due to compatibility reasons.

sample1.mean()
np.quantile(sample1, [0.5]) # median

#sample1.mean(): Calculates the mean of the sample1.
#np.quantile(sample1, [0.5]): Calculates the 0.5 quantile (which is the median) of sample1.

sample2 = -stats.gamma(a=2, scale=2).rvs(size=1000)

#Here, the same gamma distribution is used, but its sign is flipped by multiplying it by -1, making the sample negatively skewed (left skewed).
#This would create a distribution with a long left tail, and for this left-skewed distribution, the mean would be less than the median (mean < median), since the extreme negative values pull the mean down.


# 6. Go find an interesting dataset and use summary statistics and visualizations to understand and demonstate some interesting aspects of the data

# In[7]:


import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/manuelamc14/fast-food-Nutritional-Database/main/Tables/nutrition.csv")
df # df.columns


# 7. Watch the classic Gapminder Video, then have a look at the plotly version and recreate the animation (perhaps after optionally exploring and changing the style, if you wish)

# In[9]:


import plotly.express as px

# Load built-in Gapminder dataset
gapminder = px.data.gapminder()

# Create the animated bubble chart
fig = px.scatter(
    gapminder, 
    x="gdpPercap", 
    y="lifeExp", 
    animation_frame="year", 
    animation_group="country",
    size="pop", 
    color="continent", 
    hover_name="country", 
    log_x=True, 
    size_max=60,
    range_x=[100,100000], 
    range_y=[20,90],
    title="Gapminder Global Development Trends"
)

# Show the plot
fig.show()


# 8. Provide a second version of the figure from the previous problem where you edit the fig = px.scatter() function from the Gapminder code so that x is "percent change", y is "rank", size is "percent", and color="sex", animation_frame is "year", and animation_group and hover_name are "name". Then use size_max=50, range_x=[-0.005,0.005]) and remove the log_x=True and range_y parameters

# In[14]:


import pandas as pd
import plotly.express as px

# Load the dataset
bn = pd.read_csv('https://raw.githubusercontent.com/hadley/data-baby-names/master/baby-names.csv')

# Make identical boy and girl names distinct
bn['name'] = bn['name'] + " " + bn['sex'] 

# Calculate rank based on percentage for each year
bn['rank'] = bn.groupby('year')['percent'].rank(ascending=False)

# Sort values for proper processing
bn = bn.sort_values(['name', 'year'])

# Calculate the increase or decrease in name prevalence from the last year
bn['percent change'] = bn['percent'].diff()
new_name = [True] + list(bn.name[:-1].values != bn.name[1:].values)
bn.loc[new_name, 'percent change'] = bn.loc[new_name, 'percent']

# Sort by year again
bn = bn.sort_values('year')

# Restrict to "common" names
bn = bn[bn.percent > 0.001]

# Create the animated scatter plot
fig = px.scatter(
    bn,
    x="percent change",     # Percent change on the x-axis
    y="rank",               # Rank on the y-axis
    animation_frame="year", # Animate by year
    animation_group="name", # Group by name for animation
    size="percent",         # Size of bubbles based on percent
    color="sex",            # Color based on sex
    hover_name="name",      # Hover name shows the name
    size_max=50,           # Maximum size for bubbles
    range_x=[-0.005, 0.005] # X-axis range for percent change
)

# Reverse the y-axis to place rank 1 on top
fig.update_yaxes(autorange='reversed')

# Show the plot
fig.show(renderer="png") # For GitHub and MarkUs submissions


# 9. Have you reviewed the course wiki-textbook and interacted with a ChatBot (or, if that wasn't sufficient, real people in the course piazza discussion board or TA office hours) to help you understand all the material in the tutorial and lecture that you didn't quite follow when you first saw it?

# Yes, I reviewed the course wiki textbook and interacted with the ChatBot to help me understand the material in the tutorials and lectures.

# Summary:
# 
# Visualization Methods:
# 
# Discussed the advantages and disadvantages of boxplots, histograms, and Kernel Density Estimation (KDE), highlighting their uses for data distribution, central tendency, outlier detection, and smoothness of representation.
# 
# Mean and Median Relationship with Skewness:
# 
# Discussed how the mean and median relate to right (positive) skewness (mean > median) and left (negative) skewness (mean < median), explaining the reasons behind these relationships.
# Python Code Explanation:
# 
# Explained a Python code snippet using scipy.stats to generate data from a gamma distribution, create histograms, and calculate the mean and median.
# 
# Discussed how the first sample represented right skewness, while a second sample, created by flipping the sign, represented left skewness.
# 
# Gapminder Animation:
# 
# Provided a code example to recreate the Gapminder animated bubble chart using Plotly, detailing the parameters and their significance.
# 
# Gave instructions for creating a second version of the animation with specific parameters (percent change, rank, etc.).
# 
# Corrected Code for Baby Names Dataset:
# 
# Provided a corrected version of your code for analyzing baby names, creating an animated scatter plot with the appropriate settings.
# 
# The link of google document for the summary of chatbot chating:https://docs.google.com/document/d/1wBdVnvFr5H879NwyVQdqB_75RpA88c8UuhCM063CyDI/edit?addon_store
