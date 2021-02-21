import pydicom as dicom
import os
import numpy as np
from matplotlib import pyplot as plt, cm
import math


def computeArrayRate(errG, dir,index):
    criteria = np.arange(0.5, 3.5, 0.5)
    rateGlobal = np.zeros(len(criteria), dtype=float)
    #print(np.size(criteria))
    for i in range(0, np.size(criteria)):
        #print(errG)
        erSup5 = errG[index]
        #print(erSup5)
        dims = erSup5.shape #array 3D errG linéarisé (erSup5)par index => de dimension /3
        #print(dims)
        #print(np.size(index)/3)
        #rateGlobal[i] = 100.*np.size(np.where(np.abs(errG) <= criteria[i]))/3./(
        #    dims[0]*dims[1]*dims[2]-np.size(np.where(np.isnan(errG)))/3.)
        rateGlobal[i] = 100.*np.size(np.where(np.abs(erSup5) <= criteria[i]))/3./(
            dims[0]/3)
        #print(np.size(np.where(np.isnan(errG)))/3.)
    #print(np.size(np.where(np.isnan(errG)))/3.)
    #print(list(rateGlobal))
    #print(list(criteria))
    fig = plt.figure()
    # fig.set_size_inches(4.,3.)
    low = min(rateGlobal)
    high = max(rateGlobal)
    plt.ylim([math.ceil(low-0.5*(high-low)), math.ceil(high+1)])
    plt.ylim([0,101])

    plt.bar(list(criteria), list(rateGlobal), align='center',
            width=0.3, color='yellow', edgecolor='red')
    plt.xlabel('Critère: erreur en %')
    plt.ylabel('Taux de passage en %')
    plt.title('Changement de version Raystation: spots à ' + dir)
    fig.savefig('fig/' + dir + '_Rate_histo.pdf',
                facecolor='w', edgecolor='w', format='pdf')



def draw2DMapDoseTransverse(dim1,dim2,array, dir, namefig,version):
    fig = plt.figure()
    im = plt.pcolormesh(dim1, dim2, array)
    plt.title('Dose à la profondeur du maximum : '+version)
    cbar = plt.colorbar(im)
    cbar.set_label('Dose en Gy')
    #plt.axes().set_aspect('equal', 'datalim')
    plt.xlabel('Y en mm')
    plt.ylabel('X en mm')
    plt.set_cmap(plt.get_cmap('jet'))
    fig.savefig('fig/' + dir + '_DoseMapTransverse' + namefig+version+'.pdf',
                facecolor='w', edgecolor='w', format='pdf')


def draw2DMapDoseDepth2(dim1,dim2,array, dir, namefig,version):
    fig = plt.figure()
    im = plt.pcolormesh(dim1, dim2, array)
    plt.title('Dose en fonctionde la profondeur: '+version)
    cbar = plt.colorbar(im)
    cbar.set_label('Dose en Gy')

   
    #plt.axes().set_aspect('equal', 'datalim')
    plt.xlabel('Z en mm')
    plt.ylabel('X en mm')
    plt.set_cmap(plt.get_cmap('jet'))
    fig.savefig('fig/' + dir + '_DoseMapDepth' + namefig+version+'.pdf',
                facecolor='w', edgecolor='w', format='pdf')

def draw2DMapErrorTransverse(dim1,dim2,array, dir,maxDose):
    fig = plt.figure()
    im = plt.pcolormesh(dim1, dim2, array)
    plt.title('Erreur de dose à la profondeur du maximum')
    cbar = plt.colorbar(im)
    plt.clim(-3, 3)
    cbar.set_label('Erreur en %'+' de '+str(maxDose)+ ' (Gy)')
    #plt.axes().set_aspect('equal', 'datalim')
    plt.xlabel('Y en mm')
    plt.ylabel('X en mm')
    plt.set_cmap(plt.get_cmap('RdYlBu_r'))
    fig.savefig('fig/' + dir + '_ErrorMapTransverse' + '.pdf',
                facecolor='w', edgecolor='w', format='pdf')


