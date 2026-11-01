import { initializeApp, getApps } from "firebase/app";

let appFirebase = null;

// Init sekali pakai config dari API (Config/initializeConfig), bukan dari env/dotenv.
// projectId/authDomain/storageBucket bukan rahasia (selalu terlihat di bundle client
// semua app Firebase), jadi boleh fallback ke env kalau BE belum mengirimnya.
export function initializeFirebaseApp(firebaseConfig) {
  if (appFirebase) return appFirebase;
  if (!firebaseConfig?.apiKey) return null;

  appFirebase = getApps().length
    ? getApps()[0]
    : initializeApp({
        apiKey: firebaseConfig.apiKey,
        authDomain: process.env.VUE_APP_AUTH_DOMAIN,
        projectId: process.env.VUE_APP_PROJECT_ID,
        storageBucket: process.env.VUE_APP_STORAGE_BUCKET,
        messagingSenderId: firebaseConfig.senderId,
        appId: firebaseConfig.appId,
        measurementId: firebaseConfig.measurementId,
      });

  return appFirebase;
}

export function getFirebaseApp() {
  return appFirebase;
}
