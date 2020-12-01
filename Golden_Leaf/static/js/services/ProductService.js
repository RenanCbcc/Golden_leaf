class ProductService {
    constructor(url) {
        this.BASE_API_URL = url;
    }
    importProducts(category_id, handler) {
        return fetch(this.BASE_API_URL + '/product/category/' + category_id)
            .then(res => handler(res))
            .then(res => res.json())
            .then((data) => data.map(p => new Product(p.id, p.description, p.unit_cost)))
            .catch(error => { throw new Error(error); });
    }
}
