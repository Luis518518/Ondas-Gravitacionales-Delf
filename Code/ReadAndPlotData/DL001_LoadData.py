#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 20:13:55 2018

@author: gravwaves
"""





# *********************************************
# IMPORT LIBRARIES
# *********************************************
import CWB_ReadLogJobs, CWB_ReadStrain
import numpy as np
import sys
import pylab





# *********************************************
# INITIALIZE PARAMETERS
# *********************************************
#
# -------------------------------
# Parameters
#
FolderName        = 'O2_L1H1_RUN2_SIM_SCH'   # (O2_L1H1_RUN2_SIM_SCH,O2_L1H1_RUN3_SIM_SCH)
pc                = 'ligocluster'                    # ('mac','ligocluster')

# -----------------------------
# Data Path
#
if   pc == 'jacs':
    DataPath          = '/home/jacs/Documents/TRABAJOS_EXTRA/PracticasProfesionales/Trabajos/Inyecciones/'
elif pc == 'ligocluster':
    DataPath          = '/home/jacs/Documents/TRABAJOS_EXTRA/PracticasProfesionales/Trabajos/Inyecciones/'

# -----------------------------
# Sampling frequency
#
if   FolderName[8:11] == 'RUN' or FolderName[8:11] == 'SEG' or FolderName[8:14] == 'HYBRID':
    fs                = 2048  
                     
else:
    print('PILAS PERRITO: define sampling frequency for the selected project')
    sys.exit()     

# -----------------------------
# Lower frequency of the detector
#
flow              = 10                            

# -------------------------------
# Debugging parameters
#
doplot            = 0
doprint           = 1





# *********************************************
# DEFINE JOBS AND FACTORS
# *********************************************
#
# -------------------------------
# JOBS & FACTORS
#
# Define jobs for the selected FolderName 
if   FolderName == 'O2_L1H1_RUN2_SIM_SCH':
    JOBS   = np.array([2,3,4,5])
elif FolderName == 'O2_L1H1_RUN3_SIM_SCH':
    JOBS   = np.array([2,3,4,5,6,7,8,9,10,11,12,13,14,15])
else:
    print('PILAS PERRITO: Unknown FolderName')
    sys.exit()
    
# Define factors
if   FolderName[8:11] == 'RUN' or FolderName[8:11] == 'SEG' or FolderName[8:14] == 'HYBRID':
    FACTORS = np.array(['0.03','0.04','0.06','0.07','0.10','0.13','0.18','0.24','0.32','0.42','0.56','0.75','1.00','1.33','1.78','2.37','3.16','4.22','5.62','7.50','10.00','13.34','17.78','23.71','31.62','42.17','56.23','74.99','100.00','133.35','177.83','237.14','316.23'])
    segEdge = 10;    
else:
    sys.exit()

# For debugging: choose only one job and one factor
#JOBS    = np.array([2,5])
JOBS = np.array([2])
FACTORS = np.array(['316.23'])





# *********************************************
# NOTE
# *********************************************
# Para este script no hay necesidad de los bucles "for" que siguen a 
# continuacion, no obstante, si son importantes para las actividades siguientes





# *********************************************
# FOR EACH DATA JOB
# *********************************************
# 
for i_job in np.arange(0,len(JOBS)): 
    print('                                               ')
    print('***********************************************')
    print('Job:         ' + str(i_job+1) + ' of ' + str(JOBS.size) + '  -  ' + str(JOBS[i_job]))
    
    
    # -------------------------------
    # GET THE NUMBER OF THE JOB
    job          = JOBS[i_job]
    
    
    # -------------------------------
    # GET GPSINI
    GPSini = CWB_ReadLogJobs.GetGPSini(DataPath,FolderName,job)
    
    
    # -------------------------------
    # GET INJECTION TIMES FOR THE CURRENT JOB (ACROSS-ALL-TEMPLATES)
    #
    # Get injection times and the name of the injected waveform
    GPSiniEdge, TinjAll, WFnameAll, TinjL1All, TinjH1All = CWB_ReadLogJobs.GetInjectionTimes(DataPath,FolderName,job,GPSini)
    
    #Check segEdge
    if segEdge != GPSini-GPSiniEdge:
        print('PILAS PERRITO: problem with segEdge')
        sys.exit() 
    
    # -------------------------------
    # GET INJECTION TIMES RE-REFERENCED TO T=0 
    Tinj                = TinjAll    - GPSiniEdge
    TinjL1              = TinjL1All  - GPSiniEdge
    TinjH1              = TinjH1All  - GPSiniEdge
    GPSiniEdge          = 0 
    
    print('# of inj:    ' + str(Tinj.size) )

#    print(str(Tinj))
    print('Times where injections of L1 ocurred' + str(TinjL1[:5]))
    print('Times where injections of H1 ocurred' + str(TinjH1[:5]))
    
    
    # *********************************************
    # FOR EACH FACTOR
    # *********************************************
    #
    for i_fac in np.arange(0,FACTORS.size): 
        print('Factor:      ' + str(i_fac+1) + ' of ' + str(FACTORS.size) + '  -  ' + FACTORS[i_fac] )
      
        
        # -------------------------------
        # GET CURRENT FACTOR AND COMPUTE DISTANCE
        #
        # Get the current factor
        fac               = FACTORS[i_fac]
        
        # Get current distance
        Rinj              = 1./float(fac)
                
        print('Distance:    ' + str(i_fac+1) + ' of ' + str(FACTORS.size) + '  -  ' + str(Rinj) + 'Kpc')
        
        
        # -------------------------------
        # LOAD AND PLOT STRAIN DATA:
        strainH1raw, strainL1raw    = CWB_ReadStrain.ReadStrain(DataPath,FolderName,job,fac,GPSini,fs,'r',doplot)
        if doprint == 1:
            print('----')
            print('Raw data duration H1: ' + str(strainH1raw.duration) + ' seconds')
            print('Raw data duration L1: ' + str(strainL1raw.duration) + ' seconds')
            #sys.exit()
        
        # BREAK
        #sys.exit()
        
        
        # -------------------------------
        # PLOT STRAIN DATA AROUND ONE OF THE INJECTIONS:
        if doplot == 1:
            
            # Choose one of the injections
            iTemp    = 5 # Cuidado: este numero no puede ser mayor a Tinj.size
            
            # Imprimir nombre de la injected GW
            print('Injected GW:    ' + WFnameAll[iTemp] )
            
            # Selecccionar un intervalos de tiempo alrededor del tiempo Tinj
            t_inj    = Tinj[iTemp]
            li       = t_inj - 0.25
            lf       = t_inj + 0.25
            
            # Plot strain data
            pylab.figure(figsize=(12,4))
            pylab.plot(strainL1raw.sample_times,strainL1raw,linewidth=2.0 , label='L1')
            pylab.plot(strainH1raw.sample_times,strainH1raw,linewidth=2.0 , label='H1')
            pylab.legend()
            pylab.title('Strain around injection (RAW)',fontsize=18)
            pylab.xlabel('Time (s)',fontsize=18,color='black')
            pylab.ylabel('Strain',fontsize=18,color='black')
            pylab.grid(True)
            
            # Plot Tinj, TinjH1, TinjL1
#            for ti in Tinj:
#                pylab.axvline(x=ti, color='r', linestyle='--', linewidth=1)
            for ti in TinjL1:
                pylab.axvline(x=ti, color='g', linestyle=':', linewidth=1)           
            for ti in TinjH1:
                pylab.axvline(x=ti, color='b', linestyle=':', linewidth=1)
            
            # Ajustar xlim al intervalo de interes
            pylab.xlim(li,lf)        

            pylab.show()
            # Break system
#            sys.exit()
#print(strainH1raw.sample_times == strainL1raw.sample_times)

  
###########################################
#FORMAS DE ONDA DE SCHEIDEGGER
#sch1: R1E1CA_L : 0.09284648
#sch2: R3E1AC_L : 0.19687465
#sch3: R4E1FC_L : 0.09754108

##########################################
#DURACION DE CADA FORMA DE ONDA
tsch1 = 0.09284648
tsch2 = 0.19687465
tsch3 = 0.09754108

######### TIEMPOS
tiempo = strainH1raw.sample_times

######### STRAINS
STRAINL1 = strainL1raw
STRAINH1 = strainH1raw

######## TIEMPOS DE INYECCION DE OG
inyecL1 = TinjL1
inyecH1 = TinjH1

#rint(STRAINL1.shape)
#rint(tiempo.shape)        
        
Twin = 0.25
NumDatos = int(Twin*fs)

NumVentanas = int(2*len(tiempo)/NumDatos)

print(NumVentanas)

Labels = []
TwinH1 = []
TwinL1 = []
TwinTIME = []

PLOT = 0

print(len(inyecL1))

k = 50
print('Injected GW:    ' + WFnameAll[k] )
for k in range(0,len(inyecL1)): #len(inyecL1)): range(int(2*TinjL1[k]/Twin)-3,int(2*TinjL1[k]/Twin)-3)
#    print(WFnameAll[k])
    if k==0:
        for i in range(0,int((2*inyecL1[k])/Twin)+3): #range(int((2*inyecL1[k])/Twin)-3,int((2*inyecL1[k])/Twin)+5):  #tiempo/NumDatos):
            mitad = int(((i*NumDatos)+((i+1)*NumDatos))/2)            #    print(mitad)
            mediopaso = int(NumDatos/2)
            STRAINOL1 = STRAINL1[(i*mediopaso):((i+2)*mediopaso)]
            TwinL1.append(STRAINOL1)
            STRAINOH1 = STRAINH1[(i*mediopaso):((i+2)*mediopaso)]
            TwinH1.append(STRAINOH1)
            timo = tiempo[(i*mediopaso):((i+2)*mediopaso)]
            TwinTIME.append(timo)
            if WFnameAll[k] == 'sch1':
                tsch = tsch1
            if WFnameAll[k] == 'sch2':
                tsch = tsch2
            if WFnameAll[k] == 'sch3':
                tsch = tsch3
            DurIny = tsch/2
            if tiempo[i*mediopaso]>(inyecL1[k]-Twin) and tiempo[(i+2)*mediopaso]<(inyecL1[k]+Twin):
                pylab.axvline(x=inyecL1[k] , color='g', linestyle=':', linewidth=1)
            if tiempo[(i)*mediopaso]<(inyecL1[k]-DurIny) and tiempo[(i+2)*mediopaso]>(inyecL1[k]-DurIny):
                pylab.axvline(x=inyecL1[k]-DurIny , color='r', linestyle=':', linewidth=1)
#                Labels.append(1)# = 1
            if tiempo[(i)*mediopaso]<(inyecL1[k]+DurIny) and tiempo[(i+2)*mediopaso]>(inyecL1[k]+DurIny):
                pylab.axvline(x=inyecL1[k]+DurIny , color='b', linestyle=':', linewidth=1)
#                Labels.append(1)# = 1
            if tiempo[i*mediopaso]>(inyecH1[k]-Twin) and tiempo[(i+2)*mediopaso]<(inyecH1[k]+Twin):
                pylab.axvline(x=inyecH1[k] , color='g', linestyle='--', linewidth=1)
            if tiempo[(i)*mediopaso]<(inyecH1[k]-DurIny) and tiempo[(i+2)*mediopaso]>(inyecH1[k]-DurIny):
                pylab.axvline(x=inyecH1[k]-DurIny , color='r', linestyle='--', linewidth=1)     
            if tiempo[(i)*mediopaso]<(inyecH1[k]+DurIny) and tiempo[(i+2)*mediopaso]>(inyecH1[k]+DurIny):
                pylab.axvline(x=inyecH1[k]+DurIny , color='b', linestyle='--', linewidth=1)
            if tiempo[i*mediopaso]>(inyecL1[k]-Twin) and tiempo[(i+2)*mediopaso]<(inyecL1[k]+Twin) or tiempo[(i)*mediopaso]<(inyecL1[k]-DurIny) and tiempo[(i+2)*mediopaso]>(inyecL1[k]-DurIny) or tiempo[(i)*mediopaso]<(inyecL1[k]+DurIny) and tiempo[(i+2)*mediopaso]>(inyecL1[k]+DurIny):
                Labels.append(1)
            else:
                Labels.append(0)
            if PLOT==1:
                pylab.plot(timo,STRAINOL1, label=Labels[-1])
                pylab.plot(timo,STRAINOH1)
                pylab.legend(loc='upper right')
                pylab.show()
        
    if k>0 and k<(len(inyecL1)-1):
        for i in range(int((2*inyecL1[k-1])/Twin)+3,int((2*inyecL1[k])/Twin)+3):
            mitad = int(((i*NumDatos)+((i+1)*NumDatos))/2)            #    print(mitad)
            mediopaso = int(NumDatos/2)
            STRAINOL1 = STRAINL1[(i*mediopaso):((i+2)*mediopaso)]
            TwinL1.append(STRAINOL1)
            STRAINOH1 = STRAINH1[(i*mediopaso):((i+2)*mediopaso)]
            TwinH1.append(STRAINOH1)
            timo = tiempo[(i*mediopaso):((i+2)*mediopaso)]
            TwinTIME.append(timo)
            if WFnameAll[k] == 'sch1':
                tsch = tsch1
            if WFnameAll[k] == 'sch2':
                tsch = tsch2
            if WFnameAll[k] == 'sch3':
                tsch = tsch3
            DurIny = tsch/2
            if tiempo[i*mediopaso]>(inyecL1[k]-Twin) and tiempo[(i+2)*mediopaso]<(inyecL1[k]+Twin):
                pylab.axvline(x=inyecL1[k] , color='g', linestyle=':', linewidth=1)
            if tiempo[(i)*mediopaso]<(inyecL1[k]-DurIny) and tiempo[(i+2)*mediopaso]>(inyecL1[k]-DurIny):
                pylab.axvline(x=inyecL1[k]-DurIny , color='r', linestyle=':', linewidth=1)
#                Labels.append(1)# = 1
            if tiempo[(i)*mediopaso]<(inyecL1[k]+DurIny) and tiempo[(i+2)*mediopaso]>(inyecL1[k]+DurIny):
                pylab.axvline(x=inyecL1[k]+DurIny , color='b', linestyle=':', linewidth=1)
#                Labels.append(1)# = 1
            if tiempo[i*mediopaso]>(inyecH1[k]-Twin) and tiempo[(i+2)*mediopaso]<(inyecH1[k]+Twin):
                pylab.axvline(x=inyecH1[k] , color='g', linestyle='--', linewidth=1)
            if tiempo[(i)*mediopaso]<(inyecH1[k]-DurIny) and tiempo[(i+2)*mediopaso]>(inyecH1[k]-DurIny):
                pylab.axvline(x=inyecH1[k]-DurIny , color='r', linestyle='--', linewidth=1)     
            if tiempo[(i)*mediopaso]<(inyecH1[k]+DurIny) and tiempo[(i+2)*mediopaso]>(inyecH1[k]+DurIny):
                pylab.axvline(x=inyecH1[k]+DurIny , color='b', linestyle='--', linewidth=1)
            if tiempo[i*mediopaso]>(inyecL1[k]-Twin) and tiempo[(i+2)*mediopaso]<(inyecL1[k]+Twin) or tiempo[(i)*mediopaso]<(inyecL1[k]-DurIny) and tiempo[(i+2)*mediopaso]>(inyecL1[k]-DurIny) or tiempo[(i)*mediopaso]<(inyecL1[k]+DurIny) and tiempo[(i+2)*mediopaso]>(inyecL1[k]+DurIny):
                Labels.append(1)
            else:
                Labels.append(0)
            if PLOT==1:
                pylab.plot(timo,STRAINOL1, label = Labels[-1])
                pylab.plot(timo,STRAINOH1)
                pylab.legend(loc='upper right')
                pylab.show()
    if k==(len(inyecL1)-1):
#        print(k)
#        print(inyecL1[k])
#        print((NumVentanas)*mediopaso)
        for i in range(int((2*inyecL1[k-1])/Twin)+3,NumVentanas-2):
#            mitad = int(((i*NumDatos)+((i+1)*NumDatos))/2)            #    print(mitad)
            mediopaso = int(NumDatos/2)
            STRAINOL1 = STRAINL1[(i*mediopaso):((i+2)*mediopaso)]
            TwinL1.append(STRAINOL1)
            STRAINOH1 = STRAINH1[(i*mediopaso):((i+2)*mediopaso)]
            TwinH1.append(STRAINOH1)
            timo = tiempo[(i*mediopaso):((i+2)*mediopaso)]
            TwinTIME.append(timo)
#            print(tiempo[i*mediopaso])
            if WFnameAll[k] == 'sch1':
                tsch = tsch1
            if WFnameAll[k] == 'sch2':
                tsch = tsch2
            if WFnameAll[k] == 'sch3':
                tsch = tsch3
            DurIny = tsch/2
            if tiempo[i*mediopaso]>(inyecL1[k]-Twin) and tiempo[(i+2)*mediopaso]<(inyecL1[k]+Twin) or tiempo[(i)*mediopaso]<(inyecL1[k]-DurIny) and tiempo[(i+2)*mediopaso]>(inyecL1[k]-DurIny) or tiempo[(i)*mediopaso]<(inyecL1[k]+DurIny) and tiempo[(i+2)*mediopaso]>(inyecL1[k]+DurIny):
                Labels.append(1)
            else:
                Labels.append(0)
            if PLOT==1:
                if tiempo[i*mediopaso]>(inyecL1[k]-Twin) and tiempo[(i+2)*mediopaso]<(inyecL1[k]+Twin):
                    pylab.axvline(x=inyecL1[k] , color='g', linestyle=':', linewidth=1)
                if tiempo[(i)*mediopaso]<(inyecL1[k]-DurIny) and tiempo[(i+2)*mediopaso]>(inyecL1[k]-DurIny):
                    pylab.axvline(x=inyecL1[k]-DurIny , color='r', linestyle=':', linewidth=1)
    #                Labels.append(1)# = 1
                if tiempo[(i)*mediopaso]<(inyecL1[k]+DurIny) and tiempo[(i+2)*mediopaso]>(inyecL1[k]+DurIny):
                    pylab.axvline(x=inyecL1[k]+DurIny , color='b', linestyle=':', linewidth=1)
    #                Labels.append(1)# = 1
                if tiempo[i*mediopaso]>(inyecH1[k]-Twin) and tiempo[(i+2)*mediopaso]<(inyecH1[k]+Twin):
                    pylab.axvline(x=inyecH1[k] , color='g', linestyle='--', linewidth=1)
                if tiempo[(i)*mediopaso]<(inyecH1[k]-DurIny) and tiempo[(i+2)*mediopaso]>(inyecH1[k]-DurIny):
                    pylab.axvline(x=inyecH1[k]-DurIny , color='r', linestyle='--', linewidth=1)     
                if tiempo[(i)*mediopaso]<(inyecH1[k]+DurIny) and tiempo[(i+2)*mediopaso]>(inyecH1[k]+DurIny):
                    pylab.axvline(x=inyecH1[k]+DurIny , color='b', linestyle='--', linewidth=1)
                pylab.plot(timo,STRAINOL1, label = Labels[-1])
                pylab.plot(timo,STRAINOH1)
                pylab.legend(loc='upper right')
                pylab.show()
                
                
print(len(Labels))
#print(Labels[(int((2*inyecL1[0])/Twin)-5:int((2*inyecL1[0])/Twin)+5])
#print(TwinL1[0])
#print(TwinH1[0])
#print(TwinTIME[0])
# *********************************************
    # END: for i_fac in np.arange(0,FACTORS.size):
    # *********************************************
    
    
#CWB_ReadStrain.Original(DataPath,FolderName,job,GPSini,fs,doplot)

            
# *********************************************
# END: for i_job in np.array([0]):
# *********************************************  

