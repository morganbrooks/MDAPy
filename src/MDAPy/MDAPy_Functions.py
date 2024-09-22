# -*- coding: utf-8 -*-
"""
Created Sep 2, 2020

@author: morganbrooks
"""
#%%


# Import required modules
import pathlib2
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
import seaborn as sns
import math 
import peakutils
from scipy import stats 
from matplotlib.backends.backend_pdf import PdfPages
from scipy import optimize
import re
import IPython.display as dp
import glob, os, json, subprocess

#Compiles all the MDA calculators into one step 

def MDA_Calculator(ages, errors, sample_list, dataToLoad_MLA, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, U238_decay_constant, U235_decay_constant, U238_U235,excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, Data_Type, best_age_cut_off):
    YSG_MDA = YSG(ages, errors, sample_list,  eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type, best_age_cut_off)
    
    YC2s_MDA,YC2s_cluster_arrays = YC2s(ages, errors, sample_list, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, U238_decay_constant, U235_decay_constant, U238_U235, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, Data_Type, best_age_cut_off, min_cluster_size=3)
      
    YC1s_MDA, YC1s_cluster_arrays = YC1s(ages, errors, sample_list, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, U238_decay_constant, U235_decay_constant, U238_U235, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, Data_Type, best_age_cut_off, min_cluster_size=2)
    
    YDZ_MDA, minAges, mode = YDZ(ages, errors, iterations=10000, chartOutput = False, bins=25)
    
    Y3Zo_MDA, Y3Zo_cluster_arrays = Y3Zo(ages, errors, sample_list, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, U238_decay_constant, U235_decay_constant, U238_U235, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, Data_Type, best_age_cut_off)
    
    Y3Za_MDA, Y3Za_cluster_arrays = Y3Za(ages, errors, sample_list, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, U238_decay_constant, U235_decay_constant, U238_U235, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, Data_Type, best_age_cut_off)
    
    Tau_MDA, Tau_Grains, Tau_PDP_age, Tau_PDP,ages_errors1s_filtered = tau(ages, errors, sample_list, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, U238_decay_constant, U235_decay_constant, U238_U235, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, Data_Type, best_age_cut_off, min_cluster_size=3, thres=0.01, minDist=1, xdif=1, x1=0, x2=4000)
    
    YSP_MDA, YSP_cluster = YSP(ages, errors, sample_list, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, U238_decay_constant, U235_decay_constant, U238_U235, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, Data_Type, best_age_cut_off, min_cluster_size=2, MSWD_threshold=1)
        
    YPP_MDA = YPP(ages, errors, min_cluster_size=2, thres=0.01, minDist=1, xdif=0.1)
    
    MLA_MDA = MLA(sample_list, dataToLoad_MLA)
    
    return U238_decay_constant, U235_decay_constant, U238_U235, YSG_MDA, YC1s_MDA, YC1s_cluster_arrays, YC2s_MDA, YC2s_cluster_arrays, YDZ_MDA, minAges, mode, Y3Zo_MDA, Y3Zo_cluster_arrays, Y3Za_MDA, Y3Za_cluster_arrays, Tau_MDA, Tau_Grains, Tau_PDP_age, Tau_PDP,ages_errors1s_filtered, YSP_MDA, YSP_cluster, YPP_MDA, MLA_MDA

         
            
#Creates an Output table of all the MDA data (MDAs, errors...etc) and saves it to an excel file in the Data folder. Also creates a table of only the MDA data

def output_tables(sample_list, YSG_MDA, YC1s_MDA, YC2s_MDA, YDZ_MDA, Y3Zo_MDA, Y3Za_MDA, Tau_MDA, YSP_MDA, YPP_MDA, MLA_MDA):
    
    YSG_Table = pd.DataFrame(data=YSG_MDA, index=[sample_list], columns=['YSG_MDA', 'YSG_+/-1σ']) 
    YDZ_Table = pd.DataFrame(data=YDZ_MDA, index=[sample_list], columns=['YDZ_MDA', 'YDZ_+2σ', 'YDZ_-2σ'])
    YPP_Table = pd.DataFrame(data=YPP_MDA, index=[sample_list], columns=['YPP_MDA'])
    YC1s_Table = pd.DataFrame(data=YC1s_MDA, index=[sample_list], columns=['YC1σ_MDA', 'YC1σ_+/-1σ', 'YC1σ_MSWD', 'YC1σ_Grains'])
    YC2s_Table = pd.DataFrame(data=YC2s_MDA, index=[sample_list], columns=['YC2σ_MDA', 'YC2σ_+/-1σ', 'YC2σ_MSWD', 'YC2σ_Grains'])
    Y3Zo_Table = pd.DataFrame(data=Y3Zo_MDA, index=[sample_list], columns=['Y3Zo_MDA', 'Y3Zo_+/-1σ', 'Y3Zo_MSWD', 'Y3Zo_Grains'])
    Y3Za_Table = pd.DataFrame(data=Y3Za_MDA, index=[sample_list], columns=['Y3Za_MDA', 'Y3Za_+/-1σ', 'Y3Za_MSWD','Y3Za_Grains'])
    Tau_Table = pd.DataFrame(data=Tau_MDA, index=[sample_list], columns=['Tau_MDA', 'Tau_+/-1σ', 'Tau_MSWD','Tau_Grains'])
    YSP_Table = pd.DataFrame(data=YSP_MDA, index=[sample_list], columns=['YSP_MDA', 'YSP_+/-1σ', 'YSP_MSWD','YSP_Grains'])
    MLA_Table = pd.DataFrame(data=MLA_MDA, index=[sample_list], columns=['MLA_MDA', 'MLA_+/-1σ'])
    
    #create a sample_ID column in each MDA result table 
    Y3Zo_Table['Sample_ID'] = sample_list
    YSP_Table['Sample_ID'] = sample_list
    Tau_Table['Sample_ID'] = sample_list
    Y3Za_Table['Sample_ID'] = sample_list
    YC2s_Table['Sample_ID'] = sample_list
    YC1s_Table['Sample_ID'] = sample_list
    YPP_Table['Sample_ID'] = sample_list
    YDZ_Table['Sample_ID'] = sample_list
    YSG_Table['Sample_ID'] = sample_list
    MLA_Table['Sample_ID'] = sample_list

    #merge all MDA tables into one, move Sample_ID Column to front, print 'output' excel spreadsheet to excel 
    merge1 = pd.merge(Y3Zo_Table, YSP_Table)
    merge2 = pd.merge(merge1, Tau_Table)
    merge3 = pd.merge(merge2, Y3Za_Table)
    merge4 = pd.merge(merge3, YC2s_Table)
    merge5 = pd.merge(merge4, YC1s_Table)
    merge6 = pd.merge(merge5, YPP_Table)
    merge7 = pd.merge(merge6, YDZ_Table)
    merge8 = pd.merge(merge7, MLA_Table)
    all_MDA_data = pd.merge(merge8, YSG_Table)
   
    all_MDA_data = pd.DataFrame(data=all_MDA_data, columns=['Sample_ID','Y3Zo_MDA', 'Y3Zo_+/-1σ', 'Y3Zo_MSWD','Y3Zo_Grains', 'YSP_MDA', 'YSP_+/-1σ', 'YSP_MSWD', 'YSP_Grains', 'Tau_MDA', 'Tau_+/-1σ', 'Tau_MSWD', 'Tau_Grains', 'Y3Za_MDA', 'Y3Za_+/-1σ', 'Y3Za_MSWD', 'Y3Za_Grains', 'YC2σ_MDA', 'YC2σ_+/-1σ', 'YC2σ_MSWD', 'YC2σ_Grains', 'YC1σ_MDA', 'YC1σ_+/-1σ', 'YC1σ_MSWD', 'YC1σ_Grains', 'YPP_MDA', 'YDZ_MDA', 'YDZ_+2σ', 'YDZ_-2σ', 'YSG_MDA', 'YSG_+/-1σ','MLA_MDA', 'MLA_+/-1σ'])
    
    excel_MDA_data = all_MDA_data.to_excel("data/All_MDA_Data.xlsx") 

    MDAs_1s_table = pd.DataFrame(data=all_MDA_data, columns=['Sample_ID','Y3Zo_MDA','Y3Zo_+/-1σ','YSP_MDA','YSP_+/-1σ','Tau_MDA','Tau_+/-1σ','Y3Za_MDA','Y3Za_+/-1σ','YC1σ_MDA', 'YC1σ_+/-1σ','YC2σ_MDA','YC2σ_+/-1σ','YPP_MDA', 'YDZ_MDA', 'YDZ_+2σ', 'YDZ_-2σ','YSG_MDA','YSG_+/-1σ','MLA_MDA', 'MLA_+/-1σ'])
    
    pd.options.display.float_format = "{:,.2f}".format
    
    MDAs_1s_table.reset_index(drop=True)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    return MDAs_1s_table, excel_MDA_data, all_MDA_data

#Function to build a graph/sample of all MDA methods plotted 

def Plot_MDA(MDAs_1s_table, all_MDA_data, sample_list, YSG_MDA, YC1s_MDA, YC2s_MDA, YDZ_MDA, Y3Zo_MDA, Y3Za_MDA, Tau_MDA, YSP_MDA, YPP_MDA, MLA_MDA, Image_File_Option, plotwidth, plotheight):
    
    #Builds large cumulative table with 1s and 2s error added and subtracted from MDAs  
    MDA_plot = all_MDA_data[['Sample_ID','Y3Zo_MDA', 'Y3Zo_+/-1σ', 'YSP_MDA', 'YSP_+/-1σ', 'Tau_MDA', 'Tau_+/-1σ', 'Y3Za_MDA', 'Y3Za_+/-1σ', 'YC2σ_MDA', 'YC2σ_+/-1σ', 'YC1σ_MDA', 'YC1σ_+/-1σ', 'YPP_MDA', 'YDZ_MDA', 'YDZ_+2σ', 'YDZ_-2σ', 'YSG_MDA', 'YSG_+/-1σ','MLA_MDA', 'MLA_+/-1σ']]
    MDA_plot.reset_index(inplace = True, drop = True)

    Y3Zo_1sErrorM = list((MDA_plot['Y3Zo_MDA'])-(MDA_plot['Y3Zo_+/-1σ']))
    Y3Zo_1sErrorP = list((MDA_plot['Y3Zo_MDA'])+(MDA_plot['Y3Zo_+/-1σ']))
    Y3Zo_2sErrorM = list((MDA_plot['Y3Zo_MDA'])-(MDA_plot['Y3Zo_+/-1σ']*2))
    Y3Zo_2sErrorP = list((MDA_plot['Y3Zo_MDA'])+(MDA_plot['Y3Zo_+/-1σ']*2))

    YSP_1sErrorM = list((MDA_plot['YSP_MDA'])-(MDA_plot['YSP_+/-1σ']))
    YSP_1sErrorP = list((MDA_plot['YSP_MDA'])+(MDA_plot['YSP_+/-1σ']))
    YSP_2sErrorM = list((MDA_plot['YSP_MDA'])-(MDA_plot['YSP_+/-1σ']*2))
    YSP_2sErrorP = list((MDA_plot['YSP_MDA'])+(MDA_plot['YSP_+/-1σ']*2))

    Tau_1sErrorM = list((MDA_plot['Tau_MDA'])-(MDA_plot['Tau_+/-1σ']))
    Tau_1sErrorP = list((MDA_plot['Tau_MDA'])+(MDA_plot['Tau_+/-1σ']))
    Tau_2sErrorM = list((MDA_plot['Tau_MDA'])-(MDA_plot['Tau_+/-1σ']*2))
    Tau_2sErrorP = list((MDA_plot['Tau_MDA'])+(MDA_plot['Tau_+/-1σ']*2))

    Y3Za_1sErrorM = list((MDA_plot['Y3Za_MDA'])-(MDA_plot['Y3Za_+/-1σ']))
    Y3Za_1sErrorP = list((MDA_plot['Y3Za_MDA'])+(MDA_plot['Y3Za_+/-1σ']))
    Y3Za_2sErrorM = list((MDA_plot['Y3Za_MDA'])-(MDA_plot['Y3Za_+/-1σ']*2))
    Y3Za_2sErrorP = list((MDA_plot['Y3Za_MDA'])+(MDA_plot['Y3Za_+/-1σ']*2))

    YC2s_1sErrorM = list((MDA_plot['YC2σ_MDA'])-(MDA_plot['YC2σ_+/-1σ']))
    YC2s_1sErrorP = list((MDA_plot['YC2σ_MDA'])+(MDA_plot['YC2σ_+/-1σ']))
    YC2s_2sErrorM = list((MDA_plot['YC2σ_MDA'])-(MDA_plot['YC2σ_+/-1σ']*2))
    YC2s_2sErrorP = list((MDA_plot['YC2σ_MDA'])+(MDA_plot['YC2σ_+/-1σ']*2))

    YC1s_1sErrorM = list((MDA_plot['YC1σ_MDA'])-(MDA_plot['YC1σ_+/-1σ']))
    YC1s_1sErrorP = list((MDA_plot['YC1σ_MDA'])+(MDA_plot['YC1σ_+/-1σ']))
    YC1s_2sErrorM = list((MDA_plot['YC1σ_MDA'])-(MDA_plot['YC1σ_+/-1σ']*2))
    YC1s_2sErrorP = list((MDA_plot['YC1σ_MDA'])+(MDA_plot['YC1σ_+/-1σ']*2))

    YSG_1sErrorM = list((MDA_plot['YSG_MDA'])-(MDA_plot['YSG_+/-1σ']))
    YSG_1sErrorP = list((MDA_plot['YSG_MDA'])+(MDA_plot['YSG_+/-1σ']))
    YSG_2sErrorM = list((MDA_plot['YSG_MDA'])-(MDA_plot['YSG_+/-1σ']*2))
    YSG_2sErrorP = list((MDA_plot['YSG_MDA'])+(MDA_plot['YSG_+/-1σ']*2))

    YDZ_1sErrorM = list((MDA_plot['YDZ_MDA'])-(MDA_plot['YDZ_-2σ']/2))
    YDZ_1sErrorP = list((MDA_plot['YDZ_MDA'])+(MDA_plot['YDZ_+2σ']/2))
    YDZ_2sErrorMi = list((MDA_plot['YDZ_MDA'])-(MDA_plot['YDZ_-2σ']))
    YDZ_2sErrorPl = list((MDA_plot['YDZ_MDA'])+(MDA_plot['YDZ_+2σ']))
    
    MLA_1sErrorM = list((MDA_plot['MLA_MDA'])-(MDA_plot['MLA_+/-1σ']))
    MLA_1sErrorP = list((MDA_plot['MLA_MDA'])+(MDA_plot['MLA_+/-1σ']))
    MLA_2sErrorM = list((MDA_plot['MLA_MDA'])-(MDA_plot['MLA_+/-1σ']*2))
    MLA_2sErrorP = list((MDA_plot['MLA_MDA'])+(MDA_plot['MLA_+/-1σ']*2))

    sample_list = list(MDA_plot['Sample_ID'])
    
    MDA_errors = pd.DataFrame(list(zip(sample_list, Y3Zo_1sErrorM, Y3Zo_1sErrorP, Y3Zo_2sErrorM, Y3Zo_2sErrorP, YSP_1sErrorM, YSP_1sErrorP, YSP_2sErrorM, YSP_2sErrorP, Tau_1sErrorM, Tau_1sErrorP, Tau_2sErrorP, Tau_2sErrorM,  Y3Za_1sErrorM, Y3Za_1sErrorP, Y3Za_2sErrorM, Y3Za_2sErrorP, YC2s_1sErrorM, YC2s_1sErrorP, YC2s_2sErrorM, YC2s_2sErrorP, YC1s_1sErrorM, YC1s_1sErrorP, YC1s_2sErrorM, YC1s_2sErrorP, YSG_1sErrorM, YSG_1sErrorP, YSG_2sErrorM, YSG_2sErrorP, YDZ_1sErrorM, YDZ_1sErrorP, YDZ_2sErrorMi, YDZ_2sErrorPl, MLA_1sErrorM, MLA_1sErrorP, MLA_2sErrorM, MLA_2sErrorP)), columns = ['Sample_ID', 'Y3Zo_1sErrorM', 'Y3Zo_1sErrorP', 'Y3Zo_2sErrorM', 'Y3Zo_2sErrorP', 'YSP_1sErrorM', 'YSP_1sErrorP', 'YSP_2sErrorM', 'YSP_2sErrorP', 'Tau_1sErrorM', 'Tau_1sErrorP', 'Tau_2sErrorP', 'Tau_2sErrorM', 'Y3Za_1sErrorM','Y3Za_1sErrorP','Y3Za_2sErrorM', 'Y3Za_2sErrorP', 'YC2s_1sErrorM','YC2s_1sErrorP','YC2s_2sErrorM','YC2s_2sErrorP','YC1s_1sErrorM','YC1s_1sErrorP','YC1s_2sErrorM','YC1s_2sErrorP', 'YSG_1sErrorM','YSG_1sErrorP','YSG_2sErrorM','YSG_2sErrorP', 'YDZ_1sErrorM', 'YDZ_1sErrorP', 'YDZ_2sErrorMi', 'YDZ_2sErrorPl', 'MLA_1sErrorM', 'MLA_1sErrorP', 'MLA_2sErrorM', 'MLA_2sErrorP'])
    
    MDA_plot_merge = pd.merge(MDA_plot, MDA_errors)
    
    MDA_plot_final = MDA_plot_merge[['Sample_ID','Y3Zo_MDA', 'Y3Zo_1sErrorM', 'Y3Zo_1sErrorP', 'Y3Zo_2sErrorM', 'Y3Zo_2sErrorP', 'YSP_MDA', 'YSP_1sErrorM', 'YSP_1sErrorP', 'YSP_2sErrorM', 'YSP_2sErrorP','Tau_MDA', 'Tau_1sErrorP','Tau_1sErrorM', 'Tau_2sErrorP', 'Tau_2sErrorM', 'Y3Za_MDA', 'Y3Za_1sErrorM','Y3Za_1sErrorP','Y3Za_2sErrorM', 'Y3Za_2sErrorP', 'YC2σ_MDA', 'YC2s_1sErrorP','YC2s_1sErrorM','YC2s_2sErrorP','YC2s_2sErrorM', 'YC1σ_MDA', 'YC1s_1sErrorP', 'YC1s_1sErrorM', 'YC1s_2sErrorM', 'YC1s_2sErrorP', 'YPP_MDA', 'YDZ_MDA', 'YDZ_1sErrorM', 'YDZ_1sErrorP', 'YDZ_2sErrorMi', 'YDZ_2sErrorPl', 'YSG_MDA', 'YSG_1sErrorP', 'YSG_1sErrorM','YSG_2sErrorM','YSG_2sErrorP', 'MLA_MDA', 'MLA_1sErrorM', 'MLA_1sErrorP', 'MLA_2sErrorM', 'MLA_2sErrorP']]
    
    MDA_plot_final.reset_index(inplace = True, drop = True)
    
    MDAs_Only = MDA_plot_merge[['Y3Zo_MDA', 'YSP_MDA', 'Tau_MDA', 'Y3Za_MDA', 'YC2σ_MDA', 'YC1σ_MDA', 'YPP_MDA', 'YDZ_MDA', 'YSG_MDA', 'MLA_MDA']]
    
    Errors_only = all_MDA_data[['Y3Zo_+/-1σ', 'YSP_+/-1σ', 'Tau_+/-1σ', 'Y3Za_+/-1σ',  'YC2σ_+/-1σ', 'YC1σ_+/-1σ','YDZ_+2σ', 'YDZ_-2σ', 'YSG_+/-1σ', 'MLA_+/-1σ']]

    #Arrange MDA data for each method into sets of arrays 

    #Tables 
    MDA_table_array = np.array(MDA_plot)
    MDA_table_arrays = np.split(MDA_table_array,len(MDA_table_array))
    table_plot_array = np.array(MDAs_1s_table)
    table_plot_arrays = np.split(table_plot_array,len(table_plot_array))

    #Sample_List
    sample_array = np.array(sample_list)
    sample_arrays = np.split(sample_array,len(sample_array))

    #Setting Graph Y-Limits 
    MDAs_array_ = np.array(MDAs_Only)
    MDAs_array_int = MDAs_array_.astype('int')
    Errors_array = np.array(Errors_only)
    Errors_array_int = Errors_array.astype('float')
    y_space = ((Errors_array_int.max(axis=1)*2)+5)
    
    sample_ymax = (MDAs_array_int.max(axis = 1) +  y_space)
    sample_ymin = (MDAs_array_int.min(axis = 1) -  y_space)
    ymax = np.split(sample_ymax,len(sample_ymax))
    ymin = np.split(sample_ymin,len(sample_ymin))

    #YSG
    YSG_array = np.array(YSG_MDA)
    YSG_MDAs = YSG_array[:,0]
    YSG_error1s = YSG_array[:,1]
    YSG_MDAs_arrays = np.split(YSG_MDAs,len(YSG_MDAs))
    YSG_error1s_arrays = np.split(YSG_error1s,len(YSG_MDAs))

    #YDZ
    YDZ_array = np.array(YDZ_MDA)
    YDZ_MDAs = YDZ_array[:,0]
    YDZ_error1sP = YDZ_array[:,1]/2
    YDZ_error1sM = YDZ_array[:,2]/2
    YDZ_MDAs_arrays = np.split(YDZ_MDAs,len(YDZ_MDAs))
    YDZ_error1sP_arrays = np.split(YDZ_error1sP,len(YDZ_MDAs))
    YDZ_error1sM_arrays = np.split(YDZ_error1sM,len(YDZ_MDAs))

    #YPP
    YPP_array = np.array(YPP_MDA)
    YPP_MDAs_arrays = np.split(YPP_array,len(YPP_array))

    #YC1s
    YC1s_array = np.array(YC1s_MDA)
    YC1s_MDAs = YC1s_array[:,0]
    YC1s_error1s = YC1s_array[:,1]
    YC1s_MDAs_arrays = np.split(YC1s_MDAs,len(YC1s_MDAs))
    YC1s_error1s_arrays = np.split(YC1s_error1s,len(YC1s_MDAs))

    #YC2s
    YC2s_array = np.array(YC2s_MDA)
    YC2s_MDAs = YC2s_array[:,0]
    YC2s_error1s = YC2s_array[:,1]
    YC2s_MDAs_arrays = np.split(YC2s_MDAs,len(YC2s_MDAs))
    YC2s_error1s_arrays = np.split(YC2s_error1s,len(YC2s_MDAs))

    #Y3Za
    Y3Za_array = np.array(Y3Za_MDA)
    Y3Za_MDAs = Y3Za_array[:,0]
    Y3Za_error1s = Y3Za_array[:,1]
    Y3Za_MDAs_arrays = np.split(Y3Za_MDAs,len(Y3Za_MDAs))
    Y3Za_error1s_arrays = np.split(Y3Za_error1s,len(Y3Za_MDAs))

    #Tau
    Tau_array = np.array(Tau_MDA)
    Tau_MDAs = Tau_array[:,0]
    Tau_error1s = Tau_array[:,1]
    Tau_MDAs_arrays = np.split(Tau_MDAs,len(Tau_MDAs))
    Tau_error1s_arrays = np.split(Tau_error1s,len(Tau_MDAs))

    #YSP
    YSP_array = np.array(YSP_MDA)
    YSP_MDAs = YSP_array[:,0]
    YSP_error1s = YSP_array[:,1]
    YSP_MDAs_arrays = np.split(YSP_MDAs,len(YSP_MDAs))
    YSP_error1s_arrays = np.split(YSP_error1s,len(YSP_MDAs))

    #Y3Zo
    Y3Zo_array = np.array(Y3Zo_MDA)
    Y3Zo_MDAs = Y3Zo_array[:,0]
    Y3Zo_error1s = Y3Zo_array[:,1]
    Y3Zo_MDAs_arrays = np.split(Y3Zo_MDAs,len(Y3Zo_MDAs))
    Y3Zo_error1s_arrays = np.split(Y3Zo_error1s,len(Y3Zo_MDAs))
    
    #MLA
    MLA_array = np.array(MLA_MDA)
    MLA_MDAs = MLA_array[:,0]
    MLA_error1s = MLA_array[:,1]
    MLA_MDAs_arrays = np.split(MLA_MDAs,len(MLA_MDAs))
    MLA_error1s_arrays = np.split(MLA_error1s,len(MLA_MDAs))
    
    N = len(sample_arrays)
    
    MDA_methods = [" ","YSG","YDZ","YPP","YC1σ","YC2σ","Y3Za","Y3Zo","Tau","YSP", "MLA"," "]
    
    #Plotting     
    
    MDAfig, ax = plt.subplots(N, 1, figsize=(plotwidth, N*plotheight), dpi=600)
    
        
    for i in range(N):
        #Preparing the data to be plotted"
        
        if N > 1:
            ax[i] = plt.subplot2grid((N,1),(i,0))
            axi = ax[i]
        else:
            axi = ax
        if Image_File_Option == 'web':
            MDAfig, axi = plt.subplots(1, 1, figsize=(plotwidth, 1*plotheight))
            
        #Setting graph y-limits
        ymax_ = ymax[i]
        ymin_ = ymin[i]
        yrange = int(ymax_[0])
         
        #Sample_List 
        samples = sample_arrays[i]
        
        #Tables
        tables = MDA_table_arrays[i]
        plot_tables = table_plot_arrays[i]
        
        #YSG MDA and Errors formatted for plotting  
        YSG_error1s = YSG_error1s_arrays[i]
        YSG_error2s = YSG_error1s_arrays[i]*2
        YSG_MDAs_1s = list(zip(YSG_MDAs_arrays[i],YSG_error1s))
        YSG_MDAs_2s = list(zip(YSG_MDAs_arrays[i], YSG_error2s))
        YSG1 = YSG_MDAs_1s[0][0]
        YSG_err1s = YSG_MDAs_1s[0][1]
        YSG_err2s = YSG_MDAs_2s[0][1]
    
        #YDZ MDA and Errors formatted for plotting  
        YDZ_error1sP = YDZ_error1sP_arrays[i]
        YDZ_error2sP = YDZ_error1sP_arrays[i]*2
        YDZ_error1sM = YDZ_error1sM_arrays[i]
        YDZ_error2sM = YDZ_error1sM_arrays[i]*2
        YDZ_MDAs_1sP = list(zip(YDZ_MDAs_arrays[i], YDZ_error1sP))
        YDZ_MDAs_2sP = list(zip(YDZ_MDAs_arrays[i], YDZ_error2sP))
        YDZ_MDAs_1sM = list(zip(YDZ_MDAs_arrays[i], YDZ_error1sM))
        YDZ_MDAs_2sM = list(zip(YDZ_MDAs_arrays[i], YDZ_error2sM))
        YDZ1 = YDZ_MDAs_1sP[0][0]
        YDZ_err1sP = YDZ_MDAs_1sP[0][1]
        YDZ_err2sP = YDZ_MDAs_2sP[0][1]
        YDZ_err1sM = YDZ_MDAs_1sM[0][1]
        YDZ_err2sM = YDZ_MDAs_2sM[0][1]
        
        #YPP MDAs formatted for plotting (no error for YPP )
        YPP_MDAs_1s = YPP_MDAs_arrays[i]
        YPP1 = YPP_MDAs_1s[0]
        
        #YC1s MDA and Errors formatted for plotting  
        YC1s_error1s = YC1s_error1s_arrays[i]
        YC1s_error2s = YC1s_error1s_arrays[i]*2
        YC1s_MDAs_1s = list(zip(YC1s_MDAs_arrays[i],YC1s_error1s))
        YC1s_MDAs_2s = list(zip(YC1s_MDAs_arrays[i], YC1s_error2s))
        YC1s1 = YC1s_MDAs_1s[0][0]
        YC1s_err1s = YC1s_MDAs_1s[0][1]
        YC1s_err2s = YC1s_MDAs_2s[0][1]
        
        #YC2s MDA and Errors formatted for plotting  
        YC2s_error1s = YC2s_error1s_arrays[i]
        YC2s_error2s = YC2s_error1s_arrays[i]*2
        YC2s_MDAs_1s = list(zip(YC2s_MDAs_arrays[i],YC2s_error1s))
        YC2s_MDAs_2s = list(zip(YC2s_MDAs_arrays[i], YC2s_error2s))
        YC2s1 = YC2s_MDAs_1s[0][0]
        YC2s_err1s = YC2s_MDAs_1s[0][1]
        YC2s_err2s = YC2s_MDAs_2s[0][1]
        
        #Y3Za MDA and Errors formatted for plotting  
        Y3Za_error1s = Y3Za_error1s_arrays[i]
        Y3Za_error2s = Y3Za_error1s_arrays[i]*2
        Y3Za_MDAs_1s = list(zip(Y3Za_MDAs_arrays[i],Y3Za_error1s))
        Y3Za_MDAs_2s = list(zip(Y3Za_MDAs_arrays[i], Y3Za_error2s))
        Y3Za1 = Y3Za_MDAs_1s[0][0]
        Y3Za_err1s = Y3Za_MDAs_1s[0][1]
        Y3Za_err2s = Y3Za_MDAs_2s[0][1]
        
        #Y3Zo MDA and Errors formatted for plotting  
        Y3Zo_error1s = Y3Zo_error1s_arrays[i]
        Y3Zo_error2s = Y3Zo_error1s_arrays[i]*2
        Y3Zo_MDAs_1s = list(zip(Y3Zo_MDAs_arrays[i],Y3Zo_error1s))
        Y3Zo_MDAs_2s = list(zip(Y3Zo_MDAs_arrays[i], Y3Zo_error2s))
        Y3Zo1 = Y3Zo_MDAs_1s[0][0]
        Y3Zo_err1s = Y3Zo_MDAs_1s[0][1]
        Y3Zo_err2s = Y3Zo_MDAs_2s[0][1]
        
        #Tau MDA and Errors formatted for plotting  
        Tau_error1s = Tau_error1s_arrays[i]
        Tau_error2s = Tau_error1s_arrays[i]*2
        Tau_MDAs_1s = list(zip(Tau_MDAs_arrays[i],Tau_error1s))
        Tau_MDAs_2s = list(zip(Tau_MDAs_arrays[i], Tau_error2s))
        Tau1 = Tau_MDAs_1s[0][0]
        Tau_err1s = Tau_MDAs_1s[0][1]
        Tau_err2s = Tau_MDAs_2s[0][1]
        
        #YSP MDA and Errors formatted for plotting  
        YSP_error1s = YSP_error1s_arrays[i]
        YSP_error2s = YSP_error1s_arrays[i]*2
        YSP_MDAs_1s = list(zip(YSP_MDAs_arrays[i],YSP_error1s))
        YSP_MDAs_2s = list(zip(YSP_MDAs_arrays[i], YSP_error2s))
        YSP1 = YSP_MDAs_1s[0][0]
        YSP_err1s = YSP_MDAs_1s[0][1]
        YSP_err2s = YSP_MDAs_2s[0][1]
        
        #MLA MDA and Errors formatted for plotting  
        MLA_error1s = MLA_error1s_arrays[i]
        MLA_error2s = MLA_error1s_arrays[i]*2
        MLA_MDAs_1s = list(zip(MLA_MDAs_arrays[i],MLA_error1s))
        MLA_MDAs_2s = list(zip(MLA_MDAs_arrays[i], MLA_error2s))
        MLA1 = MLA_MDAs_1s[0][0]
        MLA_err1s = MLA_MDAs_1s[0][1]
        MLA_err2s = MLA_MDAs_2s[0][1]
        
        #YSG
        axi.broken_barh([(0.9, 0.22)], (YSG1-YSG_err2s, YSG_err1s), facecolors=('lightsteelblue'), label='2σ  Uncertainty')
        axi.broken_barh([(0.9, 0.22)], (YSG1-YSG_err1s,YSG_err1s), facecolors=('cornflowerblue'), label='1σ  Uncertainty')
        axi.broken_barh([(0.9, 0.22)], (YSG1, YSG_err1s), facecolors=('cornflowerblue'))
        axi.broken_barh([(0.9, 0.22)], (YSG1+YSG_err1s, YSG_err1s), facecolors=('lightsteelblue'))
        axi.hlines(y=YSG1, xmin=1.1, xmax=0.9, color = 'midnightblue', lw=1, label='MDA', linewidth=3)

        #YDZ
        axi.broken_barh([(1.9, 0.22)], (YDZ1-YDZ_err2sM, YDZ_err1sM), facecolors=('lightsteelblue'))
        axi.broken_barh([(1.9, 0.22)], (YDZ1-YDZ_err1sM, YDZ_err1sM), facecolors=('cornflowerblue'))
        axi.broken_barh([(1.9, 0.22)], (YDZ1, YDZ_err1sP), facecolors=('cornflowerblue'))
        axi.broken_barh([(1.9, 0.22)], (YDZ1+YDZ_err1sP, YDZ_err1sP), facecolors=('lightsteelblue'))
        axi.hlines(y=YDZ1, xmin=2.09, xmax=1.9, color = 'midnightblue', lw=1, linewidth=3)
        
        #YPP
        axi.broken_barh([(2.9, 0.22)], (YPP1, 0), facecolors=('midnightblue'))
        axi.broken_barh([(2.9, 0.22)], (YPP1, 0.33), facecolors=('midnightblue'))
        axi.broken_barh([(2.9, 0.22)], (YPP1, 0), facecolors=('midnightblue'))
        axi.broken_barh([(2.9, 0.22)], (YPP1, 0), facecolors=('midnightblue'))
        
        #YC1s
        axi.broken_barh([(3.9, 0.22)], (YC1s1-YC1s_err2s, YC1s_err1s), facecolors=('lightsteelblue'))
        axi.broken_barh([(3.9, 0.22)], (YC1s1-YC1s_err1s, YC1s_err1s), facecolors=('cornflowerblue'))
        axi.broken_barh([(3.9, 0.22)], (YC1s1, YC1s_err1s), facecolors=('cornflowerblue'))
        axi.broken_barh([(3.9, 0.22)], (YC1s1+YC1s_err1s, YC1s_err1s), facecolors=('lightsteelblue'))
        axi.hlines(y=YC1s1, xmin=4.09, xmax=3.9, color = 'midnightblue', lw=1, linewidth=3)
         
        #YC2s
        axi.broken_barh([(4.9, 0.22)], (YC2s1-YC2s_err2s, YC2s_err1s), facecolors=('lightsteelblue'))
        axi.broken_barh([(4.9, 0.22)], (YC2s1-YC2s_err1s, YC2s_err1s), facecolors=('cornflowerblue'))
        axi.broken_barh([(4.9, 0.22)], (YC2s1, YC2s_err1s), facecolors=('cornflowerblue'))
        axi.broken_barh([(4.9, 0.22)], (YC2s1+YC2s_err1s, YC2s_err1s), facecolors=('lightsteelblue'))
        axi.hlines(y=YC2s1, xmin=5.1, xmax=4.9, color = 'midnightblue', lw=1, linewidth=3)
        
        #Y3Za
        axi.broken_barh([(5.9, 0.22)], (Y3Za1-Y3Za_err2s, Y3Za_err1s), facecolors=('lightsteelblue'))
        axi.broken_barh([(5.9, 0.22)], (Y3Za1-Y3Za_err1s, Y3Za_err1s), facecolors=('cornflowerblue'))
        axi.broken_barh([(5.9, 0.22)], (Y3Za1, Y3Za_err1s), facecolors=('cornflowerblue'))
        axi.broken_barh([(5.9, 0.22)], (Y3Za1+Y3Za_err1s, Y3Za_err1s), facecolors=('lightsteelblue'))
        axi.hlines(y=Y3Za1, xmin=6.1, xmax=5.9, color = 'midnightblue', lw=1, linewidth=3)
        
        #Y3Zo
        axi.broken_barh([(6.9, 0.22)], (Y3Zo1-Y3Zo_err2s, Y3Zo_err1s), facecolors=('lightsteelblue'))
        axi.broken_barh([(6.9, 0.22)], (Y3Zo1-Y3Zo_err1s, Y3Zo_err1s), facecolors=('cornflowerblue'))
        axi.broken_barh([(6.9, 0.22)], (Y3Zo1, Y3Zo_err1s), facecolors=('cornflowerblue'))
        axi.broken_barh([(6.9, 0.22)], (Y3Zo1+Y3Zo_err1s, Y3Zo_err1s), facecolors=('lightsteelblue'))
        axi.hlines(y=Y3Zo1, xmin=7.1, xmax=6.9, color = 'midnightblue', lw=1, linewidth=3)
        
        #Tau
        axi.broken_barh([(7.9, 0.22)], (Tau1-Tau_err2s, Tau_err1s), facecolors=('lightsteelblue'))
        axi.broken_barh([(7.9, 0.22)], (Tau1-Tau_err1s, Tau_err1s), facecolors=('cornflowerblue'))
        axi.broken_barh([(7.9, 0.22)], (Tau1, Tau_err1s), facecolors=('cornflowerblue'))
        axi.broken_barh([(7.9, 0.22)], (Tau1+Tau_err1s, Tau_err1s), facecolors=('lightsteelblue'))
        axi.hlines(y=Tau1, xmin=8.1, xmax=7.9, color = 'midnightblue', lw=1, linewidth=3)
        
        #YSP
        axi.broken_barh([(8.9, 0.22)], (YSP1-YSP_err2s, YSP_err1s), facecolors=('lightsteelblue'))
        axi.broken_barh([(8.9, 0.22)], (YSP1-YSP_err1s, YSP_err1s), facecolors=('cornflowerblue'))
        axi.broken_barh([(8.9, 0.22)], (YSP1, YSP_err1s), facecolors=('cornflowerblue'))
        axi.broken_barh([(8.9, 0.22)], (YSP1+YSP_err1s, YSP_err1s), facecolors=('lightsteelblue'))
        axi.hlines(y=YSP1, xmin=9.1, xmax=8.9, color = 'midnightblue', lw=1, linewidth=3)
        
        #MLA
        axi.broken_barh([(9.9, 0.22)], (MLA1-MLA_err2s, MLA_err1s), facecolors=('lightsteelblue'))
        axi.broken_barh([(9.9, 0.22)], (MLA1-MLA_err1s,MLA_err1s), facecolors=('cornflowerblue'))
        axi.broken_barh([(9.9, 0.22)], (MLA1, MLA_err1s), facecolors=('cornflowerblue'))
        axi.broken_barh([(9.9, 0.22)], (MLA1+MLA_err1s, MLA_err1s), facecolors=('lightsteelblue'))
        axi.hlines(y=MLA1, xmin=10.09, xmax=9.9, color = 'midnightblue', lw=1, linewidth=3)
        
        plt.legend(loc='lower right')
        axi.set_ylim(ymin_,ymax_)
        axi.set_ylabel('Age'+" " +'(Ma)',labelpad=25)
        axi.set_xlabel('MDA Methods',labelpad=25)
        axi.set_xticks([0,1,2,3,4,5,6,7,8,9,10,11])
        axi.set_xticklabels(MDA_methods)
        axi.set_title(samples[0])
        axi.yaxis.grid(True)
        plt.margins(0.02)
        plt.subplots_adjust(bottom=0.15)
        MDAfig.tight_layout(pad=3)
                
        if Image_File_Option == 'web':
            filename = 'All_MDA_Methods_Plots_' + str(i)
            asset_folder = 'assets/plots/All_MDA_Methods_Plots/'
            for fileformat in ['.svg', '.tiff', '.eps', '.png', '.pdf', '.jpeg']:
                MDAfig.savefig(asset_folder + filename + fileformat)
            plt.close(MDAfig)   
        else:
            MDAfig.savefig('Saved_Files/All_MDA_Methods_Plots/All_MDA_Methods_Plots.' + Image_File_Option)   
       
    plt.close(MDAfig)        

    return MDAfig, MDA_plot_final

