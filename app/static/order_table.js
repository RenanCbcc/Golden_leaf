$(document).ready(populateCategories);
$("#categories").click(getProductsByCategory);
$("#products").click(updateUnitcost);
$("#statusList li").click(changeOrderStatus);
$("#add-product-btn-manual-form").click(insert_order_from_manual_form);
$("#add-product-btn-automatic-form").click(insert_order_from_automatic_form);
$("#save-items-btn").click(saveItems);

BASE_APP_URL = 'http://127.0.0.1:5000/order/'
BASE_API_URL = 'http://127.0.0.1:5000/api';
CATEGORY_URL = BASE_API_URL + '/category';
PRODUCT_BY_CODE_URL = BASE_API_URL + '/product/code/';
PRODUCT_BY_CATEGORY_URL = BASE_API_URL + '/product/category/';
PRODUCT_UNIT_COST_URL = BASE_API_URL + '/product/unit_cost/';
ORDER_URL = BASE_API_URL + '/order';

function getProductsByCategory() {
    $("#unit_cost").val("")
    $("#quantity_manual_form").val("");
    let category_id = $(this).val();
    $.get(PRODUCT_BY_CATEGORY_URL + category_id, function (response) {
        let option = '';
        $.each(response.products, function (idx, product) {
            option += '<option value="' + product.id + '">' + product.description + '</option>';
        });
        $("#products").html(option);
    });
}

function updateUnitcost() {
    $("#quantity_manual_form").val("");
    $.get(PRODUCT_UNIT_COST_URL + $("#products").val(), function (response) {
        $("#unit_cost").val(response.unit_cost)
    });

}

function insert_order_from_manual_form() {
    let product = $("#products");
    let body_table = $("#items-table").find("tbody");
    let product_id = product.val();
    let product_description = $(product).children("option:selected").text();
    let product_cost = $("#unit_cost").val();
    let product_quantity = $("#quantity_manual_form").val();
    if (!validateQuantity(product_quantity)) {
        alert("Erro. Quantidade do produto inválida.");
        return;
    }
    let line = new_line(product_id, product_description, product_cost, product_quantity);
    body_table.append(line);


}

function insert_order_from_automatic_form() {
    let product_id = $("#product-id");
    let body_table = $("#items-table").find("tbody");
    let product_description = $("#description_automatic_form").val();
    let product_cost = $("#unit_cost_automatic_form").val();
    let product_quantity = $("#quantity_automatic_form").val();
    if (!validateQuantity(product_quantity)) {
        alert("Erro. Quantidade do produto inválida.");
        return;
    }
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

    let button_remove = $("<button>")
        .addClass("btn btn-danger")
        .attr("type", "button")
        .attr("id", "buttonRemove")
        .click(removeLine);

    let i_remove = $("<i>").addClass("glyphicon glyphicon-remove");
    let span_remove = $("<span>").text("Remover");

    button_remove.append(i_remove);
    button_remove.append(span_remove);
    column_remove.append(button_remove);


    line.append(column_id);
    line.append(column_description);
    line.append(column_price);
    line.append(column_quantity);
    line.append(column_total);
    line.append(column_remove);
    line.append(column_edit);

    return line;
}

function removeLine() {
    $(this).parent().parent().remove();
}

function populateCategories() {
    $.get(CATEGORY_URL, function (response) {
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

        $.getJSON(PRODUCT_BY_CODE_URL + code, function (response) {

            if (!("error" in response)) {
                //Update the fields with the fetched value
                $("#description_automatic_form").val(response.description);
                $("#unit_cost_automatic_form").val(response.unit_cost);
                $("#product-id").val(response.id);
            } else {
                alert("Codigo nao encontrado");
            }
        });
    }
);

function changeOrderStatus() {
    $('#stateButton').text($(this).text());
}

function saveItems() {
    let status = $('#stateButton').text();
    if (!validateStatus(status)) {
        alert("Erro. Estado do pagamento inválido.");
        return;
    }
    let items = [];
    let clerk_id = $('#clerk-id').attr('data-url');
    let client_id = $('#client-id').attr('data-url');

    $("tbody>tr").each(function () {
        let product_id = $(this).find("td:nth-child(1)").text();
        let product_quantity = $(this).find("td:nth-child(4)").text();
        let item = {
            product_id: product_id,
            quantity: product_quantity
        };
        items.push(item)
    });

    const order = {
        clerk_id: clerk_id,
        client_id: client_id,
        status: status,
        items: items
    };

    $.ajax({
        url: ORDER_URL,
        data: JSON.stringify(order),
        type: 'POST',
        traditional: true,
        contentType: 'application/json',
        success: function (data) {
            window.location.replace(BASE_APP_URL + data['order_id'] + '/update');
        },
        error: function () {
            alert("Não foi possível salvar o pedido.")
        }
    });


}

function validateQuantity(quantity) {
    return quantity > 0;
}

function validateStatus(status) {
    return status === 'PAGO' || status === 'PENDENTE';
}
