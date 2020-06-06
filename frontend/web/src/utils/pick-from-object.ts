import { KeyedObjectType } from '@han/types/generic-object-types';

export const pickFromObj = <ObjectValuesType>(
    keys: (string | number)[],
    obj: KeyedObjectType<ObjectValuesType>,
): KeyedObjectType<ObjectValuesType> =>
    keys.reduce(
        (acc: KeyedObjectType<ObjectValuesType>, key: string) => {
            if (obj.hasOwnProperty(key)) {
                acc[key] = obj[key];
            }

            return acc;
        },
        {},
    );
