var min = 6;
var max = 12;
var textset1 = "NO";
var textset2 = "NO";




function removehack1() {
    document.getElementById("hack2").style.display = "block";
    document.getElementById("arrowsh0").style.display = "block";
    var seconds_left = Math.floor(Math.random() * (max - min) + min);
    var interval = setInterval(function () {
        --seconds_left;
        if (timeDoubler == "yes") {
            --seconds_left
        }
        if (seconds_left <= 0) {
            document.getElementById("hack2button").style.display = "block";
            clearInterval(interval);
        }
    }, 1000);
}

function removehack2() {
    document.getElementById("arrowsh1").style.display = "block";
    document.getElementById("hack3").style.display = "block";
    var seconds_left = Math.floor(Math.random() * (max - min) + min);
    var interval = setInterval(function () {
        --seconds_left;
        if (timeDoubler == "yes") {
            --seconds_left
        }
        if (seconds_left <= 0) {
            document.getElementById("hack3button").style.display = "block";
            clearInterval(interval);
        }
    }, 1000);
}


function removehack3() {
    document.getElementById("arrowsh2").style.display = "block";
    document.getElementById("hack4").style.display = "block";

    var seconds_left = Math.floor(Math.random() * (max - min) + min);
    var interval = setInterval(function () {
        --seconds_left;
        if (timeDoubler == "yes") {
            --seconds_left
        }
        if (seconds_left <= 0) {
            document.getElementById("hack4button").style.display = "block";
            clearInterval(interval);
        }
    }, 1000);
}


function removehack4() {
    var hackremaudio = "/audioadd/" + room + "/", hack_remaudio = "unhack";

    $.ajax({
        type: 'POST',
        url: hackremaudio,
        data: {
            toplay: hack_remaudio
        }
    });

    var redirect = '/sRemove/';
    $.ajax({
        type: 'POST',
        url: redirect,
        data: {
            station: station
        }
    });
    var interval = setInterval(function () {
        document.getElementById("hack2button").style.display = "none";
        document.getElementById("hack3button").style.display = "none";
        document.getElementById("hack3").style.display = "none";
        document.getElementById("hack4button").style.display = "none";
        document.getElementById("hack4").style.display = "none";
        document.getElementById("hack").style.display = "none";
        document.getElementById("arrowsh0").style.display = "none";
        document.getElementById("arrowsh1").style.display = "none";
        document.getElementById("arrowsh2").style.display = "none";
        document.getElementById("hack2").style.display = "none";
        document.getElementById("main_loader").style.display = "block";
        clearInterval(interval);
    }, 1000);
}
