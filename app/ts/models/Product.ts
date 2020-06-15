class Product {
    constructor(private _id: number, private _description: string, private _unit_cost: string) { }

    get id() {
        return this._id;
    }

    get description(): string {
        return this._description
    }

    get unit_cost(): string {
        return this._unit_cost;
    }
}