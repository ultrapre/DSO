from silas import *

piority = {
"M number": "M",
"C number": "C",
"NGC number": "NGC",
"IC number": "IC",
"B number": "B",
"Sh2 number": "Sh 2-",
"VdB number": "vdB",
"RCW number": "RCW",
"LDN number": "LDN",
"LBN number": "LBN",
"Mel number": "Mel",
"Cr number": "Cr",
"PGC number": "PGC",
"UGC number": "UGC",
"Ced number": "Ced",
"Arp number": "Arp",
"VV number": "VV",
"PK identificator": "PK",
"PN G identificator": "PN G",
"SNR G identificator": "SNR G",
"ACO number": "Abell",
"HCG identificator": "HCG",
"ESO identificator": "ESO",
"VdBH identificator": "vdBH",
"DWB number": "DWB",
"Tr number": "Tr",
"St number": "St",
"Ru number": "Ru",
"VdB-Ha number": "vdB-Ha",
}

vpiority = {
"^Abell\s*(\d+.*)$": "ACO number",
"^Arp\s*(\d+.*)$": "Arp number",
"^B\s*(\d+.*)$": "B number",
"^C\s*(\d+.*)$": "C number",
"^Ced\s*(\d+.*)$": "Ced number",
"^Cr\s*(\d+.*)$": "Cr number",
"^DWB\s*(\d+.*)$": "DWB number",
"^ESO\s*(\d+.*)$": "ESO identificator",
"^HCG\s*(\d+.*)$": "HCG identificator",
"^IC\s*(\d+.*)$": "IC number",
"^LBN\s*(\d+.*)$": "LBN number",
"^LDN\s*(\d+.*)$": "LDN number",
"^M\s*(\d+.*)$": "M number",
"^Mel\s*(\d+.*)$": "Mel number",
"^NGC\s*(\d+.*)$": "NGC number",
"^PGC\s*(\d+.*)$": "PGC number",
"^PK\s*(\d+.*)$": "PK identificator",
"^PN G\s*(\d+.*)$": "PN G identificator",
"^RCW\s*(\d+.*)$": "RCW number",
"^Ru\s*(\d+.*)$": "Ru number",
"^SNR G\s*(\d+.*)$": "SNR G identificator",
"^Sh 2-\s*(\d+.*)$": "Sh2 number",
"^St\s*(\d+.*)$": "St number",
"^Tr\s*(\d+.*)$": "Tr number",
"^UGC[A]*\s*(\d+.*)$": "UGC number",
"^VV\s*(\d+.*)$": "VV number",
"^vdB-Ha\s*(\d+.*)$": "VdB number",
"^vdBH\s*(\d+.*)$": "VdB-Ha number",
"^vdB\s*(\d+.*)$": "VdBH identificator"
}
# for it in piority:
#     vpiority[piority[it]] = it

piorities2 = {
"M number": "0",
"C number": "0",
"NGC number": "0",
"IC number": "0",
"B number": "0",
"Sh2 number": "0",
"VdB number": "0",
"RCW number": "0",
"LDN number": "0",
"LBN number": "0",
"Mel number": "0",
"Cr number": "0",
"PGC number": "0",
"UGC number": "0",
"Ced number": "",
"Arp number": "0",
"VV number": "0",
"PK identificator": "",
"PN G identificator": "",
"SNR G identificator": "",
"ACO number": "",
"HCG identificator": "",
"ESO identificator": "",
"VdBH identificator": "",
"DWB number": "0",
"Tr number": "0",
"St number": "0",
"Ru number": "0",
"VdB-Ha number": "0",
}

plis = [
"M\s*\d+",
"C\s*\d+",
"NGC\s*\d+",
"IC\s*\d+",
"B\s*\d+",
"Sh 2-\s*\d+",
"vdB\s*\d+",
"RCW\s*\d+",
"LDN\s*\d+",
"LBN\s*\d+",
"Mel\s*\d+",
"Cr\s*\d+",
"PGC\s*\d+",
"UGC\s*\d+",
"UGCA\s*\d+",
"Ced\s*\d+",
"Arp\s*\d+",
"VV\s*\d+",
"PK\s*\d+",
"PN G\s*\d+",
"SNR G\s*\d+",
"Abell\s*\d+",
"HCG\s*\d+",
"ESO\s*\d+",
"vdBH\s*\d+",
"DWB\s*\d+",
"Tr\s*\d+",
"St\s*\d+",
"Ru\s*\d+",
"vdB-Ha\s*\d+"
]

