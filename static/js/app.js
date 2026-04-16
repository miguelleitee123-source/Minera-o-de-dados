let statusChart;

async function fetchData() {
    try {
        const response = await fetch('/api/data');
        const result = await response.json();
        
        if (result.status === 'success') {
            updateDashboard(result);
        }
    } catch (error) {
        console.error("Erro ao buscar dados:", error);
    }
}

function updateDashboard(result) {
    const { data, stats } = result;

    // Update Stats
    document.getElementById('stat-total').innerText = stats.total;
    document.getElementById('stat-mitigados').innerText = stats.mitigados;
    document.getElementById('stat-percent').innerText = `${stats.percent_mitigado}% do tráfego sob mitigação`;

    // Update Table
    const tableBody = document.getElementById('data-table-body');
    tableBody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');
        const isMitigated = item.status_mitigacao.includes('Mitigada');
        
        row.innerHTML = `
            <td style="color: var(--text-dim)">${item.timestamp}</td>
            <td style="font-weight: 600">${item.prefixo}</td>
            <td>
                <span class="status-label ${isMitigated ? 'mitigated' : 'normal'}">
                    ${isMitigated ? 'MITIGADA' : 'NORMAL'}
                </span>
            </td>
            <td>${item.asn_mitigador || '---'}</td>
            <td>
                <span style="opacity: 0.8">${item.as_path_len} saltos</span>
            </td>
        `;
        tableBody.appendChild(row);
    });

    // Update Chart
    updateChart(stats);
}

function updateChart(stats) {
    const ctx = document.getElementById('statusChart').getContext('2d');
    
    const chartData = {
        labels: ['Normal', 'Mitigado'],
        datasets: [{
            data: [stats.total - stats.mitigados, stats.mitigados],
            backgroundColor: ['#3b82f6', '#ef4444'],
            borderWidth: 0,
            hoverOffset: 4
        }]
    };

    if (statusChart) {
        statusChart.data = chartData;
        statusChart.update();
    } else {
        statusChart = new Chart(ctx, {
            type: 'doughnut',
            data: chartData,
            options: {
                cutout: '70%',
                plugins: {
                    legend: { display: false }
                },
                maintainAspectRatio: false
            }
        });
    }
}

// Polling a cada 5 segundos
setInterval(fetchData, 5000);

// Carga inicial
fetchData();
