import React from 'react';

import { RouteType } from '@han/routing/types';
import { HomePage } from '@han/components/home-page';

export const routes: RouteType[] = [
    {
        path: '/',
        component: HomePage,
        exact: true,
    },
];
