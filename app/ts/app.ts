const controller = new OrderController();

document
    .querySelector('#add-product-btn-manual-form')
    .addEventListener('click',controller.add.bind(controller));