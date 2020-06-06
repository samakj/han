import {
    FetchActionObjectType,
    FetchDispatcherObjectType,
    FetchStoreHandlerObjectType,
} from '@han/factories/fetch/types';
import { generateActionTypes } from '@han/factories/store-handler/actionTypeFactory';
import {
    externalFetchActionPrefix,
    fetchActionMethods,
    internalFetchActionPrefix,
} from '@han/factories/fetch/constants';
import { generateUpdateReducer } from '@han/factories/store-handler/reducerFactory';
import { generateStoreMaps } from '@han/factories/store-handler/storeMapFactory';
import { generateFetchActionsObject } from '@han/factories/fetch/actionFactory';
import { StoreMapObjectType } from '@han/factories/store-handler/types';
import { Reducer } from 'redux';
import { generateDispatchers } from '@han/factories/fetch/dispatcherFactory';
import { StateObjectType } from '@han/store/types';

export const generateFetchStoreHandler = <StateValueType>(
    storeKey: string,
    internal: boolean = false,
): FetchStoreHandlerObjectType<StateValueType> => {
    const actionPrefix = internal ? internalFetchActionPrefix : externalFetchActionPrefix;
    const actionTypes = generateActionTypes(storeKey, fetchActionMethods, actionPrefix);
    const actions: FetchActionObjectType<StateValueType> = generateFetchActionsObject(
        actionTypes,
        fetchActionMethods,
    );
    const reducer: Reducer<StateObjectType<StateValueType>> = generateUpdateReducer(
        actionTypes.SUCCESS,
    );
    const dispatchers: FetchDispatcherObjectType<StateValueType> = generateDispatchers(actions);
    const storeMaps: StoreMapObjectType<StateValueType> = generateStoreMaps(storeKey);

    return {
        actionTypes,
        actions,
        dispatchers,
        reducer,
        storeKey,
        storeMaps,
        actionMethods: fetchActionMethods,
    };
};
