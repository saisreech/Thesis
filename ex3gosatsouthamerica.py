# This code is Developed by Sai Sree Laya Chukkapalli mail id : saisree1@umbc.edu. Date 1st March, Friday 2019 Time  3:30 PM for  converting .h5 to csv  
#Can be used for multiple number of variables for GOSAT and places over the world by changing latitude and longitude values. The below is for  south america satellite data 
# Below is the the commented line to run the code by creating output folder  
from netCDF4 import Dataset
import netCDF4
import pandas as pd
import csv
import os
import sys
from os import path
import sys, getopt
from os.path import basename

# variables
inputFolderPath = ''
outputFolderPath = ''
fileArr = [];

def transferCheck():
	global fileArr;
	for f in range(0,len(fileArr)):
		try:
			transferData(fileArr[f])
		except Exception as ex:
			#print("Exception in file " + fileArr[f])
			template = "An exception of type {0} occurred. Arguments:\n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print (message)
			print("Exception in file " + fileArr[f])


def transferData(fileName):
		f = fileName
		print(f)
		fWithoutExt = f.split(".h5")[0]
		print(fWithoutExt)
		#fpath = path.join(inputFolderPath,f)
		nc = Dataset(f, mode='r')
		nc.variables.keys()
	        
		latitude = nc.groups['Data'].groups['geolocation'].variables['latitude'][:]
		longitude = nc.groups['Data'].groups['geolocation'].variables['longitude'][:]
                #co2flux= nc.variables['xco2'][:]
		xco2 = nc.groups['scanAttribute'].groups['referenceData'].variables['XCO2'][:]
                
		timecol = nc.groups['scanAttribute'].variables['time'][0]
		df = pd.DataFrame({'timecol':str(timecol),'latitude':latitude,'longitude':longitude, 'xco2':xco2})
		#df = pd.DataFrame({'latitude':latitude,'longitude':longitude,'xco2':XCO2,'surfacepressure':surfacePressure, 'windspeed':surfaceWindSpeed, 'temperature':temperatureProfile })
		print(df.head())
                #df = df[df.warn_level < 14]
		df = df[(df.latitude >= -20) & (df.longitude >= -70)]
		df = df[(df.latitude <= 0) & (df.longitude <= -40)]
		df = df[['timecol','latitude','longitude','xco2']]
		df.set_index('timecol',inplace = True)
		df.to_csv(outputFolderPath+fWithoutExt+ '.csv', sep=',')
		

def getFiles():
        global fileArr;
        fileArr = [f for f in os.listdir(inputFolderPath) if f.endswith(".h5")]
        print(len(fileArr))

def main(argv):
   global inputFolderPath;
   global outputFolderPath;
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifolder=","ofolder="])
   except getopt.GetoptError:
      print ('test.py -i <inputFolderPath> -o <outputFolderPath>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('test.py -i <inputFolderPath> -o <outputFolderPath>')
         sys.exit()
      elif opt in ("-i", "--ifolder"):
         inputFolderPath = arg
      elif opt in ("-o", "--ofolder"):
         outputFolderPath = arg
   print ('Input file is "', inputFolderPath)
   print ('Output file is "', outputFolderPath)

if __name__ == "__main__":
   main(sys.argv[1:])
   getFiles()
   transferCheck()
#   transferData()



#python ex3gosatsouthamerica.py -i "/home/saisree1/GOSATnew/" --ofolder "/home/saisree1/GOSATnew/gosatsouthamerica/"

