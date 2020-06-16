abstract class View<T> {

    protected _selector: JQuery;

    constructor(selector: string) {
        this._selector = $(selector);
    }

    public update(model: T): void {
        this._selector.html(this.template(model))
    }

    protected abstract template(model: T): string;
}