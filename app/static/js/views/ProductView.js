class ProductView {
    constructor(selector) {
        this._select = $(selector);
    }
    update(model) {
        this._select.html(this.template(model));
    }
    template(model) {
        return `<label for="product_id_manual_form">Produto</label>
        <select class="form-control" id="product_id_manual_form">
            ${model.toArray().map(p => {
            return `<option value="${p.id}" >${p.description}</option>`;
        }).join('')}
        </select>`;
    }
}