#Plot for All samples using one MDA method: Code by morganbrooks 

def MDA_Strat_Plot(YSG_MDA, YC1s_MDA, YC2s_MDA, YDZ_MDA, Y3Zo_MDA, Y3Za_MDA, Tau_MDA, YSP_MDA, YPP_MDA, MLA_MDA, ages, errors, sample_list, Image_File_Option, plotwidth, plotheight, MDA_Method):

    if not hasattr(ages[0], '__len__'):
        ages = [ages]
        errors = [errors]

    #Plotting    
    #YSG
    def YSG_Strat_Plot(YSG_MDA, sample_list, Image_File_Option):
        
        N = len(sample_list)
        sample_array = np.array(sample_list)
        sample_arrays = np.split(sample_array,len(sample_array))
        
        YSGfig, YSGaxi = plt.subplots(figsize=(plotwidth, plotheight))
        width = [] 
        
        #Setting up the x-axis placements
        for i in range(N): 
            samplesi = sample_list[i]

            def create_x(t, w, n, d):
                return [t*x + w*n for x in range(d)]

            t = 1 # sets of data
            w = 0.3 # We generally want bars to be 0.8
            n = 1 # first set of data
            d = len(sample_list) # topics we're plotting
            plot_x = create_x(t,w,n,d)
            middle = [ a / 2.0 for a in plot_x]
            middle_x_array = np.array(middle)
            x_arrays = np.split(middle_x_array,len(sample_list))
       
        YSG_array = np.array(YSG_MDA)
        YSGMDAs = YSG_array[:,0]        
        YSG_error1s = YSG_array[:,1]
        YSG_MDAs_arrays = np.split(YSGMDAs,len(YSGMDAs))
        YSG_error1s_arrays = np.split(YSG_error1s,len(YSGMDAs))   
        YSG_sorted = []
    
        for i in range(N):
            YSG_Zipped = list(zip(YSG_MDAs_arrays[i],YSG_error1s_arrays[i],sample_arrays[i]))
            YSG_Zipped.sort(key=lambda d: d[0])
            YSG_sorted.append([YSG_Zipped[0][0],YSG_Zipped[0][1],YSG_Zipped[0][2]])
            YSG_sorted.sort(reverse=True)
    
        YSG_sorted_array = np.array(YSG_sorted)
        YSG_MDA_sort = YSG_sorted_array[:,0]        
        YSG_error_sort = YSG_sorted_array[:,1]
        YSG_sample_sort = YSG_sorted_array[:,2]
        YSG_MDAs_sorted_arrays = np.split(YSG_MDA_sort,len(YSG_MDA_sort))
        YSG_error_sorted_arrays = np.split(YSG_error_sort,len(YSG_MDA_sort))
        YSG_sample_arrays = np.split(YSG_sample_sort,len(YSG_MDA_sort))
        YSG_Y_Max = np.array(YSG_MDA_sort, dtype='f')

        for i in range(N):
            samples = YSG_sample_arrays[i]
            x_arraysi = x_arrays[i]
            x_tick_adjust = 0
            width = 0
            YSG_MDAS_error_1s = list(zip(YSG_MDAs_sorted_arrays[i],YSG_error_sorted_arrays[i],x_arraysi,samples))
            
            for idx, (x, y, z, a) in enumerate(YSG_MDAS_error_1s): 
                YSG_MDAS_error_1s[idx] = (float(x), float(y), float(z), str(a)) 
                
            for l, m, n, o in YSG_MDAS_error_1s:    
                YSG_age_values = l 
                YSG_error1s_values = m
                YSG_age_plus_err = l+m
                YSG_error2s_values = m*2
                x_tick = n
                sample = o
                
                if N==1:
                    x_tick_adjust = 0.0002
                    width = 0.002
                    x_tick = 0
                    x_arrays = [0]
                
                if N==2:
                    x_tick_adjust = 0.002
                    width = 0.02
                
                if N>2:
                    x_tick_adjust = 0.002
                    width = 0.02
                
                if N>4:
                    x_tick_adjust = 0.006
                    width = 0.05
                
                if N>6:
                    x_tick_adjust = 0.006
                    width = 0.07
                
                if N>8:
                    x_tick_adjust = 0.009
                    width = 0.09
                
                if N>12:
                    width=0.11
                    x_tick_adjust=0.02
                
                if N>17:
                    width=0.12
                    x_tick_adjust=0.02
                
                if N>20:
                    width=0.17
                    x_tick_adjust=0.02
                
                YSGaxi.broken_barh([(x_tick, width)], (YSG_age_values-YSG_error2s_values, YSG_error1s_values), facecolors=('lightsteelblue'))
                YSGaxi.broken_barh([(x_tick, width)], (YSG_age_values-YSG_error1s_values,YSG_error1s_values), facecolors=('cornflowerblue'))
                YSGaxi.broken_barh([(x_tick, width)], (YSG_age_values, YSG_error1s_values), facecolors=('cornflowerblue'))
                YSGaxi.broken_barh([(x_tick, width)], (YSG_age_values+YSG_error1s_values, YSG_error1s_values), facecolors=('lightsteelblue'))   
                YSGaxi.hlines(y=YSG_age_values, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'midnightblue', lw=1,linewidth=3)
        
        for i in range(N):
            YSGaxi.set_xticks(x_arrays)
            YSGaxi.set_xticklabels(YSG_sample_sort,rotation='vertical') 
            
        YSGaxi.hlines(y=YSG_age_values, xmin=0, xmax=(0), color = 'midnightblue', lw=1, linewidth=3, label='MDA: YSG')
        YSGaxi.broken_barh([(0.15, 0)], (YSG_age_values,0), facecolors=('cornflowerblue'), label='1σ Uncertainty')
        YSGaxi.broken_barh([(0.15, 0)], (YSG_age_values,0), facecolors=('lightsteelblue'), label='2σ Uncertainty')

        YSGaxi.set_ylabel('Age'+" " +'(Ma)', labelpad=25)
        YSGaxi.set_yticks(np.arange(round(YSG_Y_Max[-1]-20),round(YSG_sorted[0][0]+20), 5))
        plt.gca().invert_yaxis()
        
        YSGaxi.yaxis.grid(True)
        YSGaxi.set_xlabel('Samples', labelpad=25)
        
        YSGaxi.set_title('YSG MDA: All Samples') 
        plt.legend(loc='upper left')
        
        if Image_File_Option == 'web':
            filename = 'YSG_All_Samples_Plot'
            asset_folder = 'assets/plots/Stratigraphic_Plots/'
            for fileformat in ['.svg', '.tiff', '.eps', '.png', '.pdf', '.jpeg']:
                YSGfig.savefig(asset_folder + filename + fileformat)
        else:
            YSGfig.savefig('Saved_Files/Stratigraphic_Plots/YSG_All_Samples_Plot.' + Image_File_Option)  
                
        plt.close(YSGfig)

        return YSGfig
       
    #YDZ
    def YDZ_Strat_Plot(YDZ_MDA, sample_list, Image_File_Option):
        
        #Sample_List
        N = len(sample_list)

        sample_array = np.array(sample_list)
        sample_arrays = np.split(sample_array,len(sample_array))
        
        #YDZ
        YDZ_array = np.array(YDZ_MDA)
        YDZ_MDAs = YDZ_array[:,0]
        YDZ_error1sP = YDZ_array[:,1]/2
        YDZ_error1sM = YDZ_array[:,2]/2
        YDZ_MDAs_arrays = np.split(YDZ_MDAs,len(YDZ_MDAs))
        YDZ_error1sP_arrays = np.split(YDZ_error1sP,len(YDZ_MDAs))
        YDZ_error1sM_arrays = np.split(YDZ_error1sM,len(YDZ_MDAs))
    
        YDZ_sorted = []
    
        for i in range(N):
            YDZ_Zipped = list(zip(YDZ_MDAs_arrays[i],YDZ_error1sP_arrays[i],YDZ_error1sM_arrays, sample_arrays[i]))
            YDZ_Zipped.sort(key=lambda d: d[0])
            YDZ_sorted.append([YDZ_Zipped[0][0],YDZ_Zipped[0][1],YDZ_Zipped[0][2],YDZ_Zipped[0][3]])
            YDZ_sorted.sort(reverse=True)
    
        YDZ_sorted_array = np.array(YDZ_sorted, dtype=object)
        
        YDZ_MDA_sort = YDZ_sorted_array[:,0]        
        YDZ_error1sP_sort = YDZ_sorted_array[:,1]
        YDZ_error1sM_sort = YDZ_sorted_array[:,2]
        YDZ_sample_sort = YDZ_sorted_array[:,3]
        YDZ_MDAs_sorted_arrays = np.split(YDZ_MDA_sort,len(YDZ_MDA_sort))
        YDZ_error1sP_sort_sorted_arrays = np.split(YDZ_error1sP_sort,len(YDZ_MDA_sort))
        YDZ_error1sM_sort_sorted_arrays = np.split(YDZ_error1sM_sort,len(YDZ_MDA_sort))
        YDZ_sample_arrays = np.split(YDZ_sample_sort,len(YDZ_MDA_sort))
        YDZ_Y_Max = np.array(YDZ_MDA_sort, dtype='f')
        
        #Setting up the x-axis placements
        for i in range(N): 
            samplesi = sample_list[i]

            def create_x(t, w, n, d):
                return [t*x + w*n for x in range(d)]

            t = 1 # sets of data
            w = 0.3 # We generally want bars to be 0.8
            n = 1 # first set of data
            d = len(sample_list) # topics we're plotting
            plot_x = create_x(t,w,n,d)
            middle = [ a / 2.0 for a in plot_x]
            middle_x_array = np.array(middle)
            x_arrays = np.split(middle_x_array,len(sample_list))

        YDZfig, YDZaxi = plt.subplots(figsize=(plotwidth, plotheight))
                
        for i in range(N):

            samples = YDZ_sample_arrays[i]
            x_arraysi = x_arrays[i]  
            
            x_tick_adjust = 0
            width = 0
            
            YDZ_MDAS_error_1s = list(zip(YDZ_MDAs_sorted_arrays[i],YDZ_error1sP_sort_sorted_arrays[i],YDZ_error1sM_sort_sorted_arrays[i],x_arraysi,samples))
            
            for idx, (a,b,c,d,e) in enumerate(YDZ_MDAS_error_1s): 
                YDZ_MDAS_error_1s[idx] = (float(a), float(b), float(c), float(d), str(e)) 
            
            for l, m, n, o, p in YDZ_MDAS_error_1s:    
                YDZ_age_values = l 
                YDZ_plus_1s = m
                YDZ_minus_1s = n
                YDZ_Plus_2s = m*2
                YDZ_Minus_2s = n*2
                x_tick = o
                sample = p
                
                if N==1:
                    x_tick_adjust = 0.0002
                    width = 0.002
                    x_tick = 0
                    x_arrays = [0]
                
                if N==2:
                    x_tick_adjust = 0.002
                    width = 0.02
                
                if N>2:
                    x_tick_adjust = 0.002
                    width = 0.02
                
                if N>4:
                    x_tick_adjust = 0.006
                    width = 0.05
                
                if N>6:
                    x_tick_adjust = 0.006
                    width = 0.07
                
                if N>8:
                    x_tick_adjust = 0.009
                    width = 0.09
                
                if N>12:
                    width=0.11
                    x_tick_adjust=0.02
                
                if N>17:
                    width=0.12
                    x_tick_adjust=0.02
                
                if N>20:
                    width=0.17
                    x_tick_adjust=0.02
                    
                YDZaxi.broken_barh([(x_tick, width)], (YDZ_age_values-YDZ_Minus_2s, YDZ_Minus_2s), facecolors=('lightsteelblue'))
                YDZaxi.broken_barh([(x_tick, width)], (YDZ_age_values-YDZ_minus_1s,YDZ_minus_1s), facecolors=('cornflowerblue'))
                YDZaxi.broken_barh([(x_tick, width)], (YDZ_age_values, YDZ_plus_1s), facecolors=('cornflowerblue'))
                YDZaxi.broken_barh([(x_tick, width)], (YDZ_age_values+YDZ_plus_1s, YDZ_plus_1s), facecolors=('lightsteelblue'))   
                YDZaxi.hlines(y=YDZ_age_values, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'midnightblue', lw=1,linewidth=3)
                    
        for i in range(N):
            YDZaxi.set_xticks(x_arrays)
            YDZaxi.set_xticklabels(YDZ_sample_sort, rotation='vertical')  
            
        YDZaxi.hlines(y=YDZ_age_values, xmin=0, xmax=(0), color = 'midnightblue', lw=1, linewidth=3, label='MDA: YDZ')
        YDZaxi.broken_barh([(0.15, 0)], (YDZ_age_values,0), facecolors=('cornflowerblue'), label='1σ Uncertainty')
        YDZaxi.broken_barh([(0.15, 0)], (YDZ_age_values,0), facecolors=('lightsteelblue'), label='2σ Uncertainty')
            
        YDZaxi.set_ylabel('Age'+" " +'(Ma)', labelpad=25)
        YDZaxi.yaxis.grid(True)
        
        YDZaxi.set_yticks(np.arange(round(YDZ_Y_Max[-1]-20),round(YDZ_sorted[0][0]+20), 5))
        
        plt.gca().invert_yaxis()
        
        YDZaxi.set_xlabel('Samples', labelpad=25)
      
        YDZaxi.set_title('YDZ MDA: All Samples') 
       
        plt.legend(loc='upper left')
   
        if Image_File_Option == 'web':
            filename = 'YDZ_All_Samples_Plot'
            asset_folder = 'assets/plots/Stratigraphic_Plots/'
            for fileformat in ['.svg', '.tiff', '.eps', '.png', '.pdf', '.jpeg']:
                YDZfig.savefig(asset_folder + filename + fileformat)
        else:
            YDZfig.savefig('Saved_Files/Stratigraphic_Plots/YDZ_All_Samples_Plot.' + Image_File_Option)  
                
        plt.close(YDZfig)
        
        return YDZfig
        
    #YC1s
    def YC1s_Strat_Plot(YC1s_MDA, sample_list, Image_File_Option):
        
        #Sample_List
        N = len(sample_list)
        sample_array = np.array(sample_list)
        sample_arrays = np.split(sample_array,len(sample_array))

        #Setting up the x-axis placements
        for i in range(N): 
            samplesi = sample_list[i]

            def create_x(t, w, n, d):
                return [t*x + w*n for x in range(d)]

            t = 1 # sets of data
            w = 0.3 # We generally want bars to be 0.8
            n = 1 # first set of data
            d = len(sample_list) # topics we're plotting
            plot_x = create_x(t,w,n,d)
            middle = [ a / 2.0 for a in plot_x]
            middle_x_array = np.array(middle)
            x_arrays = np.split(middle_x_array,len(sample_list))
            
        #YC1s
        YC1s_array = np.array(YC1s_MDA)
        YC1sMDAs = YC1s_array[:,0]        
        YC1s_error1s = YC1s_array[:,1]
        YC1s_MDAs_arrays = np.split(YC1sMDAs,len(YC1sMDAs))
        YC1s_error1s_arrays = np.split(YC1s_error1s,len(YC1sMDAs))
    
        YC1s_sorted = []
    
        for i in range(N):
            YC1s_Zipped = list(zip(YC1s_MDAs_arrays[i],YC1s_error1s_arrays[i],sample_arrays[i]))
            YC1s_Zipped.sort(key=lambda d: d[0])
            YC1s_sorted.append([YC1s_Zipped[0][0],YC1s_Zipped[0][1],YC1s_Zipped[0][2]])
            YC1s_sorted.sort(reverse=True)
    
        YC1s_sorted_array = np.array(YC1s_sorted)
        YC1s_MDA_sort = YC1s_sorted_array[:,0]        
        YC1s_error_sort = YC1s_sorted_array[:,1]
        YC1s_sample_sort = YC1s_sorted_array[:,2]
        YC1s_MDAs_sorted_arrays = np.split(YC1s_MDA_sort,len(YC1s_MDA_sort))
        YC1s_error_sorted_arrays = np.split(YC1s_error_sort,len(YC1s_MDA_sort))
        YC1s_sample_arrays = np.split(YC1s_sample_sort,len(YC1s_MDA_sort))
        YC1s_Y_Max = np.array(YC1s_MDA_sort, dtype='f')
        
        YC1sfig, YC1saxi = plt.subplots(figsize=(plotwidth, plotheight))
        width = []  

        for i in range(N):

            samples = YC1s_sample_arrays[i]
            x_arraysi = x_arrays[i]
            
            x_tick_adjust = 0
            width = 0
            
            YC1s_MDAS_error_1s = list(zip(YC1s_MDAs_sorted_arrays[i],YC1s_error_sorted_arrays[i],x_arraysi,samples))
            
            for idx, (x, y, z, a) in enumerate(YC1s_MDAS_error_1s): 
                YC1s_MDAS_error_1s[idx] = (float(x), float(y), float(z), str(a)) 
           
            for l, m, n, o in YC1s_MDAS_error_1s:
                YC1s_age_values = l 
                YC1s_error1s_values = m
                YC1s_age_plus_err = l+m
                YC1s_error2s_values = m*2
                x_tick = n
                samples = o
                
                if N==1:
                    x_tick_adjust = 0.0002
                    width = 0.002
                    x_tick = 0
                    x_arrays = [0]
                
                if N==2:
                    x_tick_adjust = 0.002
                    width = 0.02
                
                if N>2:
                    x_tick_adjust = 0.002
                    width = 0.02
                
                if N>4:
                    x_tick_adjust = 0.006
                    width = 0.05
                
                if N>6:
                    x_tick_adjust = 0.006
                    width = 0.07
                
                if N>8:
                    x_tick_adjust = 0.009
                    width = 0.09
                
                if N>12:
                    width=0.11
                    x_tick_adjust=0.02
                
                if N>17:
                    width=0.12
                    x_tick_adjust=0.02
                
                if N>20:
                    width=0.17
                    x_tick_adjust=0.02
                
                YC1saxi.broken_barh([(x_tick, width)], (YC1s_age_values-YC1s_error2s_values, YC1s_error1s_values), facecolors=('lightsteelblue'))
                YC1saxi.broken_barh([(x_tick, width)], (YC1s_age_values-YC1s_error1s_values,YC1s_error1s_values), facecolors=('cornflowerblue'))
                YC1saxi.broken_barh([(x_tick, width)], (YC1s_age_values, YC1s_error1s_values), facecolors=('cornflowerblue'))
                YC1saxi.broken_barh([(x_tick, width)], (YC1s_age_values+YC1s_error1s_values, YC1s_error1s_values), facecolors=('lightsteelblue'))   
                YC1saxi.hlines(y=YC1s_age_values, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'midnightblue', lw=1,linewidth=3)
                
        
        for i in range(N):
            YC1saxi.set_xticks(x_arrays)
            YC1saxi.set_xticklabels(YC1s_sample_sort, rotation='vertical') 
        
        YC1saxi.hlines(y=YC1s_age_values, xmin=0, xmax=(0), color = 'midnightblue', lw=1, linewidth=3, label='MDA: YC1s')
        YC1saxi.broken_barh([(0.15, 0)], (YC1s_age_values,0), facecolors=('cornflowerblue'), label='1σ Uncertainty')
        YC1saxi.broken_barh([(0.15, 0)], (YC1s_age_values,0), facecolors=('lightsteelblue'), label='2σ Uncertainty')

        YC1saxi.yaxis.grid(True)
       
        # YC1saxi.set_yticks(np.arange(round(YC1s_Y_Max[-1]-10),round(YC1s_sorted[0][0]+10), 2))
                
        plt.gca().invert_yaxis()
        YC1saxi.set_ylabel('Age'+" " +'(Ma)',labelpad=25)
        YC1saxi.set_xlabel('Samples', labelpad=25)
        
        YC1saxi.set_title('YC1σ MDA: All Samples') 
        plt.legend(loc='upper left')

        if Image_File_Option == 'web':
            filename = 'YC1s_All_Samples_Plot'
            asset_folder = 'assets/plots/Stratigraphic_Plots/'
            for fileformat in ['.svg', '.tiff', '.eps', '.png', '.pdf', '.jpeg']:
                YC1sfig.savefig(asset_folder + filename + fileformat)
        else:
            YC1sfig.savefig('Saved_Files/Stratigraphic_Plots/YC1s_All_Samples_Plot.' + Image_File_Option)  
                
        plt.close(YC1sfig)
        
        return YC1sfig
    
    #YC2s
    def YC2s_Strat_Plot(YC2s_MDA, sample_list, Image_File_Option):
        
        #Sample_List
        N = len(sample_list)
        sample_array = np.array(sample_list)
        sample_arrays = np.split(sample_array,len(sample_array))

        #Setting up the x-axis placements
        for i in range(N): 
            samplesi = sample_list[i]

            def create_x(t, w, n, d):
                return [t*x + w*n for x in range(d)]

            t = 1 # sets of data
            w = 0.3 # We generally want bars to be 0.8
            n = 1 # first set of data
            d = len(sample_list) # topics we're plotting
            plot_x = create_x(t,w,n,d)
            middle = [ a / 2.0 for a in plot_x]
            middle_x_array = np.array(middle)
            x_arrays = np.split(middle_x_array,len(sample_list))

        
        YC2sfig, YC2saxi = plt.subplots(figsize=(plotwidth, plotheight))
        width = []  
        
        YC2s_array = np.array(YC2s_MDA)
        YC2s_MDAs = YC2s_array[:,0]
        YC2s_error1s = YC2s_array[:,1]
        YC2s_MDAs_arrays = np.split(YC2s_MDAs,len(YC2s_MDAs))
        YC2s_error1s_arrays = np.split(YC2s_error1s,len(YC2s_MDAs))
    
        YC2s_sorted = []
    
        for i in range(N):
            YC2s_Zipped = list(zip(YC2s_MDAs_arrays[i],YC2s_error1s_arrays[i],sample_arrays[i]))
            YC2s_Zipped.sort(key=lambda d: d[0])
            YC2s_sorted.append([YC2s_Zipped[0][0],YC2s_Zipped[0][1],YC2s_Zipped[0][2]])
            YC2s_sorted.sort(reverse=True)
    
        YC2s_sorted_array = np.array(YC2s_sorted)
        YC2s_MDA_sort = YC2s_sorted_array[:,0]        
        YC2s_error_sort = YC2s_sorted_array[:,1]
        YC2s_sample_sort = YC2s_sorted_array[:,2]
        YC2s_MDAs_sorted_arrays = np.split(YC2s_MDA_sort,len(YC2s_MDA_sort))
        YC2s_error_sorted_arrays = np.split(YC2s_error_sort,len(YC2s_MDA_sort))
        YC2s_sample_arrays = np.split(YC2s_sample_sort,len(YC2s_MDA_sort))
        YC2s_Y_Max = np.array(YC2s_MDA_sort, dtype='f')

        for i in range(N):

            samples = YC2s_sample_arrays[i]
            x_arraysi = x_arrays[i]
            
            x_tick_adjust = 0
            width = 0
            
            YC2s_MDAS_error_1s = list(zip(YC2s_MDAs_sorted_arrays[i],YC2s_error_sorted_arrays[i],x_arraysi,samples))
            
            for idx, (x, y, z, a) in enumerate(YC2s_MDAS_error_1s): 
                YC2s_MDAS_error_1s[idx] = (float(x), float(y), float(z), str(a)) 
           
            for l, m, n, o in YC2s_MDAS_error_1s:
                YC2s_age_values = l 
                YC2s_error1s_values = m
                YC2s_age_plus_err = l+m
                YC2s_error2s_values = m*2
                x_tick = n
                samples = o
                
                if N==1:
                    x_tick_adjust = 0.0002
                    width = 0.002
                    x_tick = 0
                    x_arrays = [0]
                
                if N==2:
                    x_tick_adjust = 0.002
                    width = 0.02
                
                if N>2:
                    x_tick_adjust = 0.002
                    width = 0.02
                
                if N>4:
                    x_tick_adjust = 0.006
                    width = 0.05
                
                if N>6:
                    x_tick_adjust = 0.006
                    width = 0.07
                
                if N>8:
                    x_tick_adjust = 0.009
                    width = 0.09
                
                if N>12:
                    width=0.11
                    x_tick_adjust=0.02
                
                if N>17:
                    width=0.12
                    x_tick_adjust=0.02
                
                if N>20:
                    width=0.17
                    x_tick_adjust=0.02
                
                YC2saxi.broken_barh([(x_tick, width)], (YC2s_age_values-YC2s_error2s_values, YC2s_error1s_values), facecolors=('lightsteelblue'))
                YC2saxi.broken_barh([(x_tick, width)], (YC2s_age_values-YC2s_error1s_values,YC2s_error1s_values), facecolors=('cornflowerblue'))
                YC2saxi.broken_barh([(x_tick, width)], (YC2s_age_values, YC2s_error1s_values), facecolors=('cornflowerblue'))
                YC2saxi.broken_barh([(x_tick, width)], (YC2s_age_values+YC2s_error1s_values, YC2s_error1s_values), facecolors=('lightsteelblue'))   
                YC2saxi.hlines(y=YC2s_age_values, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'midnightblue', lw=1,linewidth=3)
                
        
        for i in range(N):
            YC2saxi.set_xticks(x_arrays)
            YC2saxi.set_xticklabels(YC2s_sample_sort, rotation='vertical') 
        
        YC2saxi.hlines(y=YC2s_age_values, xmin=0, xmax=(0), color = 'midnightblue', lw=1, linewidth=3, label='MDA: YC2σ')
        YC2saxi.broken_barh([(0.15, 0)], (YC2s_age_values,0), facecolors=('cornflowerblue'), label='1σ Uncertainty')
        YC2saxi.broken_barh([(0.15, 0)], (YC2s_age_values,0), facecolors=('lightsteelblue'), label='2σ Uncertainty')
    
        
        YC2saxi.set_ylabel('Age'+" " +'(Ma)',labelpad=25)
        YC2saxi.yaxis.grid(True)  
       
        YC2saxi.set_yticks(np.arange(round(YC2s_Y_Max[-1]-10),round(YC2s_sorted[0][0]+10), 2))
        
        plt.gca().invert_yaxis()
        YC2saxi.set_xlabel('Samples', labelpad=25)
        
        YC2saxi.set_title('YC2σ MDA: All Samples') 
        plt.legend(loc='upper left')
        
        if Image_File_Option == 'web':
            filename = 'YC2s_All_Samples_Plot'
            asset_folder = 'assets/plots/Stratigraphic_Plots/'
            for fileformat in ['.svg', '.tiff', '.eps', '.png', '.pdf', '.jpeg']:
                YC2sfig.savefig(asset_folder + filename + fileformat)
        else:
            YC2sfig.savefig('Saved_Files/Stratigraphic_Plots/YC2s_All_Samples_Plot.' + Image_File_Option)  
                
        plt.close(YC2sfig)
        
        return YC2sfig
    
    #Y3Zo
    def Y3Zo_Strat_Plot(Y3Zo_MDA, sample_list, Image_File_Option):
      
        N = len(sample_list)
        sample_array = np.array(sample_list)
        sample_arrays = np.split(sample_array,len(sample_array))

        #Setting up the x-axis placements
        for i in range(N): 
            samplesi = sample_list[i]

            def create_x(t, w, n, d):
                return [t*x + w*n for x in range(d)]

            t = 1 # sets of data
            w = 0.3 # We generally want bars to be 0.8
            n = 1 # first set of data
            d = len(sample_list) # topics we're plotting
            plot_x = create_x(t,w,n,d)
            middle = [ a / 2.0 for a in plot_x]
            middle_x_array = np.array(middle)
            x_arrays = np.split(middle_x_array,len(sample_list))
            
        #Y3Zo
        Y3Zo_array = np.array(Y3Zo_MDA)
        Y3Zo_MDAs = Y3Zo_array[:,0]
        Y3Zo_error1s = Y3Zo_array[:,1]
        Y3Zo_MDAs_arrays = np.split(Y3Zo_MDAs,len(Y3Zo_MDAs))
        Y3Zo_error1s_arrays = np.split(Y3Zo_error1s,len(Y3Zo_MDAs))
    
        Y3Zo_sorted = []
    
        for i in range(N):
            Y3Zo_Zipped = list(zip(Y3Zo_MDAs_arrays[i],Y3Zo_error1s_arrays[i],sample_arrays[i]))
            Y3Zo_Zipped.sort(key=lambda d: d[0])
            Y3Zo_sorted.append([Y3Zo_Zipped[0][0],Y3Zo_Zipped[0][1],Y3Zo_Zipped[0][2]])
            Y3Zo_sorted.sort(reverse=True)
    
        Y3Zo_sorted_array = np.array(Y3Zo_sorted)
        Y3Zo_MDA_sort = Y3Zo_sorted_array[:,0]        
        Y3Zo_error_sort = Y3Zo_sorted_array[:,1]
        Y3Zo_sample_sort = Y3Zo_sorted_array[:,2]
        Y3Zo_MDAs_sorted_arrays = np.split(Y3Zo_MDA_sort,len(Y3Zo_MDA_sort))
        Y3Zo_error_sorted_arrays = np.split(Y3Zo_error_sort,len(Y3Zo_MDA_sort))
        Y3Zo_sample_arrays = np.split(Y3Zo_sample_sort,len(Y3Zo_MDA_sort))
        Y3Zo_Y_Max = np.array(Y3Zo_MDA_sort, dtype='f')
        
        Y3Zofig, Y3Zoaxi = plt.subplots(figsize=(plotwidth, plotheight))
        width = []  

        for i in range(N):

            samples = Y3Zo_sample_arrays[i]
            x_arraysi = x_arrays[i]  
            
            x_tick_adjust = 0
            width = 0
            
            Y3Zo_MDAS_error_1s = list(zip(Y3Zo_MDAs_sorted_arrays[i],Y3Zo_error_sorted_arrays[i],x_arraysi,samples))
            
            for idx, (x, y, z, a) in enumerate(Y3Zo_MDAS_error_1s): 
                Y3Zo_MDAS_error_1s[idx] = (float(x), float(y), float(z), str(a)) 
           
            for l, m, n, o in Y3Zo_MDAS_error_1s:
                Y3Zo_age_values = l 
                Y3Zo_error1s_values = m
                Y3Zo_age_plus_err = l+m
                Y3Zo_error2s_values = m*2
                x_tick = n
                samples = o
                
                if N==1:
                    x_tick_adjust = 0.0002
                    width = 0.002
                    x_tick = 0
                    x_arrays = [0]
                
                if N==2:
                    x_tick_adjust = 0.002
                    width = 0.02
                
                if N>2:
                    x_tick_adjust = 0.002
                    width = 0.02
                
                if N>4:
                    x_tick_adjust = 0.006
                    width = 0.05
                
                if N>6:
                    x_tick_adjust = 0.006
                    width = 0.07
                
                if N>8:
                    x_tick_adjust = 0.009
                    width = 0.09
                
                if N>12:
                    width=0.11
                    x_tick_adjust=0.02
                
                if N>17:
                    width=0.12
                    x_tick_adjust=0.02
                
                if N>20:
                    width=0.17
                    x_tick_adjust=0.02
                
                Y3Zoaxi.broken_barh([(x_tick, width)], (Y3Zo_age_values-Y3Zo_error2s_values, Y3Zo_error1s_values), facecolors=('lightsteelblue'))
                Y3Zoaxi.broken_barh([(x_tick, width)], (Y3Zo_age_values-Y3Zo_error1s_values,Y3Zo_error1s_values), facecolors=('cornflowerblue'))
                Y3Zoaxi.broken_barh([(x_tick, width)], (Y3Zo_age_values, Y3Zo_error1s_values), facecolors=('cornflowerblue'))
                Y3Zoaxi.broken_barh([(x_tick, width)], (Y3Zo_age_values+Y3Zo_error1s_values, Y3Zo_error1s_values), facecolors=('lightsteelblue'))   
                Y3Zoaxi.hlines(y=Y3Zo_age_values, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'midnightblue', lw=1,linewidth=3)
                
        
        for i in range(N):
            Y3Zoaxi.set_xticks(x_arrays)
            Y3Zoaxi.set_xticklabels(Y3Zo_sample_sort, rotation='vertical') 
        
        Y3Zoaxi.hlines(y=Y3Zo_age_values, xmin=0, xmax=(0), color = 'midnightblue', lw=1, linewidth=3, label='MDA: Y3Zo')
        Y3Zoaxi.broken_barh([(0.15, 0)], (Y3Zo_age_values,0), facecolors=('cornflowerblue'), label='1σ Uncertainty')
        Y3Zoaxi.broken_barh([(0.15, 0)], (Y3Zo_age_values,0), facecolors=('lightsteelblue'), label='2σ Uncertainty')
    
        Y3Zoaxi.set_ylabel('Age'+" " +'(Ma)',labelpad=25)
        Y3Zoaxi.yaxis.grid(True)  
        
        Y3Zoaxi.set_yticks(np.arange(round(Y3Zo_Y_Max[-1]-20),round(Y3Zo_sorted[0][0]+20), 5))
        
        plt.gca().invert_yaxis()
        Y3Zoaxi.set_xlabel('Samples', labelpad=25)
        
        Y3Zoaxi.set_title('Y3Zo MDA: All Samples') 
        plt.legend(loc='upper left')

        if Image_File_Option == 'web':
            filename = 'Y3Zo_All_Samples_Plot'
            asset_folder = 'assets/plots/Stratigraphic_Plots/'
            for fileformat in ['.svg', '.tiff', '.eps', '.png', '.pdf', '.jpeg']:
                Y3Zofig.savefig(asset_folder + filename + fileformat)
        else:
            Y3Zofig.savefig('Saved_Files/Stratigraphic_Plots/Y3Zo_All_Samples_Plot.' + Image_File_Option)  
                
        plt.close(Y3Zofig)
        
        return Y3Zofig
        
    #Tau
    def Tau_Strat_Plot(Tau_MDA, sample_list, Image_File_Option):
        
        N = len(sample_list)
        sample_array = np.array(sample_list)
        sample_arrays = np.split(sample_array,len(sample_array))

        #Setting up the x-axis placements
        for i in range(N): 
            samplesi = sample_list[i]

            def create_x(t, w, n, d):
                return [t*x + w*n for x in range(d)]

            t = 1 # sets of data
            w = 0.3 # We generally want bars to be 0.8
            n = 1 # first set of data
            d = len(sample_list) # topics we're plotting
            plot_x = create_x(t,w,n,d)
            middle = [ a / 2.0 for a in plot_x]
            middle_x_array = np.array(middle)
            x_arrays = np.split(middle_x_array,len(sample_list))

        #Tau
        Tau_array = np.array(Tau_MDA)
        Tau_MDAs = Tau_array[:,0]
        Tau_error1s = Tau_array[:,1]
        Tau_MDAs_arrays = np.split(Tau_MDAs,len(Tau_MDAs))
        Tau_error1s_arrays = np.split(Tau_error1s,len(Tau_MDAs))
    
        Tau_sorted = []
    
        for i in range(N):
            Tau_Zipped = list(zip(Tau_MDAs_arrays[i],Tau_error1s_arrays[i],sample_arrays[i]))
            Tau_Zipped.sort(key=lambda d: d[0])
            Tau_sorted.append([Tau_Zipped[0][0],Tau_Zipped[0][1],Tau_Zipped[0][2]])
            Tau_sorted.sort(reverse=True)
    
        Tau_sorted_array = np.array(Tau_sorted)
        Tau_MDA_sort = Tau_sorted_array[:,0]        
        Tau_error_sort = Tau_sorted_array[:,1]
        Tau_sample_sort = Tau_sorted_array[:,2]
        Tau_MDAs_sorted_arrays = np.split(Tau_MDA_sort,len(Tau_MDA_sort))
        Tau_error_sorted_arrays = np.split(Tau_error_sort,len(Tau_MDA_sort))
        Tau_sample_arrays = np.split(Tau_sample_sort,len(Tau_MDA_sort))
        Tau_Y_Max = np.array(Tau_MDA_sort, dtype='f')

        Taufig, Tauaxi = plt.subplots(figsize=(plotwidth, plotheight))
        width = []  

        for i in range(N):

            samples = Tau_sample_arrays[i]
            x_arraysi = x_arrays[i]  
            
            x_tick_adjust = 0
            width = 0
            
            Tau_MDAS_error_1s = list(zip(Tau_MDAs_sorted_arrays[i],Tau_error_sorted_arrays[i],x_arraysi,samples))
            
            for idx, (x, y, z, a) in enumerate(Tau_MDAS_error_1s): 
                Tau_MDAS_error_1s[idx] = (float(x), float(y), float(z), str(a)) 
           
            for l, m, n, o in Tau_MDAS_error_1s:
                Tau_age_values = l 
                Tau_error1s_values = m
                Tau_age_plus_err = l+m
                Tau_error2s_values = m*2
                x_tick = n
                samples = o
                
                if N==1:
                    x_tick_adjust = 0.0002
                    width = 0.002
                    x_tick = 0
                    x_arrays = [0]
                
                if N==2:
                    x_tick_adjust = 0.002
                    width = 0.02
                
                if N>2:
                    x_tick_adjust = 0.002
                    width = 0.02
                
                if N>4:
                    x_tick_adjust = 0.006
                    width = 0.05
                
                if N>6:
                    x_tick_adjust = 0.006
                    width = 0.07
                
                if N>8:
                    x_tick_adjust = 0.009
                    width = 0.09
                
                if N>12:
                    width=0.11
                    x_tick_adjust=0.02
                
                if N>17:
                    width=0.12
                    x_tick_adjust=0.02
                
                if N>20:
                    width=0.17
                    x_tick_adjust=0.02
                
                Tauaxi.broken_barh([(x_tick, width)], (Tau_age_values-Tau_error2s_values, Tau_error1s_values), facecolors=('lightsteelblue'))
                Tauaxi.broken_barh([(x_tick, width)], (Tau_age_values-Tau_error1s_values,Tau_error1s_values), facecolors=('cornflowerblue'))
                Tauaxi.broken_barh([(x_tick, width)], (Tau_age_values, Tau_error1s_values), facecolors=('cornflowerblue'))
                Tauaxi.broken_barh([(x_tick, width)], (Tau_age_values+Tau_error1s_values, Tau_error1s_values), facecolors=('lightsteelblue'))   
                Tauaxi.hlines(y=Tau_age_values, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'midnightblue', lw=1,linewidth=3)
                
        
        for i in range(N):
            Tauaxi.set_xticks(x_arrays)
            Tauaxi.set_xticklabels(Tau_sample_sort, rotation='vertical') 
        
        Tauaxi.hlines(y=Tau_age_values, xmin=0, xmax=(0), color = 'midnightblue', lw=1, linewidth=3, label='MDA: Tau')
        Tauaxi.broken_barh([(0.15, 0)], (Tau_age_values,0), facecolors=('cornflowerblue'), label='1σ Uncertainty')
        Tauaxi.broken_barh([(0.15, 0)], (Tau_age_values,0), facecolors=('lightsteelblue'), label='2σ Uncertainty')
    
        Tauaxi.set_ylabel('Age'+" " +'(Ma)',labelpad=25)
        Tauaxi.yaxis.grid(True)  
       
        Tauaxi.set_yticks(np.arange(round(Tau_Y_Max[-1]-10),round(Tau_sorted[0][0]+10), 2))
        
        
        plt.gca().invert_yaxis()
        Tauaxi.set_xlabel('Samples', labelpad=25)
        
        Tauaxi.set_title('Tau MDA: All Samples') 
        plt.legend(loc='upper left')

        if Image_File_Option == 'web':
            filename = 'Tau_All_Samples_Plot'
            asset_folder = 'assets/plots/Stratigraphic_Plots/'
            for fileformat in ['.svg', '.tiff', '.eps', '.png', '.pdf', '.jpeg']:
                Taufig.savefig(asset_folder + filename + fileformat)
        else:
            Taufig.savefig('Saved_Files/Stratigraphic_Plots/Tau_All_Samples_Plot.' + Image_File_Option)  
                
        plt.close(Taufig)
        
        return Taufig

    #Y3Za
    def Y3Za_Strat_Plot(Y3Za_MDA, sample_list, Image_File_Option):
        
        N = len(sample_list)
        sample_array = np.array(sample_list)
        sample_arrays = np.split(sample_array,len(sample_array))

        #Setting up the x-axis placements
        for i in range(N): 
            samplesi = sample_list[i]

            def create_x(t, w, n, d):
                return [t*x + w*n for x in range(d)]

            t = 1 # sets of data
            w = 0.3 # We generally want bars to be 0.8
            n = 1 # first set of data
            d = len(sample_list) # topics we're plotting
            plot_x = create_x(t,w,n,d)
            middle = [ a / 2.0 for a in plot_x]
            middle_x_array = np.array(middle)
            x_arrays = np.split(middle_x_array,len(sample_list))
            
        #Y3Za
        Y3Za_array = np.array(Y3Za_MDA)
        Y3Za_MDAs = Y3Za_array[:,0]
        Y3Za_error1s = Y3Za_array[:,1]
        Y3Za_MDAs_arrays = np.split(Y3Za_MDAs,len(Y3Za_MDAs))
        Y3Za_error1s_arrays = np.split(Y3Za_error1s,len(Y3Za_MDAs))
    
        Y3Za_sorted = []
    
        for i in range(N):
            Y3Za_Zipped = list(zip(Y3Za_MDAs_arrays[i],Y3Za_error1s_arrays[i],sample_arrays[i]))
            Y3Za_Zipped.sort(key=lambda d: d[0])
            Y3Za_sorted.append([Y3Za_Zipped[0][0],Y3Za_Zipped[0][1],Y3Za_Zipped[0][2]])
            Y3Za_sorted.sort(reverse=True)
    
        Y3Za_sorted_array = np.array(Y3Za_sorted)
        Y3Za_MDA_sort = Y3Za_sorted_array[:,0]        
        Y3Za_error_sort = Y3Za_sorted_array[:,1]
        Y3Za_sample_sort = Y3Za_sorted_array[:,2]
        Y3Za_MDAs_sorted_arrays = np.split(Y3Za_MDA_sort,len(Y3Za_MDA_sort))
        Y3Za_error_sorted_arrays = np.split(Y3Za_error_sort,len(Y3Za_MDA_sort))
        Y3Za_sample_arrays = np.split(Y3Za_sample_sort,len(Y3Za_MDA_sort))
        Y3Za_Y_Max = np.array(Y3Za_MDA_sort, dtype='f')

        Y3Zafig, Y3Zaaxi = plt.subplots(figsize=(plotwidth, plotheight))
        width = []  

        for i in range(N):

            samples = Y3Za_sample_arrays[i]
            x_arraysi = x_arrays[i]  
            
            x_tick_adjust = 0
            width = 0
            
            Y3Za_MDAS_error_1s = list(zip(Y3Za_MDAs_sorted_arrays[i],Y3Za_error_sorted_arrays[i],x_arraysi,samples))
            
            for idx, (x, y, z, a) in enumerate(Y3Za_MDAS_error_1s): 
                Y3Za_MDAS_error_1s[idx] = (float(x), float(y), float(z), str(a)) 
           
            for l, m, n, o in Y3Za_MDAS_error_1s:
                Y3Za_age_values = l 
                Y3Za_error1s_values = m
                Y3Za_age_plus_err = l+m
                Y3Za_error2s_values = m*2
                x_tick = n
                samples = o
                
                if N==1:
                    x_tick_adjust = 0.0002
                    width = 0.002
                    x_tick = 0
                    x_arrays = [0]
                
                if N==2:
                    x_tick_adjust = 0.002
                    width = 0.02
                
                if N>2:
                    x_tick_adjust = 0.002
                    width = 0.02
                    
                if N>4:
                    x_tick_adjust = 0.006
                    width = 0.05
                
                if N>6:
                    x_tick_adjust = 0.006
                    width = 0.07
                
                if N>8:
                    x_tick_adjust = 0.009
                    width = 0.09
                
                if N>12:
                    width=0.11
                    x_tick_adjust=0.02
                
                if N>17:
                    width=0.12
                    x_tick_adjust=0.02
                
                if N>20:
                    width=0.17
                    x_tick_adjust=0.02
                
                Y3Zaaxi.broken_barh([(x_tick, width)], (Y3Za_age_values-Y3Za_error2s_values, Y3Za_error1s_values), facecolors=('lightsteelblue'))
                Y3Zaaxi.broken_barh([(x_tick, width)], (Y3Za_age_values-Y3Za_error1s_values,Y3Za_error1s_values), facecolors=('cornflowerblue'))
                Y3Zaaxi.broken_barh([(x_tick, width)], (Y3Za_age_values, Y3Za_error1s_values), facecolors=('cornflowerblue'))
                Y3Zaaxi.broken_barh([(x_tick, width)], (Y3Za_age_values+Y3Za_error1s_values, Y3Za_error1s_values), facecolors=('lightsteelblue'))   
                Y3Zaaxi.hlines(y=Y3Za_age_values, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'midnightblue', lw=1,linewidth=3)
                
        
        for i in range(N):
            Y3Zaaxi.set_xticks(x_arrays)
            Y3Zaaxi.set_xticklabels(Y3Za_sample_sort, rotation='vertical') 
        
        Y3Zaaxi.hlines(y=Y3Za_age_values, xmin=0, xmax=(0), color = 'midnightblue', lw=1, linewidth=3, label='MDA: Y3Za')
        Y3Zaaxi.broken_barh([(0.15, 0)], (Y3Za_age_values,0), facecolors=('cornflowerblue'), label='1σ Uncertainty')
        Y3Zaaxi.broken_barh([(0.15, 0)], (Y3Za_age_values,0), facecolors=('lightsteelblue'), label='2σ Uncertainty')
    
        Y3Zaaxi.set_ylabel('Age'+" " +'(Ma)',labelpad=25)
        Y3Zaaxi.yaxis.grid(True)  
        
        Y3Zaaxi.set_yticks(np.arange(round(Y3Za_Y_Max[-1]-20),round(Y3Za_sorted[0][0]+20), 5))
        
        plt.gca().invert_yaxis()
        Y3Zaaxi.set_xlabel('Samples', labelpad=25)
        
        Y3Zaaxi.set_title('Y3Za MDA: All Samples') 
        plt.legend(loc='upper left')

        if Image_File_Option == 'web':
            filename = 'Y3Za_All_Samples_Plot'
            asset_folder = 'assets/plots/Stratigraphic_Plots/'
            for fileformat in ['.svg', '.tiff', '.eps', '.png', '.pdf', '.jpeg']:
                Y3Zafig.savefig(asset_folder + filename + fileformat)
        else:
            Y3Zafig.savefig('Saved_Files/Stratigraphic_Plots/Y3Za_All_Samples_Plot.' + Image_File_Option)  
                
        plt.close(Y3Zafig)
        
        return Y3Zafig

    #YSP
    def YSP_Strat_Plot(YSP_MDA, sample_list, Image_File_Option):
        
        N = len(sample_list)
        sample_array = np.array(sample_list)
        sample_arrays = np.split(sample_array,len(sample_array))

        #Setting up the x-axis placements
        for i in range(N): 
            samplesi = sample_list[i]

            def create_x(t, w, n, d):
                return [t*x + w*n for x in range(d)]

            t = 1 # sets of data
            w = 0.3 # We generally want bars to be 0.8
            n = 1 # first set of data
            d = len(sample_list) # topics we're plotting
            plot_x = create_x(t,w,n,d)
            middle = [ a / 2.0 for a in plot_x]
            middle_x_array = np.array(middle)
            x_arrays = np.split(middle_x_array,len(sample_list))

        YSP_array = np.array(YSP_MDA)
        YSP_MDAs = YSP_array[:,0]
        YSP_error1s = YSP_array[:,1]
        YSP_MDAs_arrays = np.split(YSP_MDAs,len(YSP_MDAs))
        YSP_error1s_arrays = np.split(YSP_error1s,len(YSP_MDAs))
    
        YSP_sorted = []
    
        for i in range(N):
            YSP_Zipped = list(zip(YSP_MDAs_arrays[i],YSP_error1s_arrays[i],sample_arrays[i]))
            YSP_Zipped.sort(key=lambda d: d[0])
            YSP_sorted.append([YSP_Zipped[0][0],YSP_Zipped[0][1],YSP_Zipped[0][2]])
            YSP_sorted.sort(reverse=True)
    
        YSP_sorted_array = np.array(YSP_sorted)
        YSP_MDA_sort = YSP_sorted_array[:,0]        
        YSP_error_sort = YSP_sorted_array[:,1]
        YSP_sample_sort = YSP_sorted_array[:,2]
        YSP_MDAs_sorted_arrays = np.split(YSP_MDA_sort,len(YSP_MDA_sort))
        YSP_error_sorted_arrays = np.split(YSP_error_sort,len(YSP_MDA_sort))
        YSP_sample_arrays = np.split(YSP_sample_sort,len(YSP_MDA_sort))
        YSP_Y_Max = np.array(YSP_MDA_sort, dtype='f')

        
        YSPfig, YSPaxi = plt.subplots(figsize=(plotwidth, plotheight))
        width = []  

        for i in range(N):

            samples = YSP_sample_arrays[i]
            x_arraysi = x_arrays[i]  
            
            x_tick_adjust = 0
            width = 0
            
            YSP_MDAS_error_1s = list(zip(YSP_MDAs_sorted_arrays[i],YSP_error_sorted_arrays[i],x_arraysi,samples))
            
            for idx, (x, y, z, a) in enumerate(YSP_MDAS_error_1s): 
                YSP_MDAS_error_1s[idx] = (float(x), float(y), float(z), str(a)) 
           
            for l, m, n, o in YSP_MDAS_error_1s:
                YSP_age_values = l 
                YSP_error1s_values = m
                YSP_age_plus_err = l+m
                YSP_error2s_values = m*2
                x_tick = n
                samples = o
                
                if N==1:
                    x_tick_adjust = 0.0002
                    width = 0.002
                    x_tick = 0
                    x_arrays = [0]
                
                if N==2:
                    x_tick_adjust = 0.002
                    width = 0.02
                
                if N>2:
                    x_tick_adjust = 0.002
                    width = 0.02
                    
                if N>4:
                    x_tick_adjust = 0.006
                    width = 0.05
                
                if N>6:
                    x_tick_adjust = 0.006
                    width = 0.07
                
                if N>8:
                    x_tick_adjust = 0.009
                    width = 0.09
                
                if N>12:
                    width=0.11
                    x_tick_adjust=0.02
                
                if N>17:
                    width=0.12
                    x_tick_adjust=0.02
                
                if N>20:
                    width=0.17
                    x_tick_adjust=0.02
                
                YSPaxi.broken_barh([(x_tick, width)], (YSP_age_values-YSP_error2s_values, YSP_error1s_values), facecolors=('lightsteelblue'))
                YSPaxi.broken_barh([(x_tick, width)], (YSP_age_values-YSP_error1s_values,YSP_error1s_values), facecolors=('cornflowerblue'))
                YSPaxi.broken_barh([(x_tick, width)], (YSP_age_values, YSP_error1s_values), facecolors=('cornflowerblue'))
                YSPaxi.broken_barh([(x_tick, width)], (YSP_age_values+YSP_error1s_values, YSP_error1s_values), facecolors=('lightsteelblue'))   
                YSPaxi.hlines(y=YSP_age_values, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'midnightblue', lw=1,linewidth=3)
                
        
        for i in range(N):
            YSPaxi.set_xticks(x_arrays)
            YSPaxi.set_xticklabels(YSP_sample_sort, rotation='vertical') 
        
        YSPaxi.hlines(y=YSP_age_values, xmin=0, xmax=(0), color = 'midnightblue', lw=1, linewidth=3, label='MDA: YSP')
        YSPaxi.broken_barh([(0.15, 0)], (YSP_age_values,0), facecolors=('cornflowerblue'), label='1σ Uncertainty')
        YSPaxi.broken_barh([(0.15, 0)], (YSP_age_values,0), facecolors=('lightsteelblue'), label='2σ Uncertainty')
    
        YSPaxi.set_ylabel('Age'+" " +'(Ma)',labelpad=25)
        YSPaxi.yaxis.grid(True)  
       
        YSPaxi.set_yticks(np.arange(round(YSP_Y_Max[-1]-10),round(YSP_sorted[0][0]+10), 2))
        
        plt.gca().invert_yaxis()
        YSPaxi.set_xlabel('Samples', labelpad=25)
        
        YSPaxi.set_title('YSP MDA: All Samples') 
        plt.legend(loc='upper left')

        if Image_File_Option == 'web':
            filename = 'YSP_All_Samples_Plot'
            asset_folder = 'assets/plots/Stratigraphic_Plots/'
            for fileformat in ['.svg', '.tiff', '.eps', '.png', '.pdf', '.jpeg']:
                YSPfig.savefig(asset_folder + filename + fileformat)
        else:
            YSPfig.savefig('Saved_Files/Stratigraphic_Plots/YSP_All_Samples_Plot.' + Image_File_Option)  
                
        plt.close(YSPfig)

        return YSPfig

    #YPP
    def YPP_Strat_Plot(YPP_MDA, sample_list, Image_File_Option):
        
        N = len(sample_list)
        sample_array = np.array(sample_list)
        sample_arrays = np.split(sample_array,len(sample_array))

        #Setting up the x-axis placements
        for i in range(N): 
            samplesi = sample_list[i]

            def create_x(t, w, n, d):
                return [t*x + w*n for x in range(d)]

            t = 1 # sets of data
            w = 0.3 # We generally want bars to be 0.8
            n = 1 # first set of data
            d = len(sample_list) # topics we're plotting
            plot_x = create_x(t,w,n,d)
            middle = [ a / 2.0 for a in plot_x]
            middle_x_array = np.array(middle)
            x_arrays = np.split(middle_x_array,len(sample_list))

        YPP_array = np.array(YPP_MDA)
        YPP_MDAs_arrays = np.split(YPP_array,len(YPP_array))
    
        YPP_sorted = []
    
        for i in range(N):
            YPP_Zipped = list(zip(YPP_MDAs_arrays[i],sample_arrays[i]))
            YPP_Zipped.sort(key=lambda d: d[0])
            YPP_sorted.append([YPP_Zipped[0][0],YPP_Zipped[0][1]])
            YPP_sorted.sort(reverse=True)
    
        YPP_sorted_array = np.array(YPP_sorted)
        YPP_MDA_sort = YPP_sorted_array[:,0]       
        YPP_sample_sort = YPP_sorted_array[:,1]
        YPP_MDAs_sorted_arrays = np.split(YPP_MDA_sort,len(YPP_MDA_sort))
        YPP_sample_arrays = np.split(YPP_sample_sort,len(YPP_MDA_sort))
        YPP_Y_Max = np.array(YPP_MDA_sort, dtype='f')
            
        YPPfig, YPPaxi = plt.subplots(figsize=(plotwidth, plotheight))
        width = []  

        for i in range(N):

            samples = YPP_sample_arrays[i]
            x_arraysi = x_arrays[i]
            x_tick_adjust = 0
            
            YPP_MDAS_error_1s = list(zip(YPP_MDAs_sorted_arrays[i],x_arraysi,samples))
            
            for idx, (x, y, z) in enumerate(YPP_MDAS_error_1s): 
                YPP_MDAS_error_1s[idx] = (float(x), float(y), str(z)) 
           
            for l, m, n in YPP_MDAS_error_1s:
                YPP_age_values = l 
                x_tick = m
                samples = n
                
                YPPaxi.broken_barh([(x_tick, 0.1)], (YPP_age_values, 0), facecolors=('midnightblue'))
                YPPaxi.broken_barh([(x_tick, 0.1)], (YPP_age_values, 0.33), facecolors=('midnightblue'))
                YPPaxi.broken_barh([(x_tick, 0.1)], (YPP_age_values, 0), facecolors=('midnightblue'))
                YPPaxi.broken_barh([(x_tick, 0.1)], (YPP_age_values, 0), facecolors=('midnightblue'))   
        
        for i in range(N):
            YPPaxi.set_xticks(x_arrays)
            YPPaxi.set_xticklabels(YPP_sample_sort, rotation='vertical') 
        
        YPPaxi.hlines(y=YPP_age_values, xmin=0, xmax=(0), color = 'midnightblue', lw=1, linewidth=3, label='MDA: YPP')
        YPPaxi.broken_barh([(0.15, 0)], (YPP_age_values,0), facecolors=('cornflowerblue'), label='1σ Uncertainty')
        YPPaxi.broken_barh([(0.15, 0)], (YPP_age_values,0), facecolors=('lightsteelblue'), label='2σ Uncertainty')
    
        YPPaxi.set_ylabel('Age'+" " +'(Ma)',labelpad=25)
        YPPaxi.yaxis.grid(True)  
        
        YPPaxi.set_yticks(np.arange(round(YPP_Y_Max[-1]-10),round(YPP_sorted[0][0]+10), 5))
        
        plt.gca().invert_yaxis()
        YPPaxi.set_xlabel('Samples', labelpad=25)
        
        YPPaxi.set_title('YPP MDA: All Samples') 
        plt.legend(loc='upper left')

        if Image_File_Option == 'web':
            filename = 'YPP_All_Samples_Plot'
            asset_folder = 'assets/plots/Stratigraphic_Plots/'
            for fileformat in ['.svg', '.tiff', '.eps', '.png', '.pdf', '.jpeg']:
                YPPfig.savefig(asset_folder + filename + fileformat)
        else:
            YPPfig.savefig('Saved_Files/Stratigraphic_Plots/YPP_All_Samples_Plot.' + Image_File_Option)  
                
        plt.close(YPPfig)
                
        return YPPfig

    #MLA
    def MLA_Strat_Plot(MLA_MDA, sample_list, Image_File_Option):
        N = len(sample_list)
        sample_array = np.array(sample_list)
        sample_arrays = np.split(sample_array,len(sample_array))
        
        #MLA
        MLA_array = np.array(MLA_MDA)
        MLA_MDAs = MLA_array[:,0]
        MLA_error1s = MLA_array[:,1]
        MLA_MDAs_arrays = np.split(MLA_MDAs,len(MLA_MDAs))
        MLA_error1s_arrays = np.split(MLA_error1s,len(MLA_MDAs))
    
        MLA_sorted = []
    
        for i in range(N):
            MLA_Zipped = list(zip(MLA_MDAs_arrays[i],MLA_error1s_arrays[i],sample_arrays[i]))
            MLA_Zipped.sort(key=lambda d: d[0])
            MLA_sorted.append([MLA_Zipped[0][0],MLA_Zipped[0][1],MLA_Zipped[0][2]])
            MLA_sorted.sort(reverse=True)
    
        MLA_sorted_array = np.array(MLA_sorted)
        MLA_MDA_sort = MLA_sorted_array[:,0]        
        MLA_error_sort = MLA_sorted_array[:,1]
        MLA_sample_sort = MLA_sorted_array[:,2]
        MLA_MDAs_sorted_arrays = np.split(MLA_MDA_sort,len(MLA_MDA_sort))
        MLA_error_sorted_arrays = np.split(MLA_error_sort,len(MLA_MDA_sort))
        MLA_sample_arrays = np.split(MLA_sample_sort,len(MLA_MDA_sort))
        MLA_Y_Max = np.array(MLA_MDA_sort, dtype='f')
       
        
        #Setting up the x-axis placements
        for i in range(N): 
            samplesi = sample_list[i]

            def create_x(t, w, n, d):
                return [t*x + w*n for x in range(d)]

            t = 1 # sets of data
            w = 0.3 # We generally want bars to be 0.8
            n = 1 # first set of data
            d = len(sample_list) # topics we're plotting
            plot_x = create_x(t,w,n,d)
            middle = [ a / 2.0 for a in plot_x]
            middle_x_array = np.array(middle)
            x_arrays = np.split(middle_x_array,len(sample_list))
        
        MLAfig, MLAaxi = plt.subplots(figsize=(plotwidth, plotheight))
        width = []  

        for i in range(N):

            samples = MLA_sample_arrays[i]
            x_arraysi = x_arrays[i]  
            
            x_tick_adjust = 0
            width = 0
            
            MLA_MDAS_error_1s = list(zip(MLA_MDAs_sorted_arrays[i],MLA_error_sorted_arrays[i],x_arraysi,samples))
            
            for idx, (x, y, z, a) in enumerate(MLA_MDAS_error_1s): 
                MLA_MDAS_error_1s[idx] = (float(x), float(y), float(z), str(a)) 
           
            for l, m, n, o in MLA_MDAS_error_1s:
                MLA_age_values = l 
                MLA_error1s_values = m
                MLA_age_plus_err = l+m
                MLA_error2s_values = m*2
                x_tick = n
                samples = o
                
                if N==1:
                    x_tick_adjust = 0.0002
                    width = 0.002
                    x_tick = 0
                    x_arrays = [0]
                
                if N==2:
                    x_tick_adjust = 0.002
                    width = 0.02
                
                if N>2:
                    x_tick_adjust = 0.002
                    width = 0.02
                    
                if N>4:
                    x_tick_adjust = 0.006
                    width = 0.05
                
                if N>6:
                    x_tick_adjust = 0.006
                    width = 0.07
                
                if N>8:
                    x_tick_adjust = 0.009
                    width = 0.09
                
                if N>12:
                    width=0.11
                    x_tick_adjust=0.02
                
                if N>17:
                    width=0.12
                    x_tick_adjust=0.02
                
                if N>20:
                    width=0.17
                    x_tick_adjust=0.02
                
                MLAaxi.broken_barh([(x_tick, width)], (MLA_age_values-MLA_error2s_values, MLA_error1s_values), facecolors=('lightsteelblue'))
                MLAaxi.broken_barh([(x_tick, width)], (MLA_age_values-MLA_error1s_values,MLA_error1s_values), facecolors=('cornflowerblue'))
                MLAaxi.broken_barh([(x_tick, width)], (MLA_age_values, MLA_error1s_values), facecolors=('cornflowerblue'))
                MLAaxi.broken_barh([(x_tick, width)], (MLA_age_values+MLA_error1s_values, MLA_error1s_values), facecolors=('lightsteelblue'))   
                MLAaxi.hlines(y=MLA_age_values, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'midnightblue', lw=1,linewidth=3)
                
        for i in range(N):
            MLAaxi.set_xticks(x_arrays)
            MLAaxi.set_xticklabels(MLA_sample_sort, rotation='vertical') 
        
        MLAaxi.hlines(y=MLA_age_values, xmin=0, xmax=(0), color = 'midnightblue', lw=1, linewidth=3, label='MDA: MLA')
        MLAaxi.broken_barh([(0.15, 0)], (MLA_age_values,0), facecolors=('cornflowerblue'), label='1σ Uncertainty')
        MLAaxi.broken_barh([(0.15, 0)], (MLA_age_values,0), facecolors=('lightsteelblue'), label='2σ Uncertainty')
    
        MLAaxi.set_ylabel('Age'+" " +'(Ma)',labelpad=25)
        MLAaxi.yaxis.grid(True)  
        
        MLAaxi.set_yticks(np.arange(round(MLA_Y_Max[-1]-10),round(MLA_sorted[0][0]+10), 2))
        
        plt.gca().invert_yaxis()
        MLAaxi.set_xlabel('Samples', labelpad=25)
        
        MLAaxi.set_title('MLA MDA: All Samples') 
        plt.legend(loc='upper left')
        
        if Image_File_Option == 'web':
            filename = 'MLA_All_Samples_Plot' 
            asset_folder = 'assets/plots/Stratigraphic_Plots/'
            for fileformat in ['.svg', '.tiff', '.eps', '.png', '.pdf', '.jpeg']:
                MLAfig.savefig(asset_folder + filename + fileformat)
        else:
            MLAfig.savefig('Saved_Files/Stratigraphic_Plots/MLA_All_Samples_Plot.' + Image_File_Option)  
                
        plt.close(MLAfig)
                
        return MLAfig
        
    if MDA_Method == "YSG":
        Plot = YSG_Strat_Plot(YSG_MDA, sample_list, Image_File_Option)
    if MDA_Method == 'YC1s':
        Plot = YC1s_Strat_Plot(YC1s_MDA, sample_list, Image_File_Option)
    if MDA_Method == 'YC2s':
        Plot = YC2s_Strat_Plot(YC2s_MDA, sample_list, Image_File_Option)
    if MDA_Method == 'YDZ':
        Plot = YDZ_Strat_Plot(YDZ_MDA, sample_list, Image_File_Option)
    if MDA_Method == 'Y3Zo':
        Plot = Y3Zo_Strat_Plot(Y3Zo_MDA, sample_list, Image_File_Option)
    if MDA_Method == 'Y3Za':
        Plot = Y3Za_Strat_Plot(Y3Za_MDA, sample_list, Image_File_Option)
    if MDA_Method == 'Tau':
        Plot = Tau_Strat_Plot(Tau_MDA, sample_list, Image_File_Option)
    if MDA_Method == 'YSP':
        Plot = YSP_Strat_Plot(YSP_MDA, sample_list, Image_File_Option)
    if MDA_Method == 'YPP':
        Plot = YPP_Strat_Plot(YPP_MDA, sample_list, Image_File_Option)
    if MDA_Method == 'MLA':
        Plot = MLA_Strat_Plot(MLA_MDA, sample_list, Image_File_Option)
    if MDA_Method == 'All':
        Plot = YSG_Strat_Plot(YSG_MDA, sample_list, Image_File_Option), YC1s_Strat_Plot(YC1s_MDA, sample_list, Image_File_Option), YC2s_Strat_Plot(YC2s_MDA, sample_list, Image_File_Option), YDZ_Strat_Plot(YDZ_MDA, sample_list, Image_File_Option), Y3Zo_Strat_Plot(Y3Zo_MDA, sample_list, Image_File_Option), Y3Za_Strat_Plot(Y3Za_MDA, sample_list, Image_File_Option), Tau_Strat_Plot(Tau_MDA, sample_list, Image_File_Option), YSP_Strat_Plot(YSP_MDA, sample_list, Image_File_Option), YPP_Strat_Plot(YPP_MDA, sample_list, Image_File_Option), MLA_Strat_Plot(MLA_MDA, sample_list, Image_File_Option)
        
    return Plot

