const classify = async function() {
    console.log('classify');
    document.getElementById('idLoader').style="display: block;";
    let idDF = document.getElementById('idDataFrame').innerHTML - 1;

    let endPoint = `/classifier/${idDF}`;
    const response = await fetch(
	endPoint,
	{
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        }
    )

    let jsonObjs = {};
    
    try {
        jsonObjs = await response.json();
	console.log('response: ' + jsonObjs);
    } catch(ex) {
	console.log("Exception in classifier: " + ex.message);	
	jsonObjs = {"distilBert": "error", "bert": "error", "gpt2": "error"}
    }

    loadClassifierResultsPane(jsonObjs);
    openClassifierResults();
}

const loadClassifierResultsPane = function(jsonObjs) {
    openClassifierResults();
    document.getElementById('idLoader').style="display: none;";
    
    let groundTruth = document.getElementById('idViewConcepts').innerHTML;

    document.getElementById('idGroundTruthClassifier').innerHTML =  groundTruth;
    document.getElementById('idResultClassifierDistilBert').innerHTML = buildInnerHtml(jsonObjs.distilBert);
    document.getElementById('idResultClassifierBert').innerHTML = buildInnerHtml(jsonObjs.bert);
    document.getElementById('idResultClassifierGpt2').innerHTML = buildInnerHtml(jsonObjs.gpt2);    
}

const buildInnerHtml = function( jsonArray ) {
    let retValue = "";

    let numElems = jsonArray.length;
    for(let i = 0; i < numElems; i++) {
	retValue += (jsonArray[i] + "<br />")
    }

    return retValue;
}
