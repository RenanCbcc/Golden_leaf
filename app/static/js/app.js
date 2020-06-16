const controller = new OrderController();
document
    .querySelector('#add-item-btn-manual-form')
    .addEventListener('click', controller.addFromManualForm.bind(controller));
document
    .querySelector('#search-product-btn-automatic-form')
    .addEventListener('click', controller.searchFromAutomaticForm.bind(controller));
document
    .querySelector('#add-product-btn-automatic-form')
    .addEventListener('click', controller.addFromAutomaticForm.bind(controller));
document
    .querySelector('#categories')
    .addEventListener('click', controller.importProducts.bind(controller));
