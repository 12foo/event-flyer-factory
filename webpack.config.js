var webpack = require("webpack");
var ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
    entry: ["./frontend/js/factory", "./frontend/css/style.less"],
    output: {
        path: __dirname + "/static",
        filename: "factory.js",
        publicPath: "/static/"
    },
    module: {
        loaders: [
            { test: /\.coffee$/, loader: "coffee-loader" },
            { test: /\.less$/, loader: ExtractTextPlugin.extract("css!less") },
            { test: /\.(ttf|eot|svg|woff(2)?)(\?[a-z0-9]+)?$/, loader: "file?name=[name].[ext]" }
        ]
    },
    plugins: [
        new webpack.ProvidePlugin({
            "m": "mithril",
            "_": "lodash"
        }),
        new ExtractTextPlugin("factory.css"),
        new webpack.ContextReplacementPlugin(/moment[\/\\]locale$/, /en$/)
    ],
    resolve: {
        modulesDirectories: ["./frontend/js", "./node_modules"],
        extensions: ["", ".coffee", ".webpack.js", ".web.js", ".js"]
    }
}
