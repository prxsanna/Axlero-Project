// Cube configuration options: https://cube.dev/docs/config
/** @type{ import('@cubejs-backend/server-core').CreateOptions } */
module.exports = {
  driverFactory: () => ({
    type: 'postgres',
  }),

  checkAuth: (req, auth) => {},
};