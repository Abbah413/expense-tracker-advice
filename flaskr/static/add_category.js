function addnew() {
    var table = document.getElementById("categorytable");
    var tbody = table.getElementsByTagName("tbody")[0];
    var row = tbody.insertRow();
    var cell1 = row.insertCell();
    var testing = createTest();
    cell1.appendChild(testing);
    var cell2 = row.insertCell();
    var cell3 = row.insertCell();
    var cell4 = row.insertCell();
}

function createTest(){
    const attributeDict = {
        type: "text",
        class : "form-control",
        name : "category_input",
        placeholder : "Category",
   };
   const test = document.createElement("INPUT");
    for (const key in attributeDict){
        test.setAttribute(key, attributeDict[key]);
   }
   return test;
}