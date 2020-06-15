class Category {

    constructor(private _id: string, private _title: string) { }

    get id(): string {
        return this._id;
    }

    get title(): string {
        return this._title;
    }
}