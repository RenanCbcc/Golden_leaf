class View {
    constructor(selector) {
        this._selector = $(selector);
    }
    update(model) {
        this._selector.html(this.template(model));
    }
}
