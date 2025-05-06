const classify = async function() {
    console.log('classify');
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

    const jsonObjs = await response.json();
    console.log('response: ' + jsonObjs);

    loadClassifierResultsPane(jsonObjs);
    openClassifierResults();
}

const loadClassifierResultsPane = function(jsonObjs) {
    let groundTruth = document.getElementById('idViewConcepts').innerHTML;
    document.getElementById('idGroundTruthClassifier').innerHTML =  groundTruth;
    document.getElementById('idResultClassifierDistilBert').innerHTML = jsonObjs.distilBert;
    document.getElementById('idResultClassifierBert').innerHTML = jsonObjs.bert;
}
