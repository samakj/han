import { deepGet } from '@han/utils/deep-get';
import { pickFromObj } from '@han/utils/pick-from-object';
import { StateObjectType, StoreObjectType } from '@han/store/types';
import { StoreMapObjectType } from '@han/factories/store-handler/types';

export const generateStoreMaps = <StateValueType>(
    storeKey: string,
): StoreMapObjectType<StateValueType> => ({
    getValue: (state: StoreObjectType<StateValueType>): StateObjectType<StateValueType> =>
        deepGet(state, [storeKey]),
    getKeyValue: (state: StoreObjectType<StateValueType>, key: string | number): StateValueType =>
        deepGet(state, [storeKey, key]),
    getKeysValue: (
        state: StoreObjectType<StateValueType>,
        keys: string[],
    ): StateObjectType<StateValueType> => {
        const value = deepGet(state, [storeKey]);

        if (!value) return undefined;

        return pickFromObj(keys, value);
    },
});
