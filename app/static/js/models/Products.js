class Products {
    constructor() {
        this._products = [];
    }
    add(product) {
        this._products.push(product);
    }
    clear() {
        this._products = [];
    }
    find(id) {
        let p = this._products.find(p => p.id == id);
        return p;
    }
    toArray() {
        return [].concat(this._products);
    }
}
