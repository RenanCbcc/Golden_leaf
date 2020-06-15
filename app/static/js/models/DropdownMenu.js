class DropdownMenu {
    constructor(dropdown) {
        this.dropdownMenu = dropdown;
        this.options = dropdown.options;
    }
    OnChange() {
        alert(this.options[this.options.selectedIndex].value);
        document.location.href = this.options[this.options.selectedIndex].value;
    }
}
