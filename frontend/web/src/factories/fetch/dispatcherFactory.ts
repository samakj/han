import { KeyedObjectType } from '@han/types/generic-object-types';
import {
    FetchActionObjectType,
    FetchActionType,
    FetchDispatcherObjectType,
    FetchDispatchFunctionType,
} from '@han/factories/fetch/types';
import { Dispatch } from 'redux';

export const generateDispatchers = <PayloadValueType>(
    actions: FetchActionObjectType<PayloadValueType>,
): FetchDispatcherObjectType<PayloadValueType> => {
    return {
        PENDING: (dispatch: Dispatch): FetchDispatchFunctionType<PayloadValueType> => (
            payload?: KeyedObjectType<PayloadValueType>,
            url?: string,
            error?: Error,
        ): FetchActionType<PayloadValueType> => dispatch(actions.PENDING(payload, url, error)),
        SUCCESS: (dispatch: Dispatch): FetchDispatchFunctionType<PayloadValueType> => (
            payload?: KeyedObjectType<PayloadValueType>,
            url?: string,
            error?: Error,
        ): FetchActionType<PayloadValueType> => dispatch(actions.SUCCESS(payload, url, error)),
        ERROR: (dispatch: Dispatch): FetchDispatchFunctionType<PayloadValueType> => (
            payload?: KeyedObjectType<PayloadValueType>,
            url?: string,
            error?: Error,
        ): FetchActionType<PayloadValueType> => dispatch(actions.ERROR(payload, url, error)),
    };
};
