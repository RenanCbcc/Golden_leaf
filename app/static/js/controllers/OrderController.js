var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
class OrderController {
    constructor() {
        this._categories = new Categories();
        this._products = new Products();
        this._items = new Items();
        this.BASE_APP_URL = 'http://127.0.0.1:5000/order/';
        this.BASE_API_URL = 'http://127.0.0.1:5000/api';
        this.CATEGORY_URL = this.BASE_API_URL + '/category';
        this.PRODUCT_BY_CATEGORY_URL = this.BASE_API_URL + '/product/category/';
        this.PRODUCT_BY_CODE_URL = this.BASE_API_URL + '/product/code/';
        this.ORDER_URL = this.BASE_API_URL + '/order';
        this._categoriesView = new CategoryView('#categoriesView');
        this._productsView = new ProductView('#productsView');
        this._itemsView = new ItemView('#itemsView');
        this._messageView = new MessageView('#messageView');
        this.importCategories();
        this._productsView.update(this._products);
        this._itemsView.update(this._items);
    }
    addFromManualForm() {
        let product_id = $('#product_id_manual_form').val();
        let product_quantity = this._quantity_manual_form.val();
        let p = this._products.find(product_id);
        this._unit_cost_manual_form.val('');
        this._quantity_manual_form.val('1');
        this.addItem(product_id, p.description, parseFloat(p.unit_cost), product_quantity);
    }
    addFromAutomaticForm() {
        let product_id = this._product_id_automatic_form.val();
        let product_description = this._description_automatic_form.val();
        let product_cost = this._unit_cost_automatic_form.val();
        let product_quantity = this._quantity_automatic_form.val();
        this._product_code_automatic_form.val('');
        this._product_id_automatic_form.val('');
        this._description_automatic_form.val('');
        this._unit_cost_automatic_form.val('');
        this._quantity_automatic_form.val('1');
        this.addItem(product_id, product_description, product_cost, product_quantity);
    }
    addItem(product_id, description, price, quantity) {
        if (!(quantity > 0)) {
            this._messageView.update("Quantidade do produto inválida.");
            return;
        }
        if (!(price > 0.05)) {
            this._messageView.update("Preço do produto inválido.");
            return;
        }
        const item = new Item(product_id, description, price, quantity);
        this._items.add(item);
        this._itemsView.update(this._items);
    }
    removeItem(id) {
        this._items.remove(parseInt(id));
        this._itemsView.update(this._items);
    }
    searchFromAutomaticForm() {
        let code = this._product_code_automatic_form.val();
        if (code == null || (code.length < 9 || code.length > 13)) {
            this._messageView.update('Código do produto inválido.');
            return;
        }
        this._description_automatic_form.val('...');
        this._unit_cost_automatic_form.val('...');
        this._quantity_automatic_form.val('1');
        function isOK(res) {
            if (res.ok) {
                return res;
            }
            else {
                throw new Error(res.statusText);
            }
        }
        fetch(this.PRODUCT_BY_CODE_URL + code)
            .then(res => isOK(res))
            .then(response => response.json())
            .then(data => {
            this._description_automatic_form.val(data.description);
            this._unit_cost_automatic_form.val(data.unit_cost);
            this._product_id_automatic_form.val(data.id);
        })
            .catch(err => console.log(err));
    }
    importCategories() {
        function isOK(res) {
            if (res.ok) {
                return res;
            }
            else {
                this._messageView.update(res.statusText);
                throw new Error(res.statusText);
            }
        }
        fetch(this.CATEGORY_URL)
            .then(res => isOK(res))
            .then(res => res.json())
            .then((data) => {
            data
                .map(c => new Category(c.id, c.title))
                .forEach(category => this._categories.add(category));
            this._categoriesView.update(this._categories);
        })
            .catch((error) => this._messageView.update(error));
    }
    importProducts(category_id) {
        function isOK(res) {
            if (res.ok) {
                return res;
            }
            else {
                throw new Error(res.statusText);
            }
        }
        fetch(this.PRODUCT_BY_CATEGORY_URL + category_id)
            .then(res => isOK(res))
            .then(res => res.json())
            .then((data) => {
            this._products.clear();
            data
                .map(p => new Product(p.id, p.description, p.unit_cost))
                .forEach(p => this._products.add(p));
            this._productsView.update(this._products);
        })
            .catch((error) => this._messageView.update(error));
    }
    updateUnitcost(product_id) {
        let p = this._products.find(parseInt(product_id));
        this._unit_cost_manual_form.val(p.unit_cost);
    }
    saveItems() {
        if (this._items.isEmpty()) {
            this._messageView.update('Pedido deve ter ao menos um item.');
        }
        const order = {
            clerk_id: $('#clerk-id').attr('data-url'),
            client_id: $('#client-id').attr('data-url'),
            items: this._items.toJson()
        };
        return fetch(this.ORDER_URL, {
            headers: { 'Content-Type': 'application/json' },
            method: 'post',
            body: JSON.stringify(order)
        }).then(response => response.json())
            .then(data => { console.log(data); window.location.replace(this.BASE_APP_URL + data.order_id + '/items'); })
            .catch((error) => this._messageView.update(error));
    }
}
__decorate([
    domInject('#product_id_automatic_form')
], OrderController.prototype, "_product_id_automatic_form", void 0);
__decorate([
    domInject('#description_automatic_form')
], OrderController.prototype, "_description_automatic_form", void 0);
__decorate([
    domInject('#unit_cost_manual_form')
], OrderController.prototype, "_unit_cost_manual_form", void 0);
__decorate([
    domInject('#unit_cost_automatic_form')
], OrderController.prototype, "_unit_cost_automatic_form", void 0);
__decorate([
    domInject('#quantity_manual_form')
], OrderController.prototype, "_quantity_manual_form", void 0);
__decorate([
    domInject('#quantity_manual_form')
], OrderController.prototype, "_quantity_automatic_form", void 0);
__decorate([
    domInject('#product_code_automatic_form')
], OrderController.prototype, "_product_code_automatic_form", void 0);
