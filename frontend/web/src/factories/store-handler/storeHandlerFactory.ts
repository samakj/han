import { generateActionsObject } from '@han/factories/store-handler/actionFactory';
import { generateActionTypes } from '@han/factories/store-handler/actionTypeFactory';
import {
    generateUpdateDeleteReducer,
    generateUpdateReducer,
} from '@han/factories/store-handler/reducerFactory';
import { generateStoreMaps } from '@han/factories/store-handler/storeMapFactory';
import {
    DispatcherObjectType,
    StoreHandlerObjectType,
    StoreMapObjectType,
} from '@han/factories/store-handler/types';
import { generateDispatchers } from '@han/factories/store-handler/dispatcherFactory';
import { ActionObjectType, StateObjectType } from '@han/store/types';
import { Reducer } from 'redux';

export const generateUpdateDeleteStoreHandler = <StateValueType>(
    storeKey: string,
): StoreHandlerObjectType<StateValueType> => {
    const actionMethods = { UPDATE: 'UPDATE', DELETE: 'DELETE' };
    const actionTypes = generateActionTypes(storeKey, actionMethods);
    const actions: ActionObjectType<StateValueType> = generateActionsObject(
        actionTypes,
        actionMethods,
    );
    const reducer: Reducer<StateObjectType<StateValueType>> = generateUpdateDeleteReducer(
        actionTypes['UPDATE'],
        actionTypes['DELETE'],
    );
    const dispatchers: DispatcherObjectType<StateValueType> = generateDispatchers(actions);
    const storeMaps: StoreMapObjectType<StateValueType> = generateStoreMaps(storeKey);

    return {
        actions,
        actionMethods,
        actionTypes,
        dispatchers,
        reducer,
        storeMaps,
        storeKey,
    };
};

export const generateUpdateStoreHandler = <StateValueType>(
    storeKey: string,
): StoreHandlerObjectType<StateValueType> => {
    const actionMethods = { UPDATE: 'UPDATE' };
    const actionTypes = generateActionTypes(storeKey, actionMethods);
    const actions: ActionObjectType<StateValueType> = generateActionsObject(
        actionTypes,
        actionMethods,
    );
    const reducer: Reducer<StateObjectType<StateValueType>> = generateUpdateReducer(
        actionTypes['UPDATE'],
    );
    const dispatchers: DispatcherObjectType<StateValueType> = generateDispatchers(actions);
    const storeMaps: StoreMapObjectType<StateValueType> = generateStoreMaps(storeKey);

    return {
        actions,
        actionMethods,
        actionTypes,
        dispatchers,
        reducer,
        storeMaps,
        storeKey,
    };
};
