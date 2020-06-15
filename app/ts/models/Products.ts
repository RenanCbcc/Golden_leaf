class Products {

    private _products: Product[];

    constructor() {
        this._products = [];
    }

    add(product: Product): void {
        this._products.push(product)
    }

    toArray(): Product[] {
        return [].concat(this._products)
    }

}