import {
    ActionTypeType,
    ActionTypeObjectType,
    ActionObjectType,
    ActionMethodsType,
} from '@han/store/types';
import { KeyedObjectType } from '@han/types/generic-object-types';
import {
    FetchActionGeneratorType,
    FetchActionObjectType,
    FetchActionType,
} from '@han/factories/fetch/types';

const defaultFetchActionGenerator = <PayloadValueType>(type: ActionTypeType) => (
    payload?: KeyedObjectType<any>,
    url?: string,
    error?: Error,
    timestamp?: number,
): FetchActionType<PayloadValueType> => ({
    payload,
    error,
    url,
    type,
    timestamp: timestamp || +new Date(),
});

export const generateFetchActionsObject = <PayloadValueType>(
    actionKeys: ActionTypeObjectType,
    actionMethods: ActionMethodsType,
    actionGenerator?: FetchActionGeneratorType<PayloadValueType>,
): FetchActionObjectType<PayloadValueType> =>
    Object.keys(actionMethods).reduce(
        (
            acc: FetchActionObjectType<PayloadValueType>,
            actionMethod: string,
        ): FetchActionObjectType<PayloadValueType> => {
            acc[actionMethod] = (actionGenerator || defaultFetchActionGenerator)(
                actionKeys[actionMethod],
            );
            return acc;
        },
        {},
    );
