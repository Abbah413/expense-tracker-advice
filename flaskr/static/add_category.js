function addnew() {
    var table = document.getElementById("categorytable");
    var row = table.insertRow();
    var cell1 = row.insertCell();
    var testing = createTest();
    document.cell1.appendChild(testing);
    var cell2 = row.insertCell();
    var cell1 = row.insertCell();
    var cell2 = row.insertCell();


}

function createTest(){
    const attributeDict = {
        type: "text",
        class : "form-control",
        name : "category_input",
        value : "{{ categories.category}}",
        placeholder : "Category",
        readonly : ""
   };
   const test = document.createElement("INPUT");
    for (const key in attributeDict){
        test.setAttribute(key, attributeDict[key]);
   }
   return test;
}