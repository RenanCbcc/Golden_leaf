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
    contains(id) {
        const found = this._items.find(i => i.product_id == id);
        return found != null;
    }
    toArray() {
        return [].concat(this._items);
    }
    toJson() {
        let items = [];
        this._items.forEach(i => {
            let item = {
                product_id: i.product_id,
                quantity: i.quantity
            };
            items.push(item);
        });
        return items;
    }
    isEmpty() {
        return this._items.length == 0;
    }
}
