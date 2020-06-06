import { Reducer } from 'redux';
import { ActionType, ActionTypeType, StateObjectType } from '@han/store/types';

export const generateUpdateReducer = <PayloadValueType>(
    updateActionType: ActionTypeType,
): Reducer<StateObjectType<PayloadValueType>> => (
    state: StateObjectType<PayloadValueType> = null,
    action: ActionType<PayloadValueType>,
): StateObjectType<PayloadValueType> => {
    if (action.type !== updateActionType) {
        return state;
    }

    return Object.assign({}, state, action.payload);
};

export const generateDeleteReducer = <PayloadValueType>(
    deleteActionType: ActionTypeType,
): Reducer<StateObjectType<PayloadValueType>> => (
    state: StateObjectType<PayloadValueType> = null,
    action: ActionType<PayloadValueType>,
): StateObjectType<PayloadValueType> | undefined => {
    if (action.type !== deleteActionType) {
        return state;
    }

    return undefined;
};

export const generateUpdateDeleteReducer = <PayloadValueType>(
    updateActionType: ActionTypeType,
    deleteActionType: ActionTypeType,
): Reducer<StateObjectType<PayloadValueType>> => (
    state: StateObjectType<PayloadValueType> = null,
    action: ActionType<PayloadValueType>,
): StateObjectType<PayloadValueType> => {
    if (action.type === updateActionType) {
        return Object.assign({}, state, action.payload);
    }
    if (action.type === deleteActionType) {
        return undefined;
    }

    return state;
};
