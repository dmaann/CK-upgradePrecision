import csv
import numpy as np
import fpdf

def getRawDataArray(file):
  f = open(file)
  csv_f = csv.reader(f)
  tmp= []
  for row in csv_f:
    try:
      tmp.append(np.float(row[3]))
    except:
      pass
  arr = np.array(tmp)
  sz = arr.shape[0]
  #print(file + ' : size ', sz)
  return arr,sz


def getRawDataArrayMP(file):
  f = open(file)
  csv_f = csv.reader(f)
  tmp= []
  for row in csv_f:

    try:
      if (row[1] == 'Système de traitement: C0410 9027-1270437307383545856'):
        try:
          tmp.append(np.float(row[3]))
        except:
          pass
    except:
      pass
  arr = np.array(tmp)
  sz = arr.shape[0]
  #print(file + ' : size ', sz)
  return arr,sz

ocrFixed_Precision = 'data/Fixe/CommissioningOCR-precision.csv'
ocrFixed_Multiplan = 'data/Fixe/CommissioningOCR.csv'
tprFixed_Precision = 'data/Fixe/CommissioningTPR-precision.csv'
tprFixed_Multiplan = 'data/Fixe/CommissioningTPR.csv'
ofFixed_Precision = 'data/Fixe/CommissioningOF-precision.csv'
ofFixed_Multiplan = 'data/Fixe/CommissioningOF.csv'
ocrX_MLC_Precision = 'data/MLC/CommissioningOCRX-precision.csv'
ocrX_MLC_Multiplan = 'data/MLC/CommissioningOCRX.csv'
ocrY_MLC_Precision = 'data/MLC/CommissioningOCRY-precision.csv'
ocrY_MLC_Multiplan = 'data/MLC/CommissioningOCRY.csv'
tprMLC_Precision = 'data/MLC/CommissioningTPR-precision.csv'
tprMLC_Multiplan = 'data/MLC/CommissioningTPR.csv'
ofMLC_Precision = 'data/MLC/CommissioningOF-precision.csv'
ofMLC_Multiplan = 'data/MLC/CommissioningOF.csv'
filesMP = [tprFixed_Multiplan,ofFixed_Multiplan,tprMLC_Multiplan,ofMLC_Multiplan,ocrFixed_Multiplan,ocrX_MLC_Multiplan,ocrY_MLC_Multiplan]
filesP=[tprFixed_Precision,ofFixed_Precision,tprMLC_Precision,ofMLC_Precision,ocrFixed_Precision,ocrX_MLC_Precision,ocrY_MLC_Precision]

output=['Measurement TPS data consistency between Multiplan and Precision upgrade ', '',]
for i in range(len(filesMP)):
  P,nP = getRawDataArray(filesP[i])
  Mp, nMp= getRawDataArrayMP(filesMP[i])
  diff = np.abs(Mp-P)
  #print(diff)
  checkSum = np.sum(diff)
  boolOut=False
  if checkSum == 0.:
    boolOut = True
  output.append('file comparison: ' + filesMP[i]+ '   '+ filesP[i])
  output.append('Consistency status (False/True): ' + str(boolOut))
  output.append('CheckSum difference between Multiplan and Precision for all field sizes and depths : ' +  str(checkSum))
  output.append(' ')
  #print(checkSum)


pdf = fpdf.FPDF(format='letter')
pdf.add_page()
pdf.set_font("Arial", size=12)

for i in output:
    pdf.write(5,str(i))
    pdf.ln()
pdf.output("ReportUpgrade-MeasurementTPS-consistency.pdf")