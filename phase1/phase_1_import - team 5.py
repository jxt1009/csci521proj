#!/usr/bin/env python
# coding: utf-8

# # ***Phase 1 - Combination and preparation of the data***

# Team #5 | Movie Pruners
# 
# Zachary Chang - Hugo Tessier - Jameson Toper - Ellis Wright
# 

# For this phae 4 files need to be imported and merged:
# - `title.akas.tsv`
# - `title.basics.tsv`
# - `title.ratings.tsv`
# - `name.basics.tsv`

# ---
# # 1 - IMPORT

# Libraries used to import and treat the datasets. All the files has to be in a `data/` folder. `import_tsv` is a function

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


datapath = "data/"
def import_tsv(filename):
    return pd.read_csv( datapath + filename, sep='\t', encoding='utf-8', dtype=str)


# ***Notes:*** 
# Few things can be noted after a first glance at the files and are considered in the `import_tsv` function.
# - `sep='\t'`: the values are separated by tabulates (TSV files)
# - `encoding='utf-8'`: the files are encoding in UTF-8
# - `dtype=str` as we won't use datatypes in this phase, it's easier and faster to consider every columns as strings

# ### Import `title.akas.tsv`

# In[3]:


title_akas = import_tsv("title.akas.tsv")


# In[4]:


len(title_akas)


# In[5]:


title_akas.head(10)


# ### Import `title.basics.tsv`

# In[6]:


title_basics = import_tsv("title.basics.tsv")


# In[7]:


len(title_basics)


# In[8]:


title_basics.head(10)


# ### Explode multiple valued cells
# 
# Some cells have multiple values separated by commas and need to by plit into several rows.
# 
# #### `genres` explosion

# In[9]:


title_basics_exploded = title_basics.assign(
    genres = title_basics['genres'].str.split(',')
).explode(
    'genres'
)


# In[10]:


len(title_basics_exploded)


# In[11]:


title_basics_exploded.head(10)


# *Remark:*
# 
# as a point of comparison we can count the number of different values in the multi-valued cells by counting the number of commas and compare the number of values to the number of rows in the final dataset.

# In[12]:


title_basics.assign(
    valueCount  = title_basics['genres'].map(lambda x: 1 + str(x).count(','))
)['valueCount'].sum()


# There is no difference. This is a simple way to validate our number of records.

# In[13]:


title_basics = title_basics_exploded


# ### Import `title.ratings.tsv`

# In[14]:


title_ratings = import_tsv("title.ratings.tsv")


# In[15]:


len(title_ratings)


# In[16]:


title_ratings.head(10)


# ### Import `name.basics.tsv`

# In[17]:


name_basics = import_tsv("name.basics.tsv")


# In[18]:


len(name_basics)


# In[19]:


name_basics.head(10)


# ### Explode multiple valued cells
# 
# Two variables (`knownForTitles` and`primaryProfession`) have multiple values and nedd to be treated.

# #### `knownForTitles` explosion

# In[20]:


name_basics_exploded_titles = name_basics.assign(
    knownForTitles = name_basics['knownForTitles'].str.split(',')
).explode(
    'knownForTitles'
)


# In[21]:


len(name_basics_exploded_titles)


# In[22]:


name_basics_exploded_titles.head(10)


# *Remark:*
# 
# as a point of comparison we can count the number of different values in the multi-valued cells by counting the number of commas.

# In[23]:


name_basics.assign(
    valueCount  = name_basics['knownForTitles'].map(lambda x: 1 + str(x).count(','))
)['valueCount'].sum()


# There isn't any difference.

# #### `primaryProfession` explosion

# In[24]:


name_basics_exploded_titles_profession = name_basics_exploded_titles.assign(
    primaryProfession = name_basics_exploded_titles['primaryProfession'].str.split(',')
).explode(
    'primaryProfession'
)


# In[25]:


len(name_basics_exploded_titles_profession)


# In[26]:


name_basics_exploded_titles_profession.head(10)


# *Remark :*
# 
# We now compare with an estimation of the number of rows. As in the previous explosion, we want to estimate the number of rows by counting the number of values in the cells.

# In[27]:


name_basics_exploded_titles.assign(
    valueCount  = name_basics_exploded_titles['primaryProfession'].map(lambda x: 1 + str(x).count(','))
)['valueCount'].sum()


# No difference.

# In[28]:


name_basics = name_basics_exploded_titles_profession


# ---
# # 2 - FILTERING 

# Doing this stage before the merge makes it less memory-consuming. We need to filter several categories: 
# - filter on the **US** region 
# - filter on the type **movie**
# - filter on the profession **actress/actor**

# ### Filter on the ***US*** region
# This informations is contained in the `region` variable of `title_akas` dataset.

# In[29]:


c_bold = "\033[1m" 
c_end = "\033[0m"

# title_akas.region
print(c_bold + "title_akas.region categories\n" + c_end, title_akas.region.unique(), "\n")


