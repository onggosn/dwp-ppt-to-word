import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import Shimmer from "vue3-shimmer";
import { loadFonts } from "./plugins/webfontloader";
import filters from "./helpers/filters";
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import Vue3Progress from "vue3-progress";
import { SnackbarService, Vue3Snackbar } from "vue3-snackbar";
import Vue3Sanitize from "vue-3-sanitize";
import VueApexCharts from "vue3-apexcharts";
import { checkAppVersion } from "./v2/helpers/appVersion";
import { installPocMock } from "./v2/poc/pocMock";

// Toastification
import Toast, { POSITION } from "vue-toastification";
import "vue-toastification/dist/index.css";
import type { PluginOptions } from "vue-toastification";

// // APM ELASTIC
// import { init as initApm } from "@elastic/apm-rum";

// const apm = initApm({
//   serviceName: process.env.VUE_APP_ELA_SERVICE_NAME,
//   serverUrl: process.env.VUE_APP_ELA_SERVER_URL,
//   environment: process.env.VUE_APP_ELA_ENV,
// });

checkAppVersion();
installPocMock(store);

const options = {
  position: "fixed",
  height: "6px",
};

loadFonts();

declare module "@vue/runtime-core" {
  interface ComponentCustomProperties {
    $store: store;
  }
}
/* eslint-disable */
const optionsToast: PluginOptions = {
  container: () => document.getElementById("app")!,
  shareAppContext: true,
  position: POSITION.TOP_RIGHT,
};

const app = createApp(App)
  .use(Toast, optionsToast)
  .use(SnackbarService)
  .use(Shimmer)
  .use(Vue3Progress, options)
  .use(router)
  .use(store)
  .use(vuetify)
  .use(Vue3Sanitize)
  .use(VueApexCharts);
app.component("vue3-snackbar", Vue3Snackbar);
app.component("VueDatePicker", VueDatePicker);
app.config.globalProperties.$filters = filters;
app.mount("#app");

app.config.globalProperties.$filters = {
  formatTimeEngtoInd(stringDate) {
    const dates = new Date(stringDate);
    const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    const month = dates.getMonth() + 1;
    const year = dates.getFullYear();

    return (
      days[dates.getDay()] + ", " + dates.getDate() + "/" + month + "/" + year
    );
  },
  formatTimeAmPm(stringDate) {
    const date = new Date(stringDate);
    let hours = date.getHours();
    let minutes = date.getMinutes();
    const ampm = hours >= 12 ? "PM" : "AM";
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? 0 + minutes : minutes;
    const strTime = hours + ":" + minutes + " " + ampm;
    return strTime;
  },
  getDocumentExtension(stringFileName) {
    const temp = stringFileName.split(".");
    return temp[temp.length - 1];
  },
  formatTimeEngToIndNoDays(stringDate) {
    if (stringDate == null) return null;

    const dates = new Date(stringDate);
    const month = dates.getMonth() + 1;
    const year = dates.getFullYear();

    const strDate =
      dates.getDate() < 10 ? "0" + dates.getDate() : dates.getDate();
    const strMonth = month < 10 ? "0" + month : month;

    return strDate + "/" + strMonth + "/" + year;
  },
};
