#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 10:01:58 2019

@author: gravwaves
"""




# =============================================
# IMPORT LIBRARIES
# =============================================
import numpy as np
import sys





# =============================================
# FUNCTION TO READ LOG FILE
# =============================================
def GetInjectionTimes(DataPath,FolderName,job,GPSini):
    
    # ---------------------------------------------
    # Folder and filename
    folder         = FolderName + '/output'
    logfilename    = 'log_' + str(GPSini) + '_1200_' + FolderName + '_job' + str(job) + '.txt'
    logfullpath    = DataPath + folder + '/' + logfilename
    
    # ---------------------------------------------
    # Import onset time
    TimeOnset    = np.loadtxt(logfullpath,usecols=(9))
    TimeOnset    = np.unique(TimeOnset)
    if len(TimeOnset)!=1:
        print('PILAS PERRITO: there are more than one time onset in the log file')
        print(logfullpath)
        sys.exit()
    TimeOnset = TimeOnset[0]
    
    # ---------------------------------------------
    # Import injection times
    TimeInjec    = np.loadtxt(logfullpath,usecols=(10))
    TimeInjecL1  = np.loadtxt(logfullpath,usecols=(16))
    TimeInjecH1  = np.loadtxt(logfullpath,usecols=(20))
    
    #  Tini    Tinj    TinjL1  TinjH1
    # [C{9}   C{10}   C{16}   C{20}]
    
    # ---------------------------------------------
    # Import name of the injected waveform
    WavefromName       = np.loadtxt(logfullpath,usecols=(11),dtype=str)
    
    # Template name
    # C{11}]
    
    # ---------------------------------------------
    # RETURN OUTPUT DATA
    return TimeOnset, TimeInjec, WavefromName, TimeInjecL1, TimeInjecH1





# =============================================
# FUNCTION TO READ LOG FILE
# =============================================
def GetGPSini(DataPath,FolderName,job):
    
    # ---------------------------------------------
    # Folder and filename
    fullpath       = DataPath + FolderName + '/' + 'JobsGPSini.csv'
    
    # ---------------------------------------------
    # Read data
    JobIniAll      = np.loadtxt(fullpath,usecols=(0),delimiter=',')

    GPSini         = int(JobIniAll[job-1])
    
    # ---------------------------------------------
    # RETURN OUTPUT DATA
    return GPSini







# =============================================
# FUNCTION TO READ LOG FILE
# =============================================
def GetJobsNUM(DataPath,FolderName):
    
    # ---------------------------------------------
    # Folder and filename
    fullpath       = DataPath + FolderName + '/' + 'JobsNUM.csv'
    
    # ---------------------------------------------
    # Read data
    JobsNUM      = np.loadtxt(fullpath,usecols=(0),delimiter=',')
    
    JOBS         = JobsNUM.astype(int)
    
    # ---------------------------------------------
    # RETURN OUTPUT DATA
    return JOBS