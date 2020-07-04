class CategoryService {
    constructor(url) {
        this.BASE_API_URL = url;
    }
    importCategories(handler) {
        return fetch(this.BASE_API_URL + '/category')
            .then(res => handler(res))
            .then(res => res.json())
            .then((data) => data.map(c => new Category(c.id, c.title))).catch(error => { throw new Error(error); });
    }
}
