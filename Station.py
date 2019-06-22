#!/usr/bin/env python
# coding: utf-8

# In[11]:
###########################################################
#This code provides Reconstructed data,RMSE value and R2 using Compressive Sensing concept for DCT matrix for CO2 from  input variables such as latitude , longitude, dtime. Wavelets has been used.
#Developed by Sai Sree Laya Chukkapalli on April 5th 2019 Friday, Time 8:45 AM   mail:saisree1@umbc.edu https://carta.umbc.edu/  https://www.csee.umbc.edu/
# Requirements:  tensorflow, pandas, numpy, pywt, mathplotlib libaries
#  Can be run in jupyter notebook changing the file name extension.             
# This code be run for daily data without making any changes for any satellite or station data.

###########################################################







import matplotlib
#get_ipython().run_line_magic('matplotlib', 'inline')
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, show, figure, title
from sklearn.metrics import r2_score
import pywt
import scipy.fftpack as spfft

#from scipy.sparse import identity

#get_ipython().run_line_magic('matplotlib', 'inline')
# make sure you've got the following packages installed
#get_ipython().run_line_magic('matplotlib', 'notebook')


import datetime
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.optimize as spopt
import scipy.fftpack as spfft
import scipy.ndimage as spimg
import cvxpy as cvx

from os import listdir
from os.path import isfile, join
np.random.seed(1)
def rmse(predictions, targets):   
    return np.sqrt(((predictions - targets) ** 2).mean()), r2_score(predictions.flatten(), targets.flatten())



#write data to a CSV file
def csv_writer_datetime(date_time, orig, recons, sat, path):
    """
    Write data to a CSV file path
    """
    with open(path, 'w') as csv_file:  
        #write columname
        csv_file.write('DateTime,CO2original,CO2reconstructed,FromSat')  
        csv_file.write('\n')     
        for i in range(len(date_time)): 
            csv_file.write(str(date_time[i])+','+str(orig[i])+','+str(recons[i])+','+str(sat[i]))
            csv_file.write('\n')   
        # Close opend file
        csv_file.close()
        
        
        
        
def csv_writer_datetime1(date_time, sigoco2,yoco2, path):
    """
    Write data to a CSV file path
    """
    with open(path, 'w') as csv_file:  
        #write columname
        csv_file.write('DateTime,reconsigoco2,orig')  
        csv_file.write('\n')     
        for i in range(len(date_time)): 
            csv_file.write(str(date_time[i])+','+str(sigoco2[i])+','+str(yoco2[i]))
            csv_file.write('\n')   
        # Close opend file
        csv_file.close()
        
        
                

#masterdata = pd.read_csv('mergealaska.csv')
masterdata = pd.read_csv('wmergedalaskafull.csv')
masterdata = masterdata[['dtime','xco2','dstype']]
masterdata=masterdata.sort_values(by=['dtime'])
x = np.sort(np.array(masterdata['dtime'])) #list(masterdata['latitude'].astype(int)) #np.sort(np.random.uniform(0, 10, 15))
y = np.array(masterdata['xco2'])     #3 + 0.2 * x + 0.1 * np.random.randn(len(x))
from_sat = np.array(masterdata['dstype'])
t=x
n=len(x)
print(n)
orig_y= np.array(masterdata['xco2']) 



# sum of two sinusoids
#n = 5000
#t = np.linspace(0, 1/8, n)
#y = np.sin(1394 * np.pi * t) + np.sin(3266 * np.pi * t)
#yt = spfft.dct(y, norm='ortho')

#plot on the same figure
f,a=plt.subplots()



#a.scatter(x,y,color='k',label='original')



plt.xlim([datetime.date(2014, 9, 1) ,datetime.date(2018, 9, 1)])
plt.ylim([390, 410])
plt.xlabel('Time')
plt.xticks(rotation=90)
plt.ylabel('XCO2(ppm)')



