// FORCES ORDER
const phaseOrder = ["Planning", "Design", "Implementation", "Testing", "Documentation"];

const labels = phaseOrder.filter(p => hoursByPhase[p] !== undefined);
const values = labels.map(p => hoursByPhase[p] || 0);

const chartMaxValue = Math.max(...values);
const paddedMax = Math.ceil(chartMaxValue * 1.1); //

document.addEventListener("DOMContentLoaded", function () {

    const context = document.getElementById('phaseChart');

    if (!context) {
        console.error("Canvas not found");
        return;
    }

    new Chart(context, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                axis: 'y',
                label: 'Hours', // Label for if user hovers over bar
                data: values,
                backgroundColor: [
                    'rgba(100, 116, 139, 1.0)', // Gray
                    'rgba(59, 130, 246, 1.0)',  // Blue
                    'rgba(139, 92, 246, 1.0)',  // Purple
                    'rgba(16, 185, 129, 1.0)',  // Green
                    'rgba(245, 158, 11, 1.0)'   // Orange
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: paddedMax,
                    ticks: {
                        font: {
                            size: 18
                        }
                    }
                },
                y: {
                    ticks: {
                        font: {
                            size: 14  // labels like Planning, Design, etc.
                        }
                    }
                }
            }
        }
    });

});