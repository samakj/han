import {
    ActionTypeType,
    ActionType,
    ActionTypeObjectType,
    ActionObjectType,
    ActionMethodsType,
} from '@han/store/types';
import { KeyedObjectType } from '@han/types/generic-object-types';
import { ActionGeneratorType } from '@han/factories/store-handler/types';

const defaultActionGenerator = <PayloadValueType>(type: ActionTypeType) => (
    payload?: KeyedObjectType<PayloadValueType>,
): ActionType<PayloadValueType> => ({
    payload,
    type,
});

export const generateActionsObject = <PayloadValueType>(
    actionKeys: ActionTypeObjectType,
    actionMethods: ActionMethodsType,
    actionGenerator?: ActionGeneratorType<PayloadValueType>,
): ActionObjectType<PayloadValueType> =>
    Object.keys(actionMethods).reduce(
        (
            acc: ActionObjectType<PayloadValueType>,
            actionMethod: string,
        ): ActionObjectType<PayloadValueType> => {
            acc[actionMethod] = (actionGenerator || defaultActionGenerator)(
                actionKeys[actionMethod],
            );
            return acc;
        },
        {},
    );
