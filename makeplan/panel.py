
'''
根据设备计算深空天体可见程度并且从高到低排序
并且根据所在经纬度和时间筛选出可观测目标
支持Messier、NGC，可拓展性高
适合用来批量制定观测计划

注："双筒适合"目标为5~50°高度角的目标
'''
# 更改以下参数适配

# 经度
Mylong = 110.34
# 纬度
Mylat = 21.28

# 观测时间序列：注意！必须是北京时间(UTC+8)！
vistimes = [
    "2020-1-26 20:00:00",
    "2020-1-27 00:00:00",
    "2020-1-27 04:00:00",
    "2020-1-27 05:30:00"
]

# 地平线以上遮挡物高度角(使得物体不可见) 单位° ,可为0
heightLimit = 2

# 设备情况
# 口径 mm
diamet=80
# 焦距 mm
focal=400
# 目镜焦距 mm
eyefo=20
# 天空表面亮度 mag/sec^2
skysur=21.5
# 大气透明度 (0~1)
AOD=0.3

# 观测表格
nowtable = "Messier" # "Messier" 或者 "NGC"



# ================================== 以下是程序，谨慎改动 ===========================

import csv
def csvload(src,dem=','):
    dic = {}
    f = open(src, "r", encoding="utf-8")
    reader = csv.reader(f,delimiter=dem)
    return list(reader)
def cal_toolvis(mag, longax, shortax, diamet=80, focal=400, eyefo=20, skysur=20.5, AOD=0.3):
    mag1 = mag 
    longax1 = longax 
    shortax1 = shortax 
    diamet1 = diamet 
    focal1 = focal 
    eyefo1 = eyefo 
    skysur1 = skysur 
    AOD = AOD 
    objsrfb = mag1 + 2.5 * math.log(2827 * longax1 * shortax1) / math.log \
        (10)  
    if (AOD > 0 and AOD < 1):
        objsrfb = objsrfb - 2.5 * math.log(1 - AOD) / math.log(10)
    magnif = focal1 / eyefo1  
    appsize = math.sqrt(longax1 * shortax1) * magnif  
    exitpur = diamet1 / magnif  
    dimmi = 5 * math.log(7 / exitpur) / math.log(10)  
    objrslbr = objsrfb + dimmi  
    skyrslbr = skysur1 + dimmi  
    b0 = math.sqrt(7.5 * math.log(appsize / 15) / math.log(10) + 0.45) + 19.3
    sss = 0.42 + 0.155 * math.log(appsize / 15) / math.log(10)
    E1 = 0.35
    threshold = sss * (skyrslbr - 19) + b0 - E1 * (math.pow((skyrslbr / 24), 5))  
    contrast = threshold - objrslbr  
    return contrast
import math
import datetime
def DMS2Deg(dec):
    dec = str(dec)
    if dec.startswith("-"):
        dec = dec.replace("-","")
        delim = dec.split(":")
        return -1*(int(delim[0])+int(delim[1])/60 + float(delim[2])/3600)
    if dec.startswith("+"):
        dec = dec.replace("+","")
    delim = dec.split(":")
    return int(delim[0])+int(delim[1])/60 + float(delim[2])/3600
def Deg2DMS(deg,weishu = 2):
    D = int(deg)
    m = (deg - D)*60
    M = int(m)
    s = m - M
    S = int(s)
    return str(D)+":"+str(M)+":"+str(S)
def subdate(date1,date2):
    date1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
    date2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
    delta = date2 - date1
    return delta.days
def subtime(date1, date2):
    date1 = datetime.datetime.strptime(date1, "%H:%M:%S")
    date2 = datetime.datetime.strptime(date2, "%H:%M:%S")
    delta = datetime.datetime.strptime(r'1', "%d")
    if date2 <= date1:
        return _time(str2time(str(date1 - date2)))
    else:
        restr = (date1 - date2 + delta)
        return _time(restr)
def Angle2Time(angle):
    delta = datetime.timedelta(seconds=angle/360*24*60*60)
    return delta
def Radian2Time(angle):
    delta = datetime.timedelta(seconds=angle*24*60*60)
    return _time(str2time(str(delta)))
def Time2Angle(time1):
    time1 = datetime.datetime.strptime(time1, "%H:%M:%S")
    hours = int(time1.hour) + int(time1.minute)/60+ float(time1.second)/3600
    return hours/24*360
def Time2Radian(time1):
    time1 = datetime.datetime.strptime(time1, "%H:%M:%S")
    hours = int(time1.hour) + int(time1.minute)/60+ float(time1.second)/3600
    return hours/24
def _time(restr):
    return str(restr.hour) + ':' + str(restr.minute) + ':' + str(restr.second)
def str2time(time1):
    time1 = time1.split('.',1)[0]
    return datetime.datetime.strptime(time1, "%H:%M:%S")
