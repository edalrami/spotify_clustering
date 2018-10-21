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

#Read an initial file to obtain column headers
initial_read = r'C:\Users\edalr\Desktop\school\ANLT212\project2\spotify_clustering\playlists\Boleros'
col_names = DataFrame(pd.read_csv(initial_read, index_col = None, header = 0))
col_names["playlist"] = "" 
col_names = list(col_names.columns.values)

#Create empty dataframe with saved column headers
songs_df = DataFrame(columns = col_names)
print(songs_df.columns.values)

#Iterate through the folder titled "playlist"
#Folder contains a collection of csv files
#Each csv file represents a playlist pulled
#from Spotify's API
#Store all songs into a dataframe
#And store the playlists names
for filename in os.listdir(path):
        p = path + "\\" + filename
        #concatenate all files together and
        #add additional column "playlist" that saves
        #the name of the playlist each song originated from 
        playlist = DataFrame(pd.read_csv(p, index_col = None, header = 0))
        playlist["playlist"] = filename
        frames = [songs_df, playlist]
        songs_df = pd.concat(frames)
#Verify playlist was saved by printing out a sample
#and playlist column details and songs_df dimension.         
print(songs_df.head())
print(songs_df.shape)
print(songs_df["playlist"])
        
        