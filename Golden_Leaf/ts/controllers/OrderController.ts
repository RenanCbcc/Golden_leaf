class OrderController {

    @domInject('#product_id_automatic_form')
    private _product_id_automatic_form: JQuery

    @domInject('#description_automatic_form')
    private _description_automatic_form: JQuery

    @domInject('#unit_cost_manual_form')
    private _unit_cost_manual_form: JQuery;

    @domInject('#unit_cost_automatic_form')
    private _unit_cost_automatic_form: JQuery

    @domInject('#quantity_manual_form')
    private _quantity_manual_form: JQuery;

    @domInject('#quantity_manual_form')
    private _quantity_automatic_form: JQuery

    @domInject('#product_code_automatic_form')
    private _product_code_automatic_form: JQuery;


    private _categories = new Categories();
    private _products = new Products();
    private _items = new Items();

    private BASE_APP_URL = '/order/';
    private BASE_API_URL = '/api';
    private PRODUCT_BY_CODE_URL = this.BASE_API_URL + 'api/product/code/';
    private ORDER_URL = this.BASE_API_URL + 'api/order';

    private _categoriesView = new CategoryView('#categoriesView');
    private _productsView = new ProductView('#productsView');
    private _itemsView = new ItemView('#itemsView');
    private _messageView = new MessageView('#messageView');

    private _categoryService = new CategoryService(this.BASE_API_URL);
    private _productService = new ProductService(this.BASE_API_URL);

    constructor() {
        this.importCategories();
        this._productsView.update(this._products);
        this._itemsView.update(this._items);
    }

    @throttle()
    addFromManualForm() {
        let product_id = <number>$('#product_id_manual_form').val();
        let product_quantity = <number>this._quantity_manual_form.val();
        let p = this._products.find(product_id);

        this._unit_cost_manual_form.val('');
        this._quantity_manual_form.val('1');
        this.addItem(product_id, p.description, parseFloat(p.unit_cost), product_quantity);
    }

    @throttle()
    addFromAutomaticForm() {
        let product_id = <number>this._product_id_automatic_form.val();
        let product_description = <string>this._description_automatic_form.val();
        let product_cost = <number>this._unit_cost_automatic_form.val();
        let product_quantity = <number>this._quantity_automatic_form.val();

        this._product_code_automatic_form.val('');
        this._product_id_automatic_form.val('');
        this._description_automatic_form.val('');
        this._unit_cost_automatic_form.val('');
        this._quantity_automatic_form.val('1');

        this.addItem(product_id, product_description, product_cost, product_quantity);

    }


    private addItem(product_id: number, description: string, price: number, quantity: number) {

        if (this._items.contains(product_id)) {
            this._messageView.update('Produto já existe na listagem de items!');
            return;
        }
        if (!(quantity > 0)) {
            this._messageView.update("Quantidade do produto inválida!");
            return;
        }

        if (!(price > 0.05)) {
            this._messageView.update("Preço do produto inválido!");
            return;
        }

        const item = new Item(
            product_id,
            description,
            price,
            quantity);


        this._items.add(item);
        this._itemsView.update(this._items);
    }

    removeItem(id: string) {
        this._items.remove(parseInt(id));
        this._itemsView.update(this._items);
    }

    @throttle()
    searchFromAutomaticForm() {
        let code = <string>this._product_code_automatic_form.val();

        if (code == null || (code.length < 9 || code.length > 13)) {
            this._messageView.update('Código do produto inválido.');
            return;
        }

        this._description_automatic_form.val('...');
        this._unit_cost_automatic_form.val('...');
        this._quantity_automatic_form.val('1');

        function isOK(res: Response) {
            if (res.ok) {
                return res;
            } else {
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
            .catch(err => this._messageView.update(err));
    }


    private isOK(res: Response) {
        if (res.ok) {
            return res;
        } else {
            this._messageView.update(res.statusText);
            throw new Error(res.statusText);
        }
    }

    private importCategories() {

        this._categoryService
            .importCategories(this.isOK)
            .then(Categories => {
                Categories.forEach(category => this._categories.add(category))
                this._categoriesView.update(this._categories);
            }).catch(error => { this._messageView.update("Não foi possível importar categorias.") });

    }

    importProducts(category_id: string) {
        this._productService
            .importProducts(category_id, this.isOK)
            .then(products => {
                this._products.clear();
                products.forEach(p => this._products.add(p))
                this._productsView.update(this._products);
            }).catch(error => { this._messageView.update("Não foi possível importar produtos.") });

    }

    updateUnitcost(product_id: string) {
        let p = this._products.find(parseInt(product_id));
        this._unit_cost_manual_form.val(p.unit_cost);
    }

    @throttle()
    saveItems() {
        if (this._items.isEmpty()) {
            this._messageView.update('Pedido deve ter ao menos um item.');
        }
        var token = localStorage.getItem('token');
        const order = {
            token: token,
            items: this._items.toJson()
        };


        var headers = new Headers();
        headers.append('Content-Type', 'application/json');
        //headers.append('Authorization', 'Basic ' + btoa(token + ':'));

        var requestOptions = {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(order)
        };

        return fetch(this.ORDER_URL, requestOptions)
            .then(response => this.isOK(response))
            .then(response => response.json())
            .then(result => {
                localStorage.clear();
                window.location.replace(this.BASE_APP_URL + result.order_id + '/items')
            })
            .catch((error) => this._messageView.update("Não foi possível salvar o pedido."));
    }


}