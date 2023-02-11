// Update the database the the users new category
document.addEventListener("change", (e) => {
  let input = e.target;
  data = {action : "add", category : input.value};
  if (input.type === "text"){
    const index_url = "/"
    fetch(index_url, {
      headers : {"Content-Type" : "application/json"},
      method : "POST",
      body : JSON.stringify(data)
    })
    .then(response => {
      if(!response.ok) {
        throw new Error("Something went wrong");
      }
      return response.json();
    })
    .then(data => {
      appendTable(input, data);
    })
    .catch(function(error) {
      console.log(error);
    })
  }
});
// Update the budget in the database
document.addEventListener("change", (e) => {
  // budget input
  let input = e.target;
  if (input.type === "number"){
    let category = input.parentNode.previousElementSibling.lastElementChild.lastElementChild;
    let data = {action : "budget", category : category.value, budget : input.value};
    const index_url = "/"
    fetch(index_url, {
      headers : {"Content-Type" : "application/json"},
      method : "POST",
      body : JSON.stringify(data)
    })
    .then(response => {
      if(!response.ok) {
        throw new Error("Something went wrong");
      }
      return response.json();
    })
    .then(data => {
      update();
      console.log(data);
    })
    .catch(function(error) {
      console.log(error);
    })
  }
});
// Update the users category and the amount for corresponding category
function appendTable(input, data){
  input.value = data["category"];
  input.readOnly = true;
  let td = input.parentNode.parentNode;
  let amount = td.nextSibling.nextSibling;
  if (data["amount"]){
    let value = parseFloat(data["amount"]).toFixed(2);
    amount.innerHTML = "$" + Math.abs(value);
  }
  update();
}

// update the totals in summary table
document.addEventListener("DOMContentLoaded", update());
function update() {
  // get the budget and amount totals
  let budgets = document.getElementsByClassName("budget");
  let amounts = document.getElementsByClassName("amount");
  let removeButtons = document.getElementsByClassName("remove_button");
  // initialize the totals
  let btotal = 0;
  let atotal = 0;
  // get the sum of the budgets
  for (let i = 0; i < budgets.length; i++) {
    let category = removeButtons[i].nextElementSibling.value;
    let budget = budgets[i].firstElementChild.value;
    if (budget){
      if (budget.length > 0 && category != "Income"){
        btotal = btotal + parseFloat(budget);
      }
    }
  }
  // get the sum of absolute value of the amounts
  for (let i = 0; i < amounts.length; i++) {
    let category = removeButtons[i].nextElementSibling.value;
      if (category != "Income") {
        if (amounts[i].innerHTML){
          let a = amounts[i].innerHTML.replace(/\$/g, "");
          atotal = atotal + Math.abs(parseFloat(a));
        }
      }
  }
  // sets the value of b-total
  let total1 = document.getElementsByClassName("b-total");
  total1[0].innerHTML = "$" + btotal.toFixed(2);
  // sets the value of a-total
  let total2 = document.getElementsByClassName("a-total");
  total2[0].innerHTML = "$" + atotal.toFixed(2);
  netAfterLoad(atotal);
}

function netAfterLoad(atotal) {
  let footerIncome = document.querySelector(".t-income");
  if (footerIncome) {
    let net = document.querySelector(".net-income");
    let income = footerIncome.innerHTML.replace(/\$/g, "");
        // convert income to float
        let incomeToFloat = parseFloat(income);
        // calculate the net
        let netIncome = (incomeToFloat - atotal).toFixed(2);
        // if net is neagtive make the text red
        if (netIncome < 0) {
          net.innerHTML = "-$" + Math.abs(netIncome).toFixed(2);
          net.style.color = "red";
        }
        else {
          net.innerHTML = "$" + netIncome;
      }
  }
}

// hide the income row from the table
document.addEventListener("DOMContentLoaded", function() {
  let removeButtons = document.getElementsByClassName("remove_button");
  for (let i = 0; i < removeButtons.length; i++) {
    if (removeButtons[i].nextElementSibling.value == "Income") {
      let incomeRow = removeButtons[i].parentNode.parentNode.parentNode;
      incomeRow.parentNode.removeChild(incomeRow);
    }
  }
});