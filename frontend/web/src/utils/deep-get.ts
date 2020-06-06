export const deepGet = (
    obj: object,
    keys: (string | number)[],
    defaultValue: any = undefined,
): any => {
    let result = obj;

    for (const key of keys) {
        if (!result || !result.hasOwnProperty(key)) {
            return defaultValue;
        }

        // @ts-ignore -> obj depth is unknown so cant provide proper typing
        result = result[key];
    }

    return result;
};
