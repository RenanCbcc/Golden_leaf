
class OrderController {

    private _product_id_manual_form: JQuery;
    private _product_id_automatic_form: JQuery

    private _description_manual_form: JQuery;
    private _description_automatic_form: JQuery

    private _unit_cost_manual_form: JQuery;
    private _unit_cost_automatic_form: JQuery

    private _quantity_manual_form: JQuery;
    private _quantity_automatic_form: JQuery

    private _categories: Category[];
    private _products: Product[];

    private BASE_API_URL = 'http://127.0.0.1:5000/api';
    private CATEGORY_URL = this.BASE_API_URL + '/category';

    constructor() {
        this.populateCategories()
    }
    add(event: Event) {
        this._product_id_manual_form = $("#product_id_manual_form");
        this._product_id_automatic_form = $("#product_id_automatic_form");

        this._unit_cost_manual_form = $("#unit_cost_manual_form");
        this._unit_cost_automatic_form = $("#unit_cost_automatic_form");

        this._description_manual_form = $(this._product_id_manual_form).children("option:selected");
        this._description_automatic_form = $("#description_automatic_form");

        this._quantity_manual_form = $("#quantity_manual_form");
        this._quantity_automatic_form = $("#quantity_automatic_form");

    }

    importCatetegories() {
        function isOK(res: Response) {
            if (res.ok) {
                return res;
            } else {
                throw new Error(res.statusText);
            }
        }
        fetch(this.CATEGORY_URL)
            .then(res => isOK(res))
            .then(res => res.json())
            .then((categories: any[]) => categories.map(c => new Category(c.id, c.title)))
            .catch(err => console.log(err));
    }

    populateCategories() {
        $.get(this.CATEGORY_URL, function (response) {
            let option = '';
            $.each(response, function (index, val) {
                option += '<option value="' + val.id + '">' + val.title + '</option>';
            });
            $("#categories").html(option);
        });
    }

    showAlert(message: string) {
        let alert = $("#order-alert");
        $('#message').text(message)
        //alert.show("fade");

        $('#order-alert-btn').click(function () {
            //alert.hide("fade");
        });

    }
}