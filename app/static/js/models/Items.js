class Items {
    constructor() {
        this._items = [];
    }
    add(item) {
        this._items.push(item);
    }
    remove(item) {
        this._items = this._items.filter(i => i.product_id !== item.product_id);
    }
    toArray() {
        return [].concat(this._items);
    }
}
