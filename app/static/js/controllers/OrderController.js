class OrderController {
    constructor() {
        this._categories = new Categories();
        this._products = new Products();
        this._items = new Items();
        this.BASE_API_URL = 'http://127.0.0.1:5000/api';
        this.CATEGORY_URL = this.BASE_API_URL + '/category';
        this.PRODUCT_BY_CATEGORY_URL = this.BASE_API_URL + '/product/category/';
        this._categoriesView = new CategoryView('#categoriesView');
        this._productsView = new ProductView('#productsView');
        this._itemsView = new ItemView('#itemsView');
        this.importCategories();
        this._productsView.update(this._products);
        this._itemsView.update(this._items);
        this._product_id_manual_form = $("#product_id_manual_form");
        this._product_id_automatic_form = $("#product_id_automatic_form");
        this._unit_cost_manual_form = $("#unit_cost_manual_form");
        this._unit_cost_automatic_form = $("#unit_cost_automatic_form");
        this._description_manual_form = $(this._product_id_manual_form).children("option:selected");
        this._description_automatic_form = $("#description_automatic_form");
        this._quantity_manual_form = $("#quantity_manual_form");
        this._quantity_automatic_form = $("#quantity_automatic_form");
    }
    add() { }
    addFromManualForm() {
        let product_id = this._product_id_manual_form.val();
        let product_description = this._description_manual_form.text();
        let product_cost = this._unit_cost_manual_form.val();
        let product_quantity = this._quantity_manual_form.val();
        this.addItem(product_id, product_description, product_cost, product_quantity);
        this._itemsView.update(this._items);
    }
    addFromAutomaticForm() {
        let product_id = this._product_id_automatic_form.val();
        let product_description = this._description_automatic_form.val();
        let product_cost = this._unit_cost_automatic_form.val();
        let product_quantity = this._quantity_automatic_form.val();
        this.addItem(product_id, product_description, product_cost, product_quantity);
    }
    addItem(product_id, description, price, quantity) {
        if (!(quantity > 0)) {
            //showAlert("Quantidade do produto inválida.");
            return;
        }
        if (!(price > 0.05)) {
            //showAlert("Preço do produto inválido.")
            return;
        }
        const item = new Item(product_id, description, price, quantity);
        this._items.add(item);
    }
    importCategories() {
        function isOK(res) {
            if (res.ok) {
                return res;
            }
            else {
                throw new Error(res.statusText);
            }
        }
        fetch(this.CATEGORY_URL)
            .then(res => isOK(res))
            .then(res => res.json())
            .then((categories) => {
            categories
                .map(c => new Category(c.id, c.title))
                .forEach(category => this._categories.add(category));
            this._categoriesView.update(this._categories);
        })
            .catch(err => console.log(err));
    }
    importProducts() {
        function isOK(res) {
            if (res.ok) {
                return res;
            }
            else {
                throw new Error(res.statusText);
            }
        }
        fetch(this.PRODUCT_BY_CATEGORY_URL)
            .then(res => isOK(res))
            .then(res => res.json())
            .then((data) => {
            data
                .map(p => new Product(p.id, p.description, p.unit_cost))
                .forEach(p => this._products.add(p));
            this._productsView.update(this._products);
        })
            .catch(err => console.log(err));
    }
}
