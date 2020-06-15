class ProductView {

    private _select: JQuery;

    constructor(selector: string) {
        this._select = $(selector);
    }
    
    public update(model: Products): void {
        this._select.html(this.template(model))
    }

    private template(model: Products): string {
        return `<label for="product_id_manual_form">Produto</label>
        <select class="form-control" id="product_id_manual_form">
            ${model.toArray().map(p => {
            return `<option value="${p.id}" >${p.description}</option>`
        }).join('')}
        </select>`;
    }
}