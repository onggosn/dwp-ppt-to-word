import { ref } from "vue";
import { useStore } from "vuex";
import { getMessaging, onMessage, getToken } from "firebase/messaging";
import { getFirebaseApp } from "@/library/FirebaseHelper";
import sanitizeHtml from "sanitize-html";
import MyToastComponent from "@/components/utils/MyToastComponent.vue";
import { useToast } from "vue-toastification";

export function useFirebaseMessaging() {
  const store = useStore();
  const toastAlert = useToast();
  const fcmToken = ref<string | null>(null);

  const getVapidKey = () =>
    store.getters["userStore/getInitializeConfig"]?.firebase?.vapid || "";

  // Helper: Format pesan jika berbentuk array (bold logic)
  const formatMessages = (messages: any[]): string => {
    if (!Array.isArray(messages)) return messages || "";
    const formatted = messages
      .reduce((acc, item) => {
        const text = item.isBold
          ? `<b>${item.message || ""}</b>`
          : item.message || "";
        return acc + " " + text;
      }, "")
      .trim();
    return sanitizeHtml(formatted);
  };

  // Helper: Tampilkan Toast Custom
  const showNotificationToast = (payload: {
    title: string;
    body: string;
    link?: string;
  }) => {
    toastAlert(
      {
        component: MyToastComponent,
        props: {
          title: payload.title ?? "Digital Workplace",
          body: payload.body ?? "-",
        },
        listeners: {
          click: () => {
            if (payload.link) {
              window.location.href = `${window.location.origin}/${payload.link}`;
            }
          },
        },
      } as any,
      {
        timeout: 10000,
        toastClassName: "my-custom-toast-class",
        icon: false,
      }
    );
  };

  // 1. Fungsi Ambil Token
  const fetchToken = async () => {
    // 1. Cek apakah browser mendukung notifikasi
    if (!("Notification" in window)) return null;

    // 2. Jika sudah diblokir, jangan paksa panggil getToken Firebase
    if (Notification.permission === "denied") {
      console.warn("FCM: Notification permission is blocked by user.");
      return null;
    }

    try {
      const app = getFirebaseApp();
      if (!app) return null;

      const vapidKey = getVapidKey();
      if (!vapidKey) {
        console.warn("FCM: vapidKey kosong, getToken dibatalkan.");
        return null;
      }

      const messaging = getMessaging(app);
      const serviceWorkerRegistration = await navigator.serviceWorker.ready;
      // Gunakan getToken hanya jika permission 'granted' atau 'default' (prompt)
      const token = await getToken(messaging, {
        vapidKey,
        serviceWorkerRegistration,
      });
      return token;
    } catch (error: any) {
      // Tangkap error 'permission-blocked' agar tidak crash
      if (error.code === "messaging/permission-blocked") {
        console.warn("FCM: Permission was blocked, skipping token retrieval.");
      } else {
        console.error("FCM: Error retrieving token", error.code, error.message);
      }
      return null;
    }
  };

  const requestNotificationPermission = async () => {
    try {
      const permission = await Notification.requestPermission();
      if (permission === "granted") {
        const app = getFirebaseApp();
        if (!app) return null;

        const vapidKey = getVapidKey();
        if (!vapidKey) {
          console.warn("FCM: vapidKey kosong, getToken dibatalkan.");
          return null;
        }

        const messaging = getMessaging(app);
        const serviceWorkerRegistration = await navigator.serviceWorker.ready;
        const token = await getToken(messaging, {
          vapidKey,
          serviceWorkerRegistration,
        });
        if (token) {
          fcmToken.value = token;
          return token;
        }
      }
      return null;
    } catch (error: any) {
      console.warn("FCM Permission Error:", error.code, error.message);
      return null;
    }
  };

  // 2. Fungsi Listener (Foreground Messaging)
  const initListener = () => {
    const app = getFirebaseApp();
    if (!app) return;

    const messaging = getMessaging(app);
    onMessage(messaging, (payload: any) => {
      let formattedBody = payload?.notification?.body;

      if (payload.data?.message) {
        try {
          const parsed = JSON.parse(payload.data.message);
          formattedBody = Array.isArray(parsed)
            ? formatMessages(parsed)
            : payload.data.message;
        } catch {
          formattedBody = payload.data.message;
        }
      }

      showNotificationToast({
        title: payload?.notification?.title ?? "Digital Workplace",
        body: formattedBody ?? "No message content",
        link: payload.data?.web,
      });
    });
  };

  // 3. Register SW with Firebase config embedded in URL params so Firebase
  // can initialize synchronously on initial SW evaluation (required by push API)
  const registerServiceWorkerWithConfig = async () => {
    if (!("serviceWorker" in navigator) || !("PushManager" in window)) return;

    const firebaseConfig =
      store.getters["userStore/getInitializeConfig"]?.firebase;
    if (!firebaseConfig?.apiKey) return;

    const plainConfig = JSON.parse(JSON.stringify(firebaseConfig));
    const params = new URLSearchParams({
      apiKey: plainConfig.apiKey || "",
      authDomain:
        process.env.VUE_APP_AUTH_DOMAIN || plainConfig.authDomain || "",
      projectId: process.env.VUE_APP_PROJECT_ID || plainConfig.projectId || "",
      storageBucket:
        process.env.VUE_APP_STORAGE_BUCKET || plainConfig.storageBucket || "",
      messagingSenderId: plainConfig.senderId || "",
      appId: plainConfig.appId || "",
      measurementId: plainConfig.measurementId || "",
    });

    try {
      const reg = await navigator.serviceWorker.register(
        `/firebase-messaging-sw.js?v=${Date.now()}&${params.toString()}`
      );
      // Wait for new SW to reach 'activated' state (skipWaiting in SW makes this fast).
      // Also resolve on 'redundant' to avoid hanging if installation fails.
      const sw = reg.installing ?? reg.waiting ?? reg.active;
      if (sw && sw.state !== "activated") {
        await new Promise<void>((resolve) => {
          const onStateChange = () => {
            if (sw.state === "activated" || sw.state === "redundant") {
              sw.removeEventListener("statechange", onStateChange);
              resolve();
            }
          };
          sw.addEventListener("statechange", onStateChange);
        });
      }
    } catch (err) {
      console.error("SW registration failed:", err);
    }
  };

  return {
    fcmToken,
    fetchToken,
    initListener,
    requestNotificationPermission,
    registerServiceWorkerWithConfig,
  };
}
