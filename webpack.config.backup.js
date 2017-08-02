var webpack = require('webpack');
var path = require('path');

var BUILD_DIR = './client/static/js';	// bundle.js path
var APP_DIR = 'client';		// react application's codebase


var webpack_config = {
  entry: './client/entry.js',
  output: {
    path: BUILD_DIR,
    filename: 'bundle.js'
  },
  module: {
  	loaders: [
  		{
    		test: /\.jsx?$/,
        exclude: /(node_modules|bower_components)/,
        loaders: [
          'react-hot',
          'babel?presets[]=react,presets[]=es2015,presets[]=stage-0'
        ]

  		}
  	]
  }
};

module.exports = webpack_config;


