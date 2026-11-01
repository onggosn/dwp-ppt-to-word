const { defineConfig } = require("@vue/cli-service");
const path = require("path");
const fs = require("fs");
// POC mode (npm run serve-poc): fill everything .env.poc does not set from .env.development
const isPoc = process.env.VUE_APP_POC_MOCK === "true";
if (isPoc) {
  const devEnv = path.resolve(__dirname, ".env.development");
  if (fs.existsSync(devEnv)) {
    for (const line of fs.readFileSync(devEnv, "utf8").split(/\r?\n/)) {
      const m = line.match(/^\s*([\w.-]+)\s*=\s*(.*?)\s*$/);
      if (m && process.env[m[1]] === undefined) {
        process.env[m[1]] = m[2].replace(/^["']|["']$/g, "");
      }
    }
  }
}
module.exports = defineConfig({
  transpileDependencies: true,
  productionSourceMap: false,
  configureWebpack: {
    devtool: process.env.VUE_APP_MODE === "production" ? false : undefined,
    // devtool: false,
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "src"),
        "@v2": path.resolve(__dirname, "src/v2"),
        "@omPro": path.resolve(__dirname, "src/v2/modules/omPro"),
      },
    },
  },
  devServer: {
    // POC: conversion backend backend/app.py
    proxy: isPoc
      ? {
          "/poc-api": {
            target: process.env.POC_API_TARGET || "http://localhost:5003",
            pathRewrite: { "^/poc-api": "/api/poc" },
          },
        }
      : undefined,
    // host: "devdigi.corp.bi.go.id",
    // port: 443,
    // https: {
    //   key: fs.readFileSync(
    //     path.resolve("/Users/gilang/certs/devdigi.corp.bi.go.id+1-key.pem")
    //   ),
    //   cert: fs.readFileSync(
    //     path.resolve("/Users/gilang/certs/devdigi.corp.bi.go.id+1.pem")
    //   ),
    // },
    allowedHosts: [
      // "devdigiworkplace.corp.bi.go.id",
      // "digiworkplacetest.corp.bi.go.id",
      // "digiworkplace.corp.bi.go.id",
      // "digiworkplace.bi.go.id",
      "*.bi.go.id",
      "localhost:8010",
    ],
  },
  pluginOptions: {
    vuetify: {
      undefined,
    },
  },
  chainWebpack: (config) => {
    config.plugin("define").tap(([definitions]) => {
      definitions["__VUE_OPTIONS_API__"] = JSON.stringify(true);
      definitions["__VUE_PROD_DEVTOOLS__"] = JSON.stringify(false);
      definitions["__VUE_PROD_HYDRATION_MISMATCH_DETAILS__"] =
        JSON.stringify(false);
      return [definitions];
    });
  },
});
