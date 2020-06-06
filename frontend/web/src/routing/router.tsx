import React from 'react';
import { ConnectedRouter } from 'connected-react-router';
import { StaticRouter, Route, Switch } from 'react-router-dom';

import {
    ClientRouterPropsType,
    RoutesSwitchPropsType,
    RouteType,
    ServerRouterPropsType,
} from '@han/routing/types';
import { routes } from '@han/routing/routes';

export const RoutesSwitch: React.FunctionComponent<RoutesSwitchPropsType> = () => {
    return (
        <Switch>
            {routes.map(
                (route: RouteType): JSX.Element => (
                    <Route
                        path={route.path}
                        exact={route.exact || false}
                        component={route.component}
                        key={route.path}
                    />
                ),
            )}
        </Switch>
    );
};

export const ClientRouter: React.FunctionComponent<ClientRouterPropsType> = ({ history }) => {
    return (
        <ConnectedRouter history={history}>
                <RoutesSwitch />
        </ConnectedRouter>
    );
};

export const ServerRouter: React.FunctionComponent<ServerRouterPropsType> = ({
    context,
    location,
}) => {
    return (
        <StaticRouter context={context} location={location}>
            <RoutesSwitch />
        </StaticRouter>
    );
};
