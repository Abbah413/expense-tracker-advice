document.addEventListener("click", (e) => {
  let deleteButton = e.target;
  if (deleteButton.id == "modal-delete-button"){
    let data = {action : "delete"};
    const transactions_url = "/transactions";
    fetch(transactions_url, {
      headers : {
        "Content-Type" : "application/json"
      },
      method : "POST",
      body : JSON.stringify(data)
    })
    .then(function(response) {
      if(!response.ok) {
        throw Error("Something went wrong");
      }
      return response.json();
    })
    .then(data => {
        console.log(data);
        clearTable();
    })
    .catch(function(error) {
      console.log(error);
    })
  }
});

function clearTable(){
  let tbody = document.querySelector("tbody");
  while(tbody.hasChildNodes()) {
    tbody.removeChild(tbody.firstChild);
  }
}