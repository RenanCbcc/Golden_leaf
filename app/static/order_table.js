$("#category").change(getProductsByCategory);

function getProductsByCategory() {
    var products_list = $("#product");
    var category_id = $(this).val();
    $.get('http://127.0.0.1:8000//product/category/' + category_id, function (response) {
        console.log(JSON.stringify(response.products));
        var option = '';
        $.each(response.products, function (idx, product) {
            option += '<option value="' + product.id + '">' + product.description + '</option>';
        });
        $("#product").html(option);
    });
}


function insert_order() {
    var body_table = $(".orders").find("tbody");
    var usuario = "Douglas"
    var numPalavras = $("#contador-palavras").text();

    var linha = new_line(usuario, numPalavras);
    linha.find(".botao-remover").click(removeLinha);

    corpoTabela.append(linha);
    $(".placar").slideDown(500);
    scrollPlacar();
}


function new_line(description, price, quantity) {
    var line = $("<tr>");
    var column_description = $("<td>").text(description);
    var column_price = $("<td>").text(price);
    var column_quantity = $("<td>").text(quantity);

    line.append(column_description);
    line.append(column_price);
    line.append(column_quantity);

    return line;
}

