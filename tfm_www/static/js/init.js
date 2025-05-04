const getPageNum = function() {
    let pageNum =  document.getElementById("idDestPage").value;
    if (pageNum > 1938) { pageNum = 1938; }
    if (pageNum < 1) {	pageNum = 1; }
    document.getElementById("idDestPage").value = pageNum;

    return pageNum;
}

const goPageNum = function() {
    let pageNum = getPageNum();
    goPage(pageNum);
}

const goPage = async function(pageNum) {
    let endPoint = `/getPage/${pageNum}`;
    const response = await fetch(
	endPoint,
	{
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        }
    )

    const jsonObjs = await response.json();

    buildTable(jsonObjs);
    setPageNum(pageNum);
}

const setPageNum = function(num) {
    document.getElementById('idNumPage').innerHTML = "" + num;
}

const buildTable = function(jsonObjs) {
    let fileTable = document.getElementById('idFileTable');
    let pageNum = getPageNum()
    fileTable.innerHTML = '';

    let id = 1;
    let pageIdBase = (pageNum - 1) * 15;
    for(let jsonObj in jsonObjs['fileName']) {
        let trObj = document.createElement('tr');
        let tdId = document.createElement('td');
        tdId.innerHTML='&nbsp;&nbsp;' + id + '&nbsp;&nbsp;';
	let tdIdTotal = document.createElement('td');
	let idTotal = pageIdBase + id;
	tdIdTotal.innerHTML = '&nbsp;&nbsp;' + idTotal + '&nbsp;&nbsp;';
	id++;
        let tdFileName = document.createElement('td');
        let fullPath = jsonObjs['fileName'][jsonObj];
        let filtered = filterName(fullPath);
        tdFileName.innerHTML = filtered.fileName;
        tdFileName.addEventListener('click', buildFileListener(idTotal, filtered.filteredFullpath));
        trObj.appendChild(tdId);
	trObj.appendChild(tdIdTotal);
        trObj.appendChild(tdFileName);
        fileTable.appendChild(trObj);
    }
}

const buildFileListener = function(idTotal, fullPath) {
    return getFullPath = function(obj) {
        loadJsonData(idTotal, fullPath);
    }
} 

const loadJsonData = async function(idTotal, fullPath) {
    const param = {jsonPath: fullPath};
    const response = await fetch('/getJsonData',{
        method: 'POST',
        body: JSON.stringify( param )
    });
    
    const jsonResponse = await response.json();

    setViewValues(idTotal, jsonResponse);
}

const setViewValues = function(idTotal, jsonResponse) {
    document.getElementById("idDataFrame").innerHTML = idTotal;
    document.getElementById("idViewCelexId").innerHTML = jsonResponse.celex_id;
    document.getElementById("idViewUri").innerHTML = jsonResponse.uri;
    document.getElementById("idViewType").innerHTML = jsonResponse.type;
    document.getElementById("idViewConcepts").innerHTML = jsonResponse.concepts;
    document.getElementById("idViewTitle").innerHTML = jsonResponse.title;
    document.getElementById("idViewHeader").innerHTML = jsonResponse.header;
    document.getElementById("idViewRecitals").innerHTML = jsonResponse.recitals;
    document.getElementById("idViewMainBody").innerHTML = jsonResponse.main_body;
    document.getElementById("idViewAttachments").innerHTML = jsonResponse.attachments;
    document.getElementById("idJsonData").style="display:block";
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
