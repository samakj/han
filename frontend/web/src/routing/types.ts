import React from 'react';
import { History } from 'history';

export interface RouteType {
    path: string;
    component: React.ComponentClass<any, any> | React.FunctionComponent<any>;
    exact: boolean;
}

export interface RoutesSwitchPropsType {}

export interface ClientRouterPropsType {
    history: History;
}

export interface ServerRouterPropsType {
    context: object;
    location: string;
}
