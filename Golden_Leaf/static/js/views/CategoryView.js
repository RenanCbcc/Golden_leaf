class CategoryView extends View {
    template(model) {
        return `<label class="label" for="categories">Categoria</label>
            <select class="form" id="categories" onchange="controller.importProducts(value)">
                ${model.toArray().map(c => {
            return `<option value="${c.id}" >${c.title}</option>`;
        }).join('')}
            </select>`;
    }
}