#Functions for individual MDA method outputs 

def YSG_outputs(ages, errors, plotwidth, plotheight, sample_list, YSG_MDA, age_addition_set_max_plot, Image_File_Option):
    #YC1s plotting code author: morganbrooks 
    if not hasattr(ages[0], '__len__'):
        ages = [ages]
        errors = [errors]

    N = len(sample_list)
    sample_array = np.array(sample_list)
    sample_arrays = np.split(sample_array,len(sample_array))

    #YSG: splitting up the array of: MDA/WM, 1s error
    YSG_array = np.array(YSG_MDA)
    YSGMDAs = YSG_array[:,0]
    YSG_error1s = YSG_array[:,1]
    YSG_MDA_plus_error = YSGMDAs+YSG_error1s
    YSG_MDAs_arrays = np.split(YSGMDAs,len(YSGMDAs))
    YSG_error1s_arrays = np.split(YSG_error1s,len(YSGMDAs))
    YSG_MDA_plus_error_arrays = np.split(YSG_MDA_plus_error,len(YSG_MDA_plus_error))
    
    #Ages/Errors
    age_array = np.array(ages,dtype=object)
    error_array = np.array(errors,dtype=object)
    YSG_age_arrays = np.split(age_array,len(ages))
    YSG_error_arrays = np.split(error_array,len(ages))
    
    for i in range(len(age_array)): 
        agesi = age_array[i]
  
    for i in range(len(agesi)):
        def create_x(t, w, n, d):
            return [t*x + w*n for x in range(d)]

        t = 1 # sets of data
        w = 0.3 # We generally want bars to be 0.8
        n = 1 # first set of data
        d = len(agesi) # topics we're plotting
        plot_x = create_x(t,w,n,d)
        middle = [ a / 2.0 for a in plot_x]
    
        middle_x_array = np.array(middle)
        x_arrays = np.split(middle_x_array,len(agesi))
            
    #Plotting     
    
    YSGfig, YSGax = plt.subplots(N,1, figsize=(plotwidth, N*plotheight))
  
    width = []
        
    for i in range(N):      
        #Preparing the data to be plotted    
        #Setting up the age and error by sample: sorted by age
        YSG_age_error_1s_ = list(zip(ages[i],errors[i]))
        YSG_age_error_1s_.sort(key=lambda d: d[0])
        YSG_age_error_1s_sorted = np.array(YSG_age_error_1s_)
        
        YSG_ages = YSG_age_error_1s_sorted[:,0]
        YSG_error = YSG_age_error_1s_sorted[:,1]
        
        YSG_age_error_1s = list(zip(YSG_ages,YSG_error,middle_x_array))    
        
        if N > 1:
            YSGax[i] = plt.subplot2grid((N,1),(i,0))
            YSGaxi = YSGax[i]
        else:
            YSGaxi = YSGax
        if Image_File_Option == 'web': 
            YSGfig, YSGaxi = plt.subplots(1,1, figsize=(plotwidth, 1*plotheight))

        #Sample_List 
        samples = sample_arrays[i]
        
        #YSG MDA, Errors; formatted for plotting  
        YSG_error1s = YSG_error1s_arrays[i]
        YSG_error2s = YSG_error1s_arrays[i]*2
        YSG_MDAs_1s = list(zip(YSG_MDAs_arrays[i],YSG_error1s))
        YSG_MDAs_2s = list(zip(YSG_MDAs_arrays[i], YSG_error2s))
        YSG_value = YSG_MDAs_1s[0][0]
        YSG_err1s_value = YSG_MDAs_1s[0][1]
        YSG_err2s_value = YSG_MDAs_2s[0][1]
        
        #Ages/Errors
        YSG_error1s_i = errors[i]
        YSG_error2s_i = errors[i]*2
        YSG_ages_i = ages[i]
      
        #Set up plotting parameters
        plotting_max = YSG_value + age_addition_set_max_plot
       
        plotted_ages = np.count_nonzero(YSG_ages_i < plotting_max)
        
        if plotted_ages<6:
            width=0.002
            x_tick_adjust=0.0002
            x_tick = n/20
        
        elif plotted_ages<15:
            width=0.11
            x_tick_adjust=0.02
        
        elif plotted_ages>15:
            width=0.22
            x_tick_adjust=0.059
        
        YSG_MDAs_i = YSG_MDAs_arrays[i]
        
        for l, m, n in YSG_age_error_1s:    
            YSG_age_values = l 
            YSG_error1s_values = m
            YSG_age_plus_err = l+m
            YSG_error2s_values = m*2
            x_tick = n
            
            if YSG_age_values < plotting_max:
                           
                if any(YSG_MDAs_i==l) == True:
                    YSGaxi.broken_barh([(x_tick, width)], (YSG_age_values-YSG_error2s_values, YSG_error1s_values), facecolors=('lightcoral'))
                    YSGaxi.broken_barh([(x_tick, width)], (YSG_age_values-YSG_error1s_values,YSG_error1s_values), facecolors=('crimson'))
                    YSGaxi.broken_barh([(x_tick, width)], (YSG_age_values, YSG_error1s_values), facecolors=('crimson'))
                    YSGaxi.broken_barh([(x_tick, width)], (YSG_age_values+YSG_error1s_values, YSG_error1s_values), facecolors=('lightcoral'))   
                    YSGaxi.hlines(y=YSG_age_values, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'pink', lw=1,linewidth=3)
                           
                else:
                    YSGaxi.broken_barh([(x_tick, width)], (YSG_age_values-YSG_error2s_values, YSG_error1s_values), facecolors=('lightsteelblue'))
                    YSGaxi.broken_barh([(x_tick, width)], (YSG_age_values-YSG_error1s_values,YSG_error1s_values), facecolors=('cornflowerblue')) 
                    YSGaxi.broken_barh([(x_tick, width)], (YSG_age_values, YSG_error1s_values), facecolors=('cornflowerblue'))
                    YSGaxi.broken_barh([(x_tick, width)], (YSG_age_values+YSG_error1s_values, YSG_error1s_values), facecolors=('lightsteelblue'))      
                    YSGaxi.hlines(y=YSG_age_values, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'midnightblue', lw=1, linewidth=3)
                           
            else:
                break 
        
        YSGaxi.hlines(y=YSG_value, xmin=0, xmax=(0), color = 'midnightblue', lw=1, linewidth=3, label='Age'+" " +'(Ma)')
        YSGaxi.broken_barh([(0.15, 0)], (YSG_value,0), facecolors=('cornflowerblue'), label='1σ Uncertainty')
        YSGaxi.broken_barh([(0.15, 0)], (YSG_value,0), facecolors=('lightsteelblue'), label='2σ Uncertainty')
        YSGaxi.broken_barh([(0.15, 0)], (YSG_value,0), facecolors=('crimson'), label='YSG: '+str(round(YSG_value,2)) +"+/- "+str(round(YSG_err1s_value,2)))
        YSGaxi.set_xticks([])
        YSGaxi.set_ylabel('Age'+" " +'(Ma)')                
        YSGaxi.set_xlabel('Individual Age Measurements +/- 1s/2s Error')
        YSGaxi.set_title(samples[0]) 
        YSGaxi.yaxis.grid(True)
        plt.legend(loc='lower right')

        if Image_File_Option == 'web':
            asset_folder = 'assets/plots/Individual_MDA_Plots/'
            filename = 'YSG_Plots_' + str(samples[0])
            for fileformat in ['.svg', '.tiff', '.eps', '.png', '.pdf', '.jpeg']:
                YSGfig.savefig(asset_folder + filename + fileformat)
            plt.close(YSGfig)   
        else:
            YSGfig.savefig('Saved_Files/Individual_MDA_Plots/YSG_Plots.' + Image_File_Option)
        YSGfig.tight_layout(pad=3)

    plt.close(YSGfig)    
    YSG_Table_ = pd.DataFrame(data=YSG_MDA, index=[sample_list], columns=['YSG_MDA (Ma)', 'YSG_+/-1σ'])
    YSG_Table_['Sample_ID'] = sample_list
    YSG_Table_ = YSG_Table_[['Sample_ID', 'YSG_MDA (Ma)', 'YSG_+/-1σ']] 
    
    return YSG_MDA, YSG_Table_

