class Items {
    constructor() {
        this._items = [];
    }
    add(item) {
        this._items.push(item);
    }
    remove(id) {
        this._items = this._items.filter(i => i.product_id != id);
    }
    toArray() {
        return [].concat(this._items);
    }
}
