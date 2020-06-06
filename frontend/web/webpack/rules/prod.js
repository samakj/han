var path = require('path');
var MCEP = require('mini-css-extract-plugin');

module.exports = {
    ts: {
        test: /\.tsx?$/,
        use: [
            {
                loader: 'awesome-typescript-loader',
            },
        ],
        include: path.join(__dirname, '..', '..', 'src'),
        exclude: /node_modules/,
    },
    js: {
        test: /\.jsx?$/,
        use: [
            {
                loader: 'babel-loader',
                options: {
                    presets: ['@babel/preset-env'],
                },
            },
        ],
        include: path.join(__dirname, '..', '..', 'src'),
        exclude: /node_modules/,
    },
    scss: {
        test: /\.(sc|c)ss$/,
        use: [
            MCEP.loader,
            {
                loader: 'css-loader',
            },
            {
                loader: 'sass-loader',
            },
        ],
        include: path.join(__dirname, '..', '..', 'src'),
        exclude: /node_modules/,
    },
};
