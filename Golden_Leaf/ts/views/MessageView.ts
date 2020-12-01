class MessageView extends View<string> {

    protected template(model: string): string {
        this._selector.show('slow');
        return `<a id="link-close" href="#" class="close" >&times;</a>
                    <p>${model}</p>
                    `;
    }
}
