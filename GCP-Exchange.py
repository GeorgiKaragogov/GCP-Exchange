import string
import numpy as np

from Tkinter import Tk
from tkFileDialog import askopenfilename

Tk().withdraw()

def ReadFile(directory):
    file = open(directory,'r')
    lines = file.read().split('\n')
    lines.pop(0)

    mainArray = []
    j = 0
    for line in lines:
        mainArray.append([])
        elements = line.split(',')
        for el in elements:
            mainArray[j].append(el)

        j = j + 1

    return mainArray

def ParseGCPFiles(array):

    resultArray = []
    for row in array:
        resultArray.append([float(row[0]),float(row[1])])

    return resultArray

def ParseCoordFiles(array):

    resultArray = []
    for row in array:
        resultArray.append([int(row[0]),float(row[2]),float(row[1])])

    return resultArray

def FilesMatching(GCPArray, coordArray):

    indexes = []
    for GCPRow in GCPArray:
        for coordRow in coordArray:
            if ((coordRow[1] == GCPRow[0]) and (coordRow[2] == GCPRow[1])):
                indexes.append(coordRow[0])

    return indexes

def findRow(index,pointsArray):
    foundRow = []
    for i in range(0,len(pointsArray),1):
        if (index == pointsArray[i][0]):
            foundRow.append(pointsArray[i])

            return foundRow

def SnappingCoords(configuration,coordinates):

    resultArray = []
    for index in configuration:
        currentRow = findRow(index,coordinates)
        for el in currentRow:
            resultArray.append(el)

    return resultArray

def StringLines(GCPArray,changedArray):

    resultList = []
    changedArray = np.asarray(changedArray)

    for i in range(0,len(changedArray),1):
        resultList.append([str(changedArray[i][1]) + "," + str(changedArray[i][2]) + "," + GCPArray[i][2] + "," + GCPArray[i][3] + "," + GCPArray[i][4]])

    return resultList

GCPFileDir = askopenfilename(title = "Choose GCP file from QGIS",filetypes = (("GCP files","*.points"),("All files","*.*")))
sourceCoordsFileDir = askopenfilename(title = "Choose source coordinate file",filetypes = (("Coordinate files as *.txt","*.txt"),("Coordinate files as *.csv","*.csv"),("All files","*.*")))
destinationCoordsFileDir = askopenfilename(title = "Choose destination coordinate file",filetypes = (("Coordinate files as *.txt","*.txt"),("Coordinate files as *.csv","*.csv"),("All files","*.*")))

GCPRowFile = ReadFile(GCPFileDir)
sourceRowFile = ReadFile(sourceCoordsFileDir)
destinationRowFile = ReadFile(destinationCoordsFileDir)

mainFile = open(GCPFileDir,'r')
mainFileName = string.replace(GCPFileDir,'.points','')

parsedGCPFile = ParseGCPFiles(GCPRowFile)
parsedSourceFile = ParseCoordFiles(sourceRowFile)
parsedDestinationFile = ParseCoordFiles(destinationRowFile)

confArray = FilesMatching(parsedGCPFile,parsedSourceFile)
mainString = StringLines(GCPRowFile,SnappingCoords(confArray,parsedDestinationFile))

resultFile = open(mainFileName + "_NEW_.points","w")
resultFile.write("%s\n" % "mapX,mapY,pixelX,pixelY,enable")
for line in mainString:
    for el in line:
        resultFile.write("%s" % el)
    resultFile.write("%s\n" % "")

resultFile.close()