def YDZ_outputs(ages, errors, sample_list, plotwidth, plotheight, Image_File_Option,iterations=10000, bins=25):

# YDZ Code below (with modifications) obtained from detritalPy_v1.3: @authors: glennrsharman, jonathanpsharman, zoltansylvester

    if not hasattr(ages[0], '__len__'):
        ages = [ages]
        errors = [errors]

    YDZ_MDAs = []
    
    sample_array = np.array(sample_list)
    sample_arrays = np.split(sample_array,len(sample_array))
    N = len(sample_list)
    

    for i in range(N):
        samples = sample_arrays[i]

        data_err1s = list(zip(ages[i], errors[i]))
        
       # Identify the youngest analysis
        YSG_age, YSG_err1s = YSG_for_YDZ(ages[i], errors[i])[0]

        ageCutoff = YSG_age + YSG_err1s*5 # 5 for 5-sigma

        # Identify all analyses within 5 sigma of the youngest analysis
        data_err1s.sort(key=lambda d: d[0]) # Sort based on age
        filtered = list(filter(lambda x: x[0] < ageCutoff, data_err1s)) # Filter out ages too old

        minAges = []
        mode = []
        for i in range(10000):
            newAge_Ma = []
            for analysis in filtered:
                newAge_Ma.append(np.random.normal(loc = analysis[0], scale=analysis[1]))
            minAges.append(min(newAge_Ma))
    
        # Find the mode of the minimum ages
        binIndex, binAge = np.histogram(minAges, bins=25)
        binMaxIndex = np.argmax(binIndex)
        binMaxAge = binAge[binMaxIndex]
        mode = binMaxAge + (binAge[binMaxIndex+1] - binMaxAge)/2
        plus_error = np.percentile(minAges, 97.5)-mode
        minus_error = mode-np.percentile(minAges, 2.5)

        YDZ_MDAs.append([mode, np.percentile(minAges, 97.5)-mode, mode-np.percentile(minAges, 2.5)])

        YDZfig, axYDZ = plt.subplots(1,figsize=(plotwidth, plotheight))
        axYDZ.set_xlim(int(min(minAges))-1,int(max(minAges))+1,0.5)
           
        axYDZ.hist(minAges, bins=25)
        axYDZ.axvline(mode,color='red', linewidth=3,label='MDA:'+str(round(mode,2)))
            
        axYDZ.axvline(np.percentile(minAges,2.5),linestyle='--',color='black', label='2s Uncertainty: - '+str(round(minus_error,2)))
        axYDZ.axvline(np.percentile(minAges,97.5),linestyle='dashdot',color='black', label='2s Uncertainty: + '+str(round(plus_error,2)))
            
           
        axYDZ.set_xlabel('Age (Ma)')
        YDZfig.tight_layout(pad=3)
        plt.legend(loc='upper left')
        axYDZ.set_title(samples[0])
        
        if Image_File_Option == 'web':
            asset_folder = 'assets/plots/Individual_MDA_Plots/'
            filename = 'YDZ_Plots_' + str(samples[0])
            for fileformat in ['.svg', '.tiff', '.png', '.eps','.pdf', '.jpeg']:
                YDZfig.savefig(asset_folder + filename + fileformat)
            plt.close(YDZfig)   
        else:
            YDZfig.savefig('Saved_Files/Individual_MDA_Plots/YDZ_Plots.' + Image_File_Option)
    

    plt.close(YDZfig)
    
    YDZ_Table_ = pd.DataFrame(data=YDZ_MDAs, index=[sample_list], columns=['YDZ_MDA (Ma)', 'YDZ_+2σ', 'YDZ_-2σ'])
    YDZ_Table_['Sample_ID'] = sample_list
    YDZ_Table_ = YDZ_Table_[['Sample_ID', 'YDZ_MDA (Ma)', 'YDZ_+2σ', 'YDZ_-2σ']] 
  
    return YDZfig, YDZ_MDAs, YDZ_Table_

def YPP_outputs(ages, errors, sample_list, plotwidth, plotheight, Image_File_Option, sigma=1, min_cluster_size=2, thres=0.01, minDist=1, xdif=0.1):
    
    # YPP calculation code below (with modifications) obtained from detritalPy_v1.3: @authors: glennrsharman, jonathanpsharman, zoltansylvester 
    # YPP plotting code author: morganbrooks 

    # Check to see if ages is a list of arrays or just a single list of ages
    if not hasattr(ages[0], '__len__'):
        ages = [ages]
        errors = [errors]

    # Calculate the PDP - note that a small xdif may be desired for increased precision
    PDP_age, PDP = PDPcalcAges(ages, errors, xdif=xdif, cumulative=False)
  
    YPP_MDAs = []
    
    sample_array = np.array(sample_list)
    sample_arrays = np.split(sample_array,len(sample_array))
    
    for i in range(len(ages)):
        samples = sample_arrays[i]
        agesi = ages[i]
        
        # Calculate peak indexes
        indexes = list(peakutils.indexes(PDP[i], thres=thres, min_dist=minDist))
        # Peak ages
        peakAges = PDP_age[indexes]
        # Number of grains per peak
        peakAgeGrain = peakAgesGrains([peakAges], [ages[i]], [errors[i]])[0]
        # Zip peak ages and grains per peak
        peakAgesGrains_ = list(zip(peakAges, peakAgeGrain))
        # Filter out peaks with less than min_cluster_size grains
        peakAgesGrainsFiltered = list(filter(lambda x: x[1] >= min_cluster_size, peakAgesGrains_))

        # Check if a YPP was found, and if not return NaN
        if len(peakAgesGrainsFiltered) > 0:
            YPP_MDAs.append(np.round(np.min([x[0] for x in peakAgesGrainsFiltered]),1))
        else:
            YPP_MDAs.append(np.nan)
              
        #peakAgeGraini = peakAgeGrain[i]
        
        #PDP Plots
        YPPfig, axYPP = plt.subplots(1,figsize=(plotwidth, plotheight))
        axYPP.plot(PDP_age, PDP[i])
        xmin, xmax = axYPP.get_xlim()
        ymin, ymax = axYPP.get_ylim()
        xdif = xmax-xmin
        ydif = ymax-ymin   
        axYPP.set_xlim(0,(YPP_MDAs[i]+200))
        axYPP.set_ylim(ymin, ymax)
        
        axYPP.set_xlabel('Age (Ma)')
        YPPfig.tight_layout(pad=3)
        axYPP.axvline(YPP_MDAs[i],color='red', label='MDA:'+str(YPP_MDAs[i]))
        #axYPP.axvline(YPP_MDAs[i], color='red',label='Grains in Peak:'+str(peakAgeGraini))
        axYPP.set_title(samples[0])
        plt.legend(loc='upper right')        

        if Image_File_Option == 'web':
            filename = 'YPP_Plots_' + str(samples[0])
            asset_folder = 'assets/plots/Individual_MDA_Plots/'
            for fileformat in ['.svg', '.tiff', '.eps', '.png', '.pdf', '.jpeg']:
                YPPfig.savefig(asset_folder + filename + fileformat)
            plt.close(YPPfig)   
        else:
            YPPfig.savefig('Saved_Files/Individual_MDA_Plots/YPP_Plots.' + Image_File_Option)   
       
    plt.close(YPPfig)
    YPP_Table_ = pd.DataFrame(data=YPP_MDAs, index=[sample_list], columns=['YPP_MDA (Ma)'])
    YPP_Table_['Sample_ID'] = sample_list
    YPP_Table_ = YPP_Table_[['Sample_ID', 'YPP_MDA (Ma)']] 
    
    return YPP_MDAs, YPP_Table_

def YC1s_outputs(ages, errors, sample_list, YC1s_MDA, YC1s_cluster_arrays, plotwidth, plotheight, age_addition_set_max_plot, Image_File_Option, min_cluster_size=2):
# YC1s plotting code author: morganbrooks 
    
    #Check to see if ages is a list of arrays or just a single list of ages
        
    if not hasattr(ages[0], '__len__'):
        ages_array = [ages]
        errors_array = [errors]
    
    #Sample_List
    sample_array = np.array(sample_list)
    sample_arrays = np.split(sample_array,len(sample_array))
    N = len(sample_arrays)
    
    #YC1s_Cluster
    YC1s_cluster_array = np.array(YC1s_cluster_arrays,dtype=object)
   
    
    #YC1s: splitting up the array of: MDA/WM, 1s error, MSWD, grains in cluster  
    YC1s_array = np.array(YC1s_MDA)
    YC1sMDAs = YC1s_array[:,0]
    YC1s_error1s = YC1s_array[:,1]
    YC1s_MSWD = YC1s_array[:,2]
    YC1s_grains = YC1s_array[:,3]
    YC1s_MDAs_arrays = np.split(YC1sMDAs,len(YC1sMDAs))
    YC1s_error1s_arrays = np.split(YC1s_error1s,len(YC1sMDAs))
    YC1s_MSWD_arrays = np.split(YC1s_MSWD,len(YC1sMDAs))
    YC1s_grains_arrays = np.split(YC1s_grains,len(YC1sMDAs))
    
    #Ages/Errors
    age_array = np.array(ages,dtype=object)
    error_array = np.array(errors,dtype=object)
    YC1s_age_arrays = np.split(age_array,len(ages))
    YC1s_error_arrays = np.split(error_array,len(ages))
    
    
    for i in range(len(age_array)): 
        agesi = age_array[i]

    for i in range(len(agesi)):
        def create_x(t, w, n, d):
            return [t*x + w*n for x in range(d)]

        t = 1 # sets of data
        w = 0.3 # We generally want bars to be 0.8
        n = 1 # first set of data
        d = len(agesi) # topics we're plotting
        plot_x = create_x(t,w,n,d)
        middle = [ a / 2.0 for a in plot_x]
    
        middle_x_array = np.array(middle)
        x_arrays = np.split(middle_x_array,len(agesi))
            
    #Plotting     
    
    YC1sfig, YC1sax = plt.subplots(N,1, figsize=(plotwidth, N*plotheight))
    cluster_age_plus_error = []
    width = []
    YC1s_age_error_1s = []
    
    
    for i in range(N):        
        #Preparing the data to be plotted        
        #Setting up the age and error by sample: sorted by age
        YC1s_age_error_1s_ = list(zip(ages[i],errors[i]))
        YC1s_age_error_1s_.sort(key=lambda d: d[0])
        YC1s_age_error_1s_sorted = np.array(YC1s_age_error_1s_)
        
        YC1s_ages = YC1s_age_error_1s_sorted[:,0]
        YC1s_error = YC1s_age_error_1s_sorted[:,1]
        
        YC1s_age_error_1s = list(zip(YC1s_ages,YC1s_error,middle_x_array))
    
        if N > 1:
            YC1sax[i] = plt.subplot2grid((N,1),(i,0))
            YC1saxi = YC1sax[i]
        else:
            YC1saxi = YC1sax
        if Image_File_Option == 'web': 
            YC1sfig, YC1saxi = plt.subplots(1,1, figsize=(plotwidth, 1*plotheight))

        #Sample_List 
        samples = sample_arrays[i]
        
        #YC1s MDA, Errors, MSWD, grains in cluster; formatted for plotting  
        YC1s_error1s = YC1s_error1s_arrays[i]
        YC1s_error2s = YC1s_error1s_arrays[i]*2
        YC1s_MDAs_1s = list(zip(YC1s_MDAs_arrays[i],YC1s_error1s,YC1s_MSWD_arrays[i],YC1s_grains_arrays[i]))
        YC1s_MDAs_2s = list(zip(YC1s_MDAs_arrays[i], YC1s_error2s,YC1s_MSWD_arrays[i],YC1s_grains_arrays[i]))
        YC1s_value = YC1s_MDAs_1s[0][0]
        YC1s_err1s_value = YC1s_MDAs_1s[0][1]
        YC1s_err2s_value = YC1s_MDAs_2s[0][1]
        YC1s_MSWD_value = YC1s_MDAs_1s[0][2]
        YC1s_grains_value = YC1s_MDAs_1s[0][3]
                
        #YC1s Cluster 
        YC1s_cluster_age_arrays_split_i = YC1s_cluster_arrays[i]
        YC1s_max_cluster = np.max(YC1s_cluster_age_arrays_split_i)
        
        for s, t in YC1s_cluster_age_arrays_split_i:
            clust_age = s
            clust_error = t
            clust_age_and_error = s+t
            cluster_age_plus_error.append(clust_age_and_error)
        
        L = len(YC1s_cluster_age_arrays_split_i)
        
        C = cluster_age_plus_error[-L:] 
        
        #Ages/Errors
        YC1s_error1s_i = errors[i]
        YC1s_error2s_i = errors[i]*2
        YC1s_ages_i = ages[i]
           
        
        #Set up plotting parameters
        plotting_max = YC1s_max_cluster + age_addition_set_max_plot
        plotted_ages = np.count_nonzero(YC1s_ages_i < plotting_max)
        
        if plotted_ages<6:
            width=0.002
            x_tick_adjust=0.0002
        
        elif plotted_ages<16:
            width=0.11
            x_tick_adjust=0.019
        
        elif plotted_ages<20:
            width=0.22
            x_tick_adjust=0.03
           
        else:
            width=0.22
            x_tick_adjust=0.09
        
        for l, m, n in YC1s_age_error_1s:    
            YC1s_age_value = l 
            YC1s_error1s_value = m
            YC1s_age_plus_error = l+m
            YC1s_error2s_value = m*2
            x_tick = n
            
            if YC1s_age_value < plotting_max:
                    
                if plotted_ages<6:
                        x_tick = n/20
                            
                if any(C==YC1s_age_plus_error) == True:
                    YC1saxi.broken_barh([(x_tick, width)], (YC1s_age_value-YC1s_error2s_value, YC1s_error1s_value), facecolors=('lightcoral'))
                    YC1saxi.broken_barh([(x_tick, width)], (YC1s_age_value-YC1s_error1s_value,YC1s_error1s_value), facecolors=('crimson'))
                    YC1saxi.broken_barh([(x_tick, width)], (YC1s_age_value, YC1s_error1s_value), facecolors=('crimson'))
                    YC1saxi.broken_barh([(x_tick, width)], (YC1s_age_value+YC1s_error1s_value, YC1s_error1s_value), facecolors=('lightcoral'))   
                    YC1saxi.hlines(y=YC1s_age_value, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'pink', lw=1,linewidth=3)  
                
                else:
                    YC1saxi.broken_barh([(x_tick, width)], (YC1s_age_value-YC1s_error2s_value, YC1s_error1s_value), facecolors=('lightsteelblue'))
                    YC1saxi.broken_barh([(x_tick, width)], (YC1s_age_value-YC1s_error1s_value,YC1s_error1s_value), facecolors=('cornflowerblue')) 
                    YC1saxi.broken_barh([(x_tick, width)], (YC1s_age_value, YC1s_error1s_value), facecolors=('cornflowerblue'))
                    YC1saxi.broken_barh([(x_tick, width)], (YC1s_age_value+YC1s_error1s_value, YC1s_error1s_value), facecolors=('lightsteelblue'))      
                    YC1saxi.hlines(y=YC1s_age_value, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'midnightblue', lw=1, linewidth=3)
            else:
                break 
        
        YC1saxi.hlines(y=YC1s_value, xmin=0, xmax=(0), color = 'midnightblue', lw=1, linewidth=3, label='Age'+" " +'(Ma)')
        YC1saxi.axhline(YC1s_value,color='black', linestyle='dotted', label='MDA: '+str(round(YC1s_value,2))+"+/- "+str(round(YC1s_err1s_value,2)))
        YC1saxi.broken_barh([(0.15, 0)], (YC1s_value,0), facecolors=('cornflowerblue'), label='1σ Uncertainty')
        YC1saxi.broken_barh([(0.15, 0)], (YC1s_value,0), facecolors=('lightsteelblue'), label='2σ Uncertainty')
        YC1saxi.broken_barh([(0.15, 0)], (YC1s_value,0), facecolors=('crimson'), label='Cluster: '+str(YC1s_grains_value))
        YC1saxi.set_xticks([])
        YC1saxi.set_ylabel('Age'+" " +'(Ma)')                
        YC1saxi.set_xlabel('Individual Age Measurements +/- 1σ/2σ Uncertainty')
        YC1saxi.set_title(samples[0]) 
        YC1saxi.yaxis.grid(True)
        plt.legend(loc='lower right')
        YC1sfig.tight_layout(pad=3)

        if Image_File_Option == 'web':
            filename = 'YC1s_Plots_' + str(samples[0])
            asset_folder = 'assets/plots/Individual_MDA_Plots/'
            for fileformat in ['.svg', '.tiff', '.eps', '.png', '.pdf', '.jpeg']:
                YC1sfig.savefig(asset_folder + filename + fileformat)
            plt.close(YC1sfig)   
        else:
            YC1sfig.savefig('Saved_Files/Individual_MDA_Plots/YC1s_Plots.' + Image_File_Option)  
    
    plt.close(YC1sfig)
    YC1s_Table_= pd.DataFrame(data=YC1s_MDA, index=[sample_list], columns=['YC1σ_MDA (Ma)', 'YC1σ_+/-1σ', 'YC1σ_MSWD', 'YC1σ_Grains'])
    YC1s_Table_['Sample_ID'] = sample_list
    YC1s_Table_ = YC1s_Table_[['Sample_ID', 'YC1σ_MDA (Ma)', 'YC1σ_+/-1σ', 'YC1σ_MSWD', 'YC1σ_Grains']] 
    
    return YC1s_MDA, YC1s_Table_