# Defines a wavelet object - 'db1' defines a Daubechies wavelet
w = pywt.Wavelet('db2')
plot(w.dec_lo)


# Multilevel decomposition of the input matrix
coeffs = pywt.wavedec(y, w, level=6)



#y=pywt.waverec(coeffs, w)  #using full reconstruction
#tested with other approximation, for this data it returns almost the same results
y=pywt.waverec(coeffs[:-1] + [None] * 1, w) # leaving out detail coefficients up to lvl 5



# extract small sample of signal
m = int(5 * n/100) #500 # 10% sample
#ri = np.random.normal(0.0,1.0, m).astype(int)
ri = np.random.choice(n, m, replace=False).astype(int) # random sample of indices
ri.sort() # sorting not strictly necessary, but convenient for plotting
t2 = t[ri]
y2 = y[ri]


# create idct matrix operator sensing matrix
A = spfft.idct(np.identity(n, dtype='int8'), norm='ortho', axis=0)
A = A[ri]

# do L1 optimization tested using Lasso as alternative
vx = cvx.Variable(n)
objective = cvx.Minimize(cvx.norm(vx, 1))
constraints = [A*vx == y2]
prob = cvx.Problem(objective, constraints)
result = prob.solve(verbose=True)

# reconstruct signal
l1 = np.array(vx.value)
l1 = np.squeeze(l1)
sig = spfft.idct(l1, norm='ortho', axis=0)
#wavelet give one additional point

master1 = masterdata[masterdata['dstype'].str.contains("oco2")]
print(len(master1))
#print(master1)
master1=master1.sort_values(by=['dtime'])
xoco2 = np.sort(np.array(master1['dtime'])) #list(masterdata['latitude'].astype(int)) #np.sort(np.random.uniform(0, 10, 15))
yoco2 = np.array(master1['xco2']) #3 + 0.2 * x + 0.1 * np.random.randn(len(x))
print(len(yoco2))

master2 = masterdata[masterdata['dstype'].str.contains("gosat")]
print(len(master2))
#print(master2)
master2=master2.sort_values(by=['dtime'])
xgosat = np.sort(np.array(master2['dtime'])) #list(masterdata['latitude'].astype(int)) #np.sort(np.random.uniform(0, 10, 15))
ygosat = np.array(master2['xco2']) 



a.scatter(t,sig,color='r',label='Reconstructed',s=10)
a.scatter(xoco2,yoco2,color='k',label='OCO-2',s=10)
a.scatter(xgosat,ygosat,color='b',label='GOSAT',s=10)
#a.legend(['Original signal', 'Reconstructed signal'])
a.legend(loc='upper left',fontsize = 7)
#plt.suptitle('Latitude: 30º to 50º and Longitude: -120º to -70º')

plt.title('GOSAT & OCO2 data fusion Alaska, year 2014-2018 ' +"\n"+ 'Lat: 60º to 70º and Lon:  -165º to -90º')
#plt.suptitle('Latitude: 30º to 50º and Longitude: -120º to -70º')
#sig=np.append(sig,398)
error,r2=rmse(sig, orig_y)
print("RMSE alaska =")
print(error)
print("R2 alaska =")
print(r2)
print(len(sig))








#plt.suptitle('Latitude: 30º to 50º and Longitude: -120º to -70º')
#title('CO2 (ppm) GOSAT and CO2 (ppm) OCO2 in a part of North America for the year 2015 using Compressive Sensing  RMSE='+str(round(error,2))+" R2="+str(round(r2,2)))
#plt.savefig('oco2_gosat_reconstructed_sig15.png')
plt.savefig('oco2_gosat_reconstructed_sig20.png')
csv_writer_datetime(t, orig_y, sig,from_sat,'outputalaskawithoutmean.csv')
#write data to csv file
#csv_writer_datetime(t, orig_y, sig,from_sat,'outputalaska15.csv')
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:




