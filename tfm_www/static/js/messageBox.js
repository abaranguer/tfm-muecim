var modalMessageBox = null;

const showMessageBox = function(title, message) {
    if ( modalMessageBox == null) {
        modalMessageBox = new bootstrap.Modal(document.getElementById('idMessageBox'), {})
    }
    let textField = document.getElementById('idMessageText');
    let textTitle = document.getElementById('idMessageTitle');
    textField.innerText = message;
    textTitle.innerText = title;

    modalMessageBox.show()
}

const closeMessageBox = function() {
    modalMessageBox.hide();
}