def YC2s_outputs(ages, errors, sample_list, YC2s_MDA, YC2s_cluster_arrays, plotwidth, plotheight, age_addition_set_max_plot, Image_File_Option, min_cluster_size=3):
#YC2s plotting code author: morganbrooks 
    

    #Check to see if ages is a list of arrays or just a single list of ages
        
    if not hasattr(ages[0], '__len__'):
        ages_array = [ages]
        errors_array = [errors]
    
    #Sample_List
    sample_array = np.array(sample_list)
    sample_arrays = np.split(sample_array,len(sample_array))
    N = len(sample_arrays)
    
    #YC2s_Cluster
    YC2s_cluster_array = np.array(YC2s_cluster_arrays,dtype=object)
    
    #YC2s: splitting up the array of: MDA/WM, 1s error, MSWD, grains in cluster  
    YC2s_array = np.array(YC2s_MDA)
    YC2s_MDAs = YC2s_array[:,0]
    YC2s_error1s = YC2s_array[:,1]
    YC2s_MSWD = YC2s_array[:,2]
    YC2s_grains = YC2s_array[:,3]
    YC2s_MDAs_arrays = np.split(YC2s_MDAs,len(YC2s_MDAs))
    YC2s_error1s_arrays = np.split(YC2s_error1s,len(YC2s_MDAs))
    YC2s_MSWD_arrays = np.split(YC2s_MSWD,len(YC2s_MDAs))
    YC2s_grains_arrays = np.split(YC2s_grains,len(YC2s_MDAs))
    
    #Ages/Errors
    age_array = np.array(ages,dtype=object)
    error_array = np.array(errors,dtype=object)
    YC2s_age_arrays = np.split(age_array,len(ages))
    YC2s_error_arrays = np.split(error_array,len(ages))
    
    for i in range(len(age_array)): 
        agesi = age_array[i]
     
  
    
    for i in range(len(agesi)):
        def create_x(t, w, n, d):
            return [t*x + w*n for x in range(d)]

        t = 1 # sets of data
        w = 0.3 # We generally want bars to be 0.8
        n = 1 # first set of data
        d = len(agesi) # topics we're plotting
        plot_x = create_x(t,w,n,d)
        middle = [ a / 2.0 for a in plot_x]
    
        middle_x_array = np.array(middle)
        x_arrays = np.split(middle_x_array,len(agesi))
            
    #Plotting     
    
    YC2sfig, YC2sax = plt.subplots(N,1, figsize=(plotwidth, N*plotheight))
    clust_age_plus_error = []
    width = []
    YC1s_age_error_2s = []
   
    for i in range(N):
        
        #Preparing the data to be plotted
        
        #Setting up the age and error by sample: sorted by age
        YC2s_age_error_1s_ = list(zip(ages[i],errors[i]))
        YC2s_age_error_1s_.sort(key=lambda d: d[0])
        YC2s_age_error_1s_sorted = np.array(YC2s_age_error_1s_)
        
        YC2s_ages = YC2s_age_error_1s_sorted[:,0]
        YC2s_error = YC2s_age_error_1s_sorted[:,1]
        
        YC2s_age_error_1s = list(zip(YC2s_ages,YC2s_error,middle_x_array))
        
        if N > 1:
            YC2sax[i] = plt.subplot2grid((N,1),(i,0))
            YC2saxi = YC2sax[i]
        else:
            YC2saxi = YC2sax
        if Image_File_Option == 'web': 
            YC2sfig, YC2saxi = plt.subplots(1,1, figsize=(plotwidth, 1*plotheight))

        #Sample_List 
        samples = sample_arrays[i]
        
        #YC1s MDA, Errors, MSWD, grains in cluster; formatted for plotting  
        YC2s_error1s = YC2s_error1s_arrays[i]
        YC2s_error2s = YC2s_error1s_arrays[i]*2
        YC2s_MDAs_1s = list(zip(YC2s_MDAs_arrays[i],YC2s_error1s,YC2s_MSWD_arrays[i],YC2s_grains_arrays[i]))
        YC2s_MDAs_2s = list(zip(YC2s_MDAs_arrays[i], YC2s_error2s,YC2s_MSWD_arrays[i],YC2s_grains_arrays[i]))
        YC2s_value = YC2s_MDAs_1s[0][0]
        YC2s_err1s_value = YC2s_MDAs_1s[0][1]
        YC2s_err2s_value = YC2s_MDAs_2s[0][1]
        YC2s_MSWD_value = YC2s_MDAs_1s[0][2]
        YC2s_grains_value = YC2s_MDAs_1s[0][3]
        
        #YC1s Cluster 
        YC2s_cluster_age_arrays_split_i = YC2s_cluster_arrays[i]
        YC2s_max_cluster = np.max(YC2s_cluster_age_arrays_split_i)
        
        for s, t in YC2s_cluster_age_arrays_split_i:
            clust_age = s
            clust_2serror = t
            clust_age_and_error = s+t
            clust_age_plus_error.append(clust_age_and_error)
        
        L = len(YC2s_cluster_age_arrays_split_i)
        
        C = clust_age_plus_error[-L:]
      
        #Ages/Errors
        YC2s_error1s_i = errors[i]
        YC2s_error2s_i = errors[i]*2
        YC2s_ages_i = ages[i]

        #Set up plotting parameters
        plotting_max = YC2s_max_cluster + age_addition_set_max_plot
        plotted_ages = np.count_nonzero(YC2s_ages_i < plotting_max)
        
        if plotted_ages<6:
            width=0.002
            x_tick_adjust=0.0002
        
        elif plotted_ages<16:
            width=0.11
            x_tick_adjust=0.019
        
        elif plotted_ages<20:
            width=0.22
            x_tick_adjust=0.03
           
        else:
            width=0.22
            x_tick_adjust=0.09
       
        for l, m, n in YC2s_age_error_1s:    
            YC2s_age_value = l 
            YC2s_error1s_value = m
            YC2s_error2s_value = m*2
            YC2s_age_plus_error = l+YC2s_error2s_value
            x_tick = n   
            
            if YC2s_age_value < plotting_max:
                    
                if plotted_ages<6:
                        x_tick = n/20
                            
                if any(C==YC2s_age_plus_error) == True:
                    YC2saxi.broken_barh([(x_tick, width)], (YC2s_age_value-YC2s_error2s_value, YC2s_error1s_value), facecolors=('lightcoral'))
                    YC2saxi.broken_barh([(x_tick, width)], (YC2s_age_value-YC2s_error1s_value,YC2s_error1s_value), facecolors=('crimson')) 
                    YC2saxi.broken_barh([(x_tick, width)], (YC2s_age_value, YC2s_error1s_value), facecolors=('crimson'))
                    YC2saxi.broken_barh([(x_tick, width)], (YC2s_age_value+YC2s_error1s_value, YC2s_error1s_value), facecolors=('lightcoral'))   
                    YC2saxi.hlines(y=YC2s_age_value, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'pink', lw=1,linewidth=3) 
                
                else:
                    YC2saxi.broken_barh([(x_tick, width)], (YC2s_age_value-YC2s_error2s_value, YC2s_error1s_value), facecolors=('lightsteelblue')) 
                    YC2saxi.broken_barh([(x_tick, width)], (YC2s_age_value-YC2s_error1s_value,YC2s_error1s_value), facecolors=('cornflowerblue')) 
                    YC2saxi.broken_barh([(x_tick, width)], (YC2s_age_value, YC2s_error1s_value), facecolors=('cornflowerblue'))
                    YC2saxi.broken_barh([(x_tick, width)], (YC2s_age_value+YC2s_error1s_value, YC2s_error1s_value), facecolors=('lightsteelblue'))      
                    YC2saxi.hlines(y=YC2s_age_value, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'midnightblue', lw=1, linewidth=3) 
            else:
                break 
        
        YC2saxi.hlines(y=YC2s_value, xmin=0, xmax=(0), color = 'midnightblue', lw=1, linewidth=3, label='Age'+" " +'(Ma)')
        YC2saxi.axhline(YC2s_value,color='black', linestyle='dotted', label='MDA: '+str(round(YC2s_value,2))+"+/- "+str(round(YC2s_err1s_value,2)))
        YC2saxi.broken_barh([(0.15, 0)], (YC2s_value,0), facecolors=('cornflowerblue'), label='1σ Uncertainty')
        YC2saxi.broken_barh([(0.15, 0)], (YC2s_value,0), facecolors=('lightsteelblue'), label='2σ Uncertainty')
        YC2saxi.broken_barh([(0.15, 0)], (YC2s_value,0), facecolors=('crimson'), label='Cluster: '+str(YC2s_grains_value))
        
        YC2saxi.set_xticks([])
        
        YC2saxi.set_ylabel('Age'+" " +'(Ma)')                
        YC2saxi.set_xlabel('Individual Age Measurements +/- 1σ/2σ Uncertainty')
        YC2saxi.set_title(samples[0]) 
        YC2saxi.yaxis.grid(True)
        plt.legend(loc='lower right')
        YC2sfig.tight_layout(pad=2)
        
        if Image_File_Option == 'web':
            filename = 'YC2s_Plots_' + str(samples[0])
            asset_folder = 'assets/plots/Individual_MDA_Plots/'
            for fileformat in ['.svg', '.tiff', '.eps', '.png', '.pdf', '.jpeg']:
                YC2sfig.savefig(asset_folder + filename + fileformat)
            plt.close(YC2sfig)   
        else:
            YC2sfig.savefig('Saved_Files/Individual_MDA_Plots/YC2s_Plots.' + Image_File_Option)  

    plt.close(YC2sfig)
    YC2s_Table_ = pd.DataFrame(data=YC2s_MDA, index=[sample_list], columns=['YC2σ_MDA (Ma)', 'YC2σ_+/-1s', 'YC2σ_MSWD', 'YC2σ_Grains'])
    YC2s_Table_['Sample_ID'] = sample_list
    YC2s_Table_ = YC2s_Table_[['Sample_ID', 'YC2σ_MDA (Ma)', 'YC2σ_+/-1s', 'YC2σ_MSWD', 'YC2σ_Grains']]
    
    return YC2s_MDA, YC2s_Table_

def Y3Zo_outputs(ages, errors, sample_list, Y3Zo_MDA, Y3Zo_cluster_arrays, plotwidth, plotheight, age_addition_set_max_plot, Image_File_Option, min_cluster_size=3):
    # Y3Zos plotting code author: morganbrooks     
    # Check to see if ages is a list of arrays or just a single list of ages
    if not hasattr(ages[0], '__len__'):
        ages = [ages]
        errors = [errors]
   
    #Sample_List
    sample_array = np.array(sample_list)
    sample_arrays = np.split(sample_array,len(sample_array))
    N = len(sample_arrays)
    
    #Y3Zo_Cluster
    Y3Zo_cluster_array = np.array(Y3Zo_cluster_arrays)
    Y3Zo_cluster_age_arrays_split = np.split(Y3Zo_cluster_array,len(Y3Zo_cluster_array))
    
    #Y3Zo: splitting up the array of: MDA/WM, 1s error, MSWD, grains in cluster  
    Y3Zo_array = np.array(Y3Zo_MDA)
    Y3Zo_MDAs = Y3Zo_array[:,0]
    Y3Zo_error1s = Y3Zo_array[:,1]
    Y3Zo_MSWD = Y3Zo_array[:,2]
    Y3Zo_MDAs_arrays = np.split(Y3Zo_MDAs,len(Y3Zo_MDAs))
    Y3Zo_error1s_arrays = np.split(Y3Zo_error1s,len(Y3Zo_MDAs))
    Y3Zo_MSWD_arrays = np.split(Y3Zo_MSWD,len(Y3Zo_MDAs))
    
    
    #Ages/Errors
    age_array = np.array(ages,dtype=object)
    error_array = np.array(errors,dtype=object)
    Y3Zo_age_arrays = np.split(age_array,len(ages))
    Y3Zo_error_arrays = np.split(error_array,len(ages))
    
    for i in range(len(age_array)): 
        agesi = age_array[i]
  
    
    for i in range(len(agesi)):
        def create_x(t, w, n, d):
            return [t*x + w*n for x in range(d)]

        t = 1 # sets of data
        w = 0.3 # We generally want bars to be 0.8
        n = 1 # first set of data
        d = len(agesi) # topics we're plotting
        plot_x = create_x(t,w,n,d)
        middle = [ a / 2.0 for a in plot_x]
    
        middle_x_array = np.array(middle)
        x_arrays = np.split(middle_x_array,len(agesi))
            
    #Plotting     
    
    Y3Zofig, Y3Zoax = plt.subplots(N,1, figsize=(plotwidth, N*plotheight))
    cluster_age_plus_error = []
    width = []
    
    for i in range(N):
        
        #Preparing the data to be plotted
        
        #Setting up the age and error by sample: sorted by age
        Y3Zo_age_error_1s_ = list(zip(ages[i],errors[i]))
        Y3Zo_age_error_1s_.sort(key=lambda d: d[0])
        Y3Zo_age_error_1s_sorted = np.array(Y3Zo_age_error_1s_)
        
        Y3Zo_ages = Y3Zo_age_error_1s_sorted[:,0]
        Y3Zo_error = Y3Zo_age_error_1s_sorted[:,1]
        
        Y3Zo_age_error_1s = list(zip(Y3Zo_ages,Y3Zo_error,middle_x_array))
        
        
        if N > 1:
            Y3Zoax[i] = plt.subplot2grid((N,1),(i,0))
            Y3Zoaxi = Y3Zoax[i]
        else:
            Y3Zoaxi = Y3Zoax
        if Image_File_Option == 'web': 
            Y3Zofig, Y3Zoaxi = plt.subplots(1,1, figsize=(plotwidth, 1*plotheight))

        #Sample_List 
        samples = sample_arrays[i]
        
        #Y3Zo MDA, Errors, MSWD, grains in cluster; formatted for plotting  
        Y3Zo_error1s = Y3Zo_error1s_arrays[i]
        Y3Zo_error2s = Y3Zo_error1s_arrays[i]*2
        Y3Zo_MDAs_1s = list(zip(Y3Zo_MDAs_arrays[i],Y3Zo_error1s,Y3Zo_MSWD_arrays[i]))
        Y3Zo_MDAs_2s = list(zip(Y3Zo_MDAs_arrays[i], Y3Zo_error2s,Y3Zo_MSWD_arrays[i]))
        Y3Zo_value = Y3Zo_MDAs_1s[0][0]
        Y3Zo_err1s_value = Y3Zo_MDAs_1s[0][1]
        Y3Zo_err2s_value = Y3Zo_MDAs_2s[0][1]
        Y3Zo_MSWD_value = Y3Zo_MDAs_1s[0][2]
       
        
        #Y3Zo Cluster 
        Y3Zo_cluster_age_arrays_split_i = Y3Zo_cluster_arrays[i]
        Y3Zo_max_cluster = np.max(Y3Zo_cluster_age_arrays_split_i)
        
        for s, t in Y3Zo_cluster_age_arrays_split_i:
            clust_age = s
            clust_error = t
            cluster_age_and_error = s+t
            cluster_age_plus_error.append(cluster_age_and_error)
        
        L = len(Y3Zo_cluster_age_arrays_split_i)
        
        C = cluster_age_plus_error[-L:]
        
        #Ages/Errors
        Y3Zo_error1s_i = errors[i]
        Y3Zo_error2s_i = errors[i]*2
        Y3Zo_ages_i = ages[i]
      
        #Set up plotting parameters
        plotting_max = Y3Zo_max_cluster + age_addition_set_max_plot
        plotted_ages = np.count_nonzero(Y3Zo_ages_i < plotting_max)
        
        if plotted_ages<6:
            width=0.002
            x_tick_adjust=0.0002
        
        elif plotted_ages<16:
            width=0.11
            x_tick_adjust=0.019
        
        elif plotted_ages<19:
            width=0.22
            x_tick_adjust=0.03
           
        else:
            width=0.22
            x_tick_adjust=0.05
       
        for l, m, n in Y3Zo_age_error_1s:    
            Y3Zo_age_value = l 
            Y3Zo_error1s_value = m
            Y3Zo_error2s_value = m*2
            Y3Zo_age_plus_error = l+Y3Zo_error2s_value
            x_tick = n
            
            if Y3Zo_age_value < plotting_max:
                    
                if plotted_ages<6:
                        x_tick = n/20
                            
                if any(C==Y3Zo_age_plus_error) == True:
                    Y3Zoaxi.broken_barh([(x_tick, width)], (Y3Zo_age_value-Y3Zo_error2s_value, Y3Zo_error1s_value), facecolors=('lightcoral')) #label='2s Uncertainty')
                    Y3Zoaxi.broken_barh([(x_tick, width)], (Y3Zo_age_value-Y3Zo_error1s_value,Y3Zo_error1s_value), facecolors=('crimson')) #label='1s Uncertainty')
                    Y3Zoaxi.broken_barh([(x_tick, width)], (Y3Zo_age_value, Y3Zo_error1s_value), facecolors=('crimson'))
                    Y3Zoaxi.broken_barh([(x_tick, width)], (Y3Zo_age_value+Y3Zo_error1s_value, Y3Zo_error1s_value), facecolors=('lightcoral'))   
                    Y3Zoaxi.hlines(y=Y3Zo_age_value, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'pink', lw=1,linewidth=3) #label='Cluster' )
                
                else:
                    Y3Zoaxi.broken_barh([(x_tick, width)], (Y3Zo_age_value-Y3Zo_error2s_value, Y3Zo_error1s_value), facecolors=('lightsteelblue')) #label='2s Uncertainty')
                    Y3Zoaxi.broken_barh([(x_tick, width)], (Y3Zo_age_value-Y3Zo_error1s_value,Y3Zo_error1s_value), facecolors=('cornflowerblue')) #label='1s Uncertainty')
                    Y3Zoaxi.broken_barh([(x_tick, width)], (Y3Zo_age_value, Y3Zo_error1s_value), facecolors=('cornflowerblue'))
                    Y3Zoaxi.broken_barh([(x_tick, width)], (Y3Zo_age_value+Y3Zo_error1s_value, Y3Zo_error1s_value), facecolors=('lightsteelblue'))      
                    Y3Zoaxi.hlines(y=Y3Zo_age_value, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'midnightblue', lw=1, linewidth=3) #label='Age', )
            else:
                break 
        
        Y3Zoaxi.hlines(y=Y3Zo_value, xmin=0, xmax=(0), color = 'midnightblue', lw=1, linewidth=3, label='Age'+" " +'(Ma)')
        Y3Zoaxi.axhline(Y3Zo_value,color='black', linestyle='dotted', label='MDA: '+str(round(Y3Zo_value,2))+"+/- "+str(round(Y3Zo_err1s_value,2)))
        Y3Zoaxi.broken_barh([(0.15, 0)], (Y3Zo_value,0), facecolors=('cornflowerblue'), label='1σ Uncertainty')
        Y3Zoaxi.broken_barh([(0.15, 0)], (Y3Zo_value,0), facecolors=('lightsteelblue'), label='2σ Uncertainty')
        Y3Zoaxi.broken_barh([(0.15, 0)], (Y3Zo_value,0), facecolors=('crimson'), label='3 Grain Cluster')
        
        Y3Zoaxi.set_xticks([])
        Y3Zoaxi.set_ylabel('Age'+" " +'(Ma)')                
        Y3Zoaxi.set_xlabel('Individual Age Measurements +/- 1σ/2σ  Uncertainty')
        Y3Zoaxi.set_title(samples[0]) 
        Y3Zoaxi.yaxis.grid(True)
        plt.legend(loc='lower right')
        Y3Zofig.tight_layout(pad=3)
 
        if Image_File_Option == 'web':
            filename = 'Y3Zo_Plots_' + str(samples[0])
            asset_folder = 'assets/plots/Individual_MDA_Plots/'
            for fileformat in ['.svg', '.tiff', '.eps', '.png', '.pdf', '.jpeg']:
                Y3Zofig.savefig(asset_folder + filename + fileformat)
            plt.close(Y3Zofig)   
        else:
            Y3Zofig.savefig('Saved_Files/Individual_MDA_Plots/Y3Zo_Plots.' + Image_File_Option)  
    
    plt.close(Y3Zofig)
    Y3Zo_Table_ = pd.DataFrame(data=Y3Zo_MDA, index=[sample_list], columns=['Y3Zo_MDA (Ma)', 'Y3Zo_+/-1σ', 'Y3Zo_MSWD','Y3Zo_Grains'])
    Y3Zo_Table_['Sample_ID'] = sample_list
    Y3Zo_Table_ = Y3Zo_Table_[['Sample_ID', 'Y3Zo_MDA (Ma)', 'Y3Zo_+/-1σ', 'Y3Zo_MSWD','Y3Zo_Grains']] 
    
    return Y3Zo_MDA, Y3Zo_Table_

def Y3Za_outputs(ages, errors, Y3Za_MDA, Y3Za_cluster_arrays, sample_list, plotwidth, plotheight, age_addition_set_max_plot, Image_File_Option):
    
# Y3Zas plotting code author: morganbrooks 
    

    # Check to see if ages is a list of arrays or just a single list of ages
    if not hasattr(ages[0], '__len__'):
        ages = [ages]
        errors = [errors]
    
   
    #Sample_List
    sample_array = np.array(sample_list)
    sample_arrays = np.split(sample_array,len(sample_array))
    N = len(sample_arrays) 
    
    #Y3Za_Cluster
    Y3Za_cluster_array = np.array(Y3Za_cluster_arrays)
    Y3Za_cluster_age_arrays_split = np.split(Y3Za_cluster_array,len(Y3Za_cluster_array))
    
    #Y3Za: splitting up the array of: MDA/WM, 1s error, MSWD, grains in cluster  
    Y3Za_array = np.array(Y3Za_MDA)
    Y3Za_MDAs = Y3Za_array[:,0]
    Y3Za_error1s = Y3Za_array[:,1]
    Y3Za_MSWD = Y3Za_array[:,2]
    Y3Za_MDAs_arrays = np.split(Y3Za_MDAs,len(Y3Za_MDAs))
    Y3Za_error1s_arrays = np.split(Y3Za_error1s,len(Y3Za_MDAs))
    Y3Za_MSWD_arrays = np.split(Y3Za_MSWD,len(Y3Za_MDAs))
    
    
    #Ages/Errors
    age_array = np.array(ages,dtype=object)
    error_array = np.array(errors,dtype=object)
    Y3Za_age_arrays = np.split(age_array,len(ages))
    Y3Za_error_arrays = np.split(error_array,len(ages))
    
    for i in range(len(age_array)): 
        agesi = age_array[i]
  
    
    for i in range(len(agesi)):
        def create_x(t, w, n, d):
            return [t*x + w*n for x in range(d)]

        t = 1 # sets of data
        w = 0.3 # We generally want bars to be 0.8
        n = 1 # first set of data
        d = len(agesi) # topics we're plotting
        plot_x = create_x(t,w,n,d)
        middle = [ a / 2.0 for a in plot_x]
    
        middle_x_array = np.array(middle)
        x_arrays = np.split(middle_x_array,len(agesi))
            
    #Plotting     
    
    Y3Zafig, Y3Zaax = plt.subplots(N,1, figsize=(plotwidth, N*plotheight))
    cluster_age_plus_error = []
    width = []
    
    for i in range(N):        
        #Preparing the data to be plotted        
        #Setting up the age and error by sample: sorted by age
        Y3Za_age_error_1s_ = list(zip(ages[i],errors[i]))
        Y3Za_age_error_1s_.sort(key=lambda d: d[0])
        Y3Za_age_error_1s_sorted = np.array(Y3Za_age_error_1s_)
        
        Y3Za_ages = Y3Za_age_error_1s_sorted[:,0]
        Y3Za_error = Y3Za_age_error_1s_sorted[:,1]
        
        Y3Za_age_error_1s = list(zip(Y3Za_ages,Y3Za_error,middle_x_array))
        
        if N > 1:
            Y3Zaax[i] = plt.subplot2grid((N,1),(i,0))
            Y3Zaaxi = Y3Zaax[i]
        else:
            Y3Zaaxi = Y3Zaax
        if Image_File_Option == 'web': 
            Y3Zafig, Y3Zaaxi = plt.subplots(1,1, figsize=(plotwidth, 1*plotheight))

        #Sample_List 
        samples = sample_arrays[i]
        
        #YC1s MDA, Errors, MSWD, grains in cluster; formatted for plotting  
        Y3Za_error1s = Y3Za_error1s_arrays[i]
        Y3Za_error2s = Y3Za_error1s_arrays[i]*2
        Y3Za_MDAs_1s = list(zip(Y3Za_MDAs_arrays[i],Y3Za_error1s,Y3Za_MSWD_arrays[i]))
        Y3Za_MDAs_2s = list(zip(Y3Za_MDAs_arrays[i], Y3Za_error2s,Y3Za_MSWD_arrays[i]))
        Y3Za_value = Y3Za_MDAs_1s[0][0]
        Y3Za_err1s_value = Y3Za_MDAs_1s[0][1]
        Y3Za_err2s_value = Y3Za_MDAs_2s[0][1]
        Y3Za_MSWD_value = Y3Za_MDAs_1s[0][2]
       
        #YC1s Cluster 
        Y3Za_cluster_age_arrays_split_i = Y3Za_cluster_arrays[i]
        Y3Za_max_cluster = np.max(Y3Za_cluster_age_arrays_split_i)
        
        for s,t,u,v,w,x in Y3Za_cluster_age_arrays_split_i:
            clust_age = s
            clust_error = t
            clust_age_and_error = s+t
            cluster_age_plus_error.append(clust_age_and_error)
       
        L = len(Y3Za_cluster_age_arrays_split_i)
        
        C = cluster_age_plus_error[-L:]
        
        #Ages/Errors
        Y3Za_error1s_i = errors[i]
        Y3Za_error2s_i = errors[i]*2
        Y3Za_ages_i = ages[i]
      

        #Set up plotting parameters
        plotting_max = Y3Za_max_cluster + age_addition_set_max_plot
       
        plotted_ages = np.count_nonzero(Y3Za_ages_i < plotting_max)
        
        if plotted_ages<6:
            width=0.002
            x_tick_adjust=0.0002
        
        elif plotted_ages<16:
            width=0.11
            x_tick_adjust=0.019
        
        elif plotted_ages<19:
            width=0.22
            x_tick_adjust=0.02
           
        else:
            width=0.22
            x_tick_adjust=0.05
       
        for l, m, n in Y3Za_age_error_1s:    
            Y3Za_age_value = l 
            Y3Za_error1s_value = m
            Y3Za_age_plus_error = m+l
            Y3Za_error2s_value = m*2
            x_tick = n
            
            if Y3Za_age_value < plotting_max:
                    
                if plotted_ages<6:
                        x_tick = n/20
                            
                if any(C==Y3Za_age_plus_error) == True:
                    Y3Zaaxi.broken_barh([(x_tick, width)], (Y3Za_age_value-Y3Za_error2s_value, Y3Za_error1s_value), facecolors=('lightcoral')) #label='2s Uncertainty')
                    Y3Zaaxi.broken_barh([(x_tick, width)], (Y3Za_age_value-Y3Za_error1s_value,Y3Za_error1s_value), facecolors=('crimson')) #label='1s Uncertainty')
                    Y3Zaaxi.broken_barh([(x_tick, width)], (Y3Za_age_value, Y3Za_error1s_value), facecolors=('crimson'))
                    Y3Zaaxi.broken_barh([(x_tick, width)], (Y3Za_age_value+Y3Za_error1s_value, Y3Za_error1s_value), facecolors=('lightcoral'))   
                    Y3Zaaxi.hlines(y=Y3Za_age_value, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'pink', lw=1,linewidth=3) #label='Cluster' )
                
                else:
                    Y3Zaaxi.broken_barh([(x_tick, width)], (Y3Za_age_value-Y3Za_error2s_value, Y3Za_error1s_value), facecolors=('lightsteelblue')) #label='2s Uncertainty')
                    Y3Zaaxi.broken_barh([(x_tick, width)], (Y3Za_age_value-Y3Za_error1s_value,Y3Za_error1s_value), facecolors=('cornflowerblue')) #label='1s Uncertainty')
                    Y3Zaaxi.broken_barh([(x_tick, width)], (Y3Za_age_value, Y3Za_error1s_value), facecolors=('cornflowerblue'))
                    Y3Zaaxi.broken_barh([(x_tick, width)], (Y3Za_age_value+Y3Za_error1s_value, Y3Za_error1s_value), facecolors=('lightsteelblue'))      
                    Y3Zaaxi.hlines(y=Y3Za_age_value, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'midnightblue', lw=1, linewidth=3) #label='Age', )
            else:
                break 
        
        Y3Zaaxi.hlines(y=Y3Za_value, xmin=0, xmax=(0), color = 'midnightblue', lw=1, linewidth=3, label='Age'+" " +'(Ma)')
        Y3Zaaxi.axhline(Y3Za_value,color='black', linestyle='dotted', label='MDA: '+str(round(Y3Za_value,2))+"+/- "+str(round(Y3Za_err1s_value,2)))
        Y3Zaaxi.broken_barh([(0.15, 0)], (Y3Za_value,0), facecolors=('cornflowerblue'), label='1σ Uncertainty')
        Y3Zaaxi.broken_barh([(0.15, 0)], (Y3Za_value,0), facecolors=('lightsteelblue'), label='2σ Uncertainty')
        Y3Zaaxi.broken_barh([(0.15, 0)], (Y3Za_value,0), facecolors=('crimson'), label='3 Grain Cluster')
        
        Y3Zaaxi.set_xticks([])
        Y3Zaaxi.set_ylabel('Age'+" " +'(Ma)')                
        Y3Zaaxi.set_xlabel('Individual Age Measurements +/- 1σ/2σ Uncertainty')
        Y3Zaaxi.set_title(samples[0]) 
        Y3Zaaxi.yaxis.grid(True)
        plt.legend(loc='lower right')
        Y3Zafig.tight_layout(pad=1)
 
        if Image_File_Option == 'web':
            filename = 'Y3Za_Plots_' + str(samples[0])
            asset_folder = 'assets/plots/Individual_MDA_Plots/'
            for fileformat in ['.svg', '.tiff', '.eps', '.png', '.pdf', '.jpeg']:
                Y3Zafig.savefig(asset_folder + filename + fileformat)
            plt.close(Y3Zafig)   
        else:
            Y3Zafig.savefig('Saved_Files/Individual_MDA_Plots/Y3Za_Plots.' + Image_File_Option)  
    
    plt.close(Y3Zafig)    
    Y3Za_Table_ = pd.DataFrame(data=Y3Za_MDA, index=[sample_list], columns=['Y3Za_MDA (Ma)', 'Y3Za_+/-1σ', 'Y3Za_MSWD','Y3Za_Grains'])
    Y3Za_Table_['Sample_ID'] = sample_list
    Y3Za_Table_ = Y3Za_Table_[['Sample_ID', 'Y3Za_MDA (Ma)', 'Y3Za_+/-1σ', 'Y3Za_MSWD','Y3Za_Grains']] 
    
    
    return Y3Za_MDA, Y3Za_Table_

