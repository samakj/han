import { defaultActionPrefix } from '@han/factories/store-handler/constants';

import { ActionMethodsType, ActionTypeObjectType } from '@han/store/types';

export const generateActionTypes = (
    storeKey: string,
    actionMethods: ActionMethodsType,
    actionPrefix?: string,
): ActionTypeObjectType => {
    return Object.keys(actionMethods).reduce(
        (acc: ActionTypeObjectType, method: string): ActionTypeObjectType => {
            const prefix = actionPrefix || defaultActionPrefix;
            // @ts-ignore -> Indexing an enum not working?
            acc[method] = `${prefix}_${storeKey}_${actionMethods[method]}`;
            return acc;
        },
        {},
    );
};
