const colors = [
    "#FF6B6B",
    "#4DABF7",
    "#51CF66",
    "#FFD43B",
    "#CC5DE8",
    "#FF922B",
    "#20C997",
    "#748FFC",
    "#F06595",
    "#94D82D",
    "#E599F7",
    "#66D9E8",
    "#FFA8A8",
    "#B197FC"
];

const defaultOptions = {
    responsive: true,
    maintainAspectRatio: true,
aspectRatio: 2,
    resizeDelay: 200,
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
            beginAtZero: true,
            ticks: {
                color: "#F0F6FC",
                precision: 0
            },
            grid: {
                color: "#30363D"
            }
        }
    }
};

function createChart(id, config) {
    const canvas = document.getElementById(id);

    if (!canvas) {
        return;
    }

    new Chart(canvas, config);
}

function buildMultiLineChart(rawData, groupKey) {
    const labels = [...new Set(rawData.map(item => item.date))];
    const groups = [...new Set(rawData.map(item => item[groupKey]))];

    const datasets = groups.map((group, index) => {
        const data = labels.map(date => {
            const found = rawData.find(
                item => item.date === date && item[groupKey] === group
            );

            return found ? found.count : 0;
        });

        return {
            label: group,
            data: data,
            borderColor: colors[index % colors.length],
            backgroundColor: "transparent",
            tension: 0.35,
            pointRadius: 3,
            pointHoverRadius: 5
        };
    });

    return {
        labels: labels,
        datasets: datasets
    };
}

createChart("defectsChart", {
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

createChart("camerasChart", {
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

createChart("datesChart", {
    type: "line",
    data: {
        labels: datesLabels,
        datasets: [{
            label: "Rejections",
            data: datesData,
            borderColor: "#F78166",
            backgroundColor: "transparent",
            tension: 0.35,
            pointRadius: 3,
            pointHoverRadius: 5
        }]
    },
    options: defaultOptions
});

createChart("hoursChart", {
    type: "line",
    data: {
        labels: hoursLabels,
        datasets: [{
            label: "Rejections",
            data: hoursData,
            borderColor: "#D2A8FF",
            backgroundColor: "transparent",
            tension: 0.35,
            pointRadius: 3,
            pointHoverRadius: 5
        }]
    },
    options: defaultOptions
});

createChart("defectTrendChart", {
    type: "line",
    data: buildMultiLineChart(defectTrendRaw, "defect"),
    options: defaultOptions
});

createChart("cameraTrendChart", {
    type: "line",
    data: buildMultiLineChart(cameraTrendRaw, "camera"),
    options: defaultOptions
});
