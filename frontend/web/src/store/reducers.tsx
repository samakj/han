import { History } from 'history';
import { combineReducers, Reducer } from 'redux';
import { connectRouter } from 'connected-react-router';
import { fetchRequestHistoryStoreHandler } from '@han/store/handlers/fetch-request-history';

export const loadCombinedReducers = (history: History): Reducer =>
    combineReducers({
        router: connectRouter(history),
        [fetchRequestHistoryStoreHandler.storeKey]: fetchRequestHistoryStoreHandler.reducer,
    });
