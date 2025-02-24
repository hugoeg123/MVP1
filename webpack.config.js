const path = require('path');

module.exports = {
  entry: './static/js/components/MedicationAutocomplete.jsx',
  output: {
    filename: 'react_bundle.js',
    path: path.resolve(__dirname, 'static/js/dist'),
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react']
          }
        }
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.jsx']
  },
  mode: 'development'
}