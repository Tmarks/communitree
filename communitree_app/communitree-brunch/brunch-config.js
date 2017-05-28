module.exports = {
  // See http://brunch.io for documentation.

  npm: {styles: {leaflet: ['dist/leaflet.css']}},

  files: {
    javascripts: {joinTo: 'app.js'},
    stylesheets: {joinTo: 'app.css'},
    templates: {joinTo: 'app.js'}
  },

  paths: {
    public: '../static/communitree_app'
  },

  plugins: {
    autoReload: {enabled: false}
  }
}
