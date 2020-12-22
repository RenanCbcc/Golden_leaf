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
                height: 400,
                width: 350,
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
        width: 700,
        vAxis: { format: 'currency' },
        curveType: 'function'

    }

    var graficoLinha = new google.visualization.LineChart(document.getElementById('grafico-linha'));
    graficoLinha.draw(tabela, opcoesLinha);

    

}