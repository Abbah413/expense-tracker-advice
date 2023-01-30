document.addEventListener("click", (e) => {
    if (e.target.id == 'clear_filter') {
        document.getElementById('filter').selectedIndex = 0;
    }
    if (e.target.id == 'clear_sort') {
        document.getElementById('sort').selectedIndex = 0;
    }
});