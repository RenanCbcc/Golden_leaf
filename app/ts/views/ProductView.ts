class ProductView extends View<Products> {

    protected template(model: Products): string {
        return `<label for="product_id_manual_form">Produto</label>
        <select class="form-control" id="product_id_manual_form">
            ${model.toArray().map(p => {
            return `<option value="${p.id}" >${p.description}</option>`
        }).join('')}
        </select>`;
    }
}