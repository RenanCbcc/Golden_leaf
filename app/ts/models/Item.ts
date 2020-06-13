class Item {


    constructor(private _product_id: string, private _description: string, private _price: number,
        private _quantity: number, private _extended_cost: number = 0) {
    }

    get product_id(): string {
        return this.product_id
    }

}