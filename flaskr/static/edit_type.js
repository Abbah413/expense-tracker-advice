
document.addEventListener("input", function () {
  let edit = document.getElementById("can_edit");
  let x = document
    .getElementById("transaction_table")
    .elements.namedItem("type_input");
  if (edit.checked == true) {
    for (let i = 0; i < x.length; i++) {
      x[i].readOnly = false;
    }
  } else {
    for (let i = 0; i < x.length; i++) {
      x[i].readOnly = true;
    }
  }
});

document.addEventListener("change", (e) => {
  let type = e.target;
  data = {action : "type", transid : type.dataset.transid, category : type.value};
  if (data["transid"]){
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
    })
    .catch(function(error) {
      console.log(error);
    })
  }
});
