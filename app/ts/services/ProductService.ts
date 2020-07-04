class ProductService {

    private readonly BASE_API_URL: string;

    constructor(url: string) {
        this.BASE_API_URL = url;
    }

    importProducts(category_id: string, handler: HandlerFunction): Promise<Product[]> {
        return fetch(this.BASE_API_URL + '/product/category/' + category_id)
            .then(res => handler(res))
            .then(res => res.json())
            .then((data: PartialProduct[]) =>
                data.map(p => new Product(p.id, p.description, p.unit_cost))
            )
            .catch(error => { throw new Error(error) });
    }
}