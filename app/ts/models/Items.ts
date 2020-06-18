class Items {
    private _items: Item[];

    constructor() {
        this._items = [];
    }

    add(item: Item): void {
        this._items.push(item);
    }

    remove(id: number): void {
        this._items = this._items.filter(i => i.product_id != id);
    }

    toArray(): Item[] {
        return [].concat(this._items);
    }

}