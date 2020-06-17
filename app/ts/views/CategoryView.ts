class CategoryView extends View<Categories> {

    protected template(model: Categories): string {
        return `<label for="categories">Categoria</label>
            <select class="form-control" id="categories">
                ${model.toArray().map(c => {
            return `<option value="${c.id}" >${c.title}</option>`
        }).join('')}
            </select>`;
    }
}

