
document.addEventListener("input", function () {
  var edit = document.getElementById("can_edit");
  var x = document
    .getElementById("transaction_table")
    .elements.namedItem("type_input");
  if (edit.checked == true) {
    for (var i = 0; i < x.length; i++) {
      x[i].readOnly = false;
    }
  } else {
    for (var i = 0; i < x.length; i++) {
      x[i].readOnly = true;
    }
  }
});

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
