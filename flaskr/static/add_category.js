function addnew() {
    var table = document.getElementById("categorytable");
    var tbody = table.getElementsByTagName("tbody")[0];
    var row = tbody.insertRow();
    createCategory(row);
    var cell2 = row.insertCell();
        cell2.innerHTML = 'budget'
    var cell3 = row.insertCell();
}

function createCategory(row){
    var cell1 = row.insertCell();
    cell1.setAttribute("class", "py-1")
    var div = document.createElement('DIV');
    div.setAttribute("class", "input-group py-0");
    cell1.appendChild(div);
    var button = buttonAttributes();
    var input = inputAttributes();
    div.appendChild(button);
    div.appendChild(input);

}

function inputAttributes(){
    const attributeDict = {
        type : "text",
        class : "form-control",
        name : "category_input",
        placeholder : "Category",
   };
   const input = document.createElement("INPUT");
    for (const key in attributeDict){
        input.setAttribute(key, attributeDict[key]);
   }
   return input;
}

function buttonAttributes(){
    const attributeDict = {
        type : "button",
        class : "remove_button"
    }
    const button = document.createElement("BUTTON");
    for (const key in attributeDict){
        button.setAttribute(key, attributeDict[key]);
    }
    var icon = document.createElement('I');
    icon.setAttribute("class", "bi bi-x-lg");
    button.appendChild(icon);
    return button;
}