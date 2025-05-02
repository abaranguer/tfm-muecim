const initTable = async function() {
    const response = await fetch('/getPage/1',{
        method: 'GET',
        headers: {
            'Accept': 'application/json',
        },
    })
    const jsonObjs = await response.json();

    buildTable(jsonObjs)
    setPageNum(1);
}      

const setPageNum = function(num) {
    document.getElementById('idNumPage').innerHTML = "" + num;
}

const buildTable = function(jsonObjs) {
    let fileTable = document.getElementById('idFileTable');
    fileTable.innerHTML = '';

    let id = 1;
    for(let jsonObj in jsonObjs['fileName']) {
        let trObj = document.createElement('tr');
        let tdId = document.createElement('td');
        tdId.innerHTML=id;
        id++;
        let tdFileName = document.createElement('td');
        let fullPath = jsonObjs['fileName'][jsonObj];
        let filtered = filterName(fullPath);
        tdFileName.innerHTML = filtered.fileName;
        tdFileName.addEventListener('click', buildFileListener(filtered.filteredFullpath));
        trObj.appendChild(tdId);
        trObj.appendChild(tdFileName);
        fileTable.appendChild(trObj);
    }
}

const buildFileListener = function(fullPath) {
    return getFullPath = function(obj) {
        loadJsonData(fullPath);
    }
} 

const loadJsonData = async function(fullPath) {
    const param = {jsonPath: fullPath};
    const response = await fetch('/getJsonData',{
        method: 'POST',
        body: JSON.stringify( param )
    });
    
    const jsonResponse = await response.json();

    setViewValues(jsonResponse);
}

const setViewValues = function(jsonResponse) {
    document.getElementById("idViewCelexId").innerHTML = jsonResponse.celex_id;
    document.getElementById("idViewUri").innerHTML = jsonResponse.uri;
    document.getElementById("idViewType").innerHTML = jsonResponse.type;
    document.getElementById("idViewConcepts").innerHTML = jsonResponse.concepts;
    document.getElementById("idViewTitle").innerHTML = jsonResponse.title;
    document.getElementById("idViewHeader").innerHTML = jsonResponse.header;
    document.getElementById("idViewRecitals").innerHTML = jsonResponse.recitals;
    document.getElementById("idViewMainBody").innerHTML = jsonResponse.main_body;
    document.getElementById("idViewAttachments").innerHTML = jsonResponse.attachments;
}

const filterName = function(fullPath) {
    let tokens = fullPath.split('/');
    let fileName =  tokens[4];
    fileName = fileName.substring(0, fileName.length - 4);
    let filteredFullpath = 
        '/data/' + tokens[1]  +
        '/' + tokens[2] +
        '/' + tokens[3] +
        '/' + fileName;

    return { fileName, filteredFullpath };
}