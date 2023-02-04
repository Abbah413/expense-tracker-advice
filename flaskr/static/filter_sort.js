// Listens for the sort or filter buttons to be clicked
document.addEventListener("click", (e) => {
    // If the clear filter button is clicked, reset the filter select
    if (e.target.id == 'clear_filter') {
        document.getElementById('filter').selectedIndex = 0;
    }
    // If the clear sort button is clicked, reset the sort select
    if (e.target.id == 'clear_sort') {
        document.getElementById('sort').selectedIndex = 0;
    }
});

// Listens for the sort or filter selects to be changed
document.addEventListener("change", (e) => {
    // Stores the target of the event as select
    let select = e.target;
    // If the filter select is changed, log the index of the selected option
    if (select.id == 'filter') {
        console.log('filter: ', select.selectedIndex);
    }
    // If the sort select is changed, log the index of the selected option
    if (select.id == 'sort') {
        console.log('sort: ', select.selectedIndex);
    }
});

// Filter the table based on the selected filter
function filterTable() {
    let table = document.getElementById('transaction-table');
    let rows = table.getElementsByTagName('tr');

}

function sortTable() {
    let table = document.getElementById('transaction-table');
    let rows = table.getElementsByTagName('tr');
    
}