def draw2DMapErrorDepth2(dim1,dim2,array, dir,maxDose):
    fig = plt.figure()
    im = plt.pcolormesh(dim1, dim2, array)
    plt.title('Erreur de dose à la profondeur du maximum')
    cbar = plt.colorbar(im)
    plt.clim(-3, 3)
    cbar.set_label('Erreur en %'+' de '+str(maxDose)+ ' (Gy)')
    #plt.axes().set_aspect('equal', 'datalim')
    plt.xlabel('Y en mm')
    plt.ylabel('X en mm')
    plt.set_cmap(plt.get_cmap('RdYlBu_r'))
    fig.savefig('fig/' + dir + '_ErrorMapDepth' +'.pdf',
                facecolor='w', edgecolor='w', format='pdf')

PathDicom = "RTDose/SingleBeam/"
#PathDicom = "RTDose/test/"
refFile = "Mp.dcm"
testedFile = "P.dcm"
# lstFilesDCM = []  # create an empty list
for dirName, subdirList, fileList in os.walk(PathDicom):
    for d in subdirList:
        rFile = os.path.join(dirName+d, refFile)
        tFile = os.path.join(dirName+d, testedFile)
        print(rFile, tFile)
        # for filename in fileList:
        #    if ".dcm" in filename.lower():  # check whether the file's DICOM
        #        lstFilesDCM.append(os.path.join(dirName,filename))
        refDs = dicom.read_file(rFile)
        testedDs = dicom.read_file(tFile)
        #print(refDs)
        
        ds = refDs.pixel_array
        doseScalingRef = refDs.DoseGridScaling
        doseScalingTested =testedDs.DoseGridScaling
        ConstPixelDims = ds.shape

        print(ConstPixelDims)
        # Load spacing values (in mm)
        ConstPixelSpacing = (float(refDs.PixelSpacing[0]), float(
            refDs.PixelSpacing[1]), float(refDs.SliceThickness))
        print(ConstPixelSpacing)

        x = np.arange(
            0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
        y = np.arange(
            0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])
        z = np.arange(
            0.0, (ConstPixelDims[2]+1)*ConstPixelSpacing[2], ConstPixelSpacing[2])

        refArray = refDs.pixel_array

        testedArray = testedDs.pixel_array
        testedArray = testedArray[:,:ConstPixelDims[1],:]
        refArray = refArray*doseScalingRef
        testedArray = testedArray*doseScalingTested
        maxA = np.max(refArray)
        errorGlobal = 100*(refArray-testedArray)/maxA
        #print(maxA)
        errorGlobal[refArray == 0.] = np.nan # where it's 0 data do not considered for statistics 
        
        criterVoxelDoseMin = 0.05
        indiceRefArrayUpTo5 = np.where(refArray/maxA >= criterVoxelDoseMin)
        computeArrayRate(errorGlobal, d,indiceRefArrayUpTo5)
        MaxIndices = np.where(refArray == np.amax(refArray))
        ref = 'MP'
        tested = 'Precision'
        
        draw2DMapDoseTransverse(z, x, refArray[:, 15, :],d, 'AtMaxDepth',ref)
        draw2DMapDoseTransverse(z, x, testedArray[:, 15, :],d, 'AtMaxDepth',tested)
        draw2DMapErrorTransverse(z, x, errorGlobal[:, 15, :],d,np.round(maxA,2))

        draw2DMapDoseDepth2(y, x, refArray[:, :, np.int(ConstPixelDims[2]/2)], d, 'AtMaxDepth',ref)
        draw2DMapDoseDepth2(y, x, testedArray[:, :, np.int(ConstPixelDims[2]/2)], d, 'AtMaxDepth',tested)
        draw2DMapErrorDepth2(y, x, errorGlobal[:,:,np.int(ConstPixelDims[2]/2)],d,np.round(maxA,2))

        