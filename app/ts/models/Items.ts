class Items {
    private _items: Item[];

    constructor() {
        this._items = [];
    }

    add(item: Item) {
        this._items.push(item);
    }

    remove(item: Item) {
        this._items = this._items.filter(i => i.product_id !== item.product_id);
    }

    toArray(): Item[] {
        return [].concat(this._items);
    }

}