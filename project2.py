# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 08:48:15 2018

@author: edalr
"""

import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, leaves_list
from sklearn.cluster import KMeans
import os

import pandas as pd
import numpy as np
from pandas import DataFrame
from scipy.cluster.hierarchy import fcluster


path = r'C:\Users\edalr\Desktop\school\ANLT212\project2\spotify_clustering\playlists'

for filename in os.listdir(path):
        p = path + "\\" + filename
        print(p)
        print(filename)
        songs_df = DataFrame(pd.read_csv(p, index_col = None, header = 0))
        print(songs_df)