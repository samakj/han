import { StringKeyedObjectType } from '@han/types/generic-object-types';

export class FetchError extends Error {
    constructor(message: string) {
        super(message);
        this.name = 'FetchError';
    }
}

export class HTTPError extends FetchError {
    statusCode: number;
    data: StringKeyedObjectType<any>;

    constructor(message: string, statusCode: number, data: StringKeyedObjectType<any>) {
        super(message);
        this.name = 'HTTPError';
        this.statusCode = statusCode;
        this.data = data;
    }
}
