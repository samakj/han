import React from 'react';
import { hydrate } from 'react-dom';
import { ClientRouter } from '@han/routing/router';
import { createBrowserHistory, History } from 'history';

import { App } from '@han/app';
import { tryRegisterServiceWorker } from '@han/service-worker/try-register-service-worker';
// @ts-ignore: Has to be old style for webpack plugin.
import templateParameters from '@han/page-templates/template-parameters';

declare global {
    interface Window {
        __PRELOADED_STATE__: object;
    }
}

const browserHistory: History = createBrowserHistory();

tryRegisterServiceWorker();

hydrate(
    <App preloadedState={window.__PRELOADED_STATE__} history={browserHistory}>
        <ClientRouter history={browserHistory} />
    </App>,
    document.getElementById(templateParameters.appMountId),
);
