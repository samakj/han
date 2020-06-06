import React, { useState } from 'react';

import '@han/components/home-page/style.scss';
import { HomePagePropsType } from '@han/components/home-page/types';

export const HomePage: React.FunctionComponent<HomePagePropsType> = ({}) => {
    return (
        <main className="home-page page-width-wrapper">
            <h1>Home Page</h1>
        </main>
    );
};
