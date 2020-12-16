class ProductView extends View {
    template(model) {
        return `<label class="label" for="product_id_manual_form">Produto</label>
            <select class="form" id="product_id_manual_form" 
                onchange="controller.updateUnitcost(value)">
                ${model.toArray().map(p => {
            return `<option value="${p.id}" >${p.description}</option>`;
        }).join('')}
            </select>`;
    }
}
