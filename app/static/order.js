var ctx = document.getElementById("myBarChart");

var myLineChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro",
            "Outubro", "Novembro", "Dezembro"],
        datasets: [{
            label: "Pago",
            backgroundColor: "rgba(2,117,216,1)",
            borderColor: "rgba(2,117,216,1)",
            data: [5312, 6251, 7841, 9821, 14084, 2991, 6251, 1432, 6876, 1234, 5672, 6543],
        }, {
            label: "Pendente",
            backgroundColor: "rgb(216,38,33)",
            borderColor: "rgb(216,38,33)",
            data: [5231, 5162, 8417, 2198, 15004, 5162, 4704, 6543, 1234, 6742, 1453, 9654],
        }
        ],
    },
    options: {
        scales: {
            xAxes: [{
                time: {
                    unit: 'month'
                },
                gridLines: {
                    display: false
                },
                ticks: {
                    maxTicksLimit: 12
                }
            }],
        },
        legend: {
            display: false
        }
    }
});
