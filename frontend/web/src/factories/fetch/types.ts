import { KeyedObjectType } from '@han/types/generic-object-types';
import {
    ActionMethodsType,
    ActionObjectType,
    ActionType,
    ActionTypeObjectType,
    ActionTypeType,
    DispatchFunctionType,
    StoreKeyType,
} from '@han/store/types';
import { Dispatch, Reducer } from 'redux';
import {
    DispatcherObjectType,
    StoreHandlerObjectType,
    StoreMapObjectType,
} from '@han/factories/store-handler/types';

export interface RequestHistoryTimingsType {
    request?: number;
    response?: number;
    duration?: number;
}

export interface RequestHistoryType {
    status: string;
    error?: Error;
    timings: RequestHistoryTimingsType;
}

export interface RequestHistoryStateType {
    [url: string]: RequestHistoryType;
}

export interface FetchActionType<PayloadValueType> extends ActionType<PayloadValueType> {
    url: string;
    error?: Error;
    timestamp?: number;
}

export type FetchActionGeneratorType<PayloadValueType> = (
    type: ActionTypeType,
) => (
    payload?: KeyedObjectType<PayloadValueType>,
    url?: string,
    error?: Error,
) => FetchActionType<PayloadValueType>;

export interface FetchActionObjectType<PayloadValueType>
    extends ActionObjectType<PayloadValueType> {
    [status: string]: (
        payload?: KeyedObjectType<PayloadValueType>,
        url?: string,
        error?: Error,
        timestamp?: number,
    ) => FetchActionType<PayloadValueType>;
}

export type FetchDispatchFunctionType<PayloadValueType> = (
    payload?: KeyedObjectType<PayloadValueType>,
    url?: string,
    error?: Error,
) => void;

export interface FetchDispatcherObjectType<PayloadValueType> {
    PENDING?: (dispatch: Dispatch) => FetchDispatchFunctionType<PayloadValueType>;
    SUCCESS?: (dispatch: Dispatch) => FetchDispatchFunctionType<PayloadValueType>;
    ERROR?: (dispatch: Dispatch) => FetchDispatchFunctionType<PayloadValueType>;
}

export interface FetchStoreHandlerObjectType<StoreValueType> {
    storeKey: StoreKeyType;
    actionMethods: ActionMethodsType;
    actionTypes: ActionTypeObjectType;
    actions: ActionObjectType<StoreValueType>;
    reducer: Reducer;
    dispatchers: FetchDispatcherObjectType<StoreValueType>;
    storeMaps: StoreMapObjectType<StoreValueType>;
}

export type ResponseHandlerType<ResponseObjectType, HandledResponseType> = (
    response: ResponseObjectType,
) => HandledResponseType;

export type ErrorHandlerType = (response: Response) => Response;

export type FetchRequestType = (dispatch: Dispatch) => Promise<void>;
