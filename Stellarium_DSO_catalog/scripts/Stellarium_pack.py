from PyQt5.QtCore import QDataStream, QByteArray, QBuffer, QIODevice, QFile
import math
import re


otypeMap = {"G": "Nebula::NebGx",
"GX": "Nebula::NebGx",
"GC": "Nebula::NebGc",
"OC": "Nebula::NebOc",
"NB": "Nebula::NebN",
"PN": "Nebula::NebPn",
"DN": "Nebula::NebDn",
"RN": "Nebula::NebRn",
"C+N": "Nebula::NebCn",
"RNE": "Nebula::NebRn",
"HII": "Nebula::NebHII",
"SNR": "Nebula::NebSNR",
"BN": "Nebula::NebBn",
"EN": "Nebula::NebEn",
"SA": "Nebula::NebSA",
"SC": "Nebula::NebSC",
"CL": "Nebula::NebCl",
"IG": "Nebula::NebIGx",
"RG": "Nebula::NebRGx",
"AGX": "Nebula::NebAGx",
"QSO": "Nebula::NebQSO",
"ISM": "Nebula::NebISM",
"EMO": "Nebula::NebEMO",
"GNE": "Nebula::NebHII",
"RAD": "Nebula::NebISM",
"LIN": "Nebula::NebAGx",
"BLL": "Nebula::NebBLL",
"BLA": "Nebula::NebBLA",
"MOC": "Nebula::NebMolCld",
"YSO": "Nebula::NebYSO",
"Q?": "Nebula::NebPossQSO",
"PN?": "Nebula::NebPossPN",
"*": "Nebula::NebStar",
"SFR": "Nebula::NebMolCld",
"IR": "Nebula::NebDn",
"**": "Nebula::NebStar",
"MUL": "Nebula::NebStar",
"PPN": "Nebula::NebPPN",
"GIG": "Nebula::NebIGx",
"OPC": "Nebula::NebOc",
"MGR": "Nebula::NebSA",
"IG2": "Nebula::NebIGx",
"IG3": "Nebula::NebIGx",
"SY*": "Nebula::NebSymbioticStar",
"PA*": "Nebula::NebPPN",
"CV*": "Nebula::NebStar",
"Y*?": "Nebula::NebYSO",
"CGB": "Nebula::NebISM",
"SNRG": "Nebula::NebSNR",
"Y*O": "Nebula::NebYSO",
"SR*": "Nebula::NebStar",
"EM*": "Nebula::NebEmissionLineStar",
"AB*": "Nebula::NebStar",
"MI*": "Nebula::NebStar",
"MI?": "Nebula::NebStar",
"TT*": "Nebula::NebStar",
"WR*": "Nebula::NebStar",
"C*": "Nebula::NebEmissionLineStar",
"WD*": "Nebula::NebStar",
"EL*": "Nebula::NebStar",
"NL*": "Nebula::NebStar",
"NO*": "Nebula::NebStar",
"HS*": "Nebula::NebStar",
"LP*": "Nebula::NebStar",
"OH*": "Nebula::NebStar",
"S?R": "Nebula::NebStar",
"IR*": "Nebula::NebStar",
"POC": "Nebula::NebMolCld",
"PNB": "Nebula::NebPn",
"GXCL": "Nebula::NebGxCl",
"AL*": "Nebula::NebStar",
"PR*": "Nebula::NebStar",
"RS*": "Nebula::NebStar",
"S*B": "Nebula::NebStar",
"SN?": "Nebula::NebSNC",
"SR?": "Nebula::NebSNRC",
"DNE": "Nebula::NebDn",
"RG*": "Nebula::NebStar",
"PSR": "Nebula::NebSNR",
"HH": "Nebula::NebISM",
"V*": "Nebula::NebStar",
"*IN": "Nebula::NebCn",
"SN*": "Nebula::NebStar",
"PA?": "Nebula::NebPPN",
"BUB": "Nebula::NebISM",
"CLG": "Nebula::NebGxCl",
"POG": "Nebula::NebPartOfGx",
"CGG": "Nebula::NebGxCl",
"SCG": "Nebula::NebGxCl",
"REG": "Nebula::NebRegion",
"?": "Nebula::NebUnknown"
}
otypedic = {
"G": 0,
"GX": 0,
"GC": 7,
"OC": 6,
"NB": 10,
"PN": 11,
"DN": 12,
"RN": 13,
"C+N": 16,
"RNE": 13,
"HII": 17,
"SNR": 18,
"BN": 14,
"EN": 15,
"SA": 8,
"SC": 9,
"CL": 5,
"IG": 3,
"RG": 2,
"AGX": 1,
"QSO": 4,
"ISM": 19,
"EMO": 20,
"GNE": 17,
"RAD": 19,
"LIN": 1,
"BLL": 21,
"BLA": 22,
"MOC": 23,
"YSO": 24,
"Q?": 25,
"PN?": 26,
"*": 28,
"SFR": 23,
"IR": 12,
"**": 28,
"MUL": 28,
"PPN": 27,
"GIG": 3,
"OPC": 6,
"MGR": 8,
"IG2": 3,
"IG3": 3,
"SY*": 29,
"PA*": 27,
"CV*": 28,
"Y*?": 24,
"CGB": 19,
"SNRG": 18,
"Y*O": 24,
"SR*": 28,
"EM*": 30,
"AB*": 28,
"MI*": 28,
"MI?": 28,
"TT*": 28,
"WR*": 28,
"C*": 30,
"WD*": 28,
"EL*": 28,
"NL*": 28,
"NO*": 28,
"HS*": 28,
"LP*": 28,
"OH*": 28,
"S?R": 28,
"IR*": 28,
"POC": 23,
"PNB": 11,
"GXCL": 33,
"AL*": 28,
"PR*": 28,
"RS*": 28,
"S*B": 28,
"SN?": 31,
"SR?": 32,
"DNE": 12,
"RG*": 28,
"PSR": 18,
"HH": 19,
"V*": 28,
"*IN": 16,
"SN*": 28,
"PA?": 27,
"BUB": 19,
"CLG": 33,
"POG": 34,
"CGG": 33,
"SCG": 33,
"REG": 35,
"?": 36
}

