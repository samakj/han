import React from 'react';
import { Store } from 'redux';
import { History } from 'history';
import { Provider } from 'react-redux';

import { loadStore } from '@han/store';
import '@han/components/styles/default.scss';
import { Navigation } from '@han/components/navigation';

export interface AppPropsType {
    preloadedState: object;
    history: History;
}

export const App: React.FunctionComponent<AppPropsType> = ({
    children,
    preloadedState,
    history,
}) => {
    const store: Store = loadStore(preloadedState, history);

    return (
        <Provider store={store}>
            <div className="page-wrapper">
                <Navigation />
                {children}
            </div>
        </Provider>
    );
};
