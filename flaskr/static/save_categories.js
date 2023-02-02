document.addEventListener("change", (e) => {
    let input = e.target;
    data = {action : 'add', category : input.value};
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
            return response.json();
        })
        .then(data => {
            append_table(input, data);
        })
        .catch(function(error) {
            console.log(error);
        })
    }
});

function append_table(input, data){
    input.value = data['category'];
    input.readOnly = true;
    var td = input.parentNode.parentNode;
    var amount = td.nextSibling.nextSibling;
    amount.innerHTML = data['amount'];
}