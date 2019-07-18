$("#category").change(getProductsByCategory);
$("#product").change(updateUnitcost);
$("#add-product-btn").click(insert_order);

function getProductsByCategory() {
    var category_id = $(this).val();
    $.get('http://127.0.0.1:8000//product/category/' + category_id, function (response) {
        var option = '';
        $.each(response.products, function (idx, product) {
            option += '<option value="' + product.id + '">' + product.description + '</option>';
        });
        $("#product").html(option);
    });
}

function updateUnitcost() {
    $.get('http://127.0.0.1:8000/product/unit_cost/' + $("#product").val(), function (response) {
        $("#unit_cost").val(response.unit_cost)
    });

}

function insert_order() {
    var body_table = $("#orders").find("tbody");
    var product_id = $("#product").val();
    var product_description = $("#product").text();
    var product_cost = $("#unit_cost").val();
    var product_quantity = $("#quantity").val();

    var line = new_line(product_id, product_description, product_cost, product_quantity);
    body_table.append(line);


}


function new_line(id, description, unit_cost, quantity) {
    var line = $("<tr>");
    var column_id = $("<td>").text(id);
    var column_description = $("<td>").text(description);
    var column_price = $("<td>").text(unit_cost);
    var column_quantity = $("<td>").text(quantity);
    var column_total = $("<td>").text(unit_cost * quantity);
    var column_remove = $("<td>");
    var column_edit = $("<td>");

    var link_remove = $("<a>").addClass("btn btn-danger").attr("href", "#").text("Remover");
    var span_remove = $("<span>").addClass("glyphicon glyphicon-remove");

    link_remove.append(span_remove);
    column_remove.append(link_remove);

    var link_edit = $("<a>").addClass("btn btn-primary").attr("href", "#").text("Editar");
    var span_edit = $("<i>").addClass("small").addClass("glyphicon glyphicon-pencil");


    link_edit.append(span_edit);
    column_edit.append(link_edit);


    line.append(column_id);
    line.append(column_description);
    line.append(column_price);
    line.append(column_quantity);
    line.append(column_total);
    line.append(column_remove);
    line.append(column_edit);

    return line;
}

