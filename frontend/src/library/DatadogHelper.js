import { datadogRum } from "@datadog/browser-rum";
import { secureRandomFloat } from "@/v2/helpers/utils";
import store from "@/store/index.js";

const disabledModes = process.env.VUE_APP_DATADOG_STATUS;
const configDatadog = {
  applicationId: process.env.VUE_APP_DATADOG_APPLICATION_ID,
  clientToken: process.env.VUE_APP_DATADOG_CLIENT_TOKEN,
  site: process.env.VUE_APP_DATADOG_SITE,
  service: process.env.VUE_APP_DATADOG_SERVICE,
  env: process.env.VUE_APP_DATADOG_ENV,
  sessionSampleRate: 100,
  sessionReplaySampleRate: 60,
  traceSampleRate: 100,
  trackResources: true,
  trackLongTasks: true,
  trackBfcacheViews: true,
  trackUserInteractions: true,
  forwardErrorsToLogs: true,
  allowedTracingUrls: [
    store.state.urlApim,
    process.env.VUE_APP_MIDDLEWARE_NEW_PATH,
    process.env.VUE_APP_CKBOX,
    process.env.VUE_APP_PDF,
    process.env.VUE_APP_EXPORT_WORD,
    process.env.VUE_APP_IMPORT_WORD,
  ].filter(Boolean), // Filter nilai undefined
  allowedTracingOrigins: [
    store.state.urlApim,
    process.env.VUE_APP_MIDDLEWARE_NEW_PATH,
    process.env.VUE_APP_CKBOX,
    process.env.VUE_APP_PDF,
    process.env.VUE_APP_EXPORT_WORD,
    process.env.VUE_APP_IMPORT_WORD,
  ].filter(Boolean), // Filter nilai undefined
  defaultPrivacyLevel: process.env.VUE_APP_DATADOG_PRIVACY_LEVEL,
  beforeSend: (request) => {
    request.response = {
      ...request.response,
      json: async () => {
        try {
          return JSON.parse(request.response.body);
        } catch (e) {
          return null;
        }
      },
    };
    return request;
  },
};

// Initialize datadogRum
export function handleInitialDatadog(data) {
  if (disabledModes === "true") {
    if (localStorage.getItem("isLoggedIn") === "true") {
      datadogRum.init(configDatadog);
      datadogRum.setUser({
        id: secureRandomFloat(),
        name: data.fullname,
        email: data.username + "@bi.go.id",
      });
      datadogRum.startSessionReplayRecording();
    } else {
      datadogRum.stopSessionReplayRecording();
    }
  }
  return Promise.resolve();
}
