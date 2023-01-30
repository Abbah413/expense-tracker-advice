document.addEventListener("input", function(){
    var edit = document.getElementById("can_edit");
    var x = document.getElementById("transaction_table").elements.namedItem("type_input");
    if (edit.checked == true){
        for (var i = 0; i < x.length; i++){
            x[i].readOnly = false;
        }
    }
    else{
        for (var i = 0; i < x.length; i++){
            x[i].readOnly = true;
        }
    }
})