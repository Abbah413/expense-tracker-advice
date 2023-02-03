document.addEventListener('click', e => {
    // gets the element that triggered the event listener
    let target = e.target;
    let parent = target.parentElement
    if (parent.type === "button"){
        // if the element is the remove button
        if (parent.classList.contains("remove_button")) {
            // stores the category of the clicked row
            let category = parent.nextElementSibling.value
            let data = {action : 'remove', category : category};
            send_data(data);
            remove_element(parent);
        }
    }
});

function send_data(data){
    const index_url = "/"
    // send the category to the server to be removed from category table
    fetch(index_url, {
        headers : {'Content-Type' : 'application/json'},
        method : 'POST',
        body : JSON.stringify(data)
    })
    .then(response => {
        // if there is no response back throws  an error
        if(!response.ok) {
            throw new Error('Network response not ok')
        }
    })
    .catch(function(error) {
        console.log(error);
    });
}

// finds the parent tr element then remove the row
function remove_element(parent){
    var row = parent.parentNode.parentNode.parentNode;
    row.parentNode.removeChild(row);
}