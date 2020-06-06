import { renderToString } from 'react-dom/server';
import React from 'react';
import { Request, Response } from 'express';
import { matchPath, match } from 'react-router-dom';
import { createMemoryHistory, MemoryHistory } from 'history';
import fs from 'fs';
import cheerio from 'cheerio';

import { routes } from '@han/routing/routes';
import { RouteType } from '@han/routing/types';
import { ServerRouter } from '@han/routing/router';
import { App } from '@han/app';
// @ts-ignore: Has to be old style for webpack plugin.
const routeTemplates = require('@han/page-templates/route-templates');
// @ts-ignore: Has to be old style for webpack plugin.
import templateParameters from '@han/page-templates/template-parameters';

const getRouteMatch = (url: string): match =>
    routes.reduce((acc: match, route: RouteType): match => matchPath(url, route) || acc, null);

const getPreloadedState = (noSSR: boolean = false): Promise<object> =>
    new Promise((resolve: Function) => (noSSR ? resolve({}) : resolve({ test: 123 })));

const renderFullPage = (path: string, htmlToInject: string, preloadedState: object): string => {
    const html: string = fs.readFileSync(`public/html/${routeTemplates[path].ssrTemplate}`).toString();
    const $ = cheerio.load(html);

    $(`#${templateParameters.appMountId}`).html(htmlToInject);
    $('body').append(`
        <script id="preloaded-state">
            window.__PRELOADED_STATE__ = ${JSON.stringify(preloadedState).replace(/</g, '\\\u003c')}
            var el = document.getElementById('preloaded-state')
            el.parentElement.removeChild(el)
        </script>
    `);

    return $.html();
};

export const getPageSource = (request: Request, response: Response): Promise<Response> => {
    const routeMatch: match = getRouteMatch(request.path);

    if (!routeMatch) {
        console.error(`'${request.url}' didn't match any endpoint in routes.`);
        response.status(404).json({
            status_code: 404,
            error_type: 'PAGE_NOT_FOUND',
        });
        return;
    }

    return getPreloadedState(request.query['noSSR'])
        .then(
            (preloadedState: object): Response => {
                const context = {};
                const history: MemoryHistory = createMemoryHistory({
                    initialEntries: [routeMatch.path],
                });

                return response.status(200).send(
                    renderFullPage(
                        routeMatch.path,
                        renderToString(
                            <App preloadedState={preloadedState} history={history}>
                                <ServerRouter context={context} location={request.url} />
                            </App>,
                        ),
                        preloadedState,
                    ),
                );
            },
        )
        .catch(
            (error): Response => {
                console.error(error);
                return response.status(500).json({
                    status_code: 500,
                    error_type: 'SERVER_ERROR',
                });
            },
        );
};
