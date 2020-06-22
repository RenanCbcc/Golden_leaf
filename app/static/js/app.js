const controller = new OrderController();
$(document).on('click', '#add-item-btn-manual-form', controller
    .addFromManualForm.bind(controller));
$(document).on('click', '#search-product-btn-automatic-form', controller
    .searchFromAutomaticForm.bind(controller));
$(document).on('click', '#add-product-btn-automatic-form', controller
    .addFromAutomaticForm.bind(controller));
