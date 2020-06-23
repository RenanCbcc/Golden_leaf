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

    contains(id: number): boolean {
        const found = this._items.find(i => i.product_id == id);
        return found != null;
    }

    toArray(): Item[] {
        return [].concat(this._items);
    }

    toJson(): object[] {
        let items: Object[] = [];
        this._items.forEach(i => {
            let item = {
                product_id: i.product_id,
                quantity: i.quantity
            };
            items.push(item)
        })
        return items;
    }

    isEmpty(): boolean {
        return this._items.length == 0;
    }

}