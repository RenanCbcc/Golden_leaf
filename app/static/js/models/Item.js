class Item {
    constructor(_product_id, _description, _price, _quantity, _extended_cost = 0) {
        this._product_id = _product_id;
        this._description = _description;
        this._price = _price;
        this._quantity = _quantity;
        this._extended_cost = _extended_cost;
    }
    get product_id() {
        return this.product_id;
    }
}
