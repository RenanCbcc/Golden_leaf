function throttle(milliseconds = 500) {
    return function (target: any, key: string, descriptor: PropertyDescriptor) {

        const originalMethod = descriptor.value;
        let timer = 0;

        descriptor.value = function (...args: any[]) {
            clearInterval(timer)
            timer = setTimeout(() => { originalMethod.apply(this, args); }, 500);

        }

        return descriptor;
    }
}