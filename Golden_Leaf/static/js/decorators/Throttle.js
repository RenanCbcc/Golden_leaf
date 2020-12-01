function throttle(milliseconds = 500) {
    return function (target, key, descriptor) {
        const originalMethod = descriptor.value;
        let timer = 0;
        descriptor.value = function (...args) {
            clearInterval(timer);
            timer = setTimeout(() => { originalMethod.apply(this, args); }, 500);
        };
        return descriptor;
    };
}
