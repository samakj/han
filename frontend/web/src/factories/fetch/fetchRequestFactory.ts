import {
    ErrorHandlerType,
    FetchDispatcherObjectType,
    FetchRequestType,
    RequestHistoryStateType,
    ResponseHandlerType,
} from '@han/factories/fetch/types';
import { KeyedObjectType } from '@han/types/generic-object-types';
import { FetchError, HTTPError } from '@han/factories/fetch/errors';
import { Dispatch } from 'redux';

export const defaultErrorHandler = (response: Response): Response => {
    if (!response.ok) {
        let data = null;

        try {
            data = response.json();
        } catch {}

        throw new HTTPError(response.statusText, response.status, data);
    }

    return response;
};

export const defaultResponseHandler = <ResponseObjectType, HandledResponseType>(
    response: ResponseObjectType,
    // @ts-ignore: Default handler assumes ResponseObjectType = HandledResponseType
): HandledResponseType => response;

export const generateFetchRequest = <ResponseObjectType, PayloadValueType>(
    url: string,
    dispatchers: FetchDispatcherObjectType<PayloadValueType>,
    responseHandler: ResponseHandlerType<
        ResponseObjectType,
        KeyedObjectType<PayloadValueType>
    > = defaultResponseHandler,
    errorHandler: ErrorHandlerType = defaultErrorHandler,
): FetchRequestType => (dispatch: Dispatch): Promise<void> => {
    dispatchers.PENDING(dispatch)(null, url);
    return fetch(url)
        .then(errorHandler)
        .then((response: Response): Promise<ResponseObjectType> => response.json())
        .then((response: ResponseObjectType): void =>
            dispatchers.SUCCESS(dispatch)(responseHandler(response), url, null),
        )
        .catch((error: Error): void => {
            let formattedError = error;

            if (!(error instanceof HTTPError)) {
                formattedError = new FetchError(error.message);
            }

            return dispatchers.ERROR(dispatch)(null, url, formattedError);
        });
};
