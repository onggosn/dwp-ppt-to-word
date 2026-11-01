const path = require('path');
const TerserPlugin = require('terser-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin'); // <--- 1. Import Plugin

module.exports = {
    mode: 'production',
    entry: './src/ckeditor-inline.ts',
    output: {
        path: path.resolve(__dirname, 'build'),
        filename: 'ckeditor-inline.js',
        library: {
            name: 'CKEditorCS',
            type: 'umd',
            export: 'default'
        },
        clean: false
    },
    module: {
        rules: [
            {
                test: /\.(ts|js)$/,
                use: 'ts-loader',
                exclude: /node_modules/
            },
            {
                test: /\.css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader'
                ]
            },
            {
                resourceQuery: /raw/,
                type: 'asset/source',
            }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: 'ckeditor-inline.css'
        })
    ],
    resolve: {
        extensions: ['.ts', '.js', '.json']
    },
    optimization: {
        minimizer: [
            new TerserPlugin({
                extractComments: false,
                terserOptions: {
                    output: { comments: false },
                },
            }),
        ],
    },
    performance: { hints: false }
};