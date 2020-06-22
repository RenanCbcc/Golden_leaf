class Products {

    private _products: Product[];

    constructor() {
        this._products = [];
    }


    add(product: Product): void {
        this._products.push(product)
    }

    clear(): void {
        this._products = [];
    }

    find(id: number): Product {
        let p = this._products.find(p => p.id == id);
        return p;
    }
    toArray(): Product[] {
        return [].concat(this._products)
    }

}