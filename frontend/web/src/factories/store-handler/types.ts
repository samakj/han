import {
    ActionMethodsType,
    ActionObjectType,
    ActionType,
    ActionTypeObjectType,
    ActionTypeType,
    DispatchFunctionType,
    StoreKeyType,
    StateObjectType,
    StoreObjectType,
} from '@han/store/types';
import { KeyedObjectType } from '@han/types/generic-object-types';
import { Dispatch, Reducer } from 'redux';
import { FetchDispatcherObjectType } from '@han/factories/fetch/types';

export type ActionGeneratorType<PayloadValueType> = (
    type: ActionTypeType,
) => (payload?: KeyedObjectType<PayloadValueType>) => ActionType<PayloadValueType>;

export interface DispatcherObjectType<PayloadValueType> {
    UPDATE?: (dispatch: Dispatch) => DispatchFunctionType<PayloadValueType>;
    DELETE?: (dispatch: Dispatch) => DispatchFunctionType<PayloadValueType>;
}

export interface StoreMapObjectType<StateValueType> {
    getValue: (state: StoreObjectType<StateValueType>) => StateObjectType<StateValueType>;
    getKeyValue?: (state: StoreObjectType<StateValueType>, key: string | number) => StateValueType;
    getKeysValue?: (
        state: StoreObjectType<StateValueType>,
        keys: string[] | number[],
    ) => StateObjectType<StateValueType>;
}

export interface StoreHandlerObjectType<StoreValueType> {
    storeKey: StoreKeyType;
    actionMethods: ActionMethodsType;
    actionTypes: ActionTypeObjectType;
    actions: ActionObjectType<StoreValueType>;
    reducer: Reducer;
    dispatchers: DispatcherObjectType<StoreValueType>;
    storeMaps: StoreMapObjectType<StoreValueType>;
}
