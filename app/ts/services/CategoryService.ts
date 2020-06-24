class CategoryService {

    importCategories(handler: HandlerFunction): Promise<Category[]> {
        return fetch('https://golden-leaf.herokuapp.com/api/category')
            .then(res => handler(res))
            .then(res => res.json())
            .then((data: any[]) => data.map(c => new Category(c.id, c.title))
            ).catch(error => { throw new Error(error) });
    }
}
