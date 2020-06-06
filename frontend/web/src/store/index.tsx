import { routerMiddleware } from 'connected-react-router';
import { createStore, applyMiddleware, Store } from 'redux';
import { composeWithDevTools } from 'redux-devtools-extension';
import { History } from 'history';

import { loadCombinedReducers } from '@han/store/reducers';
import thunk from 'redux-thunk';

export const loadStore = (preloadedState: object, history: History): Store =>
    createStore(
        loadCombinedReducers(history),
        preloadedState,
        composeWithDevTools(applyMiddleware(routerMiddleware(history), thunk)),
    );
