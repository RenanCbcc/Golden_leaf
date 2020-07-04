class CategoryService {

    private readonly BASE_API_URL: string;

    constructor(url: string) {
        this.BASE_API_URL = url;
    }

    importCategories(handler: HandlerFunction): Promise<Category[]> {
        return fetch(this.BASE_API_URL + '/category')
            .then(res => handler(res))
            .then(res => res.json())
            .then((data: any[]) => data.map(c => new Category(c.id, c.title))
            ).catch(error => { throw new Error(error) });
    }
}
