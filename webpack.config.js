var webpack = require('webpack');
var path = require('path');

var BUILD_DIR = './client/static/js';	// bundle.js path
var APP_DIR = 'client';		// react application's codebase


var webpack_config = {
  entry: './client/entry.jsx',
  output: {
    path: BUILD_DIR,
    filename: 'bundle.js'
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  },
  module: {
  	loaders: [
  		{
    		test: /\.jsx?$/,
        exclude: /(node_modules|bower_components)/,
        loader: 'babel-loader',
        query: {
          presets: ['react', 'es2015']
        }
  		}
  	]
  }
};

module.exports = webpack_config;


