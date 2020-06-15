class Categories {

    private _categories: Category[];

    constructor() {
        this._categories = [];
    }

    add(category: Category): void {
        this._categories.push(category)
    }

    toArray(): Category[] {
        return [].concat(this._categories)
    }

}