# The only category that corresponds to the US region is the category `US`.

# In[30]:


title_akas_filtered = title_akas.loc[title_akas['region'] == 'US', ]


# In[32]:


print('from', len(title_basics), 'to', len(title_akas_filtered), 'rows')

title_akas_filtered


# ### Filter on the ***movie*** type
# 
# We searched for this information in 3 differents variables

# In[33]:


# title_akas.types
print(c_bold + "title_akas.types categories\n" + c_end, title_akas.types.unique(), "\n")

# title_basics.genres
print(c_bold + "title_basics.genres categories\n" + c_end, title_basics.genres.unique(), "\n")

# title_basics.titleType
print(c_bold + "title_basics.titleType categories\n" + c_end, title_basics.titleType.unique())


# After a search in `title_akas.types`, `title_basics.genres` and `title_basics.titleType` it seems that the only interesting way to filter movies is with the last variable. We can keep the categories `movie` and `tvMovie`.

# In[34]:


title_basics_filtered = title_basics.loc[title_basics['titleType'].isin({'movie', 'tvMovie'})]


# In[35]:


print('from', len(title_basics), 'to', len(title_basics_filtered), 'rows')

title_basics_filtered


# ### Filter on the ***actress/actor*** profession

# In[36]:


# name_basics.primaryProfession
print(c_bold + "name_basics.primaryProfession categories\n" + c_end, name_basics.primaryProfession.unique(), "\n")


# Information contained in the `primaryProfession` variable of `name_basics` dataset. From this list we extract 2 categories : `actor` and `actress`. We decided not to keep `miscellaneous` category which seemed too vague.  

# We also kept all the other professions of the actress/actor and as additionnal information on them. To do so, we first identify the persons ID and keep all the rows with these IDs.

# In[37]:


kept_person = name_basics.loc[name_basics['primaryProfession'].isin({'actor', 'actress'}), 'nconst'].unique()

name_basics_filtered = name_basics[name_basics['nconst'].isin(list(kept_person))]


# In[38]:


print('from', len(name_basics), 'to', len(name_basics_filtered), 'rows')

name_basics_filtered


# ---
# # 3 - MERGE

# Merge between `title.basics`, `title.akas`, `title.ratings` and `name.basics` can be made with the variable `tconst` (respectively `titleId` and `knownForTitles` in other tables) which corresponds to an alphanumeric unique identifier of the title according to the IMDb Datasets reference (https://www.imdb.com/interfaces/).

# In[39]:


title_basics_join = title_basics_filtered.set_index('tconst')
title_akas_join = title_akas_filtered.rename({'titleId':'tconst'}, axis = 1).set_index('tconst')
title_ratings_join = title_ratings.set_index('tconst')
name_basics_join = name_basics_filtered.rename({'knownForTitles':'tconst'}, axis = 1).set_index('tconst')


# ### Test of the keys for all the tables

# In[40]:


#test of the format of all the key before the join
expr = r'tt[0-9]+' #regular expression to identidy correctly formatted title IDs

print("title.akas:", title_akas_join.index.str.match(expr).all())
print("title.ratings:", title_ratings_join.index.str.match(expr).all())
print("title.basics:", title_basics_join.index.str.match(expr).all())
print("name.basics:", name_basics_join.index.str.match(expr).all())


# Some *good-formated* keys are missing in the `name_basics` dataset. It may worth investigating.

# ### Incorrect format in `name.basics`
# 
# We first count the number of values that don't matching with the regular expression.

# In[41]:


np.logical_not(name_basics_join.index.str.match(expr)).sum()


# We the most common title identifiers

# In[42]:


name_basics_join.index.value_counts().sort_values(ascending=False).head()


# We find that the most frequent is `'\N'` and that it corresponds exactly to the non-matching values amount. We just have to get rid of these missing values for title IDs.

# ### Check for the column names conflicts

# In[43]:


set().intersection(
    set(name_basics_join.columns), 
    set(title_basics_join.columns), 
    set(title_akas_join.columns), 
    set(title_ratings_join.columns)
)


# There isn't any conflict with the column names in the different datasets.

# ### join of the tables

# In[44]:


us_movies_actors = name_basics_join.join(
    title_basics_join, how = "inner"
).join(
    title_akas_join, how = "inner"
).join(
    title_ratings_join, how = "inner"
).reset_index()


# ***Note:***
# 
# For our further study, we assume that the movie needs to be present in all datasets so that we have information on its ratings, its characteristics, its famous actors, etc. That's the reason why we choose to make an `inner` join: we only keep titles that appear in all datasets. With all joins being inner, the order of the intersection doesn't change the result. 

# ### Final dataset

# In[45]:


us_movies_actors


# ### File writing

# In[46]:


filename = 'us.movies.actors.tsv'
us_movies_actors.to_csv( datapath + filename , sep='\t', encoding='utf-8', index = False)

