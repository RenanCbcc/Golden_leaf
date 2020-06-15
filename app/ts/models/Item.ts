class Item {

    private _extended_cost: number;

    constructor(private _product_id: number, private _description: string, private _price: number,
        private _quantity: number) {
        this._extended_cost = this._price * this._quantity;
    }

    get product_id(): string {
        return this.product_id
    }

    get description(): string {
        return this._description
    }

    get price(): string {
        return this._description
    }

    get quantity(): number {
        return this._quantity
    }

    get extended_cost(): number {
        return this._extended_cost
    }

}