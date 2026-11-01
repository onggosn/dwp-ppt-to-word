/* eslint-env serviceworker */
/* global firebase */
importScripts("https://www.gstatic.com/firebasejs/8.9.1/firebase-app.js");
importScripts("https://www.gstatic.com/firebasejs/8.9.1/firebase-messaging.js");

// Activate immediately so push event handlers are registered on initial evaluation
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(clients.claim()));

// Initialize Firebase synchronously from URL params (required by browser push API)
const _params = new URL(self.location.href).searchParams;

if (_params.get("apiKey")) {
  firebase.initializeApp({
    apiKey: _params.get("apiKey"),
    authDomain: _params.get("authDomain"),
    projectId: _params.get("projectId"),
    storageBucket: _params.get("storageBucket"),
    messagingSenderId: _params.get("messagingSenderId"),
    appId: _params.get("appId"),
    measurementId: _params.get("measurementId"),
  });
  const messaging = firebase.messaging();
  messaging.onBackgroundMessage(handleBackgroundMessage);
}

self.addEventListener("notificationclick", function (event) {
  event.notification.close();

  if (event.action === "close") {
    // Handle close action
  } else if (event.notification.data && event.notification.data.target_url) {
    const url = event.notification.data.target_url.trim();
    event.waitUntil(
      clients
        .matchAll({ type: "window", includeUncontrolled: true })
        .then(function (clientList) {
          for (var i = 0; i < clientList.length; i++) {
            var client = clientList[i];
            if (client.url === url && "focus" in client) {
              return client.focus();
            }
          }
          if (clients.openWindow) {
            return clients.openWindow(url).then(function (windowClient) {
              return windowClient ? windowClient.focus() : null;
            });
          }
        })
    );
  }
});

function handleBackgroundMessage(payload) {
  const title = payload.data.title || "Digital workplace";
  const link =
    payload.data.web && payload.data.web.trim() !== ""
      ? self.location.origin + "/" + payload.data.web
      : self.location.origin;

  let messages = [];
  if (payload.data.message) {
    try {
      messages = JSON.parse(payload.data.message);
    } catch (e) {
      // Silent error handling
    }
  }

  const formatMessages = (arr) =>
    arr
      .map((item) => item.message)
      .join(" ")
      .trim();

  const options = {
    body: formatMessages(messages),
    icon: "icon.png",
    image: "message-image.png",
    badge: "badge.png",
    data: { target_url: link },
    actions: [
      {
        action: "open",
        title: "Open",
      },
      {
        action: "close",
        title: "Dismiss",
      },
    ],
  };

  self.registration.showNotification(title, options);
}