pxlis = []
for it in piority:
    pxlis.append(piority[it])

# for it in plis:
#     print(it)

def findPrex(dso):
    for it in plis:
        # if dso.startswith(it):
        if re.match(it,dso):
            return True
    return False

PK = jsonload("E:/Astro/data/数据源/Stellarium/V0.4/PK.json")
def solvedso(dso):
    for it in pxlis:
        if dso.startswith(it):
            dso = dso.replace(it + ' ', it)
            if dso in PK:
                return PK[dso]
            return dso
    return dso


NI2019 = jsonload("E:/Astro/data/数据源/Stellarium/v0.4/NI2019.json")

PGCsrc = "E:/Astro/data/数据源/Stellarium/V0.4/PGC.json"
PGC = {}
for line in readdiralllines(PGCsrc):
    if line.split('\t')[1] in NI2019:
        if NI2019[line.split('\t')[1]]['TYPE'] == 'Dup':
            # print(line)
            continue
        PGC[line.split('\t')[0]] = line.split('\t')[1]





src = "E:/Astro/data/数据源/Stellarium/V0.4/OTN.txt"
OTNdic = {}
for line in readdiralllines(src):
    if line.split('\t')[1] in NI2019:
        if NI2019[line.split('\t')[1]]['TYPE'] == 'Dup':
            # print(line)
            continue
        OTNdic[line.split('\t')[0]] = line.split('\t')[1]

# print(OTNdic['ESO549-12'])

MPC = readdiralllines('E:/Astro/data/数据源/Stellarium/V0.4/M+C.txt')

NTOdic = {}
for it in OTNdic:
    if OTNdic[it] not in NTOdic:
        NTOdic[OTNdic[it]] = []
    NTOdic[OTNdic[it]].append(it)

for it in PGC:
    if PGC[it] not in NTOdic:
        NTOdic[PGC[it]] = []
    NTOdic[PGC[it]].append(it)


def checkID2():
    maps = jsonload("E:/Astro/data/数据源/Stellarium/v0.4/Source/Map.json")
    stell = jsonload("E:/Astro/data/数据源/Stellarium/v0.4/Source/Stellarium.json")
    # OTNdic = jsonload(src)
    Olis = list(it.upper() for it in maps)
    Olis += list(it.upper() for it in stell)
    msum = 0
    ssum = []
    for line in readdiralllines(src):
        if findPrex(line):
            line = solvedso(line)
            # if line not in maps and line not in stell:
            if line.upper() not in Olis:
                # print(line)
                pass
            else:
                msum += 1
                ssum.append(line)
    # print(msum)
    # for it in ssum:
    #     print(it)


def vfp(it):
    for line in vpiority:
        if re.match(line,it):
            op = re.match(line,it).group(1)
            return [vpiority[line],op]
    return False


