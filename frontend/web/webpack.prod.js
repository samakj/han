const path = require('path');
const plugins = require('./webpack/plugins');
const rules = require('./webpack/rules/prod');
const resolve = require('./webpack/resolve');

module.exports = [
    // Service Worker
    {
        resolve,
        mode: 'production',
        entry: [path.join(__dirname, 'src', 'service-worker', 'index.ts')],
        target: 'node',
        name: 'service-worker',
        output: {
            path: path.join(__dirname, '_prod_build'),
            filename: 'js/service-worker.bundle.js',
            publicPath: '/static/',
        },
        module: {
            rules: [rules.ts, rules.js],
        },
        stats: {
            children: false,
            colors: true,
        },
    },

    // Server
    {
        resolve,
        mode: 'production',
        entry: [path.join(__dirname, 'src', 'server.ts')],
        target: 'node',
        name: 'server',
        output: {
            path: path.join(__dirname, '_prod_build'),
            filename: 'js/server.bundle.js',
            publicPath: '/static/',
        },
        plugins: [plugins.MiniExtractCss],
        module: {
            rules: [rules.ts, rules.js, rules.scss],
        },
        stats: {
            children: false,
            colors: true,
        },
    },

    // Client
    {
        resolve,
        mode: 'production',
        output: {
            path: path.join(__dirname, '_prod_build'),
            chunkFilename: 'js/[name].bundle.js',
            filename: 'js/[name].bundle.js',
            publicPath: '/static/',
        },
        plugins: [...plugins.HtmlWebpackPlugin, plugins.MiniExtractCss, plugins.CopyStatic, plugins.DotEnv],
        module: {
            rules: [rules.ts, rules.js, rules.scss],
        },
        entry: [path.join(__dirname, 'src', 'client.tsx')],
        target: 'web',
        name: 'client',
        stats: {
            children: false,
            colors: true,
        },
        optimization: {
            nodeEnv: 'production',
            splitChunks: {
                cacheGroups: {
                    commons: {
                        test: /[\\/]node_modules[\\/]/,
                        name: 'vendors',
                        chunks: 'initial',
                    },
                },
            },
        },
    },
];
