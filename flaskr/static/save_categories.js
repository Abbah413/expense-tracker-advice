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

document.addEventListener("change", (e) => {
    // budget input
    let input = e.target;
    if (input.type === "number"){
        let td = input.parentNode;
        console.log(td);
        let cat_td = td.previousSibling.previousSibling;
        console.log(cat_td);
        let div = cat_td.childNodes[1];
        console.log(div);
        let category = div.childNodes[3];
        console.log(category)
        let data = {action : 'budget', category : category.value, budget : input.value};
        console.log(data);
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
            console.log(data);
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