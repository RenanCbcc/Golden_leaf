class Product {
    constructor(_id, _description, _unit_cost) {
        this._id = _id;
        this._description = _description;
        this._unit_cost = _unit_cost;
    }
    get id() {
        return this._id;
    }
    get description() {
        return this._description;
    }
    get unit_cost() {
        return this._unit_cost;
    }
}
