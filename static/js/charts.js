document.addEventListener('DOMContentLoaded', function() {
    // Initialize all chart containers
    const chartContainers = document.querySelectorAll('[data-chart-type]');
    chartContainers.forEach(container => {
        const chartType = container.getAttribute('data-chart-type');
        const chartData = JSON.parse(container.getAttribute('data-chart-data') || '{}');
        const chartOptions = JSON.parse(container.getAttribute('data-chart-options') || '{}');
        
        if (chartType && chartData) {
            initChart(container.id, chartType, chartData, chartOptions);
        }
    });
});

function initChart(containerId, chartType, data, customOptions = {}) {
    const ctx = document.getElementById(containerId).getContext('2d');
    
    // Default options for all charts
    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    // Dark theme friendly text color
                    color: '#e9ecef'
                }
            },
            tooltip: {
                mode: 'index',
                intersect: false
            }
        },
        scales: {
            x: {
                ticks: {
                    color: '#adb5bd'
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)'
                }
            },
            y: {
                ticks: {
                    color: '#adb5bd'
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)'
                }
            }
        }
    };
    
    // Merge default and custom options
    const options = Object.assign({}, defaultOptions, customOptions);
    
    // Different chart type configurations
    switch(chartType) {
        case 'pie':
        case 'doughnut':
            return new Chart(ctx, {
                type: chartType,
                data: {
                    labels: data.labels || [],
                    datasets: [{
                        data: data.data || [],
                        backgroundColor: getChartColors(data.data?.length || 0),
                        borderWidth: 1
                    }]
                },
                options: options
            });
            
        case 'bar':
            return new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels || [],
                    datasets: [{
                        label: data.label || 'Value',
                        data: data.data || [],
                        backgroundColor: getChartColors(1)[0],
                        borderWidth: 1
                    }]
                },
                options: options
            });
            
        case 'horizontalBar':
            const horizontalOptions = Object.assign({}, options, {
                indexAxis: 'y'
            });
            return new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels || [],
                    datasets: [{
                        label: data.label || 'Value',
                        data: data.data || [],
                        backgroundColor: getChartColors(1)[0],
                        borderWidth: 1
                    }]
                },
                options: horizontalOptions
            });
            
        case 'line':
            return new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels || [],
                    datasets: [{
                        label: data.label || 'Value',
                        data: data.data || [],
                        borderColor: getChartColors(1)[0],
                        backgroundColor: 'rgba(0, 123, 255, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: options
            });
            
        case 'multiLine':
            const datasets = [];
            if (data.datasets && Array.isArray(data.datasets)) {
                const colors = getChartColors(data.datasets.length);
                data.datasets.forEach((dataset, index) => {
                    datasets.push({
                        label: dataset.label || `Dataset ${index + 1}`,
                        data: dataset.data || [],
                        borderColor: colors[index],
                        backgroundColor: colors[index].replace('rgb', 'rgba').replace(')', ', 0.1)'),
                        borderWidth: 2,
                        tension: 0.4,
                        fill: false
                    });
                });
            }
            return new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels || [],
                    datasets: datasets
                },
                options: options
            });
            
        default:
            console.error(`Chart type ${chartType} not supported`);
            return null;
    }
}

function getChartColors(count) {
    // Bootstrap 5 colors
    const colors = [
        'rgb(13, 110, 253)',    // primary
        'rgb(220, 53, 69)',     // danger
        'rgb(25, 135, 84)',     // success
        'rgb(255, 193, 7)',     // warning
        'rgb(13, 202, 240)',    // info
        'rgb(108, 117, 125)',   // secondary
        'rgb(111, 66, 193)',    // purple
        'rgb(214, 51, 132)',    // pink
        'rgb(253, 126, 20)',    // orange
        'rgb(32, 201, 151)'     // teal
    ];
    
    if (count <= colors.length) {
        return colors.slice(0, count);
    }
    
    // If we need more colors than in our array, generate them
    const result = [...colors];
    for (let i = colors.length; i < count; i++) {
        const r = Math.floor(Math.random() * 255);
        const g = Math.floor(Math.random() * 255);
        const b = Math.floor(Math.random() * 255);
        result.push(`rgb(${r}, ${g}, ${b})`);
    }
    
    return result;
}

// Function to update a chart with new data
function updateChart(chartId, newData) {
    const chartElement = document.getElementById(chartId);
    if (!chartElement) return;
    
    const chart = Chart.getChart(chartId);
    if (!chart) return;
    
    if (newData.labels) {
        chart.data.labels = newData.labels;
    }
    
    if (newData.data && chart.data.datasets[0]) {
        chart.data.datasets[0].data = newData.data;
    }
    
    if (newData.datasets && Array.isArray(newData.datasets)) {
        chart.data.datasets = newData.datasets.map((dataset, index) => {
            const color = getChartColors(newData.datasets.length)[index];
            return {
                label: dataset.label || `Dataset ${index + 1}`,
                data: dataset.data || [],
                borderColor: color,
                backgroundColor: color.replace('rgb', 'rgba').replace(')', ', 0.1)'),
                borderWidth: 2,
                tension: 0.4,
                fill: false
            };
        });
    }
    
    chart.update();
}
