class Categories {
    constructor() {
        this._categories = [];
    }
    add(category) {
        this._categories.push(category);
    }
    toArray() {
        return [].concat(this._categories);
    }
}