def timeAdd(date1,date2):
    date1 = datetime.datetime.strptime(date1, "%H:%M:%S")
    date2 = datetime.datetime.strptime(date2, "%H:%M:%S")
    restr = date1 + datetime.timedelta(hours=date2.hour)
    restr = restr + datetime.timedelta(minutes=date2.minute)
    restr = restr + datetime.timedelta(seconds=date2.second)
    return _time(restr)
def timeMulti(date1,mul):
    date1 = datetime.datetime.strptime(date1, "%H:%M:%S")
    delta = datetime.timedelta(seconds=(date1.hour* 60 * 60+date1.minute*60+date1.second)*mul)
    return _time(str2time(str(delta)))
def timeAddList(base,argv):
    if len(argv) > 1:
        return timeAddList(timeAdd(base,argv[0]),list(argv[1:]))
    else:
        return timeAdd(base,argv[0])
def subtimeList(base,argv):
    if len(argv) > 1:
        return subtimeList(subtime(base,argv[0]),list(argv[1:]))
    else:
        return subtime(base,argv[0])

def cal_above(today,CST,RA,longtitude=Mylong,latitude=Mylat):
    theYear = today.split('-',1)[0]
    deltaDays = subdate(theYear+'-1-1',today)
    finalHour = subtimeList(timeAddList('6:40:00',[timeMulti('0:03:56',deltaDays+1),CST]),[Radian2Time((120-longtitude)/15/24), Radian2Time(RA/15/24)])
    return finalHour
def cal_posvis(date, time, starRA, starDec, longtitude=Mylong, latitude=Mylat, heightlimit = 0, DECisTIME = False,debug=False,RAstr=False,Decstr=False):
    if RAstr:
        starRA = DMS2Deg(starRA)/24*360
    else:
        starRA = float(starRA)
    if Decstr:
        starDec = DMS2Deg(starDec)/24*360
    else:
        starDec = float(starDec)
    timeArc = cal_above(date,time,starRA,longtitude,latitude)
    if debug:
        print("timeArc",timeArc)
    Ang = Time2Angle(timeArc)
    latitudeArc = latitude / 360 * 2 * math.pi
    if DECisTIME == True:
        starDecold = DMS2Deg(starDec)
        starDec = starDecold / 360 * 2 * math.pi
    else:
        starDec = float(starDec) / 360 * 2 * math.pi
    HeightAngleArc = math.asin(math.sin(latitudeArc) * math.sin(starDec) + math.cos(latitudeArc) * math.cos(starDec) * math.cos(Time2Radian(timeArc)*2*math.pi))
    if debug:
        print("HeightAngleArc",Deg2DMS(HeightAngleArc/2/math.pi*360))
    deHeight = round(HeightAngleArc/2/math.pi*360,2)
    if Ang > 270 or Ang < 90:
        if deHeight > heightlimit:
            return [True,True,timeArc,deHeight]
        return [True,False,timeArc,deHeight]
    else:
        return [False,False,timeArc,deHeight]

if __name__ == '__main__':
    fp = open("观测计划.txt","w",encoding="utf-8")
    RAstr = False
    Decstr = False
    if nowtable == "NGC":
        RAstr = True
        Decstr = True
    lin = csvload(""+nowtable+".csv")
    mdic = {}
    for li in lin:
        try:
            vis = round(cal_toolvis(float(li[1]), float(li[2]), float(li[3]), diamet=diamet, focal=focal, eyefo=eyefo, skysur=skysur, AOD=AOD), 2)
        except Exception:
            continue
        if vis > 0:
            mdic[li[0]] = vis
    vistable = sorted(mdic.items(), key=lambda item: item[1], reverse=True)
    poss = csvload(""+nowtable+"_RADEC.csv")
    for vistime in vistimes:
        print(vistime.split(" ")[0], vistime.split(" ")[1],"\n")
        fp.write(vistime.split(" ")[0]+"\t"+ vistime.split(" ")[1]+"\n\n")

        print("目标\t可见度\t时角\t高度角\n")
        fp.write("目标\t可见度\t时角\t高度角\n")
        for item in vistable:
            nitem = int(item[0].replace("NGC","").replace("M",""))
            posvis = cal_posvis(vistime.split(" ")[0], vistime.split(" ")[1], poss[nitem - 1][1], poss[nitem - 1][2],RAstr=RAstr,Decstr=Decstr)
            if float(posvis[3]) < heightLimit:
                continue
            easyfind = ""
            if float(posvis[3]) <= 50 and float(posvis[3]) >= 5 and float(item[1]) >= 1:
                easyfind = "双筒适合"
            if posvis[:2] == [True, True]:
                print(item[0], item[1], posvis[2], posvis[3], easyfind)
                fp.write(item[0]+"\t"+ str(item[1])+"\t"+ str(posvis[2])+"\t"+ str(posvis[3])+"\t"+ easyfind+"\n")
        print("----------------------")
        fp.write("----------------------"+"\n")
    fp.close()