def Tau_outputs(ages, errors, sample_list, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, U238_decay_constant, U235_decay_constant, U238_U235, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, Data_Type, best_age_cut_off, plotwidth, plotheight, Image_File_Option, min_cluster_size=3, thres=0.01, minDist=1, xdif=1, x1=0, x2=4000):
 #Tau calculation code below (with modifications) obtained from detritalPy_v1.3: @authors: glennrsharman, jonathanpsharman, zoltansylvester 
 #Tau plotting code author: morganbrooks 

    import peakutils

    # Check to see if ages is a list of arrays or just a single list of ages
    if not hasattr(ages[0], '__len__'):
        ages = [ages]
        errors = [errors]

    # Calculate the PDP - note that a small xdif may be desired for increased precision
    Tau_PDP_age, Tau_PDP = PDPcalcAges(ages, errors, xdif)

    Tau_Ratios = []
    Tau_MDA = []
    Tau_wo_systematic = []

        

    if Data_Type == "238U/206Pb_&_207Pb/206Pb": 
        for i in range(len(ages)): 
                
            # Calculate peak indexes
            peakIndexes = list(peakutils.indexes(Tau_PDP[i], thres=thres, min_dist=minDist))
            # Peak ages
            peakAges = Tau_PDP_age[peakIndexes]
            # Number of grains per peak
            peakAgeGrain = peakAgesGrains([peakAges], [ages[i]], [errors[i]])[0]

            # Calculate trough indexes
            troughIndexes = list(peakutils.indexes(Tau_PDP[i]*-1, thres=thres, min_dist=minDist))
            # Trough ages
            troughAges = [0] + list(Tau_PDP_age[troughIndexes]) + [4500] # Append a 0 because there is no trough on the young size of the youngest peak and no trough on the old side of the oldest peak

            # Zip peak ages and grains per peak
            peakAgesGrains_ = list(zip(peakAges, peakAgeGrain))
            # Filter out peaks with less than min_cluster_size grains (default is 3, following Barbeau et al., 2009: EPSL)
            peakAgesGrainsFiltered = list(filter(lambda x: x[1] >= min_cluster_size, peakAgesGrains_))

            # Stop the loop if no peaks are present with the min_cluster_size
            if peakAgesGrainsFiltered == []:
                Tau_Ratios.append([np.nan, np.nan, np.nan, np.nan])
                Tau_MDA.append([np.nan, np.nan, np.nan, np.nan])
                continue

            # Select the nearest trough that is younger than the youngest peak with at least min_cluster_size analyses
            troughYoung = np.max(list(filter(lambda x: x < peakAgesGrainsFiltered[0][0], troughAges)))

            # Select the nearest trough that is older than the youngest peak with at least min_cluster_size analyses
            troughOld = np.min(list(filter(lambda x: x > peakAgesGrainsFiltered[0][0], troughAges)))

            # Select ages and errors that fall between troughYoung and troughOld

            ages_errors1s = list(zip(ages[i], errors[i],1/eight_six_ratios[i], eight_six_error[i],seven_six_ratios[i], seven_six_error[i]))
            ages_errors1s_filtered = list(filter(lambda x: x[0] < troughOld and x[0] > troughYoung, ages_errors1s))

            tauMethod_WM_6_8, tauMethod_WM_err2s_6_8, tauMethod_WM_MSWD_6_8 = weightedMean(np.array([d[2] for d in ages_errors1s_filtered]), np.array([d[3] for d in ages_errors1s_filtered]))
            tauMethod_WM_7_6, tauMethod_WM_err2s_7_6, tauMethod_WM_MSWD_7_6 = weightedMean(np.array([d[4] for d in ages_errors1s_filtered]), np.array([d[5] for d in ages_errors1s_filtered]))

            Tau_Ratios.append([tauMethod_WM_6_8, tauMethod_WM_err2s_6_8/2, tauMethod_WM_MSWD_6_8, tauMethod_WM_7_6, tauMethod_WM_err2s_7_6, tauMethod_WM_MSWD_7_6, len(ages_errors1s_filtered)])

            Tau_age_calc, MDA_eight_six_age, MDA_seven_six_age = age_calculation(Tau_Ratios, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type,best_age_cut_off)

            Tau_wo_systematic.append([Tau_age_calc[0],Tau_age_calc[1],Tau_age_calc[2],Tau_age_calc[3]])
            
                
        Tau_MDA = systematic_uncertainty_addition(Tau_wo_systematic, Tau_Ratios, sample_list, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type, best_age_cut_off)
            
        for i in range(len(ages)): 
            # Calculate peak indexes
            peakIndexes = list(peakutils.indexes(Tau_PDP[i], thres=thres, min_dist=minDist))
            # Peak ages
            peakAges = Tau_PDP_age[peakIndexes]
            # Number of grains per peak
            peakAgeGrain = peakAgesGrains([peakAges], [ages[i]], [errors[i]])[0]

            # Calculate trough indexes
            troughIndexes = list(peakutils.indexes(Tau_PDP[i]*-1, thres=thres, min_dist=minDist))
            # Trough ages
            troughAges = [0] + list(Tau_PDP_age[troughIndexes]) + [4500] # Append a 0 because there is no trough on the young size of the youngest peak and no trough on the old side of the oldest peak

            # Zip peak ages and grains per peak
            peakAgesGrains_ = list(zip(peakAges, peakAgeGrain))
            # Filter out peaks with less than min_cluster_size grains (default is 3, following Barbeau et al., 2009: EPSL)
            peakAgesGrainsFiltered = list(filter(lambda x: x[1] >= min_cluster_size, peakAgesGrains_))

            # Stop the loop if no peaks are present with the min_cluster_size
            if peakAgesGrainsFiltered == []:
                Tau_Ratios.append([np.nan, np.nan, np.nan, np.nan])
                Tau_MDA.append([np.nan, np.nan, np.nan, np.nan])
                continue

            # Select the nearest trough that is younger than the youngest peak with at least min_cluster_size analyses
            troughYoung = np.max(list(filter(lambda x: x < peakAgesGrainsFiltered[0][0], troughAges)))

            # Select the nearest trough that is older than the youngest peak with at least min_cluster_size analyses
            troughOld = np.min(list(filter(lambda x: x > peakAgesGrainsFiltered[0][0], troughAges)))

            # Select ages and errors that fall between troughYoung and troughOld

            ages_errors1s_plot = list(zip(ages[i], errors[i],1/eight_six_ratios[i], eight_six_error[i],seven_six_ratios[i], seven_six_error[i]))
            ages_errors1s_filtered_plot = list(filter(lambda x: x[0] < troughOld and x[0] > troughYoung, ages_errors1s_plot))
           
            #Plotting
            sample_array = np.array(sample_list)
            sample_arrays = np.split(sample_array,len(sample_array))
            N = len(sample_list)

            samples = sample_arrays[i]

            Taufig, Tauax = plt.subplots(1,figsize=(plotwidth, plotheight))
            Tauax.plot(Tau_PDP_age, Tau_PDP[i])
            Tauax.set_xlabel('Age (Ma)')
            Tauax.set_title(samples[0])
            Tauax.set_xlim(0,(Tau_MDA[i][0]+500))
            Taufig.tight_layout(pad=3)

            for a,b,c,d,e,f in ages_errors1s_filtered_plot:
                Tauax.plot(a,0,'.',color='red',markersize="5")

            Tauax.plot(a,0,'.',color='red',markersize="5", label= str(Tau_MDA[i][3])+' Grains Between Minima of The Youngest Peak')

            Tauax.axvline(Tau_MDA[i][0],color='black', linestyle='dotted', label="MDA: "+str(round(Tau_MDA[i][0],2))+"+/- "+str(round(Tau_MDA[i][1],2)))

            plt.legend(loc='upper right')

            if Image_File_Option == 'web':
                filename = 'Tau_Plots_' + str(samples[0])
                asset_folder = 'assets/plots/Individual_MDA_Plots/'
                for fileformat in ['.svg', '.tiff', '.eps', '.png', '.pdf', '.jpeg']:
                    Taufig.savefig(asset_folder + filename + fileformat)
                plt.close(Taufig)   
            else:
                Taufig.savefig('Saved_Files/Individual_MDA_Plots/Tau_Plots.' + Image_File_Option)  



    if Data_Type == "Ages":
        for i in range(len(ages)): 
            
            
            # Calculate peak indexes
            peakIndexes = list(peakutils.indexes(Tau_PDP[i], thres=thres, min_dist=minDist))
            # Peak ages
            peakAges = Tau_PDP_age[peakIndexes]
            # Number of grains per peak
            peakAgeGrain = peakAgesGrains([peakAges], [ages[i]], [errors[i]])[0]

            # Calculate trough indexes
            troughIndexes = list(peakutils.indexes(Tau_PDP[i]*-1, thres=thres, min_dist=minDist))
            # Trough ages
            troughAges = [0] + list(Tau_PDP_age[troughIndexes]) + [4500] # Append a 0 because there is no trough on the young size of the youngest peak and no trough on the old side of the oldest peak

            # Zip peak ages and grains per peak
            peakAgesGrains_ = list(zip(peakAges, peakAgeGrain))
            # Filter out peaks with less than min_cluster_size grains (default is 3, following Barbeau et al., 2009: EPSL)
            peakAgesGrainsFiltered = list(filter(lambda x: x[1] >= min_cluster_size, peakAgesGrains_))

            # Stop the loop if no peaks are present with the min_cluster_size
            if peakAgesGrainsFiltered == []:
                Tau_Ratios.append([np.nan, np.nan, np.nan, np.nan])
                Tau_MDA.append([np.nan, np.nan, np.nan, np.nan])
                continue

            # Select the nearest trough that is younger than the youngest peak with at least min_cluster_size analyses
            troughYoung = np.max(list(filter(lambda x: x < peakAgesGrainsFiltered[0][0], troughAges)))

            # Select the nearest trough that is older than the youngest peak with at least min_cluster_size analyses
            troughOld = np.min(list(filter(lambda x: x > peakAgesGrainsFiltered[0][0], troughAges)))

            # Select ages and errors that fall between troughYoung and troughOld
            ages_errors1s = list(zip(ages[i], errors[i],ages[i], errors[i],ages[i], errors[i]))
            ages_errors1s_filtered = list(filter(lambda x: x[0] < troughOld and x[0] > troughYoung, ages_errors1s))

            tauMethod_WM, tauMethod_WM_err2s, tauMethod_WM_MSWD = weightedMean(np.array([d[0] for d in ages_errors1s_filtered]), np.array([d[1] for d in ages_errors1s_filtered]))
            Tau_MDA.append([tauMethod_WM, tauMethod_WM_err2s/2, tauMethod_WM_MSWD, len(ages_errors1s_filtered)])
                
            #Plotting
            sample_array = np.array(sample_list)
            sample_arrays = np.split(sample_array,len(sample_array))
            N = len(sample_list)

            samples = sample_arrays[i]

            Taufig, Tauax = plt.subplots(1,figsize=(plotwidth, plotheight))
            Tauax.plot(Tau_PDP_age, Tau_PDP[i])
            Tauax.set_xlabel('Age (Ma)')
            Tauax.set_title(samples[0])
            Tauax.set_xlim(0,(Tau_MDA[i][0]+500))
            Taufig.tight_layout(pad=3)
            
            for a,b,c,d,e,f in ages_errors1s_filtered:
                Tauax.plot(a,0,'.',color='red',markersize="5")

            Tauax.plot(a,0,'.',color='red',markersize="5",label= str(Tau_MDA[i][3])+' Grains Between Minima of The Youngest Peak')


            Tauax.axvline(Tau_MDA[i][0],color='black', linestyle='dotted', label="MDA: "+str(round(Tau_MDA[i][0],2))+"+/- "+str(round(Tau_MDA[i][1],2)))

            plt.legend(loc='upper right')

            if Image_File_Option == 'web':
                filename = 'Tau_Plots_' + str(samples[0])
                asset_folder = 'assets/plots/Individual_MDA_Plots/'
                for fileformat in ['.svg', '.tiff', '.eps', '.png', '.pdf', '.jpeg']:
                    Taufig.savefig(asset_folder + filename + fileformat)
                plt.close(Taufig)   
            else:
                Taufig.savefig('Saved_Files/Individual_MDA_Plots/Tau_Plots.' + Image_File_Option)  

    
    plt.close(Taufig)
    Tau_Table_ = pd.DataFrame(data=Tau_MDA, index=[sample_list], columns=['Tau_MDA (Ma)', 'Tau_+/-1σ', 'Tau_MSWD','Grains'])
    Tau_Table_['Sample_ID'] = sample_list
    Tau_Table_ = Tau_Table_[['Sample_ID', 'Tau_MDA (Ma)', 'Tau_+/-1σ', 'Tau_MSWD','Grains']] 
   
        
    return Tau_MDA, Tau_Table_

def YSP_outputs(Data_Type, ages, errors, sample_list, YSP_MDA, YSP_cluster, plotwidth, plotheight, age_addition_set_max_plot, Image_File_Option, min_cluster_size=2, MSWD_threshold=1):
    #YSP plotting code author: morganbrooks 
    # Check to see if ages is a list of arrays or just a single list of ages
    if not hasattr(ages[0], '__len__'):
        ages = [ages]
        errors = [errors]   
        
    #Sample_List
    sample_array = np.array(sample_list)
    sample_arrays = np.split(sample_array,len(sample_array))
    N = len(sample_arrays)
    
    #YSP_Cluster
    YSP_cluster_array = np.array(YSP_cluster,dtype=object)
    YSP_cluster_age_arrays_split = np.split(YSP_cluster_array,len(YSP_cluster_array))
    
    #YSP: splitting up the array of: MDA/WM, 1s error, MSWD, grains in cluster  
    YSP_array = np.array(YSP_MDA)
    YSP_MDAs = YSP_array[:,0]
    YSP_error1s = YSP_array[:,1]
    YSP_MSWD = YSP_array[:,2]
    YSP_grains = YSP_array[:,3]
    YSP_MDAs_arrays = np.split(YSP_MDAs,len(YSP_MDAs))
    YSP_error1s_arrays = np.split(YSP_error1s,len(YSP_MDAs))
    YSP_MSWD_arrays = np.split(YSP_MSWD,len(YSP_MDAs))
    YSP_grains_arrays = np.split(YSP_grains,len(YSP_MDAs))
    
    #Ages/Errors
    age_array = np.array(ages,dtype=object)
    error_array = np.array(errors,dtype=object)
    YSP_age_arrays = np.split(age_array,len(ages))
    YSP_error_arrays = np.split(error_array,len(ages))
    
    for i in range(len(age_array)): 
        agesi = age_array[i]
  
    
    for i in range(len(agesi)):
        def create_x(t, w, n, d):
            return [t*x + w*n for x in range(d)]

        t = 1 # sets of data
        w = 0.3 # We generally want bars to be 0.8
        n = 1 # first set of data
        d = len(agesi) # topics we're plotting
        plot_x = create_x(t,w,n,d)
        middle = [ a / 2.0 for a in plot_x]
    
        middle_x_array = np.array(middle)
        x_arrays = np.split(middle_x_array,len(agesi))
            
    #Plotting     
    
    YSPfig, YSPax = plt.subplots(N,1, figsize=(plotwidth, N*plotheight))
    cluster_age_plus_error = []    

    for i in range(N):
        
        #Preparing the data to be plotted"
        
        #Setting up the age and error by sample: sorted by age
        YSP_age_error_1s_ = list(zip(ages[i],errors[i]))
        YSP_age_error_1s_.sort(key=lambda d: d[0])
        YSP_age_error_1s_sorted = np.array(YSP_age_error_1s_)
        
        YSP_ages = YSP_age_error_1s_sorted[:,0]
        YSP_error = YSP_age_error_1s_sorted[:,1]
        
        YSP_age_error_1s = list(zip(YSP_ages,YSP_error,middle_x_array))
        
        if N > 1:
            YSPax[i] = plt.subplot2grid((N,1),(i,0))
            YSPaxi = YSPax[i]
        else:
            YSPaxi = YSPax
        if Image_File_Option == 'web': 
            YSPfig, YSPaxi = plt.subplots(1,1, figsize=(plotwidth, 1*plotheight))

        #Sample_List 
        samples = sample_arrays[i]
        
        #YSP MDA, Errors, MSWD, grains in cluster; formatted for plotting  
        YSP_error1s = YSP_error1s_arrays[i]
        YSP_error2s = YSP_error1s_arrays[i]*2
        YSP_MDAs_1s = list(zip(YSP_MDAs_arrays[i],YSP_error1s,YSP_MSWD_arrays[i],YSP_grains_arrays[i]))
        YSP_MDAs_2s = list(zip(YSP_MDAs_arrays[i], YSP_error2s,YSP_MSWD_arrays[i],YSP_grains_arrays[i]))
        YSP_value = YSP_MDAs_1s[0][0]
        YSP_err1s_value = YSP_MDAs_1s[0][1]
        YSP_err2s_value = YSP_MDAs_2s[0][1]
        YSP_MSWD_value = YSP_MDAs_1s[0][2]
        YSP_grains_value = YSP_MDAs_1s[0][3]
        
        #Ages/Errors
        YSP_error1s_i = errors[i]
        YSP_error2s_i = errors[i]*2
        YSP_ages_i = ages[i]
              
        YSP_cluster_age_arrays_split_i = YSP_cluster[i]
        YSP_max_cluster = np.max(YSP_cluster_age_arrays_split_i)
                
        if Data_Type == '238U/206Pb_&_207Pb/206Pb':      
            for s, t, u in YSP_cluster_age_arrays_split_i:
                clust_age = s
                clust_error = t
                cluster_age_and_error = s+t
                cluster_age_plus_error.append(cluster_age_and_error)

        if Data_Type == 'Ages':      
            for s, t, u in YSP_cluster_age_arrays_split_i:
                clust_age = s
                clust_error = t
                cluster_age_and_error = s+t
                cluster_age_plus_error.append(cluster_age_and_error)
       
        L = len(YSP_cluster_age_arrays_split_i)
        
        C = cluster_age_plus_error[-L:]
       
        #Set up plotting parameters
        plotting_max = YSP_max_cluster + age_addition_set_max_plot
        plotted_ages = np.count_nonzero(YSP_ages_i < plotting_max)
        
        if plotted_ages<6:
            width=0.002
            x_tick_adjust=0.0002
        
        elif plotted_ages<16:
            width=0.11
            x_tick_adjust=0.019
        
        elif plotted_ages<20:
            width=0.22
            x_tick_adjust=0.03
           
        else:
            width=0.22
            x_tick_adjust=0.09
       
        for l, m, n in YSP_age_error_1s:    
            YSP_age_value = l 
            YSP_error1s_value = m
            YSP_age_plus_error = l+m
            YSP_error2s_value = m*2
            x_tick = n
        
            if YSP_age_value < plotting_max:
                    
                if plotted_ages<6:
                        x_tick = n/20
                            
                if any(C==YSP_age_plus_error) == True:
                    YSPaxi.broken_barh([(x_tick, width)], (YSP_age_value-YSP_error2s_value, YSP_error1s_value), facecolors=('lightcoral')) #label='2s Uncertainty')
                    YSPaxi.broken_barh([(x_tick, width)], (YSP_age_value-YSP_error1s_value,YSP_error1s_value), facecolors=('crimson')) #label='1s Uncertainty')
                    YSPaxi.broken_barh([(x_tick, width)], (YSP_age_value, YSP_error1s_value), facecolors=('crimson'))
                    YSPaxi.broken_barh([(x_tick, width)], (YSP_age_value+YSP_error1s_value, YSP_error1s_value), facecolors=('lightcoral'))   
                    YSPaxi.hlines(y=YSP_age_value, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'pink', lw=1,linewidth=3) #label='Cluster' )
                
                else:
                    YSPaxi.broken_barh([(x_tick, width)], (YSP_age_value-YSP_error2s_value, YSP_error1s_value), facecolors=('lightsteelblue')) #label='2s Uncertainty')
                    YSPaxi.broken_barh([(x_tick, width)], (YSP_age_value-YSP_error1s_value,YSP_error1s_value), facecolors=('cornflowerblue')) #label='1s Uncertainty')
                    YSPaxi.broken_barh([(x_tick, width)], (YSP_age_value, YSP_error1s_value), facecolors=('cornflowerblue'))
                    YSPaxi.broken_barh([(x_tick, width)], (YSP_age_value+YSP_error1s_value, YSP_error1s_value), facecolors=('lightsteelblue'))      
                    YSPaxi.hlines(y=YSP_age_value, xmin=x_tick, xmax=(x_tick+(width-x_tick_adjust)), color = 'midnightblue', lw=1, linewidth=3) #label='Age', )
            else:
                break 
        
        YSPaxi.hlines(y=YSP_value, xmin=0, xmax=(0), color = 'midnightblue', lw=1, linewidth=3, label='Age'+" " +'(Ma)')
        YSPaxi.axhline(YSP_value,color='black', linestyle='dotted', label='MDA: '+str(round(YSP_value,2))+"+/- "+str(round(YSP_err1s_value,2)))
        YSPaxi.broken_barh([(0.15, 0)], (YSP_value,0), facecolors=('cornflowerblue'), label='1σ Uncertainty')
        YSPaxi.broken_barh([(0.15, 0)], (YSP_value,0), facecolors=('lightsteelblue'), label='2σ Uncertainty')
        YSPaxi.broken_barh([(0.15, 0)], (YSP_value,0), facecolors=('crimson'), label='Cluster: '+str(YSP_grains_value))
        
        YSPaxi.set_xticks([])
        
        YSPaxi.set_ylabel('Age'+" " +'(Ma)')                
        YSPaxi.set_xlabel('Individual Age Measurements +/- 1σ/2σ Uncertainty')
        YSPaxi.set_title(samples[0]) 
        YSPaxi.yaxis.grid(True)
        plt.legend(loc='lower right')
        YSPfig.tight_layout(pad=1)
 
        if Image_File_Option == 'web':
            filename = 'YSP_Plots_' + str(samples[0])
            asset_folder = 'assets/plots/Individual_MDA_Plots/'
            for fileformat in ['.svg', '.tiff', '.eps', '.png', '.pdf', '.jpeg']:
                YSPfig.savefig(asset_folder + filename + fileformat)
            plt.close(YSPfig)   
        else:
            YSPfig.savefig('Saved_Files/Individual_MDA_Plots/YSP_Plots.' + Image_File_Option)  
    
    plt.close(YSPfig)
    YSP_Table_ = pd.DataFrame(data=YSP_MDA, index=[sample_list], columns=['YSP_MDA (Ma)', 'YSP_+/-1σ', 'YSP_MSWD','YSP_Grains'])
    YSP_Table_['Sample_ID'] = sample_list
    YSP_Table_ = YSP_Table_[['Sample_ID','YSP_MDA (Ma)', 'YSP_+/-1σ', 'YSP_MSWD','YSP_Grains']] 
    
    return YSP_MDA, YSP_Table_ 

#MLA calculation code (not present) is sourced from IsoplotR: @authors: Pieter Vermeesch: Reference: Vermeesch, P., 2018, IsoplotR: a free and open toolbox for geochronology. Geoscience Frontiers, v.9, p.1479-1493, doi: 10.1016/j.gsf.2018.04.001.
#MLA import code written by Morgan Brooks 

def MLA_outputs(sample_list, dataToLoad, web=False):
    
    # Lets delete all files that are inside the temp folder
    # The solution is a mix of python, R and markdown to manage the files, plot and display of pictures here on jupyter.
    files = glob.glob("Saved_Files/MLA_Plots/*.png")    
    #
    for f in files:
        os.remove(f)
    # We convert the Python list to a json to be able to send it as an argument to R. Just make sure there are 
    # elements at this list at all times, otherwise the R script breaks.
    samples = json.dumps(sample_list)
    # we call the RScript using subprocess and send the path to the file containing the data and a string 
    # with a name for the file to be saved on the temporary folder.
    output = subprocess.check_output(["Rscript", 'R_Scripts/IsoPlotR.R', dataToLoad[0], samples])
    results = json.loads(output)
    # output2 = subprocess.check_output(["Rscript", 'R_Scripts/IsoPlotR2.R', dataToLoad[0], samples], universal_newlines=True)
    # then we convert the json returned to a dictionary by reading it as a json format
    MDA_Values = {k:results[k][0] for k in results.keys()}
    Error_Values = {k:results[k][1] for k in results.keys()}
    # Then we print the dictionary returned by R from the peakfit function
    
    # print("\n") # I just printed a line between the numbers, you can delete this line anytime
    # or we can print the value for a given sample
    #print(peak_values['UK027'])
    # ![title](temp/teste_plot_UK017.png)
    
    ds = [MDA_Values, Error_Values]
    MLA_MDA_1sError = {}
    for k in MDA_Values.keys():
        MLA_MDA_1sError[k] = tuple(MLA_MDA_1sError[k] for MLA_MDA_1sError in ds)
    
    MLA_Table = pd.DataFrame.from_dict(MLA_MDA_1sError,orient='index').reset_index()
    pd.options.display.float_format = "{:,.2f}".format
    MLA_Table.columns = ['Sample_ID', 'MLA_MDA (Ma)', 'MLA_+/-1σ']
    
    if web:
        return MLA_Table
    else:
        return radial_plots()


def radial_plots():
    
    # list all files on the temp folder
    fs = glob.glob("assets/plots/IsoplotR/*.png")     

    # And we list and import all files contained within the temp folder.
    # as we deleted the files from the previous analysis, onle the ones generated at this session are shown
    images = []
    
    for ea in fs:
        images.append(dp.Image(filename=ea, format='png'))
    
    # display all images contained in the temp folder
    
    for ea in images:
        print(" ")
        title = re.findall('(?<=plot_).+?(?=.png)', ea.filename)[0]
        print('\033[1m' + title + "\033[0m")
        print(" ")
        plots = dp.display_png(ea)
    
    return 

# Functions for loading a dataset and selecting samples 
# Code below obtained from detritalPy_v1.3: @authors: glennrsharman, jonathanpsharman, zoltansylvester

def loadDataExcel(dataToLoad, Data_Type, mainSheet = 'Samples', dataSheet = 'Data', ID_col = 'Sample_ID'):
    
    obj1 = []
    obj2 = []
    obj3 = []
    obj4 = []
    for i in range(len(dataToLoad)):
        dfs = pd.read_excel(dataToLoad[i],sheet_name=None)
        main_df = None
        main_df = dfs[mainSheet]
        samples_df = main_df.copy()
        analyses_df = dfs[dataSheet]

        for sample_ind in range(main_df.shape[0]): # loop through entries in main_df
            active_sample_id = main_df.loc[sample_ind,ID_col]
            active_UPb_data = dfs[dataSheet].loc[dfs[dataSheet][ID_col].isin([active_sample_id]),:]
            for colname in active_UPb_data:
                if colname not in [ID_col]: # Skip if the indexing column
                    # Check column naming overlap with the Samples table (having the same column name will otherwise result in an error)
                    if colname in samples_df.columns:
                        colname_adj = colname+'_'+dataSheet # New name for colname
                        if colname_adj not in main_df.columns: # Make colname with revised name if already in samples table
                            main_df[colname_adj] = (np.nan*np.empty(shape=(len(main_df),1))).tolist()
                            main_df[colname_adj] = np.asarray(main_df[colname_adj])                
                        main_df.at[sample_ind,colname_adj] = active_UPb_data[colname].values
                    else:
                        if colname not in main_df.columns: # Make colname with revised name if already in samples table
                            main_df[colname] = (np.nan*np.empty(shape=(len(main_df),1))).tolist()
                            main_df[colname] = np.asarray(main_df[colname])
                        main_df.at[sample_ind,colname] = active_UPb_data[colname].values

        # Make a copy of the dataset and set the sample ID as index
        main_byid_df = main_df.copy()
        main_byid_df.set_index(ID_col,inplace=True,drop=False)
        obj1.append(main_df)
        obj2.append(main_byid_df)
        obj3.append(samples_df)
        obj4.append(analyses_df)
    main_df = pd.concat(obj1, sort=False)
    main_byid_df = pd.concat(obj2, sort=False)
    samples_df = pd.concat(obj3, sort=False)
    analyses_df = pd.concat(obj4, sort=False)

    return main_df, main_byid_df, samples_df, analyses_df, Data_Type


#Check that the Data Loaded Properly & Review Unique Samples: code by morganbrooks


def check_data_loading(df, Data_Type): 
    

    if Data_Type == 'Ages':
        amount_of_samples = df.Sample_ID.nunique()
        sample_array = df["Sample_ID"].unique() 
        sample_list = list(sample_array)
        sample_amounts_table = df.groupby('Sample_ID').Best_Age.count().reset_index()
        sample_amounts_table.rename(columns={
        'Best_Age': 'Sample_Size'},
        inplace=True)
        print('')
        print('')
        print(str(amount_of_samples) + " unique samples were found in your data" + " " + str(sample_list) +  " " + "with the following sample sizes:")
        print('')
        
    if Data_Type == '238U/206Pb_&_207Pb/206Pb':
        amount_of_samples = df.Sample_ID.nunique()
        sample_array = df["Sample_ID"].unique() 
        sample_list = list(sample_array)
        df.rename(columns={
        '238U/206Pb': 'eight_six_U_Pb'},
        inplace=True)
        sample_amounts_table = df.groupby('Sample_ID').eight_six_U_Pb.count().reset_index()
        sample_amounts_table.rename(columns={
        'eight_six_U_Pb': 'Sample_Size'},
        inplace=True)
        print('')
        print('')
        print(str(amount_of_samples) + " unique samples were found in your data" + " " + str(sample_list) +  " " + "with the following sample sizes:")
        print('')
        
    
    return sample_amounts_table

#Convert the excel data to an array of ages and errors 
#A portion of the code was obtained from detritalPy_v1.3: @authors: glennrsharman, jonathanpsharman, zoltansylvester
#Morgan Brooks edits have been made to include a an array of 6/8 ratios 7/6 ratios, option for percent or absolute and sigma 1/2. Calculates ages and uncertainties from ratios.
    
