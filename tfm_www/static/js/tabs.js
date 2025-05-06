const closeDetailAndResults = function() {
    let tabJsonDetail = document.getElementById("idJsonData");
    let tabClassifierResults = document.getElementById("idClassifierResults");
    let tabSummarizerResults = document.getElementById("idSummarizerResults");
    
    let liClassify = document.getElementById("idLiClassify");
    let liSummarize = document.getElementById("idLiSummarize");

    liClassify.active = false;
    liSummarize.active = false;    
    tabJsonDetail.style="display: none";
    tabClassifierResults.style="display: none";
    tabSummarizerResults.style="display: none";    
}

const openJsonDetail = function() {
    closeDetailAndResults();
    
    let tabJsonDetail = document.getElementById("idJsonData");

    tabJsonDetail.style="display: block";
}

const openClassifierResults = function() {
    closeDetailAndResults();
    
    let tabClassifierResults = document.getElementById("idClassifierResults");
    let liClassify = document.getElementById("idLiClassify");

    liClassify.active = true;
    tabClassifierResults.style="display: block";
}

const openSummarizerResults = function() {
    closeDetailAndResults();
    
    let tabSummarizerResults = document.getElementById("idSummarizerResults");
    let liSummarize = document.getElementById("idLiSummarize");

    liSummarize.active = true;
    tabSummarizerResults.style="display: block";
}

const canvi = function(action) {
    let tabClassifier = document.getElementById("idClassifier");
    let tabCredits = document.getElementById("idCredits");
    let liClassifier = document.getElementById("idLiClassifier");
    let liCredits = document.getElementById("idLiCredits");

    if (action === 'classifier') {
        liClassifier.active = true;
        liCredits.active = false;
        tabClassifier.style="display: block";
        tabCredits.style="display:none";
    } else if (action === 'credits') {
        liClassifier.active = false;
        liCredits.active = true;
        tabClassifier.style="display:none";
        tabCredits.style="display:block";
    } else {
        liClassifier.active = false;
        liCredits.active = false;
        tabClassifier.style="display:none";
        tabCredits.style="display:none";
        showMessageBox('Error', "No es reconeix la pestanya seleccionada");
    }
}
