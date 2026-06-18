const defaultOptions = {
    responsive: true,
    plugins: {
        legend: {
            labels: {
                color: "#F0F6FC"
            }
        }
    },
    scales: {
        x: {
            ticks: {
                color: "#F0F6FC"
            },
            grid: {
                color: "#30363D"
            }
        },
        y: {
            ticks: {
                color: "#F0F6FC"
            },
            grid: {
                color: "#30363D"
            }
        }
    }
};

new Chart(document.getElementById("defectsChart"), {
    type: "bar",
    data: {
        labels: defectsLabels,
        datasets: [{
            label: "Occurrences",
            data: defectsData,
            backgroundColor: "#58A6FF"
        }]
    },
    options: defaultOptions
});

new Chart(document.getElementById("camerasChart"), {
    type: "bar",
    data: {
        labels: camerasLabels,
        datasets: [{
            label: "Rejections",
            data: camerasData,
            backgroundColor: "#3FB950"
        }]
    },
    options: defaultOptions
});

new Chart(document.getElementById("datesChart"), {
    type: "line",
    data: {
        labels: datesLabels,
        datasets: [{
            label: "Rejections",
            data: datesData,
            borderColor: "#F78166",
            tension: 0.3
        }]
    },
    options: defaultOptions
});

new Chart(document.getElementById("hoursChart"), {
    type: "line",
    data: {
        labels: hoursLabels,
        datasets: [{
            label: "Rejections",
            data: hoursData,
            borderColor: "#D2A8FF",
            tension: 0.3
        }]
    },
    options: defaultOptions
});