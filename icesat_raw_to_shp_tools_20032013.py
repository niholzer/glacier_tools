#! /usr/bin/python
# -*- coding: utf8 -*-

"""
Program purpose: ICESat tools

Detailed description
"""

__author__= "Nicolai Holzer"
__author_email__ = "first-name dot last-name @ tu-dresden.de"
__date__ ="2012-03-20"
__version__ = "v0.1.1" #MajorVersion(backward_incompatible).MinorVersion(backward_compatible).Patch(Bug_fixes)


#Changelog
#-------------------------------------------------------------------------------
#2012-11-02: v0.1.0 first version


#Imported libraries
#-------------------------------------------------------------------------------
#standard libraries
import time
import math
import string
import re
import os

#related libraries
import numpy as np
print np.__file__, np.__version__

#local applications / library specific import


#===============================================================================

#Module default values / constants
#-------------------------------------------------------------------------------

DATA_URL_SCRIPT_PATH = "D:\Data\Raw data\DEM\ICESat\Lake Karakul\ICESat data Lake Karakul"
DATA_ASCII_ICESAT_PATH = "D:\Data\Temporary data\DEM\ICESat\program_ngat014\output"
DATA_URL_SCRIPT_FILENAME = "data_url_script_2013-03-20_064451.txt"

ICESAT_PLACEHOLDER_STRING = "GLA14_633_...._..._...._._.._.....DAT$"


#_______________________________________________________________________________

