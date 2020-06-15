class Products {
    constructor() {
        this._products = [];
    }
    add(product) {
        this._products.push(product);
    }
    toArray() {
        return [].concat(this._products);
    }
}
