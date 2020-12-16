class ItemView extends View<Items> {

    protected template(model: Items): string {

        return `
            <table>
                <thead>
                    <tr>
                    
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
                            <td>${i.description}</td>
                            <td>${i.price}</td>
                            <td>${i.quantity}</td>
                            <td>${i.extended_cost}</td>
                            <td>
                                <button type="button" class="btn btn-danger" onClick="controller.removeItem(${i.product_id})">                                    
                                    <span>Remover</span>
                                </button>
                            </td>
                        </tr>
                         
                        ` }).join('')}
                </tbody>
    
                <tfoot>
                        <td colspan="3"></td>
                        <td>${model.total()}</td>
                </tfoot>
            </table>               
            `
    }
}

