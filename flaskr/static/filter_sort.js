
// Listens for the sort or filter buttons to be clicked
document.addEventListener("click", (e) => {
    // If the clear filter button is clicked, reset the filter select
    if (e.target.id == 'clear_filter') {
        document.getElementById('filter').selectedIndex = 0;
    }
    // If the clear sort button is clicked, reset the sort select
    if (e.target.id == 'clear_sort') {
        document.getElementById('sort').selectedIndex = 0;
        uploadDateSort()
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
        if (select.selectedIndex == 2){
            amountSort();
        }
        if (select.selectedIndex == 1){
            transDateSort();
        }
        if (select.selectedIndex == 3){
            categorySort();
        }
    }
});

// Filter the table based on the selected filter
function filterTable() {
    let table = document.getElementById('transaction-table');
    let rows = table.getElementsByTagName('tr');

}

function amountSort(){
    // access the table to bet the rows
    let table = document.getElementById('transaction-table');
    let rows;
    let switching = true;
    let row1;
    let row2;
    let i, x, y;
    rows = table.rows;
    while (switching){
        switching = false;
        for (i = 1; i < (rows.length - 1); i++){
            shouldSwitch = false;
            // get the amount value for rows[i] and rows[i + 1]
            row1 = rows[i].childNodes[5].innerHTML;
            row2 = rows[i + 1].childNodes[5].innerHTML;
            // make sure amount is positive
            x = Math.abs(parseFloat(row1));
            y = Math.abs(parseFloat(row2));
            if (x > y){
                shouldSwitch = true;
                break;
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
}

function uploadDateSort(){
    let table = document.getElementById('transaction-table');
    let rows;
    let switching = true;
    let i, x, y;
    rows = table.rows;
    while (switching){
        switching = false;
        for (i = 1; i < (rows.length - 1); i++){
            shouldSwitch = false;
            // get the upload date and convert it to a Date object
            x = new Date(rows[i].childNodes[3].dataset['date']);
            y = new Date(rows[i + 1].childNodes[3].dataset['date']);
            // if row[i] date is greater than row[i + 1] date, switch them
            if (x > y){
                shouldSwitch = true;
                break;
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
}

function transDateSort(){
    let table = document.getElementById('transaction-table');
    let rows;
    let switching = true;
    let i, x, y;
    rows = table.rows;
    while (switching){
        switching = false;
        for (i = 1; i < (rows.length - 1); i++){
            shouldSwitch = false;
            // get the transaction date and convert it to a Date object
            x = new Date(rows[i].childNodes[3].innerHTML);
            y = new Date(rows[i + 1].childNodes[3].innerHTML);
            // if row[i] date is greater than row[i + 1] date, switch them
            if (x > y){
                shouldSwitch = true;
                break;
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
}

function categorySort(){
    let table = document.getElementById('transaction-table');
    let rows = table.rows;
    let i = 1, k, x;
    let categories = [];
    for (let j = 1; j < rows.length; j++){
        let current = rows[j].childNodes[9].lastChild.value.toLowerCase();
        if (!categories.includes(current)){
            categories.push(current);
        }
    }
    // for each category in categories
    for (k = 0; k < categories.length; k++){
        // keeps track of where to place the current row
        let hasCategory = 1;
        // loops throught the table until it is sorted, does not stop until i = n-1
        for (let counter = 0; i < rows.length; counter++){
            // get the current category to sort
            x = rows[i].childNodes[9].lastChild.value.toLowerCase();
            // if category in categories add it before last element with categories[k]
            if (x == categories[k]){
                rows[i].parentNode.insertBefore(rows[i], rows[hasCategory]);
                // increments hascategory to insert next row into correct position
                hasCategory++;
                i++
            }
            // add row to end of table
            rows[i].parentNode.insertBefore(rows[i], null);
            if (counter > rows.length){
                break;
            }
        }
    }
}
