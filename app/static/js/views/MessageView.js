class MessageView extends View {
    template(model) {
        this._selector.show('slow');
        return `<a id="link-close" href="#" class="close" >&times;</a>
                <p>${model}</p>
                `;
    }
}
