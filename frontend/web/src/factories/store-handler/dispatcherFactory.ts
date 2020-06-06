import { ActionObjectType, ActionType, DispatchFunctionType } from '@han/store/types';
import { KeyedObjectType } from '@han/types/generic-object-types';
import { DispatcherObjectType } from '@han/factories/store-handler/types';
import { Dispatch } from 'redux';

export const generateDispatchers = <PayloadValueType>(
    actions: ActionObjectType<PayloadValueType>,
): DispatcherObjectType<PayloadValueType> => {
    const dispatchers: DispatcherObjectType<PayloadValueType> = {};

    if (actions.UPDATE) {
        dispatchers.UPDATE = (dispatch: Dispatch): DispatchFunctionType<PayloadValueType> => (
            payload: KeyedObjectType<PayloadValueType>,
        ): ActionType<PayloadValueType> => dispatch(actions.UPDATE(payload));
    }
    if (actions.DELETE) {
        dispatchers.DELETE = (
            dispatch: Dispatch,
        ): DispatchFunctionType<PayloadValueType> => (): ActionType<PayloadValueType> =>
            dispatch(actions.DELETE());
    }

    return dispatchers;
};
