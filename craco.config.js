const TerserPlugin = require('terser-webpack-plugin');

module.exports = {
  webpack: {
    configure: (webpackConfig) => {
      if (webpackConfig.mode === 'production') {
        webpackConfig.optimization.minimizer = [
          new TerserPlugin({
            extractComments: false,
            terserOptions: {
              format: {
                comments: false,
              },
              compress: {
                drop_console: true,
                drop_debugger: true,
              },
            },
          }),
        ];
      }
      return webpackConfig;
    },
  },
};
