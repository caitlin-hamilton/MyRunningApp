function normalizeDistance(distance){
    distance = distance/1000
    return distance.toFixed(2)
}

function removeTimeZone(date){
    date = date.split("T")[0]
    return date
}
function convertNumToTime(number) {
    var myDate = new Date(number *1000);
    var gmtDate = new Date(myDate.toGMTString())
    return gmtDate.getUTCHours() + ":" + gmtDate.getUTCMinutes() +":" + gmtDate.getUTCSeconds()
}

function standardiseTime(number) {
    var myDate = new Date(number *1000);
    var gmtDate = new Date(myDate.toGMTString())
    var d = new Date(1970, 1, 1, gmtDate.getUTCHours(), gmtDate.getUTCMinutes(), gmtDate.getUTCSeconds(), 0)
    return d
}

export {normalizeDistance, removeTimeZone, convertNumToTime, standardiseTime}
