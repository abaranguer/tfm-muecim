const summarize = async function() {
    console.log('summarize');

    let fullPath = document.getElementById('idFullPath').value;
    console.log("summarize file: " + fullPath);

    const param = {"jsonPath": fullPath};
    let endPoint = "/summarizer";
    const response = await fetch(
	endPoint,
	{
            method: 'POST',
	    body: JSON.stringify( param )
        }
    )
    
    const jsonObjs = await response.json();
    console.log('response: ' + jsonObjs);

    loadSummarizerResultsPane(jsonObjs);
    openSummarizerResults();
}

const loadSummarizerResultsPane = function(jsonObjs) {
    openSummarizerResults();
    
    let mainBody = document.getElementById('idViewMainBody').innerHTML;

    document.getElementById('idSummarizerMainBody').innerHTML = mainBody;
    document.getElementById('idSummaryPegasusXsum').innerHTML = jsonObjs.pegasus.pegasus;
    document.getElementById('idSummaryBart').innerHTML = jsonObjs.bart.bart;
    document.getElementById('idSummaryGpt2').innerHTML = jsonObjs.gpt2.gpt2;    
}

const buildInnerHtmlSum = function( jsonArray ) {
    let retValue = "";

    let numElems = jsonArray.length;
    for(let i = 0; i < numElems; i++) {
	retValue += (jsonArray[i] + "<br />")
    }

    return retValue;
}
