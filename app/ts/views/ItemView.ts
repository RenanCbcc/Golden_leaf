class ItemView {

    private _selector: JQuery;

    constructor(selector: string) {
        this._selector = $(selector);
    }

    update(model: Items): void {
        this._selector.html(this.template(model))
    }

    private template(model: Items): string {

        return `
        <table class="table table-hover table-bordered">
            <thead>
                <tr>
                    <th scope="col" style="display: none;">Id</th>
                    <th scope="col">Descriçao</th>
                    <th scope="col">Preço</th>
                    <th scope="col">Quantidade</th>
                    <th scope="col">SubTotal</th>
            </tr>
        </thead>

            <tbody>
                ${model.toArray().map(i => {
            return `
                    <tr>
                        <td>${i.product_id}</td>
                        <td>${i.description}</td>
                        <td>${i.price}</td>
                        <td>${i.quantity}</td>
                        <td>${i.extended_cost}</td>
                    </tr>
                     
                    ` }).join('')}
            </tbody>

            <tfoot>
            </tfoot>
        </table>               
        `
    }
}