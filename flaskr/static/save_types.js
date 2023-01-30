document.addEventListener("change", (e) => {
    var type = e.target;
    data = {id : type.dataset.id, type : type.value};
    if (data['id']){
        console.log(data)
        const categories_url = "/categories"
        fetch(categories_url, {
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