def sampleToData(sample_list, main_byid_df, sigma, Data_Type, uncertainty, best_age_cut_off, U238_decay_constant, U235_decay_constant,U238_U235,excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235):
    
    ages = [] 
    errors = []
    
    errors_no_conversion = []
    numGrains = []
    labels = []
        
    eight_six_ratios = []
    eight_six_error = []
    eight_six_error_no_conversion = []
    eight_six_error_inverse = []
    eight_six_age = []
    eight_six_age_error = []
         
    seven_six_ratios = []
    seven_six_error = []
    seven_six_error_no_conversion = []
    seven_six_age = []
    seven_six_ages_low = []
    seven_six_age_error = []
           
    sorting_age = []
    sorting_error = []    
    
    
    def sampleToData_238U_206Pb_207Pb_206Pb(sample_list, main_byid_df, sigma, uncertainty, best_age_cut_off, U238_decay_constant, U235_decay_constant,U238_U235, sampleLabel='Sample_ID', eight_six_U_Pb='238U/206Pb', eight_six_U_Pb_Err='238U/206Pb_sx', seven_six_Pb_Pb='207Pb/206Pb', seven_six_Pb_Pb_Err='207Pb/206Pb_sx'):

        N = len(sample_list)
        sample_array = np.array(sample_list)
        sample_arrays = np.split(sample_array,len(sample_array))
        
        Rec_U238_decay_constant = (1/(U238_decay_constant))
        Rec_U235_decay_constant = (1/(U235_decay_constant))
    
        
        from scipy import optimize
        
        if type(sample_list[0])==tuple:
            for i in range(N):
                samples = sample_list[i][0]
                # Verify that all samples are in the database
                if not all(sample in list(main_byid_df.Sample_ID) for sample in sample_list[i][0]):
                    print('These samples are not in the database - check for typos!')
                    print(list(np.setdiff1d(sample_list[i][0],list(main_byid_df.Sample_ID))))
                    print('Function stopped')
                    break
                    
                sample238U_206Pb = []
                sample238U_206Pb_Errors = []
                sample207Pb_206Pb = []
                sample207Pb_206Pb_Errors = []

                for sample in samples:                             
                    sample238U_206Pb = np.append(sample238U_206Pb, main_byid_df.loc[sample,  eight_six_U_Pb])
                    sample207Pb_206Pb = np.append(sample207Pb_206Pb, main_byid_df.loc[sample,  seven_six_Pb_Pb])
                    
                    if sigma == 2 and uncertainty == 'percent':
                        sample238U_206Pb_Errors = np.append(sample238U_206Pb_Errors, main_byid_df.loc[sample, eight_six_U_Pb_Err]/2/100)  
                        sample207Pb_206Pb_Errors = np.append(sample207Pb_206Pb_Errors, main_byid_df.loc[sample, seven_six_Pb_Pb_Err]/2/100) 
                    if uncertainty == 'percent':
                        sample238U_206Pb_Errors = np.append(sample238U_206Pb_Errors, main_byid_df.loc[sample, eight_six_U_Pb_Err]/100)  
                        sample207Pb_206Pb_Errors = np.append(sample207Pb_206Pb_Errors, main_byid_df.loc[sample, seven_six_Pb_Pb_Err]/100) 
                    if sigma == 2 and uncertainty == 'absolute':
                        sample238U_206Pb_Errors = np.append(sample238U_206Pb_Errors, main_byid_df.loc[sample, eight_six_U_Pb_Err]/2)  
                        sample207Pb_206Pb_Errors = np.append(sample207Pb_206Pb_Errors, main_byid_df.loc[sample, seven_six_Pb_Pb_Err]/2)
                    if sigma == 1 and uncertainty == 'absolute':
                        sample238U_206Pb_Errors = np.append(sample238U_206Pb_Errors, main_byid_df.loc[sample, eight_six_U_Pb_Err])  
                        sample207Pb_206Pb_Errors = np.append(sample207Pb_206Pb_Errors, main_byid_df.loc[sample, seven_six_Pb_Pb_Err]) 
                
                if uncertainty == 'percent':
                    eight_six_error_no_conversion.append(sample238U_206Pb_Errors)
                    seven_six_error_no_conversion.append(sample207Pb_206Pb_Errors)
                else:
                    eight_six_error.append(sample238U_206Pb_Errors)
                    seven_six_error.append(sample207Pb_206Pb_Errors)
                    
                eight_six_ratios.append(sample238U_206Pb)
                seven_six_ratios.append(sample207Pb_206Pb) 
                numGrains.append(len(sample238U_206Pb))
                labels.append(sample_list[i][1])

        else:
            for sample in sample_list:
                # Verify that all samples are in the database
                if not all(sample in list(main_byid_df.Sample_ID) for sample in sample_list):
                    print('These samples are not in the database - check for typos!')
                    print(list(np.setdiff1d(sample_list,list(main_byid_df.Sample_ID))))
                    print('Function stopped')
                    break            
               
                eight_six_ratios.append(main_byid_df.loc [sample, eight_six_U_Pb])
                seven_six_ratios.append(main_byid_df.loc[sample, seven_six_Pb_Pb])
                
                
                if sigma == 2 and uncertainty == 'percent':
                    eight_six_error_no_conversion.append(main_byid_df.loc[sample, eight_six_U_Pb_Err]/2./100.)
                    seven_six_error_no_conversion.append(main_byid_df.loc[sample, seven_six_Pb_Pb_Err]/2./100.)
                
                if sigma == 1 and uncertainty == 'percent':
                    eight_six_error_no_conversion.append(main_byid_df.loc[sample, eight_six_U_Pb_Err]/100.)
                    seven_six_error_no_conversion.append(main_byid_df.loc[sample, seven_six_Pb_Pb_Err]/100.)
                
                if sigma == 2 and uncertainty == 'absolute':
                    eight_six_error_no_conversion.append(main_byid_df.loc[sample, eight_six_U_Pb_Err]/2.)
                    seven_six_error.append(main_byid_df.loc[sample, seven_six_Pb_Pb_Err]/2.)
                
                if sigma == 1 and uncertainty == 'absolute':
                    eight_six_error_no_conversion.append(main_byid_df.loc[sample, eight_six_U_Pb_Err])
                    seven_six_error.append(main_byid_df.loc[sample, seven_six_Pb_Pb_Err])
                    
                numGrains.append(len(main_byid_df.loc[sample, eight_six_U_Pb]))
                labels.append(main_byid_df.loc[sample,sampleLabel])
                
        
        #converting uncertainty from percent to absolute 
        if uncertainty == 'percent':
            for i in range(len(eight_six_ratios)):
                eight_six_errors_converted = (eight_six_error_no_conversion[i]*(1/eight_six_ratios[i]))
                eight_six_error.append(eight_six_errors_converted)
                
            for i in range(len(seven_six_ratios)):
                seven_six_errors_converted = (seven_six_error_no_conversion[i]*seven_six_ratios[i])
                seven_six_error.append(seven_six_errors_converted)
        
        if uncertainty == 'absolute':
            for i in range(len(eight_six_ratios)):
                eight_six_errors_converted = (eight_six_error_no_conversion[i]*(1/eight_six_ratios[i])*(1/eight_six_ratios[i]))
                eight_six_error.append(eight_six_errors_converted)
        
   
        #age calcuation for ratios 
        #the Pb207/Pb206 Age Calculation below is borrowed from UPbPlot.py Author: Atsushi Noda Copyright: Geological Survey of Japan, AIST  
   
        def func_t76(t, r):
            res = abs(U238_U235 * r - (np.exp(U235_decay_constant * t) - 1) / (np.exp(U238_decay_constant * t) - 1))
            return res
            
        for i in range(len(seven_six_ratios)):
            
            #7/6 Mean Age
            t_m = 1 / U238_decay_constant * np.log(seven_six_ratios[i] + 1)  # initial time for calculation
            T76_m = optimize.leastsq(func_t76, t_m, args=(seven_six_ratios[i]))[0]
            seven_six_age.append(T76_m/1000000)
            
            #7/6 Low Age
            t_l = 1 / U238_decay_constant * np.log((seven_six_ratios[i]-seven_six_error[i]) + 1)  # initial time for calculation
            T76_l = optimize.leastsq(func_t76, t_l, args=(seven_six_ratios[i]-seven_six_error[i]))[0]
            seven_six_ages_low.append(T76_l/1000000)
    
            seven_six_age_errors =  seven_six_age[i] - seven_six_ages_low[i]
            seven_six_age_error.append(seven_six_age_errors)
        
        for i in range(len(eight_six_ratios)):
            log_eight_six_ratio = np.log((1+((1/eight_six_ratios[i]))))
            eight_six_ages = (((Rec_U238_decay_constant) * (log_eight_six_ratio)) / 1000000)
            
            log_eight_six_ratio_low = np.log((1+(((1/(eight_six_ratios[i])- eight_six_error[i])))))
            eight_six_ages_low = (((Rec_U238_decay_constant) * (log_eight_six_ratio_low)) / 1000000)
            
            eight_six_age_errors =  eight_six_ages - eight_six_ages_low
            eight_six_age.append(eight_six_ages)
            eight_six_age_error.append(eight_six_age_errors)
        
        for i in range(len(eight_six_age)):
            sorting_age = (np.where(seven_six_age[i] < best_age_cut_off,eight_six_age[i],seven_six_age[i]))
            ages.append(sorting_age)
            sorting_error = (np.where(ages[i] == eight_six_age[i],eight_six_age_error[i],seven_six_age_error[i]))
            errors.append(sorting_error)
    
        return ages, errors, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, numGrains, labels, sample_list
    
    def sampleToData_ages(sample_list, main_byid_df, sigma, uncertainty, best_age_cut_off, sampleLabel='Sample_ID', bestAge='Best_Age', bestAgeErr='Best_Age_sx'):

        N = len(sample_list)
        sample_array = np.array(sample_list)
        sample_arrays = np.split(sample_array,len(sample_array))
        
        
        if type(sample_list[0])==tuple:
            for i in range(N):
                samples = sample_list[i][0]
                # Verify that all samples are in the database
                if not all(sample in list(main_byid_df.Sample_ID) for sample in sample_list[i][0]):
                    print('These samples are not in the database - check for typos!')
                    print(list(np.setdiff1d(sample_list[i][0],list(main_byid_df.Sample_ID))))
                    print('Function stopped')
                    break
                sampleAges = []
                sampleErrors = []

                for sample in samples:                             
                    sampleAges = np.append(sampleAges, main_byid_df.loc[sample, bestAge])
                   
                    if sigma == 2 and uncertainty == 'percent':
                        sampleErrors = np.append(sampleErrors, main_byid_df.loc[sample, bestAgeErr]/2/100)

                    elif uncertainty == 'percent':
                        sampleErrors = np.append(sampleErrors, main_byid_df.loc[sample, bestAgeErr]/100)
                    elif sigma == 2:
                        sampleErrors = np.append(sampleErrors, main_byid_df.loc[sample, bestAgeErr]/2)
                    else:
                        sampleErrors = np.append(sampleErrors, main_byid_df.loc[sample, bestAgeErr]) 
                
                if uncertainty == 'percent':
                    errors_no_conversion.append(sampleErrors)
                else:
                    errors.append(sampleErrors)
                    
                ages.append(sampleAges)
                numGrains.append(len(sampleAges))
                labels.append(sample_list[i][1])
        
        else:
            for sample in sample_list:
                # Verify that all samples are in the database
                if not all(sample in list(main_byid_df.Sample_ID) for sample in sample_list):
                    print('These samples are not in the database - check for typos!')
                    print(list(np.setdiff1d(sample_list,list(main_byid_df.Sample_ID))))
                    print('Function stopped')
                    break            
                ages.append(main_byid_df.loc[sample, bestAge])
                
                if sigma == 2 and uncertainty == 'percent':
                    errors_no_conversion.append(main_byid_df.loc[sample, bestAgeErr]/2./100.)

                elif uncertainty == 'percent':
                    errors_no_conversion.append(main_byid_df.loc[sample, bestAgeErr]/100.)
                    
                elif sigma == 2:
                    errors.append(main_byid_df.loc[sample, bestAgeErr]/2.)

                else:
                    errors.append(main_byid_df.loc[sample, bestAgeErr])
                numGrains.append(len(main_byid_df.loc[sample, bestAge]))
                labels.append(main_byid_df.loc[sample,sampleLabel])
        
        
        if uncertainty == 'percent':
            for i in range(len(ages)):
                errors_converted = (errors_no_conversion[i]*ages[i])
                errors.append(errors_converted)
    
 
        return ages, errors, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, numGrains, labels, sample_list
    

    
    if Data_Type == "238U/206Pb_&_207Pb/206Pb":
        ages, errors, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, numGrains, labels, sample_list = sampleToData_238U_206Pb_207Pb_206Pb(sample_list, main_byid_df, sigma, uncertainty, best_age_cut_off, U238_decay_constant, U235_decay_constant,U238_U235, sampleLabel='Sample_ID', eight_six_U_Pb='238U/206Pb', eight_six_U_Pb_Err='238U/206Pb_sx', seven_six_Pb_Pb='207Pb/206Pb', seven_six_Pb_Pb_Err='207Pb/206Pb_sx')
    
    if Data_Type == "Ages":
        ages, errors, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, numGrains, labels, sample_list = sampleToData_ages(sample_list, main_byid_df, sigma, uncertainty, best_age_cut_off, sampleLabel='Sample_ID', bestAge='Best_Age', bestAgeErr='Best_Age_sx')

             
    if len(sample_list) == 1:
        ages_array = np.array(ages, dtype=object)
        Ages_Df = pd.DataFrame({'Best_Age': value for value in ages_array})
        sample = []
        for i in range(len(Ages_Df)):
            sample.append(sample_list)

        sample_index_array = np.array(sample)
        sample_index = sample_index_array.flatten()

        Ages_Df['Sample_ID'] = sample_index
        Ages_ = Ages_Df.set_index('Sample_ID')
        Ages_Table = Ages_.explode('Best_Age') 

        errors_array = np.array(errors, dtype=object)
        Errors_Df = pd.DataFrame({'Best_Age_sx': value for value in errors_array})
        Errors_Df['Sample_ID'] = sample_index
        Errors_ = Errors_Df.set_index('Sample_ID')
        Errors_Table = Errors_.explode('Best_Age_sx')
      
        sample_sheet_ = pd.DataFrame(data=sample_list, columns=['Sample_ID'])
        
        ages_errors_calculated = pd.concat([Ages_Table, Errors_Table], axis=1)


        with pd.ExcelWriter('data/ages_errors_calculated.xlsx') as writer:  
            sample_sheet_.to_excel(writer, sheet_name='Samples')
            ages_errors_calculated.to_excel(writer, sheet_name='Data')

        dataToLoad_MLA = ['data/ages_errors_calculated.xlsx']

    elif len(sample_list) > 1:
        ages_array = np.array(ages, dtype=object)
        Ages_Df = pd.DataFrame(data=ages_array, columns=['Best_Age']) 
        Ages_Df['Sample_ID'] = sample_list
        Ages_ = Ages_Df.set_index('Sample_ID')
        Ages_Table = Ages_.explode('Best_Age')
       
        errors_array = np.array(errors, dtype=object)
        Errors_Df = pd.DataFrame(data=errors_array, columns=['Best_Age_sx']) 
        Errors_Df['Sample_ID'] = sample_list
        Errors_ = Errors_Df.set_index('Sample_ID')
        Errors_Table = Errors_.explode('Best_Age_sx')
      
        sample_sheet_ = pd.DataFrame(data=sample_list, columns=['Sample_ID'])

        ages_errors_calculated = pd.concat([Ages_Table, Errors_Table], axis=1)

        with pd.ExcelWriter('data/ages_errors_calculated.xlsx') as writer:  
            sample_sheet_.to_excel(writer, sheet_name='Samples')
            ages_errors_calculated.to_excel(writer, sheet_name='Data')

        dataToLoad_MLA = ['data/ages_errors_calculated.xlsx']
    

    return  ages, errors, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, numGrains, labels, sample_list, best_age_cut_off, dataToLoad_MLA, U238_decay_constant,U235_decay_constant,U238_U235,excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235

#Function to find the youngest clusters that overlap 

#1 First half of Code obtained from detritalPy_v1.3: @authors: glennrsharman, jonathanpsharman, zoltansylvester

#2 Second half of code written by Morgan Brooks (added larger cluster criteria where all within sigma overlap are included). Code from detritalPy will sort grains by age+sigma and create a cluster until the youngest upper limit (top) is <= any of the bottom limits, and then stop. This leaves out many grains after this point. Also altered code to include the option of using isotopic ratios to cluster grains. The weighted mean of the cluster of isotopic ratios is then calculated and the age of that weighted mean ratio is computed for a final MDA. 

def find_youngest_cluster(data_err1s, sample_list, min_cluster_size=2):
    
    #1. determine top and bottom of cluster: The age and range which defines it 
    
    i_min = 0
    i_max = 0
    
    N = len(sample_list)
    
    for i in range(1, len(data_err1s)):
        bigtop = data_err1s[i_min][0] + data_err1s[i_min][1]
        bigbottom = data_err1s[i_min][0] - data_err1s[i_min][1]
            
        tops = data_err1s[i][0] + data_err1s[i][1]
        bottoms = data_err1s[i][0] - data_err1s[i][1]

        if (bigtop >= bottoms) and (bigbottom <= tops):
            i_max = i
            
        elif i_max - i_min + 1 >= min_cluster_size:
            break
        else:
            i_min = i
            i_max = i
    
    #2 grab all ages who satisfy cluster criteria 
    cluster = []
    age_cluster = []
            
    for l,m,n,o,p,q in data_err1s:
        age = l
        error1s = m
        ratio1 = n
        ratio_error1 = o
        ratio2 = p
        ratio_error2 = q
        tops = l + m
        bottoms = l - m
        
        if (bigtop >= bottoms) and (bigbottom <= tops):
            cluster.append([l,m,n,o,p,q])
            age_cluster.append([l,m])
            
         
    for i in range(N):
        array_cluster = np.array(cluster)
        max_cluster = np.max(array_cluster)
        
        
    return cluster if i_min < i_max else [], max_cluster, age_cluster

#Function to Calculate the weighted mean of a group of ages 
#Code obtained from detritalPy_v1.3: @authors: glennrsharman, jonathanpsharman, zoltansylvester

def weightedMean(ages,error1s,conf=0.95):
    """
    Calculates the weighted mean, its 2-sigma uncertainty, and MSWD

    Paramters
    ---------
    ages : a 1D array of ages
    errors : an array of 1-sigma errors
    conf : (optional) confidence level

    Returns
    -------
    Twm : weighted mean age
    sm : 2-sigma uncertainty
    MSWD : Mean Square of the Weighted Deviation

    """

    from scipy import stats
    
    w=np.array(error1s)**(-2)/np.sum(np.array(error1s)**(-2)) # weight
    Twm=np.sum(w*np.array(ages)) # weight mean of age
    S=np.sum((np.array(ages)-Twm)**2/np.array(error1s)**2) # S
    N=len(ages)
    MSWD=S/(N-1) # Mean Square of the Weighted Deviation
    
    # Standard deviation of the weighted mean (2 sigma)
    sm=stats.norm.ppf(conf+(1-conf)/2.)*np.sqrt(1./np.sum(np.array(error1s)**(-2)))
    
    return(Twm,sm,MSWD)


#Function to Calculate the PDP for an array of ages
#Code obtained from detritalPy_v1.3: @authors: glennrsharman, jonathanpsharman, zoltansylvester

def PDPcalcAges(ages, errors, x1=0, x2=4500, xdif=1, cumulative=False):    
    """
    Computes the PDP for an array of ages.
    
    Parameters
    ----------
    ages : array of ages, len(ages)=number of samples or sample groups
    errors : array of 1s errors
    x1 : (optional) beginning of range to compute PDP (default = 0 Ma)
    x2 : (optional) end of range to compute PDP (default = 4500 Ma)
    xdif : (optional) bin size to compute PDP (default = 1 Ma)
    cumulative : (optional) If True, will compute a cumulative PDP (CPDP)
    
    Returns
    -------
    PDP_age : array of ages that PDP is computed over    
    PDP : array of PDP functions
    
    Notes
    -----
    """
    from scipy.stats import norm
    PDP_age = np.arange(0, 4500+xdif, xdif) # Ensures that the PDP is calculated over all of geologic time
    PDPe = np.empty(shape=(len(ages),len(PDP_age))) # Create an empty array of appropriate shape
    PDP = np.zeros_like(PDPe) # Copy the array, but with zeros
    for i in range(len(ages)):
        data = ages[i]
        data_err = errors[i]
        pdf_cum = 0 # Creates an empty variable        
        for j in range(len(data)):      
            age = data[j]
            error = data_err[j]
            pdf = norm.pdf(PDP_age, age, error)
            pdf_cum = pdf_cum + pdf 
        pdf_cum = np.around(pdf_cum/np.trapz(pdf_cum), decimals=10)
        if cumulative:
            pdf_cum = np.cumsum(pdf_cum)        
        PDP[i] = pdf_cum
    PDP_age = PDP_age[int(x1/xdif):int((x2+xdif)/xdif)] # Only select the values within the specified plotting age range
    PDPportionRange = np.arange(x1, x2+xdif, xdif)
    PDPportionEmpty = np.empty(shape=(len(ages),len(PDPportionRange)))
    PDPportion = np.zeros_like(PDPportionEmpty) # Copy the array, but with zeros
    for i in range(len(ages)):
        PDPportion[i] = PDP[i][int(x1/xdif):int((x2+xdif)/xdif)] # Only select the values within the specified plotting age range
    return PDP_age, PDPportion


#Functions to Calculate the peak ages in a probability distribution 
#Code obtained from detritalPy_v1.3: @authors: glennrsharman, jonathanpsharman, zoltansylvester

def peakAge(DF_age, DF, ages, errors, thres=0.05, minDist=5, minPeakSize=3):
    """
    Identifies peak ages in a given relative probability distribution (e.g., PDP, KDE)
    
    Parameters
    ----------
    DF_age, DF : Arrays of ages and probability values of a relative probability distribution (e.g., PDP, KDE)
    thres : Threshold of what constitues a peak (from 0 to 1). Default = 0.05
    minDist : Minimum distance (Myr) between adjacent peaks. Default = 5
        
    Returns
    -------
    peakAges : array of peak ages (Myr) for each sample or sample group
    indexes : array of the indexes where peak ages occur
    
    Notes
    -----
    Requires the package peakutils to be installed
    pip install peakutils
    """     
    import peakutils
    peakAges = []
    indexes = []
    for i in range(len(DF)):
        indexes = indexes + [list(peakutils.indexes(DF[i], thres=thres, min_dist=minDist))]
        peakAges = peakAges + [list(DF_age[indexes[i]])]
    peakAgeGrain = peakAgesGrains(peakAges, ages, errors)
    
    # Remove peaks with fewer grains than the minimum peak size
    for i in reversed(range(len(peakAges))):
        for j in reversed(range(len(peakAgeGrain[i]))):
            if peakAgeGrain[i][j] < minPeakSize:
                del peakAges[i][j]
                del peakAgeGrain[i][j]
                del indexes[i][j]
    return peakAges, indexes, peakAgeGrain

def peakAgesGrains(peakAges, ages, errors, sig=2):
    import copy
    peakAgeGrain = copy.deepcopy(peakAges)
    for i in range(len(peakAges)): # One loop per sample or sample group
        for j in range(len(peakAges[i])): # One loop per peak
            c = 0 # counter variable
            for k in range(len(ages[i])): # Loop through each analysis
                if (ages[i][k]-errors[i][k]*sig <= peakAges[i][j] <= ages[i][k]+errors[i][k]*sig):
                    c = c+1
            peakAgeGrain[i][j] = c
    return peakAgeGrain   
           
#age calcuation for ratios after cluster formed with ages 
#code written by Morgan Brooks 
    
def age_calculation(MDAs_ratios, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type, best_age_cut_off):
    
    from scipy import optimize
        
    Rec_U238_decay_constant = (1/(U238_decay_constant))
    Rec_U235_decay_constant = (1/(U235_decay_constant))
   
    MDA_eight_six_age = []
    MDA_eight_six_age_error = []

    MDA_seven_six_age = []
    MDA_seven_six_age_error = []
    MDA_seven_six_age_low = []
    MDA_seven_six_age_error = []
        
    Age_Calculated_MDAs = []
    MDA_best_age = []
    MDA_best_error = []
    ratio_calc_WMSD = []
        
    MDA_ratio_calc_array = np.array(MDAs_ratios)
    
    MDA_6_8_ratio_age = MDA_ratio_calc_array [:,0]
    MDA_6_8_ratio_error1s = MDA_ratio_calc_array [:,1]
    MDA_6_8_ratio_calc_WMSD = MDA_ratio_calc_array [:,2]
    
    MDA_7_6_ratio_age = MDA_ratio_calc_array [:,3]
    MDA_7_6_ratio_error1s = MDA_ratio_calc_array [:,4]
    MDA_7_6_ratio_calc_WMSD = MDA_ratio_calc_array [:,5]
    
    MDA_ratio_calc_cluster_length = MDA_ratio_calc_array[:,6]
    
    
    MDA_ratio_calc_age_arrays_6_8 = np.split(MDA_6_8_ratio_age ,len(MDA_6_8_ratio_age))
    MDA_ratio_calc_age_arrays_7_6 = np.split(MDA_7_6_ratio_age ,len(MDA_7_6_ratio_age))
    
    MDA_ratio_calc_error1s_arrays = np.split(MDA_6_8_ratio_error1s ,len(MDA_6_8_ratio_error1s))
  

    if Data_Type == '238U/206Pb_&_207Pb/206Pb':
         
        #the Pb207/Pb206 Age Calculation below is borrowed from UPbPlot.py Author: Atsushi Noda Copyright: Geological Survey of Japan, AIST  
        def func_t76(t, r):
            res = abs(U238_U235 * r - (np.exp(U235_decay_constant * t) - 1) / (np.exp(U238_decay_constant * t) - 1))
            return res
            
        for i in range(len(MDA_ratio_calc_age_arrays_7_6)):
            
            #7/6 Mean Age
            t_m = 1 / U238_decay_constant * np.log(MDA_7_6_ratio_age[i] + 1)  # initial time for calculation
            T76_m = optimize.leastsq(func_t76, t_m, args=(MDA_7_6_ratio_age[i]))[0]
            MDA_seven_six_ages = (T76_m/1000000)
            MDA_seven_six_age.append(MDA_seven_six_ages)
            
            #7/6 Low Age
            t_l = 1 / U238_decay_constant * np.log((MDA_7_6_ratio_age[i]-MDA_7_6_ratio_error1s[i]) + 1)  # initial time for calculation
            T76_l = optimize.leastsq(func_t76, t_l, args=(MDA_7_6_ratio_age[i]-MDA_7_6_ratio_error1s[i]))[0]
            MDA_seven_six_age_low.append(T76_l/1000000)
    
            MDA_seven_six_age_errors =  MDA_seven_six_age[i] - MDA_seven_six_age_low[i]
            MDA_seven_six_age_error.append(MDA_seven_six_age_errors)
        
        for i in range(len(MDA_ratio_calc_age_arrays_6_8)):  
            
            #6/8 Mean Age
            MDA_log_eight_six_ratio = np.log((1+((MDA_6_8_ratio_age[i]))))
            MDA_eight_six_ages = (((Rec_U238_decay_constant) * (MDA_log_eight_six_ratio)) / 1000000)
            
            #6/8 Low Age
            MDA_log_eight_six_ratio_low = np.log((1+((((MDA_6_8_ratio_age[i])-MDA_6_8_ratio_error1s[i])))))
            MDA_eight_six_ages_low = (((Rec_U238_decay_constant) * (MDA_log_eight_six_ratio_low)) / 1000000)

            MDA_eight_six_age_errors =  MDA_eight_six_ages - MDA_eight_six_ages_low
            MDA_eight_six_age.append(MDA_eight_six_ages)
            MDA_eight_six_age_error.append(MDA_eight_six_age_errors)
     

        for i in range(len(MDA_eight_six_age)):
            MDA_best_age_ = (np.where(MDA_seven_six_age[i] < best_age_cut_off,MDA_eight_six_age[i],MDA_seven_six_age[i]))
            MDA_best_error_ = (np.where(MDA_best_age_ == MDA_eight_six_age[i],MDA_eight_six_age_error[i],MDA_seven_six_age_error[i]))
            ratio_calc_WMSD_ = (np.where(MDA_best_age_ == MDA_eight_six_age[i],MDA_6_8_ratio_calc_WMSD[i],MDA_7_6_ratio_calc_WMSD[i]))
            
            MDA_best_age = list(MDA_best_age_)
            MDA_best_error= list(MDA_best_error_)
            ratio_calc_WMSD = list (ratio_calc_WMSD_)
            ratio_calc_cluster_length = MDA_ratio_calc_cluster_length[i]
            
            eight_six_and_seven_six_ages = []
            
            age_calc = list([MDA_best_age, MDA_best_error, ratio_calc_WMSD, ratio_calc_cluster_length])
       
            eight_six_and_seven_six_ages = []
            
            age_calc_array = []
            
            def flatten_age_calc_list(age_calc):
                # iterating over the data
                for element in age_calc:
                    # checking for list
                    if type(element) == list:
                        # calling the same function with current element as new argument
                        flatten_age_calc_list(element)
                    else:
                        age_calc_array.append(element)

            # flattening the given list
            flatten_age_calc_list(age_calc)
       
       
    return age_calc_array,MDA_eight_six_age,MDA_seven_six_age

def systematic_uncertainty_addition(MDAs_ages, MDAs_ratios, sample_list, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, U238_decay_constant, U235_decay_constant, U238_U235,  Data_Type, best_age_cut_off):
 
    N = len(sample_list)
    import math 
    
    MDAs_ages_array = np.array(MDAs_ages)
    
    excess_variance_206_238_sq = (excess_variance_206_238**2)
    excess_variance_207_206_sq = (excess_variance_207_206**2)
    Sy_calibration_uncertainty_206_238_sq = (Sy_calibration_uncertainty_206_238**2) 
    Sy_calibration_uncertainty_207_206_sq = (Sy_calibration_uncertainty_207_206**2) 
    decay_constant_uncertainty_U238_sq = (decay_constant_uncertainty_U238**2)
    decay_constant_uncertainty_U235_sq =  (decay_constant_uncertainty_U235**2)
    
    Add_and_square_root_constants_206_238_ = (math.sqrt(excess_variance_206_238_sq+Sy_calibration_uncertainty_206_238_sq+decay_constant_uncertainty_U238_sq))
    Add_and_square_root_constants_207_206_= (math.sqrt(excess_variance_207_206_sq+Sy_calibration_uncertainty_207_206_sq+decay_constant_uncertainty_U238_sq+decay_constant_uncertainty_U235_sq))
    
    sy_age_cal = []
    mean_age = []
    
    seven_six_age_low = []
    seven_six_age_mean = []
    
    eight_six_age_low = []
    eight_six_age_mean = []
    
    total_uncertainty_7_6 = []
    total_uncertainty_8_6 = []
    one_s_abs_total_8_6 = []
    one_s_abs_total_7_6 = []
    total_uncertainty_7_6_ = []
    total_uncertainty_8_6_ = []
    
    
    for a,b,c,d,e,f,g in MDAs_ratios:
        error_percent_7_6 = (e/d)*100
        error_percent_7_6_2s = error_percent_7_6*2
        error_percent_sq_7_6 = error_percent_7_6_2s**2
        sqrt_added_sq_uncer_7_6 = (math.sqrt(error_percent_sq_7_6+(Add_and_square_root_constants_207_206_**2)))/100
        ratio_minus_times_sqrt_added_sq_uncer_7_6 = (d-(d*sqrt_added_sq_uncer_7_6))

        error_percent_6_8 = (b/a)*100
        error_percent_6_8_2s = error_percent_6_8*2
        error_percent_sq_6_8 = (error_percent_6_8_2s**2)
        sqrt_added_sq_uncer_6_8 = (math.sqrt(error_percent_sq_6_8+(Add_and_square_root_constants_206_238_**2)))/100
        ratio_minus_times_sqrt_added_sq_uncer_6_8 = (a-(a*sqrt_added_sq_uncer_6_8))
    
        sy_age_cal.append([ratio_minus_times_sqrt_added_sq_uncer_6_8,b,c,ratio_minus_times_sqrt_added_sq_uncer_7_6,e,f,g])
        mean_age.append([a,b,c,d,e,f,g])
        
        age_calc_low,eight_six_age_low,seven_six_age_low = age_calculation(sy_age_cal, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type, best_age_cut_off)
        age_calc_mean,eight_six_age_mean,seven_six_age_mean = age_calculation(MDAs_ratios, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type, best_age_cut_off)      
    
  
    for i in range(N):
        
        one_s_abs_total_7_6 = (seven_six_age_mean[i] - seven_six_age_low)/2
        one_s_abs_total_8_6 = (eight_six_age_mean[i] - eight_six_age_low)/2
        
        one_s_abs_total_7_6_ = np.squeeze(one_s_abs_total_7_6)
            
        if MDAs_ages_array[i][0] < best_age_cut_off:
            MDAs_ages[i][1] = one_s_abs_total_8_6[i]
        else: 
            MDAs_ages[i][1] = one_s_abs_total_7_6_[i] 
    
    return MDAs_ages

#MDA Calulators

#Code obtained from detritalPy_v1.3: @authors: glennrsharman, jonathanpsharman, zoltansylvester
#Where code has been altered from the original a note is made 

def YPP(ages, errors, min_cluster_size=2, thres=0.01, minDist=1, xdif=0.1):

    import peakutils

    # Check to see if ages is a list of arrays or just a single list of ages
    if not hasattr(ages[0], '__len__'):
        ages = [ages]
        errors = [errors]

    # Calculate the PDP - note that a small xdif may be desired for increased precision
    PDP_age, PDP = PDPcalcAges(ages, errors, xdif=xdif)
  

    YPP = []
    for i in range(len(ages)):

        # Calculate peak indexes
        indexes = list(peakutils.indexes(PDP[i], thres=thres, min_dist=minDist))
        # Peak ages
        peakAges = PDP_age[indexes]
        # Number of grains per peak
        peakAgeGrain = peakAgesGrains([peakAges], [ages[i]], [errors[i]])[0]
        # Zip peak ages and grains per peak
        peakAgesGrains_ = list(zip(peakAges, peakAgeGrain))
        # Filter out peaks with less than min_cluster_size grains
        peakAgesGrainsFiltered = list(filter(lambda x: x[1] >= min_cluster_size, peakAgesGrains_))

        # Check if a YPP was found, and if not return NaN
        if len(peakAgesGrainsFiltered) > 0:
            YPP.append(np.round(np.min([x[0] for x in peakAgesGrainsFiltered]),1))
        else:
            YPP.append(np.nan)

    return YPP

def YSG(ages, errors, sample_list,  eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type, best_age_cut_off):
    
    YSG_MDAs_ratios = []
    YSG_wo_systematic = []
    YSG_systematic_Calculation = []
    YSG = []
    
    youngest = []
    
    if Data_Type == "238U/206Pb_&_207Pb/206Pb": 
        for i in range(len(ages)):  
            data_err1s = list(zip(ages[i], errors[i],1/eight_six_ratios[i], eight_six_error[i],seven_six_ratios[i], seven_six_error[i]))
            data_err1s.sort(key=lambda d: d[0] + d[1]) # Sort based on age + 1s error
   
            youngest = data_err1s[0]
            YSG_MDAs_ratios.append([youngest[2], youngest[3], youngest[0], youngest[4], youngest[5], youngest[1], youngest[1]])
            
            YSG_age_calc, MDA_eight_six_age, MDA_seven_six_age = age_calculation(YSG_MDAs_ratios, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type,best_age_cut_off)
            
            YSG_wo_systematic.append([YSG_age_calc[0],YSG_age_calc[1],YSG_age_calc[2],YSG_age_calc[3]]) # Reporting 1-sigma error  
       
        YSG_systematic_Calculation = systematic_uncertainty_addition(YSG_wo_systematic, YSG_MDAs_ratios, sample_list, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type, best_age_cut_off)   

        for i in range(len(ages)):
            
            if YSG_systematic_Calculation[0] == 0.0:
                YSG.append([np.nan,np.nan,np.nan,np.nan])
            else:
                YSG.append([YSG_systematic_Calculation [i][0], YSG_systematic_Calculation [i][1]])
    
        
    if Data_Type == "Ages":      
        for i in range(len(ages)):
            data_err1s = list(zip(ages[i], errors[i]))
            data_err1s.sort(key=lambda d: d[0] + d[1]) # Sort based on age + 1s error
            YSG.append([data_err1s[0][0],data_err1s[0][1]]) # Reporting 1-sigma error  
    
    return YSG


def YSG_for_YDZ(ages, errors):

    # Check to see if ages is a list of arrays or just a single list of ages
    if not hasattr(ages[0], '__len__'):
        ages = [ages]
        errors = [errors]

    YSG_YDZ = []
    
    for i in range(len(ages)):
        data_err1s = list(zip(ages[i], errors[i]))
        data_err1s.sort(key=lambda d: d[0] + d[1]) # Sort based on age + 1s error
        YSG_YDZ.append([data_err1s[0][0],data_err1s[0][1]]) # Reporting 1-sigma error    
    
    return YSG_YDZ

