singsilasbjcal(mag1, longax1, shortax1, diamet1, focal1, eyefo1, skysur1, AOD){
    mag1 = parseFloat(mag1)
    longax1 = parseFloat(longax1)
    shortax1 = parseFloat(shortax1)
    diamet1 = parseFloat(diamet1)
    focal1 = parseFloat(focal1)
    eyefo1 = parseFloat(eyefo1)
    skysur1 = parseFloat(skysur1)
    AOD = parseFloat(AOD)
    var objsrfb = mag1 + 2.5 * Math.log(2827 * longax1 * shortax1) / Math.log(10)

    if (AOD > 0 && AOD < 1) {
      objsrfb = objsrfb - 2.5 * Math.log(1 - AOD) / Math.log(10)
    }


    var magnif = focal1 / eyefo1

    var appsize = Math.sqrt(longax1 * shortax1) * magnif
    
    var exitpur = diamet1 / magnif

    var dimmi = 5 * Math.log(7 / exitpur) / Math.log(10)

    var objrslbr = objsrfb + dimmi

    var skyrslbr = skysur1 + dimmi

    var b0 = Math.sqrt(7.5 * Math.log(appsize / 15) / Math.log(10) + 0.45) + 19.3

    var sss = 0.42 + 0.155 * Math.log(appsize / 15) / Math.log(10)

    var E1 = 0.35

    var threshold = sss * (skyrslbr - 19) + b0 - E1 * (Math.pow((skyrslbr / 24), 5))

    var contrast = threshold - objrslbr

    return contrast
  }