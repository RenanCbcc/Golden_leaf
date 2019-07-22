$(document).ready(populateCategories);
$("#categories").change(getProductsByCategory);
$("#products").change(updateUnitcost);
$("#add-product-btn-manual-form").click(insert_order_from_manual_form);
$("#add-product-btn-automatic-form").click(insert_order_from_automatic_form);
$("#save-items-btn").click(saveitems);

function getProductsByCategory() {
    let category_id = $(this).val();
    $.get('http://127.0.0.1:8000//product/category/' + category_id, function (response) {
        let option = '';
        $.each(response.products, function (idx, product) {
            option += '<option value="' + product.id + '">' + product.description + '</option>';
        });
        $("#products").html(option);
    });
}

function updateUnitcost() {
    $.get('http://127.0.0.1:8000/product/unit_cost/' + $("#products").val(), function (response) {
        $("#unit_cost").val(response.unit_cost)
    });

}

function insert_order_from_manual_form() {
    let product = $("#products");
    let body_table = $("#items-table").find("tbody");
    let product_id = product.val();
    let product_description = product.text();
    let product_cost = $("#unit_cost").val();
    let product_quantity = $("#quantity").val();

    let line = new_line(product_id, product_description, product_cost, product_quantity);
    body_table.append(line);


}


function new_line(id, description, unit_cost, quantity) {
    let line = $("<tr>");
    let column_id = $("<td>").text(id).attr('id', 'product_id').hide();
    let column_description = $("<td>").text(description);
    let column_price = $("<td>").text(unit_cost);
    let column_quantity = $("<td>").text(quantity).attr('id', 'product_quantity');
    let column_total = $("<td>").text(unit_cost * quantity);
    let column_remove = $("<td>");
    let column_edit = $("<td>");

    let link_remove = $("<a>").addClass("btn btn-danger").attr("href", "#").text("Remover");
    let span_remove = $("<span>").addClass("glyphicon glyphicon-remove");

    link_remove.append(span_remove);
    column_remove.append(link_remove);


    line.append(column_id);
    line.append(column_description);
    line.append(column_price);
    line.append(column_quantity);
    line.append(column_total);
    line.append(column_remove);
    line.append(column_edit);

    return line;
}

function populateCategories() {
    $.get('http://127.0.0.1:8000/api/category', function (response) {
        let option = '';
        $.each(response.categories, function (idx, category) {
            option += '<option value="' + category.id + '">' + category.title + '</option>';
        });
        $("#categories").html(option);
    });
}

$("#code").blur(function () {

        let code = $(this).val();

        //Fill the form out with "..." while  browsing webservice.
        $("#description_automatic_form").val("...");
        $("#unit_cost_automatic_form").val("...");

        $.getJSON("http://127.0.0.1:8000/api/product/code/" + code, function (response) {

            if (!("error" in response)) {
                //Atualiza os campos com os valores da consulta.
                $("#description_automatic_form").val(response.description);
                $("#unit_cost_automatic_form").val(response.unit_cost);
                $("#product-id").val(response.id);
            } else {
                alert("Codigo nao encontrado");
            }
        });
    }
);

function insert_order_from_automatic_form() {
    let product_id = $("#product-id");
    let body_table = $("#items-table").find("tbody");
    let product_description = $("#description_automatic_form").val();
    let product_cost = $("#unit_cost_automatic_form").val();
    let product_quantity = $("#quantity_automatic_form").val();

    let line = new_line(product_id, product_description, product_cost, product_quantity);
    body_table.append(line);

}


function saveitems() {
    let items = [];

    $("tbody>tr").each(function () {
        var product_id = $(this).find("td:nth-child(1)").text();
        var product_quantity = $(this).find("td:nth-child(3)").text();
        var item = {
            id: product_id,
            quantity: product_quantity
        };
        items.push(item)
    });

    let data = {
        items: items
    };

     console.log(data);
    $.post("http://127.0.0.1:8000/api/order", items, function (response) {
            console.log(response);
        }
    );
}