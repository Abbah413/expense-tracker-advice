// Added a new row to the summary table
function addnew() {
  let table = document.getElementById("categorytable");
  let tbody = table.getElementsByTagName("tbody")[0];
  let row = tbody.insertRow();
  createCategory(row);
  createBudget(row);
  let cell3 = row.insertCell();
}
// Creates the table row
function createCategory(row) {
  let cell1 = row.insertCell();
  cell1.setAttribute("class", "py-1");
  let div = document.createElement("DIV");
  div.setAttribute("class", "input-group py-0");
  cell1.appendChild(div);
  let button = buttonAttributes();
  let input = inputAttributes();
  div.appendChild(button);
  div.appendChild(input);
}
// creates the category input
function inputAttributes() {
  const attributeDict = {
    type: "text",
    class: "form-control",
    placeholder: "Category",
  };
  const input = document.createElement("INPUT");
  for (const key in attributeDict) {
    input.setAttribute(key, attributeDict[key]);
  }
  return input;
}
// creates the remove button
function buttonAttributes() {
  const attributeDict = {
    type: "button",
    class: "remove_button",
  };
  const button = document.createElement("BUTTON");
  for (const key in attributeDict) {
    button.setAttribute(key, attributeDict[key]);
  }
  let icon = document.createElement("I");
  icon.setAttribute("class", "bi bi-x-lg");
  button.appendChild(icon);
  return button;
}
// creates the budget input
function createBudget(row) {
  const attributeDict = {
    type: "number",
    class: "form-control",
    placeholder: "Budget",
  };
  const input = document.createElement("INPUT");
  for (const key in attributeDict) {
    input.setAttribute(key, attributeDict[key]);
  }
  let cell2 = row.insertCell();
  cell2.setAttribute("class", "budget");
  cell2.appendChild(input);
}

// Removes the row from the table
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
  let row = parent.parentNode.parentNode.parentNode;
  row.parentNode.removeChild(row);
}
