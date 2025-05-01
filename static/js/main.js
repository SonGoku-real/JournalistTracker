document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Add event listener for CSV export buttons
    const exportButtons = document.querySelectorAll('.export-csv');
    exportButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const endpoint = this.getAttribute('data-endpoint');
            exportToCSV(endpoint);
        });
    });
});

// Function to export data to CSV
function exportToCSV(endpoint) {
    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            // Convert JSON to CSV
            const csv = convertToCSV(data);
            
            // Create a download link
            const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.setAttribute('href', url);
            link.setAttribute('download', `export-${Date.now()}.csv`);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        })
        .catch(error => {
            console.error('Error exporting data:', error);
            alert('Error exporting data. Please try again.');
        });
}

// Helper function to convert JSON to CSV
function convertToCSV(objArray) {
    if (!objArray || !objArray.length) {
        return '';
    }
    
    const array = typeof objArray !== 'object' ? JSON.parse(objArray) : objArray;
    let str = '';
    
    // Get headers
    const headers = Object.keys(array[0]);
    str += headers.join(',') + '\r\n';
    
    // Add data rows
    for (let i = 0; i < array.length; i++) {
        let line = '';
        for (let index in headers) {
            if (line !== '') line += ',';
            
            // Handle nested objects and arrays
            let value = array[i][headers[index]];
            if (value === null || value === undefined) {
                value = '';
            } else if (typeof value === 'object') {
                value = JSON.stringify(value);
            }
            
            // Escape quotes and commas in values
            if (typeof value === 'string') {
                value = value.replace(/"/g, '""');
                if (value.includes(',') || value.includes('"') || value.includes('\n')) {
                    value = `"${value}"`;
                }
            }
            
            line += value;
        }
        str += line + '\r\n';
    }
    
    return str;
}

// Function to toggle sidebar (for mobile)
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('show');
    }
}
