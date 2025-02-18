const path = require('path');

module.exports = {
  mode: 'production',
  entry: './ui/static/js/script.js',
  output: {
    filename: 'script.min.js',
    path: path.resolve(__dirname, 'ui/static/js')
  }
};
