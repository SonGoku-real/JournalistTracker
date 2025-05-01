document.addEventListener('DOMContentLoaded', function() {
    // Initialize all tables with the 'datatable' class
    const tables = document.querySelectorAll('.datatable');
    tables.forEach(table => {
        const options = {
            paging: true,
            ordering: true,
            info: true,
            responsive: true,
            lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
            language: {
                search: "_INPUT_",
                searchPlaceholder: "Search...",
                lengthMenu: "Show _MENU_ entries",
                info: "Showing _START_ to _END_ of _TOTAL_ entries",
                infoEmpty: "Showing 0 to 0 of 0 entries",
                infoFiltered: "(filtered from _MAX_ total entries)",
                zeroRecords: "No matching records found",
                paginate: {
                    first: "First",
                    last: "Last",
                    next: "Next",
                    previous: "Previous"
                }
            },
            // Determine sort options from data attributes
            order: [[table.getAttribute('data-sort-column') || 0, table.getAttribute('data-sort-direction') || 'asc']]
        };
        
        // Initialize DataTable
        const dataTable = new DataTable(table, options);
        
        // Add search input to wrapper
        if (table.parentNode.querySelector('.datatable-search-container')) {
            const searchContainer = table.parentNode.querySelector('.datatable-search-container');
            const searchInput = searchContainer.querySelector('input[type="search"]');
            
            if (searchInput) {
                searchInput.addEventListener('keyup', function() {
                    dataTable.search(this.value).draw();
                });
            }
        }
        
        // Add export button if needed
        if (table.hasAttribute('data-export')) {
            const buttonContainer = document.createElement('div');
            buttonContainer.className = 'mt-2 mb-3';
            
            const exportButton = document.createElement('button');
            exportButton.className = 'btn btn-sm btn-outline-secondary';
            exportButton.textContent = 'Export CSV';
            exportButton.addEventListener('click', function() {
                exportTableToCSV(table);
            });
            
            buttonContainer.appendChild(exportButton);
            table.parentNode.insertBefore(buttonContainer, table);
        }
    });
});

function exportTableToCSV(table) {
    const dataTable = DataTable.instance(table);
    if (!dataTable) return;
    
    // Get all data from the table
    const data = dataTable.data().toArray();
    
    // Get header row
    const headers = [];
    table.querySelectorAll('thead th').forEach(th => {
        headers.push(th.textContent.trim());
    });
    
    // Create CSV content
    let csvContent = headers.join(',') + '\n';
    
    // Add data rows
    data.forEach(row => {
        const rowData = [];
        for (let i = 0; i < headers.length; i++) {
            // Extract text content from cells (handles HTML content)
            let cellContent = row[i];
            if (typeof cellContent === 'string' && cellContent.includes('<')) {
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = cellContent;
                cellContent = tempDiv.textContent.trim();
            }
            
            // Escape CSV special characters
            if (typeof cellContent === 'string') {
                cellContent = cellContent.replace(/"/g, '""');
                if (cellContent.includes(',') || cellContent.includes('"') || cellContent.includes('\n')) {
                    cellContent = `"${cellContent}"`;
                }
            } else if (cellContent === null || cellContent === undefined) {
                cellContent = '';
            }
            
            rowData.push(cellContent);
        }
        csvContent += rowData.join(',') + '\n';
    });
    
    // Create download link
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', 'export.csv');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
