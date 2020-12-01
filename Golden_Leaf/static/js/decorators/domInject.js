function domInject(selector) {
    return function (target, key) {
        let element;
        const getter = function () {
            if (!element) {
                element = $(selector);
            }
            return element;
        };
        Object.defineProperty(target, key, { get: getter });
    };
}
