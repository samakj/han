export const sleep = (delay: number): Promise<void> =>
    new Promise((resolve: Function) => (delay != null ? setTimeout(resolve, delay) : resolve()));