def PGCintoNGC():
    # lines = csvload("E:/Astro/data/数据源/Stellarium/V0.4/复盘前数据.csv")
    lines = csvload("E:/Astro/data/数据源/Stellarium/V0.4/catalog.txt")
    line0 = lines[0]
    lines = lines[1:]
    solvedlist = readdiralllines("E:/Astro/data/数据源/Stellarium/V0.4/M+C.txt")
    def juedeInside(line):
        for i in range(20,47):
            if line[i] in ['','0',0]:
                continue
            # if piority[line0[i]]=='ESO':
            #     print(piority[line0[i]]+line[i])
            if piority[line0[i]]+line[i] in OTNdic:
                # print(piority[line0[i]]+line[i])
                return OTNdic[piority[line0[i]]+line[i]]
        return ''

    '''
    S已有
    '''
    for i in range(0,len(lines)):
        line = lines[i]
        pgcnum = line[30]
        pgcobj = 'PGC'+str(pgcnum)
        pgcobj = pgcobj.strip()
        '''PGC路标'''
        if pgcobj in PGC:
            solvedlist.append(PGC[pgcobj])
            if PGC[pgcobj] in NI2019:
                if NI2019[PGC[pgcobj]]['TYPE'] == 'Dup':
                    continue
            if 'NGC' in PGC[pgcobj]:
                if lines[i][17] != '' and str(lines[i][17]) != '0':
                    continue
                lines[i][17] = PGC[pgcobj].replace('NGC','')
                # print(PGC[pgcobj],pgcobj)
            if 'IC' in PGC[pgcobj]:
                if lines[i][19] != '' and str(lines[i][19]) != '0':
                    continue
                lines[i][19] = PGC[pgcobj].replace('IC','')
                # print(PGC[pgcobj],pgcobj)
        else:
            '''
                    PGC不行，用其他的
                    '''
            fobj = juedeInside(line)
            if fobj != '':
                solvedlist.append(fobj)
                if fobj.startswith('NGC'):
                    if lines[i][17] != '' and str(lines[i][17]) != '0':
                        continue
                    lines[i][17] = fobj.replace('NGC', '')
                    # print(fobj)
                if fobj.startswith('IC'):
                    if lines[i][19] != '' and str(lines[i][19]) != '0':
                        continue
                    lines[i][19] = fobj.replace('IC', '')
                    # print(fobj)

    '''
    S未有
    '''
    for it in NTOdic:
        if it in solvedlist:
            continue
        # if it in MPC:
        #     continue
        solvedlist.append(it)
        if it in NI2019:
            if NI2019[it]['TYPE'] == 'Dup':
                continue
        newline = list('' for i in range(0,47))
        if it.startswith('NGC'):
            if newline[17] != '' and str(newline[17]) != '0':
                continue
            newline[17] = it.replace('NGC', '')
            # print(it)
        if it.startswith('IC'):
            if newline[19] != '' and str(newline[19]) != '0':
                continue
            newline[19] = it.replace('IC', '')
            # print(it)
        for itx in NTOdic[it]:
            cccf = vfp(itx)
            if cccf!=False:
                newline[line0.index(cccf[0])] = cccf[1]
                # print(it,itx)
        lines.append(newline)
    for it in NI2019:
        if NI2019[it]['TYPE'] == 'Dup':
            continue
        if it not in solvedlist:
            newline = list('' for i in range(0, 47))
            if 'NGC' in it:
                newline[17] = it.replace('NGC', '')
            elif 'IC' in it:
                newline[19] = it.replace('IC', '')
            # print(it)
            lines.append(newline)

    # csvdump([line0] + lines, "E:/Astro/data/数据源/Stellarium/V0.4/复盘后数据.csv")
    csvdump([line0] + lines, "E:/Astro/data/数据源/Stellarium/V0.4/catalog.new.txt")
    print(len(solvedlist))


PGCintoNGC()

# print(re.match('Ced.*','CED16'))

def csvTojson():
    src = "E:/Astro/data/数据源/Stellarium/V0.4/NI2019P.csv"
    lines = csvload(src)
    line0 = lines[0]
    lines = lines[1:]
    dicx = {}
    for line in lines:
        dicx[line[0]] = {}
        for i in range(1,17):
            dicx[line[0]][line0[i]] = line[i]
    jsondump(dicx,"E:/Astro/data/数据源/Stellarium/V0.4/NI2019P.json")

# csvTojson()

# # NISG = jsonload("E:/Astro/data/DeepSkyCatalogs/Format/NGCIC/Standard/NI-SG.json")
# src = "E:/Astro/data/数据源/Stellarium/V0.4/Unbound.txt"
# src1 = "E:/Astro/data/数据源/Stellarium/V0.4/CseMan.txt"
# lines = readdiralllines(src)
# for line in readdiralllines(src1):
#     if re.match('(IC\d+)',line):
#         op=re.match('(IC\d+)',line).group(1)
#         if op in lines:
#             print(op+'\t'+line)
#     elif re.match('(NGC\d+)',line):
#         op=re.match('(NGC\d+)',line).group(1)
#         if op in lines:
#             print(op+'\t'+line)
#     # else:
#     #     print(line)


# for src in dirlist("E:/Astro/NGCIC档案(无图版)by斌華.epub/Astro/ngcic/text/atlas",'.htm'):
#     lines = readdiralllines(src)
#     for line in lines:
#         if line.startswith('<big class="calibre16"><b class="calibre19">'):
#             line = line.replace('<big class="calibre16"><b class="calibre19">', '')
#             # print(line)
#             gps = re.match('^(.*?)<', line)
#             print(gps.group(1))