def ConverttxtToPack(in1,out1):
    dsoIn = QFile(in1)
    if dsoIn.open(QIODevice.ReadOnly | QIODevice.Text) is False:
        return
    dsoOut=QFile(out1)
    if dsoOut.open(QIODevice.WriteOnly) is False:
        return
    totalRecords = 0
    while (dsoIn.atEnd() is False):
        dsoIn.readLine()
        totalRecords+=1
    dsoIn.seek(0)
    dsoOutStream = QDataStream(dsoOut)
    dsoOutStream.setVersion(QDataStream.Qt_5_2)
    readOk = 0
    dsoOutStream.writeQString('3.11')
    dsoOutStream.writeQString('standard')
    while (dsoIn.atEnd() is False):
        record = str(dsoIn.readLine(), encoding='utf-8')
        vp = re.match("ersion\s+([\d\.]+)\s+(\w+)",record)
        if (record.startswith("//") or record.startswith("#")):
            totalRecords-=1
            continue
        lis=record.split('\t')
        try:
        # if 1:
            id = int(lis[0])
            ra = float((lis[1]).strip())
            dec = float((lis[2]).strip())
            bMag = float(lis[3])
            vMag = float(lis[4])
            oType = (lis[5]).strip()
            mType = (lis[6]).strip()
            majorAxisSize = float(lis[7])
            minorAxisSize = float(lis[8])
            orientationAngle = int(float(lis[9]))
            z = float(lis[10])
            zErr = float(lis[11])
            plx = float(lis[12])
            plxErr = float(lis[13])
            dist = float(lis[14])
            distErr = float(lis[15])
            NGC = int(lis[16])
            IC = int(lis[17])
            M = int(lis[18])
            C = int(lis[19])
            B = int(lis[20])
            Sh2 = int(lis[21])
            VdB = int(lis[22])
            RCW = int(lis[23])
            LDN = int(lis[24])
            LBN = int(lis[25])
            Cr = int(lis[26])
            Mel = int(lis[27])
            PGC = int(lis[28])
            UGC = int(lis[29])
            Ced = (lis[30]).strip()
            Arp = int(lis[31])
            VV = int(lis[32])
            PK = (lis[33]).strip()
            PNG = (lis[34]).strip()
            SNRG = (lis[35]).strip()
            ACO = (lis[36]).strip()
            HCG = (lis[37]).strip()
            ESO = (lis[38]).strip()
            VdBH = (lis[39]).strip()
            DWB = int(lis[40])
            Tr = int(lis[41])
            St = int(lis[42])
            Ru = int(lis[43])
            VdBHa = int(lis[44])
            raRad = float(ra) * math.pi / 180
            decRad = float(dec) * math.pi / 180
            majorAxisSize /= 60
            minorAxisSize /= 60
            if (bMag <= 0):
                bMag = 99
            if (vMag <= 0):
                vMag = 99
            if oType.upper() in otypedic:
                nType = otypedic[oType.upper()]
            else:
                nType = 36
            readOk += 1
            dsoOutStream.writeInt(id)
            dsoOutStream.writeFloat(ra/180*math.pi)
            dsoOutStream.writeFloat(dec/180*math.pi)
            dsoOutStream.writeFloat(bMag)
            dsoOutStream.writeFloat(vMag)
            dsoOutStream.writeInt(nType)
            # dsoOutStream.writeUInt64(nType)
            dsoOutStream.writeQString(mType)
            dsoOutStream.writeFloat(majorAxisSize)
            dsoOutStream.writeFloat(minorAxisSize)
            dsoOutStream.writeInt(orientationAngle)
            dsoOutStream.writeFloat(z)
            dsoOutStream.writeFloat(zErr)
            dsoOutStream.writeFloat(plx)
            dsoOutStream.writeFloat(plxErr)
            dsoOutStream.writeFloat(dist)
            dsoOutStream.writeFloat(distErr)
            dsoOutStream.writeInt(NGC)
            dsoOutStream.writeInt(IC)
            dsoOutStream.writeInt(M)
            dsoOutStream.writeInt(C)
            dsoOutStream.writeInt(B)
            dsoOutStream.writeInt(Sh2)
            dsoOutStream.writeInt(VdB)
            dsoOutStream.writeInt(RCW)
            dsoOutStream.writeInt(LDN)
            dsoOutStream.writeInt(LBN)
            dsoOutStream.writeInt(Cr)
            dsoOutStream.writeInt(Mel)
            dsoOutStream.writeInt(PGC)
            dsoOutStream.writeInt(UGC)
            dsoOutStream.writeQString(Ced)
            dsoOutStream.writeInt(Arp)
            dsoOutStream.writeInt(VV)
            dsoOutStream.writeQString(PK)
            dsoOutStream.writeQString(PNG)
            dsoOutStream.writeQString(SNRG)
            dsoOutStream.writeQString(ACO)
            dsoOutStream.writeQString(HCG)
            dsoOutStream.writeQString(ESO)
            dsoOutStream.writeQString(VdBH)
            dsoOutStream.writeInt(DWB)
            dsoOutStream.writeInt(Tr)
            dsoOutStream.writeInt(St)
            dsoOutStream.writeInt(Ru)
            dsoOutStream.writeInt(VdBHa)
        except:
            print(record)
            continue
    dsoIn.close()
    dsoOut.flush()
    dsoOut.close()
    return

if __name__ == '__main__':
    ConverttxtToPack("0.20.2/catalog.txt", "catalog.pack")

