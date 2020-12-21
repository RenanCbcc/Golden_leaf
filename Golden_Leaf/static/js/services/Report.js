function drawCharts() {

    //Grafico de Pizza    
    fetch('api/report/balance')
        .then(response => response.json())
        .then(data => {            
            let tabela = new google.visualization.DataTable();
            tabela.addColumn('string', 'Tipo');
            tabela.addColumn('string', 'valores');
            tabela.addRows([
                ['Vendas', data.salles],
                ['Pagamentos', data.income]
            ]);

            var opcoesPizzas = {
                title: 'Balanço do dia',
                height: 200,
                width: 400,
                is3D: true,
                legend: 'labeled',
                pieSliceText: 'value'
            }
            let graficoPizza = new google.visualization.PieChart(document.getElementById('grafico-pizza'));
            graficoPizza.draw(tabela, opcoesPizzas);
         });

    //Grafico de Linha
    tabela = new google.visualization.DataTable();
    tabela.addColumn('string', 'mês');
    tabela.addColumn('number', 'gastos');
    tabela.addColumn('number', 'entrada');
    tabela.addRows([
        ['jan', 800, 1000],
        ['fev', 400, 590],
        ['mar', 1100, 1789],
        ['abr', 400, 350],
        ['mai', 500, 677],
        ['jun', 750, 999],
        ['jul', 1500, 1890],
        ['ago', 650, 500],
        ['set', 850, 900],
        ['out', 400, 499],
        ['nov', 1000, 1409],
        ['dez', 720, 899]
    ]);

    var opcoesLinha = {
        title: 'Gastos por mês',
        height: 400,
        width: 900,
        vAxis: { format: 'currency' },
        curveType: 'function'

    }

    var graficoLinha = new google.visualization.LineChart(document.getElementById('graficoLinha'));
    graficoLinha.draw(tabela, opcoesLinha);

    //Grafico de Coluna
    tabela = new google.visualization.DataTable();
    tabela.addColumn('string', 'mês');
    tabela.addColumn('number', 'entrada');
    tabela.addColumn('number', 'saida');
    tabela.addRows(
        [
            ['jan', 2500, 1000],
            ['fev', 1000, 500],
            ['mar', 3000, 1300],
            ['abr', 1500, 1700],
            ['mai', 5000, 2250],
            ['jun', 3567, 3000],
            ['jul', 3452, 1468],
            ['ago', 1833, 5250],
            ['set', 1800, 1000],
            ['out', 1800, 1000],
            ['nov', 3569, 1500],
            ['dez', 3000, 1740]
        ]
    );


    var opcoesColuna = {
        title: 'Gatos vs Entrada',
        height: 400,
        width: 900,
        vAxis: { format: 'currency' },

    }

    var graficoColunas = new google.visualization.ColumnChart(document.getElementById('graficoColunas'));
    graficoColunas.draw(tabela, opcoesColuna);



    //Grafico de barrras com json


    fetch('dados.json')
        .then(response => response.json())
        .then(data => {
            var opcoes = {
                title: 'Usuários e Poupanças',
                height: 400,
                width: 900,
                annotations: {
                    alwaysOutside: true
                }

            }
            var tabelaJson = new google.visualization.DataTable(data);
            tabelaJson.sort([{ column: 1, desc: true }]);

            var graficoJson = new google.visualization.BarChart(document.getElementById('graficoBarrasJson'));

            graficoJson.draw(tabelaJson, opcoes);
        });



}