document.addEventListener("change", (e) => {
    var input = e.target;
    data = {category : input.value};
    if (input.type === "text"){
        console.log(data)
        const index_url = "/"
        fetch(index_url, {
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