$(document).ready(function () {
    $("#subimitPayment").click(function (event) {
        let total = $('#totalAmount').attr('data-url');
        let paymentValue = $('#inputValue').val();
        if (paymentValue <= 0 || paymentValue > total) {
            alert('Valor para débito é inválido.');
            $('#inputValue').focus();
            event.preventDefault();

        }
    });
});


