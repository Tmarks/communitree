module.exports = {
  // See http://brunch.io for documentation.
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
