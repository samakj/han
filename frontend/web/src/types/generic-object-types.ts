export interface StringKeyedObjectType<ObjectValueType> {
    [key: string]: ObjectValueType;
}

export interface NumberKeyedObjectType<ObjectValueType> {
    [key: number]: ObjectValueType;
}

export interface KeyedObjectType<ObjectValueType> {
    [key: string]: ObjectValueType;
    [key: number]: ObjectValueType;
}
