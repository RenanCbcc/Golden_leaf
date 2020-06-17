class Items {
    private _items: Item[];

    constructor() {
        this._items = [];
    }

    add(item: Item) {
        this._items.push(item);
    }

    remove(item: number) {
        this._items = this._items.filter(i => i.product_id !== item);
    }

    toArray(): Item[] {
        return [].concat(this._items);
    }

}