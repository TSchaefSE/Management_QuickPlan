document.addEventListener("DOMContentLoaded", function () {
    const chartCanvas = document.getElementById("phaseChart");
    if (!chartCanvas) return;

    // =========================
    // Get data from HTML safely
    // =========================
    let hoursByPhase = {};

    const dataElement = document.getElementById("hours-data");

    if (dataElement) {
        try {
            const parsed = JSON.parse(dataElement.textContent);
            if (typeof parsed === "object" && parsed !== null) {
                hoursByPhase = parsed;
            }
        } catch (e) {
            console.error("Failed to parse hours_by_phase JSON:", e);
        }
    }

    // =========================
    // Prepare chart data
    // =========================
    const phaseOrder = ["Planning", "Design", "Implementation", "Testing", "Documentation"];

    const labels = phaseOrder;
    const values = labels.map(phase => {
        const value = Number(hoursByPhase[phase]);
        return Number.isFinite(value) ? value : 0;
    });

    const chartMaxValue = values.length > 0 ? Math.max(...values) : 0;
    const paddedMax = chartMaxValue > 0 ? Math.ceil(chartMaxValue * 1.1) : 1;

    // =========================
    // Render chart
    // =========================
    new Chart(chartCanvas, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                axis: "y",
                label: "Hours",
                data: values,
                backgroundColor: [
                    "rgba(100, 116, 139, 1.0)",
                    "rgba(59, 130, 246, 1.0)",
                    "rgba(139, 92, 246, 1.0)",
                    "rgba(16, 185, 129, 1.0)",
                    "rgba(245, 158, 11, 1.0)"
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: "y",
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
                        font: { size: 18 }
                    }
                },
                y: {
                    ticks: {
                        font: { size: 14 }
                    }
                }
            }
        }
    });
});