document.addEventListener("change", (e) => {
    var type = e.target;
    data = {transid : type.dataset.transid, category : type.value};
    if (data['transid']){
        console.log(data)
        const transactions_url = "/transactions"
        fetch(transactions_url, {
            headers : {
                'Content-Type' : 'application/json'
            },
            method : 'POST',
            body : JSON.stringify(data)
        })
        .then(function(response) {
            if(response.ok) {
                response.json()
                .then(function(response) {
                    console.log(response);
                });
            }
            else {
                throw Error('Something went wrong');
            }
        })
        .catch(function(error) {
            console.log(error);
        });
    }
});