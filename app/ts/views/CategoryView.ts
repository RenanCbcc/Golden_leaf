class CategoryView {

    private _select: JQuery;

    constructor(selector: string) {
        this._select = $(selector);
    }

    update(model: Categories): void {
        this._select.html(this.template(model))
    }

    private template(model: Categories): string {
        return `<label for="categories">Categoria</label>
        <select class="form-control" id="categories">
            ${model.toArray().map(c => {
            return `<option value="${c.id}" >${c.title}</option>`
        }).join('')}
        </select>`;
    }
}