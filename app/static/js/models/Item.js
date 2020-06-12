class Item {

    constructor(product_id, description, price, quantity) {
        this.product_id = product_id;
        this.description = description;
        this.unit_cost = price;
        this.quantity = quantity
        this.extended_cost = 0.0
    }

    get SubTotal() {
        return this.unit_cost * this.quantity;
    }


}