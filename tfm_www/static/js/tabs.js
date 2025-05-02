const canvi = function(action) {
    let tabClassifier = document.getElementById("idClassifier");
    let tabCredits = document.getElementById("idCredits");
    let liClassifier = document.getElementById("idLiClassifier");
    let liCredits = document.getElementById("idLiCredits");

    if (action === 'classifier') {
        liClassifier.active = true;
        liCredits.active = false;
        tabClassifier.style="display:block";
        tabCredits.style="display:none";
        // showMessageBox('Acció', 'Mostra la pantalla de formulari');
    } else if (action === 'credits') {
        liClassifier.active = false;
        liCredits.active = true;
        tabClassifier.style="display:none";
        tabCredits.style="display:block";
        // showMessageBox('Acció', 'Mostra la pantalla de crèdits');
    } else {
        liClassifier.active = false;
        liCredits.active = false;
        tabClassifier.style="display:none";
        tabCredits.style="display:none";
        showMessageBox('Error', "No es reconeix la pestanya seleccionada");
    }
}