class MainInterface:
    """
    Description
    
    ICESat treatment tools by using download url script file via linux-program wget and ICESat data treatment via program ngat-0.14 

    COMMENTS:
    IMPORTANT:
    """

    #def __init__(self):
        #"""Constructor"""
        
    #def __del__ (self):
        #"""Destructor"""


    def getIceSatFileNames(self, directory_, filename_, iceSatPlaceholder_):
        """
        Programm description: 
        
        #1: Before ngat in order to obtain input and output filenames
        Filename extraction program from ICESat download data url script as input for program ngat-0.14 --> Generates as output ICESat ascii files
        
        1. Zur Extraktion aller ICESat-Dateinamen aus dem URL-Download-Skript als Input für Programm 'ngat' (Initialisierungsdatei).
        Dann: Nutzung von 'ngat' zur Konvertierung aller ICESat-files von RAW in ASCII
        
        INPUT_PARAMETERS:
        input_      - 

        COMMENTS:
        """
        
        iceSatNameList = [] #List of input filenames for ICESat for ngat
        iceSatNameListOut = []# List with names for ICESat ascii output files generated by ngat-0.14
        nFile = 0 #Counter for number of input files
        
        #Check if directory ends with '/' for correct reading, open file
        if not directory_.endswith('/') and directory_ != '': #Adds '/' to path in case that this is not the case
            directory_ = directory_+'/'
        infileName = directory_+filename_ #Add path of data directory to filename
        inputFile = open(infileName, 'r') #Open ICESat url script file
                
        #Define output filename from input filename for data file
        outfileNameTmp = filename_.rsplit(".")
        outfileName = directory_+outfileNameTmp[0]+".out"
                     
        #Read line by line of data url script with ICESat file names for input of ngat program
        for line in inputFile:
            if re.search(iceSatPlaceholder_, line) != None: #If defined pattern (see constant) in specific line of iceSatPlaceholder exists
                
                nFile+=1 #increment
                
                iceSatName = re.findall(iceSatPlaceholder_, line) #Extract IceSat filename (returns list)
                iceSatNameList.append(iceSatName[0]) #Append List value of IceSat filename to list of all filenames
                
                iceSatNameOutTmp = iceSatName[0].rsplit(".") #Set ICESAT ngat output filenames from input ICESAT filenames
                iceSatNameOutTmp = iceSatNameOutTmp[0]+".out"
                iceSatNameListOut.append(iceSatNameOutTmp)
                
        iceSatNameString = ';'.join(iceSatNameList) #Convert list to single string with separator ';'
        iceSatNameOutString = ';'.join(iceSatNameListOut) #Convert list to single string with separator ';'
        
        #Write resulting filenames to output file
        outputFile = open(outfileName, 'w')
        outputFile.write("List of input filenames for ngat: "+iceSatNameString) #ngat ICESat input files 
        outputFile.write("\n")
        outputFile.write("List of output filenames for ngat: "+iceSatNameOutString) #ngat ICESat ASCII output files
        
        print "\nDone. The following data consisting of ", nFile, " input files was written to ", str(outfileName), ": \n"
        print iceSatNameString 
        print iceSatNameOutString
        
        inputFile.close()
        outputFile.close()
        
        return 
        
        
        
    def adaptIceSatAsciiFile(self, directoryAsciiFiles_,filename_):
        """
        Programm description: 
        
        #2: After use of program ngat
        Adapt output Ascii File from program ngat-0.14 (eliminate white spaces) to get conformal csv file as input for Shapefile generation via QGis
        
        3. Nach Nutzung von 'ngat' zur Konvertierung aller ICESat-files von RAW in ASCII:
        Zur Konvertierung der ngat-Outputfiles (ASCII-Datei) in ein konformes CSV-Dokument, Aggregation aller Input-ASCII-Dateien in eine einzige 
        Datei (CSV-Outputdatei), Berechnung der EGM96-Geoidhöhe als extra Attributwert für weitere Datenverarbeitung
        
        INPUT_PARAMETERS:
        input_      - 

        COMMENTS:
        """
                
        #Check if directory ends with '/' for correct reading, open file
        if not directoryAsciiFiles_.endswith('/') and directoryAsciiFiles_ != '': #Adds '/' to path in case that this is not the case
            directoryAsciiFiles_ = directoryAsciiFiles_+'/'
        
        inputLineList = [] #Input lines read from each file
        nFile = 0 #Counter for number of input files
        
        #Read all lines of all ngat-outputfiles, as input for this program
        for root,dirs,files in os.walk(directoryAsciiFiles_): #Go through all files in determined directory
            for infileName in files:
              
                infileAscii = directoryAsciiFiles_+infileName #Add path of data directory to filename
               
                if infileName.endswith(".out"): #Open each file if ending with '.out'
                
                    nFile+=1 #increment
                    inputFile = open(infileAscii, 'r') 
                    for line in inputFile: #Read each line in file
                        inputLineList.append(line)
                    #print inputLine[0]
                    inputFile.close()
        
    
        
        #Data treatment: Get the relevant data by using string slicing, eleminating useless withespaces, saving in numpy array for csv-export
    
        #Header in csv-file
        pOutputLineList = np.array(['Record_Number', 'Date', 'Time', 'Latitude', 'Longitude', 'elevation', 'geoid', 'i_SatElevCorr', 'i_gval_rcv', 'i_UTCTime', 'i_deltaEllip', 'WGS84_EGM96_Geoidal_height'])
                    
        for inputLineListI, inputLineListValue in enumerate(inputLineList): #Go through all values that were read from the input files (list)
            
            #Get the values via slicing
            inRecordNumber = inputLineListValue[0:11].strip()
            inDate = inputLineListValue[11:22].strip()
            inTime = inputLineListValue[22:35].strip()
            inLatitude = inputLineListValue[35:46].strip()
            inLongitude = inputLineListValue[46:57].strip()
            inElevation = inputLineListValue[57:69].strip()
            inGeoid = inputLineListValue[69:85].strip()
            inISatElevCorr = inputLineListValue[85:94].strip()
            inIGvalRcv = inputLineListValue[94:100].strip()
            inIUtcTime = inputLineListValue[100:114].strip()
            inIDeltaEllip = inputLineListValue[114:123].strip()
            
            #The ICESat dataset is available in ellipsoidal heights with reference to the Topex/Poseidon ellipsoid, which is about 70 cm different from the WGS84 ellipsoid.
            #The ICESat (Topex/Poseidon ellipsoid) ellipsoidal heights were transformed to the WGS84 ellipsoid by removing 0.7 m, and then, the EGM96-geoid undulations were removed 
            #from the ellipsoidal heights to obtain orthometric heights. Now, the common reference is the geoid in WGS84 (Bhang et al., 2007)
            
            calcWGS84EGM96GeoidalHeight = float(inElevation) - float(inGeoid) - 0.7 #SRTM_geoid (WGS84?EGM96)= ICESat elevation WGS84 = ICESat elevation measured - ICESat geoid - 0.7
            
            #-->Result: Conversion inputLineList to a numpy file, with each array field having the relevant value
            pInputNumpy = np.array([inRecordNumber, inDate, inTime, inLatitude, inLongitude, inElevation, inGeoid, inISatElevCorr, inIGvalRcv, inIUtcTime, inIDeltaEllip, str(calcWGS84EGM96GeoidalHeight)])
      
            pOutputLineList = np.vstack((pOutputLineList, pInputNumpy))#Add line to ouput numpy file
           
        #Define output filename from input filename for data file
        iceSatAsciiFilenameOutTmp = filename_.rsplit(".")
        iceSatAsciiFilenameOut =  directoryAsciiFiles_+iceSatAsciiFilenameOutTmp[0]+"_allAscii.csv"
        
        #Write resulting filenames to output file
        #test = open(iceSatAsciiFilenameOut, 'w')
        np.savetxt(iceSatAsciiFilenameOut, pOutputLineList, fmt='%s', delimiter=',', newline='\n')  
        
                
        print "\nDone. The data of ", nFile, " input files was written to the csv output file ", str(iceSatAsciiFilenameOut), " (Shape: ", str(pOutputLineList.shape),"). It consists of ", str(inputLineListI+1), " ICESat points. \n"
        
        return
        
    
        
