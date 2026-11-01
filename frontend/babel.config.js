module.exports = {
  env: {
    production: {
      plugins: ["transform-remove-console"],
    },
    development: {
      plugins: [],
    },
  },
  presets: ["@vue/cli-plugin-babel/preset"],
};
