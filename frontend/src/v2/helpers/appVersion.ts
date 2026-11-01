export function checkAppVersion() {
  const APP_VERSION = process.env.VUE_APP_VERSION ?? "";
  const VERSION_KEY = "__app_version__";

  if (localStorage.getItem(VERSION_KEY) !== APP_VERSION) {
    const keysToRemove = [
      "undertaker",
      "teriyaki",
      "yakiniku",
      "ampuni",
      "akan",
    ];

    keysToRemove.forEach((key) => {
      localStorage.removeItem(key);
      sessionStorage.removeItem(key);
    });

    // make sure semua di delete
    localStorage.clear();
    sessionStorage.clear();
    // set version app
    localStorage.setItem(VERSION_KEY, APP_VERSION);
    // redirect ke login setelah clearing storage
    try {
      window.location.replace("/");
    } catch (e) {
      window.location.href = "/";
    }
  }
}