#_______________________________________________________________________________

def main():
    """
    Main function.

    Detailed description   
    """
    
    #Initialization
    #-------------------------------------------------------------------------------
    startTime = time.time()
    print("_____________________________________________________________________________________________")
    print("Starting program '" + str(__name__) + "' version '" + str(__version__) + "' from '" + str(__date__) + "':")


    #Run program
    #-------------------------------------------------------------------------------
    pInterfaceMain = MainInterface() #Initialize
    
    #Currently: Use input data values from Constants
    operation_ = 'getIceSatFileNames'
    #operation_ = 'adaptIceSatAsciiFile' 
    
    try:
        if operation_ == 'getIceSatFileNames':
            directory = str(DATA_URL_SCRIPT_PATH)
            filename = str(DATA_URL_SCRIPT_FILENAME )          
            iceSatPlaceholder = str(ICESAT_PLACEHOLDER_STRING)
            pInterfaceMain.getIceSatFileNames(directory, filename, iceSatPlaceholder) #
        
        #operation_ = 'adaptIceSatAsciiFile' 
        #if operation_ == 'adaptIceSatAsciiFile': 
        elif operation_ == 'adaptIceSatAsciiFile':
            directoryAsciiFiles = str(DATA_ASCII_ICESAT_PATH)
            filename = str(DATA_URL_SCRIPT_FILENAME )    
            pInterfaceMain.adaptIceSatAsciiFile(directoryAsciiFiles, filename) 
        
        
        else:
            raise Exception("Parser error: Operation '" + str(operation_) + "' is unknown.")
            

    except Exception: #If Exceptiation occured in this module or all connected sub-modules
        print('Exception error occured (see below)! ')
        raise

    finally:
        print("Finished. Total processing time [s]: '" + str(time.time() - startTime) + "'.")
        print("_____________________________________________________________________________________________")
      

if __name__ == "__main__":
    main()
