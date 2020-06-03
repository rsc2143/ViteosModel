# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 20:03:23 2020

@author: consultant138
"""

import pandas as pd
import numpy as np
#import os
#import datetime
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
#from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
#from sklearn.metrics import accuracy_score 
from sklearn.metrics import classification_report 
from ViteosMongoDB import ViteosMongoDB as mngdb

class ViteosModel:
	      
        def __init__(self):
		mngdb_obj = mngdb()
                print("ViteosMongoDB instance created")

                mngdb_obj.connect_with_or_without_ssh()
                print("ViteosMongoDB instance connection being established")

                mngdb_obj.df_to_evaluate()
                print("ViteosMongoDB instance dataframe to evaluate function invoked")

                mngdb_obj.make_df()
                print("ViteosMongoDB columns being renamed to begin with ViewData")

                print("ViteosMongoDB instance dataframe ready to be consumed by the ViteosModel class")
	
                print("The shape of the dataframe to be evalued for modelling is \n")
                self.df_model = mngdb.df.shape()

        def fun_reset_index(self,df):
                df = df.reset_index()
                df = df.drop('index',1)
                return df
        
        def change_side_col_type(self,df):
                df['ViewData.Side0_UniqueIds'] = df['ViewData.Side0_UniqueIds'].astype(str)
                df['ViewData.Side1_UniqueIds'] = df['ViewData.Side1_UniqueIds'].astype(str)
                return df
        
        def nan_to_zero_flag_side_column(self,df):
                df.loc[df['ViewData.Side0_UniqueIds']=='nan','flag_side0'] = 0 
                df.loc[df['ViewData.Side1_UniqueIds']=='nan','flag_side1'] = 0
                return df
   
        def add_new_cols(self,df):
                df['record_null_count'] = df[['MetaData.0._RecordID','MetaData.1._RecordID']].isnull().sum(axis=1)
                df['Date'] = pd.to_datetime(df['ViewData.Task Business Date']).dt.date 
                
                df = self.change_side_col_type(df)
                
                df['flag_side0'] = df.apply(lambda x: len(x['ViewData.Side0_UniqueIds'].split(',')), axis=1)
                df['flag_side1'] = df.apply(lambda x: len(x['ViewData.Side1_UniqueIds'].split(',')), axis=1)
                df = self.nan_to_zero_flag_side_column(df) 
                               
                
                return df
  
              