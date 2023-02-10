/*
function incomeTooltip() {
    let toolTip = document.querySelector("[data-bs-custom-class='custom-tooltip']");
    toolTip.addEventListener("hover", function(){
        
    })
}
*/

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
