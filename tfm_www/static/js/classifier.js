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

    console.log('response: ' + jsonObjs)
}
