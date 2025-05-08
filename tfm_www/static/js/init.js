const labels=[
    "3559","1005","4381","4385","893","3173","5581","2560","4692","946",
    "3611","1744","5573","3483","5231","2687","1565","4316","5034","2735",
    "889","191","2965","4687","616","5228","2897","2871","1277","2783",
    "3870","2488","2733","1264","4314","2681","1182","598","2737","5751",
    "5969","4663","1602","4320","2121","2718","2850","4689","1442","4743"];

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
        tdFileName.addEventListener('click', buildFileListener(idTotal, filtered.filteredFullPath));
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

    setViewValues(idTotal, jsonResponse, fullPath);
}

const setViewValues = function(idTotal, jsonResponse, fullPath) {
    document.getElementById("idDataFrame").innerHTML = idTotal;
    document.getElementById("idViewCelexId").innerHTML = jsonResponse.celex_id;
    document.getElementById("idViewUri").innerHTML = jsonResponse.uri;
    document.getElementById("idViewType").innerHTML = jsonResponse.type;
    document.getElementById("idViewConcepts").innerHTML = filter50Concepts(jsonResponse.concepts);
    document.getElementById("idViewTitle").innerHTML = jsonResponse.title;
    document.getElementById("idViewHeader").innerHTML = jsonResponse.header;
    document.getElementById("idViewRecitals").innerHTML = jsonResponse.recitals;
    document.getElementById("idViewMainBody").innerHTML = jsonResponse.main_body;
    document.getElementById("idViewAttachments").innerHTML = jsonResponse.attachments;
    document.getElementById("idJsonData").style="display:block";
    document.getElementById("idFullPath").value = fullPath;
    console.log("idFullPath: " + fullPath);
}

const filter50Concepts = function(concepts) {
    let retValue = [];
    
    for(let i = 0;  i < concepts.length; i++) {
	let concept = concepts[i];
	if (labels.includes(concept)) {
            retValue.push(concept);
	}
    }

    return retValue;
}

const filterName = function(fullPath) {
    let tokens = fullPath.split('/');
    let fileName =  tokens[4];
    fileName = fileName.substring(0, fileName.length - 4);
    let filteredFullPath = 
        '/data/' + tokens[1]  +
        '/' + tokens[2] +
        '/' + tokens[3] +
        '/' + fileName;

    return { fileName, filteredFullPath };
}