def YDZ(ages, errors, iterations=10000, chartOutput = False, bins=25):
    from scipy import stats


    # Check to see if ages is a list of arrays or just a single list of ages
    if not hasattr(ages[0], '__len__'):
        ages = [ages]
        errors = [errors]

    YDZ = []

    for i in range(len(ages)):

        data_err1s = list(zip(ages[i], errors[i]))
        
        # Identify the youngest analysis
        YSG_age, YSG_err1s = YSG_for_YDZ(ages[i], errors[i])[0]

        ageCutoff = YSG_age + YSG_err1s*5 # 5 for 5-sigma

        # Identify all analyses within 5 sigma of the youngest analysis
        data_err1s.sort(key=lambda d: d[0]) # Sort based on age
        filtered = list(filter(lambda x: x[0] < ageCutoff, data_err1s)) # Filter out ages too old

        minAges = []
        mode = []
        
        for i in range(iterations):
            newAge_Ma = []
            for analysis in filtered:
                newAge_Ma.append(np.random.normal(loc = analysis[0], scale=analysis[1]))
            minAges.append(min(newAge_Ma))
    
        # Find the mode of the minimum ages
        binIndex, binAge = np.histogram(minAges, bins=bins)
        binMaxIndex = np.argmax(binIndex)
        binMaxAge = binAge[binMaxIndex]
        mode = binMaxAge + (binAge[binMaxIndex+1] - binMaxAge)/2

        YDZ.append([mode, np.percentile(minAges, 97.5)-mode, mode-np.percentile(minAges, 2.5)])


    return YDZ, minAges, mode


def YC2s(ages, errors, sample_list, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, U238_decay_constant, U235_decay_constant, U238_U235, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, Data_Type, best_age_cut_off, min_cluster_size=3):
    
    if not hasattr(ages[0], '__len__'):
        ages = [ages]
        errors = [errors]
    
    YC2s_cluster_arrays = []
    YC2s_MDAs_ratios = []
    YC2s = []
    YC2s_wo_systematic = []
            
    if Data_Type == "238U/206Pb_&_207Pb/206Pb": 
        for i in range(len(ages)):  
            data_err2s = list(zip(ages[i], errors[i]*2,1/eight_six_ratios[i], eight_six_error[i]*2,seven_six_ratios[i], seven_six_error[i]*2))
            data_err2s_ageSort = list(zip(ages[i], errors[i]*2,eight_six_ratios[i], eight_six_error[i]*2,seven_six_ratios[i], seven_six_error[i]*2))
            data_err2s_ageSort.sort(key=lambda d: d[0]) # Sort based on age
            data_err2s.sort(key=lambda d: d[0] + d[1]) # Sort based on age + 2s error


            YC2s_cluster, max_cluster,YC2s_age_cluster = find_youngest_cluster(data_err2s, sample_list, min_cluster_size)
            YC2s_cluster_arrays.append(YC2s_age_cluster)

            YC2s_WM_6_8 = weightedMean(np.array([d[2] for d in YC2s_cluster]), np.array([d[3] for d in YC2s_cluster])/2)

            YC2s_WM_7_6 = weightedMean(np.array([d[4] for d in YC2s_cluster]), np.array([d[5] for d in YC2s_cluster])/2)

            if YC2s_WM_6_8[0] == 0.0:
                YC2s_MDAs_ratios.append([np.nan,np.nan,np.nan,np.nan])
            if YC2s_WM_7_6[0] == 0.0:
                YC2s_MDAs_ratios.append([np.nan,np.nan,np.nan,np.nan])
            else:
                YC2s_MDAs_ratios.append([YC2s_WM_6_8[0], YC2s_WM_6_8[1]/2, YC2s_WM_6_8[2], YC2s_WM_7_6[0], YC2s_WM_7_6[1]/2, YC2s_WM_7_6[2], len(YC2s_cluster)])

            YC2s_age_calc, MDA_eight_six_age, MDA_seven_six_age = age_calculation(YC2s_MDAs_ratios, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type,best_age_cut_off)

            YC2s_wo_systematic.append([YC2s_age_calc[0],YC2s_age_calc[1],YC2s_age_calc[2],YC2s_age_calc[3]])
        
        YC2s = systematic_uncertainty_addition(YC2s_wo_systematic, YC2s_MDAs_ratios, sample_list, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type, best_age_cut_off)   
    
    if Data_Type == "Ages":
        for i in range(len(ages)):  
            data_err2s = list(zip(ages[i], errors[i]*2,ages[i], errors[i]*2,ages[i], errors[i]*2))
            data_err2s_ageSort = list(zip(ages[i], errors[i]*2,ages[i], errors[i]*2,ages[i], errors[i]*2))
            data_err2s_ageSort.sort(key=lambda d: d[0]) # Sort based on age
            data_err2s.sort(key=lambda d: d[0] + d[1]) # Sort based on age + 2s error

            YC2s_cluster, max_cluster,YC2s_age_cluster = find_youngest_cluster(data_err2s, sample_list, min_cluster_size)
            YC2s_WM = weightedMean(np.array([d[0] for d in YC2s_cluster]), np.array([d[1] for d in YC2s_cluster])/2)

            if YC2s_WM[0] == 0.0:
                YC2s.append([np.nan,np.nan,np.nan,np.nan])
            else:
                YC2s.append([YC2s_WM[0], YC2s_WM[1]/2, YC2s_WM[2], len(YC2s_cluster)])
                YC2s_cluster_arrays.append(YC2s_age_cluster)
    
    return YC2s, YC2s_cluster_arrays



def YC1s(ages, errors, sample_list, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, U238_decay_constant, U235_decay_constant, U238_U235, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, Data_Type, best_age_cut_off, min_cluster_size=2):
    
    if not hasattr(ages[0], '__len__'):
        ages = [ages]
        errors = [errors]
    
    YC1s_cluster_arrays = []
    YC1s_MDAs_ratios = []
    YC1s = []
    YC1s_wo_systematic = []
   
            
    if Data_Type == "238U/206Pb_&_207Pb/206Pb": 
        for i in range(len(ages)):
            
            data_err1s = list(zip(ages[i], errors[i],1/eight_six_ratios[i], eight_six_error[i],seven_six_ratios[i], seven_six_error[i]))
            data_err1s_ageSort = list(zip(ages[i], errors[i],eight_six_ratios[i], eight_six_error[i],seven_six_ratios[i], seven_six_error[i]))
            data_err1s_ageSort.sort(key=lambda d: d[0]) # Sort based on age
            data_err1s.sort(key=lambda d: d[0] + d[1]) # Sort based on age + 1s error
           
            YC1s_cluster, max_cluster,YC1s_age_cluster  = find_youngest_cluster(data_err1s, sample_list, min_cluster_size)
            YC1s_cluster_arrays.append(YC1s_age_cluster)
            
            YC1s_WM_6_8 = weightedMean(np.array([d[2] for d in YC1s_cluster]), np.array([d[3] for d in YC1s_cluster]))

            YC1s_WM_7_6 = weightedMean(np.array([d[4] for d in YC1s_cluster]), np.array([d[5] for d in YC1s_cluster]))

            if YC1s_WM_6_8[0] == 0.0:
                YC1s_MDAs_ratios.append([np.nan,np.nan,np.nan,np.nan])
            if YC1s_WM_7_6[0] == 0.0:
                YC1s_MDAs_ratios.append([np.nan,np.nan,np.nan,np.nan])
            else:
                YC1s_MDAs_ratios.append([YC1s_WM_6_8[0], YC1s_WM_6_8[1]/2, YC1s_WM_6_8[2], YC1s_WM_7_6[0], YC1s_WM_7_6[1]/2, YC1s_WM_7_6[2], len(YC1s_cluster)])


            YC1s_age_calc, MDA_eight_six_age, MDA_seven_six_age = age_calculation(YC1s_MDAs_ratios, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type,best_age_cut_off)

            YC1s_wo_systematic.append([YC1s_age_calc[0],YC1s_age_calc[1],YC1s_age_calc[2],YC1s_age_calc[3]])
           
        YC1s = systematic_uncertainty_addition(YC1s_wo_systematic, YC1s_MDAs_ratios, sample_list, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type, best_age_cut_off)   
        
    if Data_Type == "Ages":
         for i in range(len(ages)):
            
            data_err1s = list(zip(ages[i], errors[i],ages[i], errors[i],ages[i], errors[i]))
            data_err1s_ageSort = list(zip(ages[i], errors[i],ages[i], errors[i],ages[i], errors[i]))
            data_err1s_ageSort.sort(key=lambda d: d[0]) # Sort based on age
            data_err1s.sort(key=lambda d: d[0] + d[1]) # Sort based on age + 1s error
            
            YC1s_cluster, max_cluster,YC1s_age_cluster = find_youngest_cluster(data_err1s, sample_list, min_cluster_size)
            YC1s_WM = weightedMean(np.array([d[0] for d in YC1s_cluster]), np.array([d[1] for d in YC1s_cluster]))
            
            if YC1s_WM[0] == 0.0:
                YC1s.append([np.nan,np.nan,np.nan,np.nan])
            else:
                YC1s.append([YC1s_WM[0], YC1s_WM[1]/2, YC1s_WM[2], len(YC1s_cluster)])
                YC1s_cluster_arrays.append(YC1s_age_cluster)
    

    return YC1s, YC1s_cluster_arrays




def Y3Zo(ages, errors, sample_list, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, U238_decay_constant, U235_decay_constant, U238_U235, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, Data_Type, best_age_cut_off):
    
    if not hasattr(ages[0], '__len__'):
        ages = [ages]
        errors = [errors]
    
    Y3Zo_cluster_arrays_before_sort = []
    Y3Zo_cluster_arrays = []
    Y3Zo_MDAs_ratios = []
    Y3Zo = []
    Y3Zo_3cluster_sort = []
    Y3Zo_wo_systematic = []

            
    if Data_Type == "238U/206Pb_&_207Pb/206Pb": 
        for i in range(len(ages)):
            
            data_err2s = list(zip(ages[i], errors[i]*2,1/eight_six_ratios[i], eight_six_error[i]*2,seven_six_ratios[i], seven_six_error[i]*2))
            data_err2s_ageSort = list(zip(ages[i], errors[i]*2,1/eight_six_ratios[i], eight_six_error[i]*2,seven_six_ratios[i], seven_six_error[i]*2))
            data_err2s_ageSort.sort(key=lambda d: d[0]) # Sort based on age
            data_err2s.sort(key=lambda d: d[0] + d[1]) # Sort based on age + 2s error
           
            Y3Zo_cluster, Y3Zo_imax,Y3Zo_age_cluster = find_youngest_cluster(data_err2s, sample_list, 3)
            
            Y3Zo_3cluster_sort.append(Y3Zo_cluster)
            Y3Zo_3cluster_sorti = Y3Zo_3cluster_sort[i]
            Y3Zo_3cluster_sorti.sort(key=lambda d: d[0]) # Sort based on age - 2s uncertainty
            Y3Zo_3cluster = Y3Zo_3cluster_sorti[:3] #take lowest 3 of cluster
            
            Y3Zo_cluster_arrays_before_sort.append(Y3Zo_age_cluster)
            Y3Zo_cluster_arrays_sorti =  Y3Zo_cluster_arrays_before_sort[i]
            Y3Zo_cluster_arrays_sorti.sort(key=lambda d: d[0]) # Sort based on age
            Y3Zo_cluster_arrays_low_3 = Y3Zo_cluster_arrays_sorti[:3] #take lowest 3 of cluster
            Y3Zo_cluster_arrays.append(Y3Zo_cluster_arrays_low_3)

            Y3Zo_WM_6_8 = weightedMean(np.array([d[2] for d in Y3Zo_3cluster]), np.array([d[3] for d in Y3Zo_3cluster])/2)

            Y3Zo_WM_7_6 = weightedMean(np.array([d[4] for d in Y3Zo_3cluster]), np.array([d[5] for d in Y3Zo_3cluster])/2)

            if Y3Zo_WM_6_8[0] == 0.0:
                Y3Zo_MDAs_ratios.append([np.nan,np.nan,np.nan,np.nan])
            if Y3Zo_WM_7_6[0] == 0.0:
                Y3Zo_MDAs_ratios.append([np.nan,np.nan,np.nan,np.nan])
            else:
                Y3Zo_MDAs_ratios.append([Y3Zo_WM_6_8[0], Y3Zo_WM_6_8[1]/2, Y3Zo_WM_6_8[2], Y3Zo_WM_7_6[0], Y3Zo_WM_7_6[1]/2, Y3Zo_WM_7_6[2], len(Y3Zo_3cluster)])


            Y3Zo_age_calc, MDA_eight_six_age, MDA_seven_six_age = age_calculation(Y3Zo_MDAs_ratios, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type,best_age_cut_off)

            Y3Zo_wo_systematic.append([Y3Zo_age_calc[0],Y3Zo_age_calc[1],Y3Zo_age_calc[2],Y3Zo_age_calc[3]])

        
        Y3Zo = systematic_uncertainty_addition(Y3Zo_wo_systematic, Y3Zo_MDAs_ratios, sample_list, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type, best_age_cut_off)
                                               
            
    if Data_Type == "Ages":
        for i in range(len(ages)):
            
            data_err2s = list(zip(ages[i], errors[i]*2,ages[i], errors[i]*2,ages[i], errors[i]*2))
            data_err2s_ageSort = list(zip(ages[i], errors[i]*2,ages[i], errors[i]*2,ages[i], errors[i]*2))
            data_err2s_ageSort.sort(key=lambda d: d[0]) # Sort based on age
            data_err2s.sort(key=lambda d: d[0] + d[1]) # Sort based on age + 2s error
            
            Y3Zo_cluster, Y3Zo_imax,Y3Zo_age_cluster = find_youngest_cluster(data_err2s, sample_list, 3)
            
            Y3Zo_3cluster_sort.append(Y3Zo_cluster)
            Y3Zo_3cluster_sorti = Y3Zo_3cluster_sort[i]
            Y3Zo_3cluster_sorti.sort(key=lambda d: d[0]) # Sort based on age 
            Y3Zo_3cluster = Y3Zo_3cluster_sorti[:3] #take lowest 3 of cluster
            
            Y3Zo_cluster_arrays_before_sort.append(Y3Zo_age_cluster)
            Y3Zo_cluster_arrays_sorti =  Y3Zo_cluster_arrays_before_sort[i]
            Y3Zo_cluster_arrays_sorti.sort(key=lambda d: d[0]) # Sort based on age
            Y3Zo_cluster_arrays_low_3 = Y3Zo_cluster_arrays_sorti[:3] #take lowest 3 of cluster
            
            Y3Zo_WM = weightedMean(np.array([d[0] for d in Y3Zo_3cluster]), np.array([d[1] for d in Y3Zo_3cluster])/2)
            
            if Y3Zo_WM[0] == 0.0:
                Y3Zo.append([np.nan,np.nan,np.nan,np.nan])
            else:
                Y3Zo.append([Y3Zo_WM[0], Y3Zo_WM[1]/2, Y3Zo_WM[2], len(Y3Zo_3cluster)])
                Y3Zo_cluster_arrays.append(Y3Zo_cluster_arrays_low_3)
   
    return Y3Zo, Y3Zo_cluster_arrays

def Y3Za(ages, errors, sample_list, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, U238_decay_constant, U235_decay_constant, U238_U235, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, Data_Type, best_age_cut_off):
    
    if not hasattr(ages[0], '__len__'):
        ages = [ages]
        errors = [errors]
    
    Y3Za_MDAs_ratios = []
    Y3Za_cluster_arrays = []
    Y3Za = []
    Y3Za_wo_systematic = []
    
 
    if Data_Type == "238U/206Pb_&_207Pb/206Pb":
        for i in range(len(ages)):
                                               
            data_err1s = list(zip(ages[i], errors[i],1/eight_six_ratios[i], eight_six_error[i],seven_six_ratios[i], seven_six_error[i]))
            data_err1s_ageSort = list(zip(ages[i], errors[i],1/eight_six_ratios[i], eight_six_error[i],seven_six_ratios[i], seven_six_error[i]))
            data_err1s_ageSort.sort(key=lambda d: d[0]) # Sort based on age
            
           
            Y3Za_WM_6_8,Y3Za_6_8_WMerr2s, Y3Za_6_8_WM_MSWD = weightedMean([x[2] for x in data_err1s_ageSort[:3]], [x[3] for x in data_err1s_ageSort[:3]])

            Y3Za_WM_7_6,Y3Za_7_6_WMerr2s, Y3Za_7_6_WM_MSWD = weightedMean([x[4] for x in data_err1s_ageSort[:3]], [x[5] for x in data_err1s_ageSort[:3]])
            
            if len(ages[i]) < 3: # Return nulls if the samples has less than 3 analyses
                Y3Za_MDAs_ratios.append([np.nan,np.nan,np.nan])
            else:
                                               
                                               
                Y3Za_MDAs_ratios.append([Y3Za_WM_6_8, Y3Za_6_8_WMerr2s/2, Y3Za_6_8_WM_MSWD, Y3Za_WM_7_6, Y3Za_7_6_WMerr2s/2, Y3Za_7_6_WM_MSWD, len(data_err1s_ageSort[:3])])
                                               
                Y3Za_cluster_arrays.append(data_err1s_ageSort[:3])
                                               

            Y3Za_age_calc, MDA_eight_six_age, MDA_seven_six_age = age_calculation(Y3Za_MDAs_ratios, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type,best_age_cut_off)

            Y3Za_wo_systematic.append([Y3Za_age_calc[0],Y3Za_age_calc[1],Y3Za_age_calc[2],Y3Za_age_calc[3]])
        
        Y3Za = systematic_uncertainty_addition(Y3Za_wo_systematic, Y3Za_MDAs_ratios, sample_list, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type, best_age_cut_off)   
    
        
    if Data_Type == "Ages":
        for i in range(len(ages)):
            
            data_err1s = list(zip(ages[i], errors[i],ages[i], errors[i],ages[i], errors[i]))
            data_err1s_ageSort = list(zip(ages[i], errors[i],ages[i], errors[i],ages[i], errors[i]))
            data_err1s_ageSort.sort(key=lambda d: d[0]) # Sort based on age
            
            
            Y3Za_WM, Y3Za_WMerr2s, Y3Za_WM_MSWD = weightedMean([x[0] for x in data_err1s_ageSort[:3]], [x[1] for x in data_err1s_ageSort[:3]])
            
            
            if len(ages[i]) < 3: # Return nulls if the samples has less than 3 analyses
                Y3Za.append([np.nan,np.nan,np.nan])
            else:
                Y3Za.append([Y3Za_WM, Y3Za_WMerr2s/2, Y3Za_WM_MSWD, len(Y3Za_cluster_arrays)])
                Y3Za_cluster_arrays.append(data_err1s_ageSort[:3])
               
    
    return Y3Za, Y3Za_cluster_arrays


def tau(ages, errors, sample_list, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, U238_decay_constant, U235_decay_constant, U238_U235, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, Data_Type, best_age_cut_off, min_cluster_size=3, thres=0.01, minDist=1, xdif=1, x1=0, x2=4000):


    import peakutils

    # Check to see if ages is a list of arrays or just a single list of ages
    if not hasattr(ages[0], '__len__'):
        ages = [ages]
        errors = [errors]

    # Calculate the PDP - note that a small xdif may be desired for increased precision
    Tau_PDP_age, Tau_PDP = PDPcalcAges(ages, errors, xdif)

    Tau_Ratios = []
    Tau_MDA = []
    Tau_Grains = []
    Tau_wo_systematic = []
    
    for i in range(len(ages)):  

        # Calculate peak indexes
        peakIndexes = list(peakutils.indexes(Tau_PDP[i], thres=thres, min_dist=minDist))
        # Peak ages
        peakAges = Tau_PDP_age[peakIndexes]
        # Number of grains per peak
        peakAgeGrain = peakAgesGrains([peakAges], [ages[i]], [errors[i]])[0]

        # Calculate trough indexes
        troughIndexes = list(peakutils.indexes(Tau_PDP[i]*-1, thres=thres, min_dist=minDist))
        # Trough ages
        troughAges = [0] + list(Tau_PDP_age[troughIndexes]) + [4500] # Append a 0 because there is no trough on the young size of the youngest peak and no trough on the old side of the oldest peak

        # Zip peak ages and grains per peak
        peakAgesGrains_ = list(zip(peakAges, peakAgeGrain))
        # Filter out peaks with less than min_cluster_size grains (default is 3, following Barbeau et al., 2009: EPSL)
        peakAgesGrainsFiltered = list(filter(lambda x: x[1] >= min_cluster_size, peakAgesGrains_))

        # Stop the loop if no peaks are present with the min_cluster_size
        if peakAgesGrainsFiltered == []:
            Tau_Ratios.append([np.nan, np.nan, np.nan, np.nan])
            Tau_MDA.append([np.nan, np.nan, np.nan, np.nan])
            continue

        # Select the nearest trough that is younger than the youngest peak with at least min_cluster_size analyses
        troughYoung = np.max(list(filter(lambda x: x < peakAgesGrainsFiltered[0][0], troughAges)))

        # Select the nearest trough that is older than the youngest peak with at least min_cluster_size analyses
        troughOld = np.min(list(filter(lambda x: x > peakAgesGrainsFiltered[0][0], troughAges)))

        # Select ages and errors that fall between troughYoung and troughOld
        
            
        if Data_Type == "238U/206Pb_&_207Pb/206Pb": 
        
                ages_errors1s = list(zip(ages[i], errors[i],1/eight_six_ratios[i], eight_six_error[i],seven_six_ratios[i], seven_six_error[i]))
                ages_errors1s_filtered = list(filter(lambda x: x[0] < troughOld and x[0] > troughYoung, ages_errors1s))

                tauMethod_WM_6_8, tauMethod_WM_err2s_6_8, tauMethod_WM_MSWD_6_8 = weightedMean(np.array([d[2] for d in ages_errors1s_filtered]), np.array([d[3] for d in ages_errors1s_filtered]))
                tauMethod_WM_7_6, tauMethod_WM_err2s_7_6, tauMethod_WM_MSWD_7_6 = weightedMean(np.array([d[4] for d in ages_errors1s_filtered]), np.array([d[5] for d in ages_errors1s_filtered]))

                Tau_Ratios.append([tauMethod_WM_6_8, tauMethod_WM_err2s_6_8/2, tauMethod_WM_MSWD_6_8, tauMethod_WM_7_6, tauMethod_WM_err2s_7_6, tauMethod_WM_MSWD_7_6, len(ages_errors1s_filtered)])

                Tau_age_calc, MDA_eight_six_age, MDA_seven_six_age = age_calculation(Tau_Ratios, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type,best_age_cut_off)

                Tau_wo_systematic.append([Tau_age_calc[0],Tau_age_calc[1],Tau_age_calc[2],Tau_age_calc[3]])
                Tau_Grains.append([ages_errors1s_filtered])
       
        if Data_Type == "Ages":
        
                ages_errors1s = list(zip(ages[i], errors[i],ages[i], errors[i],ages[i], errors[i]))
                ages_errors1s_filtered = list(filter(lambda x: x[0] < troughOld and x[0] > troughYoung, ages_errors1s))

                tauMethod_WM, tauMethod_WM_err2s, tauMethod_WM_MSWD = weightedMean(np.array([d[0] for d in ages_errors1s_filtered]), np.array([d[1] for d in ages_errors1s_filtered]))
                Tau_MDA.append([tauMethod_WM, tauMethod_WM_err2s/2, tauMethod_WM_MSWD, len(ages_errors1s_filtered)])
                Tau_Grains.append([ages_errors1s_filtered])

    if Data_Type == "238U/206Pb_&_207Pb/206Pb": 
        Tau_MDA = systematic_uncertainty_addition(Tau_wo_systematic, Tau_Ratios, sample_list, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type, best_age_cut_off)
    
    return Tau_MDA, Tau_Grains, Tau_PDP_age, Tau_PDP,ages_errors1s_filtered

def YSP(ages, errors, sample_list, eight_six_ratios, eight_six_error, seven_six_ratios, seven_six_error, U238_decay_constant, U235_decay_constant, U238_U235, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, Data_Type, best_age_cut_off, min_cluster_size=2, MSWD_threshold=1):


    # Check to see if ages is a list of arrays or just a single list of ages
    if not hasattr(ages[0], '__len__'):
        ages = [ages]
        errors = [errors]   

    YSP = []
    YSP_Ratios = []
    YSP_cluster = []
    YSP_wo_systematic = []
    
        
    if Data_Type == "238U/206Pb_&_207Pb/206Pb": 
        
        for i in range(len(ages)): 
            data_err1s_ageSort = list(zip(ages[i], errors[i],1/eight_six_ratios[i], eight_six_error[i],seven_six_ratios[i], seven_six_error[i]))
            data_err1s_ageSort.sort(key=lambda d: d[0]) # Sort based on age
            
            for j in range(len(data_err1s_ageSort)): # One loop for each analysis. Loop repeated if MSWD of the first pair is not <1.

                # Creat list of MSWD
                MSWD = []
                for k in range(len(data_err1s_ageSort)):
                    MSWD.append(weightedMean(np.array([d[0] for d in data_err1s_ageSort[:(k+2)]]), np.array([d[1] for d in data_err1s_ageSort[:(k+2)]]))[2])
            
                # Add MSWD to the ages & errors tuple   
                data_err1s_MSWD = []

                for k in range(len(data_err1s_ageSort)):
                   
                    if k == 0: # Assign the first age an MSWD of 0 (so it is always included in the MSWD)
                        data_err1s_MSWD.append((data_err1s_ageSort[k][0], data_err1s_ageSort[k][1], 0))
                    else: # Assign analyses the MSWD of the previos analysis, such that the filtering returns the correct analyses
                        data_err1s_MSWD.append((data_err1s_ageSort[k][0], data_err1s_ageSort[k][1], MSWD[k-1]))
                   
                # Need to exit the algorithm if no YSP is found
                if j == len(ages[i])-1:
                    YSP_wo_systematic.append([float('nan'), float('nan'), float('nan'), float('nan')])
                    break

                # Find the index of the analysis with an MSWD closest to 1
                idx = (np.abs(np.array([d[2] for d in data_err1s_MSWD][1:])-MSWD_threshold)).argmin()+1 # Need to add 1 because we excluded the first one that had an assigned MSWD of 0

                # Filter analyses beyond the one which has a MSWD closest to MSWD_threshold
                agesFiltered = data_err1s_MSWD[0:idx+1]
                agesFiltered_addratios = []

                for k in range(len(agesFiltered)):
                    agesFiltered_addratios.append((agesFiltered[k][0],agesFiltered[k][1],data_err1s_ageSort[k][2], data_err1s_ageSort[k][3],data_err1s_ageSort[k][4], data_err1s_ageSort[k][5]))
                
                YSP_WM_6_8, YSP_WM_err2s_6_8, YSP_WM_MSWD_6_8 = weightedMean(np.array([d[2] for d in agesFiltered_addratios]), np.array([d[3] for d in agesFiltered_addratios]))
                YSP_WM_7_6, YSP_WM_err2s_7_6, YSP_WM_MSWD_7_6 = weightedMean(np.array([d[4] for d in agesFiltered_addratios]), np.array([d[5] for d in agesFiltered_addratios]))
                
                YSP_Ratios.append([YSP_WM_6_8, YSP_WM_err2s_6_8/2, YSP_WM_MSWD_6_8,YSP_WM_7_6, YSP_WM_err2s_7_6/2, YSP_WM_MSWD_7_6,len(agesFiltered)])

                if (agesFiltered[1][2] < 1 and len(agesFiltered) >= min_cluster_size): # The first one is excluded because the MSWD is made to be 0. The second youngest analysis must have a MSWD < 1 to proceed. The minimum cluster size must also be met or exceeded.
                    
                    YSP_age_calc, MDA_eight_six_age, MDA_seven_six_age = age_calculation(YSP_Ratios, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type,best_age_cut_off)
                    YSP_wo_systematic.append([YSP_age_calc[0],YSP_age_calc[1],YSP_age_calc[2],YSP_age_calc[3]])
                    YSP_cluster.append(agesFiltered)
                    break
                else:
                    del data_err1s_ageSort[0] # Delete the first analysis, which was no use at all, and try again      
        
        
            
        YSP = systematic_uncertainty_addition(YSP_wo_systematic, YSP_Ratios, sample_list, excess_variance_206_238, excess_variance_207_206, Sy_calibration_uncertainty_206_238, Sy_calibration_uncertainty_207_206, decay_constant_uncertainty_U238, decay_constant_uncertainty_U235, U238_decay_constant, U235_decay_constant, U238_U235, Data_Type, best_age_cut_off)   
    
        
        
    if Data_Type == "Ages":
        for i in range(len(ages)): 
            data_err1s_ageSort = list(zip(ages[i], errors[i],ages[i], errors[i],ages[i], errors[i]))
            data_err1s_ageSort.sort(key=lambda d: d[0]) # Sort based on age
            
            for j in range(len(data_err1s_ageSort)): # One loop for each analysis. Loop repeated if MSWD of the first pair is not <1.

                # Creat list of MSWD
                MSWD = []
                for k in range(len(data_err1s_ageSort)):
                    MSWD.append(weightedMean(np.array([d[0] for d in data_err1s_ageSort[:(k+2)]]), np.array([d[1] for d in data_err1s_ageSort[:(k+2)]]))[2])
            
                # Add MSWD to the ages & errors tuple   
                data_err1s_MSWD = []

                for k in range(len(data_err1s_ageSort)):
                   
                    if k == 0: # Assign the first age an MSWD of 0 (so it is always included in the MSWD)
                        data_err1s_MSWD.append((data_err1s_ageSort[k][0], data_err1s_ageSort[k][1], 0))
                    else: # Assign analyses the MSWD of the previos analysis, such that the filtering returns the correct analyses
                        data_err1s_MSWD.append((data_err1s_ageSort[k][0], data_err1s_ageSort[k][1], MSWD[k-1]))
                   
                # Need to exit the algorithm if no YSP is found
                if j == len(ages[i])-1:
                    YSP_wo_systematic.append([float('nan'), float('nan'), float('nan'), float('nan')])
                    break

                # Find the index of the analysis with an MSWD closest to 1
                idx = (np.abs(np.array([d[2] for d in data_err1s_MSWD][1:])-MSWD_threshold)).argmin()+1 # Need to add 1 because we excluded the first one that had an assigned MSWD of 0

                # Filter analyses beyond the one which has a MSWD closest to MSWD_threshold
                agesFiltered = data_err1s_MSWD[0:idx+1]

                YSP_WM, YSP_WM_err2s, YSP_WM_MSWD = weightedMean(np.array([d[0] for d in agesFiltered]), np.array([d[1] for d in agesFiltered]))

                if (agesFiltered[1][2] < 1 and len(agesFiltered) >= min_cluster_size): # The first one is excluded because the MSWD is made to be 0. The second youngest analysis must have a MSWD < 1 to proceed. The minimum cluster size must also be met or exceeded.
                    YSP.append([YSP_WM, YSP_WM_err2s/2, YSP_WM_MSWD, len(agesFiltered)])
                    YSP_cluster.append(agesFiltered)
                    break
                else:
                    del data_err1s_ageSort[0] # Delete the first analysis, which was no use at all, and try again      
    
       
    return YSP, YSP_cluster

#MLA Code written by morganbrooks. Base of calculations is pulled from IsoplotR

def MLA(sample_list, dataToLoad_MLA):
    
    # Lets delete all files that are inside the temp folder
    # The solution is a mix of python, R and markdown to manage the files, plot and display of pictures here on jupyter.
    import glob, os, json, subprocess
    #
    files = glob.glob("assets/plots/IsoplotR/*.png")
    #
    for f in files:
        os.remove(f)
    # We convert the Python list to a json to be able to send it as an argument to R. Just make sure there are 
    # elements at this list at all times, otherwise the R script breaks.
    samples = json.dumps(sample_list)
    # we call the RScript using subprocess and send the path to the file containing the data and a string 
    # with a name for the file to be saved on the temporary folder.
    output = subprocess.check_output(["Rscript", 'R_Scripts/IsoPlotR.R', dataToLoad_MLA[0], samples])
    results = json.loads(output)
    # output2 = subprocess.check_output(["Rscript", 'R_Scripts/IsoPlotR2.R', dataToLoad[0], samples], universal_newlines=True)
    # then we convert the json returned to a dictionary by reading it as a json format
    MDA_Values = {k:results[k][0] for k in results.keys()}
    Error_Values = {k:results[k][1] for k in results.keys()}
    # Then we print the dictionary returned by R from the peakfit function
    # print("\n") # I just printed a line between the numbers, you can delete this line anytime
    # or we can print the value for a given sample
    #print(peak_values['UK027'])
    # ![title](temp/teste_plot_UK017.png)
    
    ds = [MDA_Values, Error_Values]
    MLA_MDA_1sError = {}
    for k in MDA_Values.keys():
        MLA_MDA_1sError[k] = tuple(MLA_MDA_1sError[k] for MLA_MDA_1sError in ds)
    MLA_MDA = []
    MLA_MDA = list(MLA_MDA_1sError.values())

    return MLA_MDA

