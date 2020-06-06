import { Action } from 'redux';
import { KeyedObjectType, StringKeyedObjectType } from '@han/types/generic-object-types';

export type ActionTypeType = string;

export interface ActionMethodsType {
    [name: string]: string;
}

export interface ActionType<PayloadValueType> extends Action {
    type: ActionTypeType;
    payload?: KeyedObjectType<PayloadValueType>;
}

export interface ActionTypeObjectType {
    [method: string]: ActionTypeType;
}

export interface ActionObjectType<PayloadValueType> {
    [method: string]: (payload?: KeyedObjectType<PayloadValueType>) => ActionType<PayloadValueType>;
}

export type StoreKeyType = string;

export type StateObjectType<StoreValueType> = KeyedObjectType<StoreValueType>;

export type StoreObjectType<StoreValueType> = StringKeyedObjectType<
    StateObjectType<StoreValueType>
>;

export type DispatchFunctionType<PayloadValueType> = (
    payload?: KeyedObjectType<PayloadValueType>,
) => void;
