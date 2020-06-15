class Item {
    constructor(_product_id, _description, _price, _quantity) {
        this._product_id = _product_id;
        this._description = _description;
        this._price = _price;
        this._quantity = _quantity;
        this._extended_cost = this._price * this._quantity;
    }
    get product_id() {
        return this.product_id;
    }
    get description() {
        return this._description;
    }
    get price() {
        return this._description;
    }
    get quantity() {
        return this._quantity;
    }
    get extended_cost() {
        return this._extended_cost;
    }
}
