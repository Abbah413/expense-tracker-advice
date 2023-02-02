document.addEventListener("change", (e) => {
    let input = e.target;
    DataTransfer = {action : 'add', category : input.value};
    if (input.type === "text"){
        const index_url = "/"
        fetch(index_url, {
            headers : {'Content-Type' : 'application/json'},
            method : 'POST',
            body : JSON.stringify(data)
        })
        .then(response => {
            if(!response.ok) {
                throw new Error('Something went wrong');
            }
        })

        .catch(function(error) {
            console.log(error);
        })
    }
});