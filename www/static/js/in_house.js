var textset1 = "NO";
var textset2 = "NO";

function text_set(text, div) {
    if (textset1 === "NO") {
        if (div === "background_upper2") {
            document.getElementById(div).innerHTML = "<h1><svg style='z-index:995;' viewBox='-5 35 1920 540'><path id='curve' d='M-1,552L593,218S801.83,92.672,970,99c136.56-5.078,363,123,363,123l588,333' /><text x='0'><textPath xlink:href='#curve' startOffset='50%' text-anchor='middle'>" + text + "</textPath></text></svg></H1>";
            textset1 = "YES"
        }

    }
    if (textset2 === "NO") {
        if (div === "background_lower2") {
            document.getElementById(div).innerHTML = "<h1><svg viewBox='0 530 1920 1080' style='z-index :999;'><path id='curve2' d='M2,528L605,868S823.65,996.141,962,984c134.73,12,368-120,368-120l587-332' /><text x='0'><textPath xlink:href='#curve2' startOffset='50%' text-anchor='middle'>" + text + "</textPath></text></svg></h1>";
            textset2 = "YES"
        }

    }
}

var textset1main = "NO";
var textset2main = "NO";

function text_set2(text, div) {
    if (textset1main === "NO") {
        if (div === "background_upper2main") {
            document.getElementById(div).innerHTML = "<h1><svg style='z-index:995;' viewBox='-5 35 1920 540'><path id='curve' d='M-1,552L593,218S801.83,92.672,970,99c136.56-5.078,363,123,363,123l588,333' /><text x='0'><textPath xlink:href='#curve' startOffset='50%' text-anchor='middle'>" + text + "</textPath></text></svg></H1>";
            textset1 = "YES"
        }

    }
    if (textset2main === "NO") {
        if (div === "background_lower2main") {
            document.getElementById(div).innerHTML = "<h1><svg viewBox='0 530 1920 1080' style='z-index :999;'><path id='curve2' d='M2,528L605,868S823.65,996.141,962,984c134.73,12,368-120,368-120l587-332' /><text x='0'><textPath xlink:href='#curve2' startOffset='50%' text-anchor='middle'>" + text + "</textPath></text></svg></h1>";
            textset2 = "YES"
        }

    }
}
//Blasts Cost 8