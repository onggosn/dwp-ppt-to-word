<template>
  <v-sheet>
    <v-layout class="overflow-visible" style="height: 56px">
      <v-app-bar app dark>
        <v-toolbar-title>
          <router-link :to="{ name: 'home' }">
            <v-img
              style="width: auto !important"
              class="shrink mr-n3"
              contain
              src="/images/logoNavbar.png"
              transition="scale-transition"
              height="4vh"
            />
          </router-link>
        </v-toolbar-title>
        <notification-menu
          v-if="router.currentRoute.value.meta.hasMobileView"
        />
        <v-menu
          min-width="100px"
          rounded
          v-if="router.currentRoute.value.meta.hasMobileView"
        >
          <template v-slot:activator="{ props }">
            <v-btn icon v-bind="props">
              <!-- <v-avatar color="#1266a6" size="small">
                <span class="text-11 text-white font-weight-bold">HH</span>
              </v-avatar> -->
              <v-icon color="#1266a6" size="x-large" class="mr-1">
                mdi-account</v-icon
              >
            </v-btn>
          </template>
          <v-card class="rounded-lg">
            <v-card-text class="">
              <div class="mx-auto text-left">
                <v-btn rounded variant="text" :to="'/app/profile'">
                  <v-icon color="#065695" size="x-large" class="mr-1">
                    mdi-account</v-icon
                  >
                  {{ $store.state.fullname }}
                </v-btn>
                <v-divider class="my-3"></v-divider>
                <v-btn rounded variant="text">
                  <v-icon color="#065695" size="x-large" class="mr-1">
                    mdi-logout</v-icon
                  >
                  Logout
                </v-btn>
              </div>
            </v-card-text>
          </v-card>
        </v-menu>
      </v-app-bar>

      <v-sheet
        style="margin-top: 5vh; max-width: 100%"
        v-if="router.currentRoute.value.meta.hasMobileView"
      >
        <router-view />
      </v-sheet>

      <v-sheet style="padding: 40px; margin-top: 20vh" v-else>
        <p style="text-align: justify; font-size: 18px" class="mb-4">
          <b>Hello, {{ $store.state.fullname }}</b>
        </p>
        <p style="text-align: justify; font-size: 14px" class="mb-4">
          We apologize for the inconvenience. This feature is currently
          <b>not available on the mobile app browser</b>. For the best
          experience, please access it via the desktop web version.
        </p>
        <p style="text-align: justify; font-size: 14px" class="mb-4">
          Our application is available in two versions,
          <b>Old DWP and New DWP</b>, both of which can be accessed or
          downloaded via the <b>App Store</b> or <b>Google Play Store</b>.
        </p>
        <p style="text-align: justify; font-size: 14px">
          Thank you for your understanding
        </p>

        <div class="download-container mt-8">
          <span class="download-span">
            <v-img
              @click="redirectToOldDWP"
              src="/images/download-old-dwp.png"
              class="cursor-pointer download-image"
              style="border-radius: 12px"
              cover
            />
          </span>

          <span class="download-span">
            <v-img
              @click="redirectToNewDWP"
              src="/images/download-new-dwp.png"
              class="cursor-pointer download-image"
              style="border-radius: 12px"
              cover
            />
          </span>
        </div>
      </v-sheet>

      <v-container
        style="position: fixed; bottom: 0; z-index: 99"
        v-if="router.currentRoute.value.meta.showMobileMenu"
      >
        <v-row class="mb-6 bg-white rounded-xl elevation-5" no-gutters>
          <v-col cols="3" style="align-self: center; text-align-last: center">
            <v-btn icon class="pa-2 ma-4" :to="{ name: 'home' }">
              <v-icon :color="getNavigationColor('Home')"
                >mdi-home-variant</v-icon
              ></v-btn
            >
          </v-col>

          <v-col cols="3" style="align-self: center; text-align-last: center">
            <v-btn icon :to="{ name: 'workspace-management' }">
              <v-icon :color="getNavigationColor('Workspace')"
                >mdi-view-dashboard</v-icon
              >
            </v-btn>
          </v-col>

          <v-col cols="3" style="align-self: center; text-align-last: center">
            <v-btn icon :to="{ name: 'meeting-management' }">
              <v-icon :color="getNavigationColor('Meeting')"
                >mdi-account-multiple</v-icon
              >
            </v-btn>
          </v-col>

          <v-col cols="3" style="align-self: center; text-align-last: center">
            <v-btn icon :to="{ name: 'document-management' }">
              <v-icon :color="getNavigationColor('Document')"
                >mdi-folder-multiple</v-icon
              >
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-layout>
  </v-sheet>
</template>
<script setup lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import NotificationMenu from "@/components/notification/NotificationMenu.vue";
import { useRoute, useRouter } from "vue-router";

defineComponent({
  components: {
    NotificationMenu,
  },
});

// const value = ref(0);
const mobileType = ref("");
const route = useRoute();
const router = useRouter();

onMounted(() => {
  if (typeof window !== "undefined" && window.navigator) {
    const agentString = window.navigator.userAgent;
    mobileType.value = detectMobile(agentString);
  }
});

const detectMobile = (agent) => {
  if (!agent) return "Android";

  const userAgent = agent.toLowerCase();

  // Deteksi iPhone/iOS
  if (/iphone|ipad|ipod/.test(userAgent)) {
    return "iOS";
  }

  // Deteksi Android
  if (/android|mobile|phone|tablet/.test(userAgent)) {
    return "Android";
  }

  return "iOS";
};

const redirectToOldDWP = () => {
  const appStoreUrl =
    "https://apps.apple.com/id/app/digital-workplace-mobile/id1644633624";
  const playStoreUrl =
    "https://play.google.com/store/apps/details?id=bi.hybrid.dmp";

  if (mobileType.value === "iOS") {
    window.open(appStoreUrl, "_blank");
  } else {
    window.open(playStoreUrl, "_blank");
  }
};

const redirectToNewDWP = () => {
  const appStoreUrl = "https://apps.apple.com/us/app/idcb/id6499212096  ";
  const playStoreUrl =
    "https://play.google.com/store/apps/details?id=bi.hybrid.dwp";

  if (mobileType.value === "iOS") {
    window.open(appStoreUrl, "_blank");
  } else {
    window.open(playStoreUrl, "_blank");
  }
};

const getNavigationColor = (menu) => {
  switch (menu) {
    case "Home":
      if (route.name == "home") {
        return "#065695";
      } else {
        return "grey";
      }
    case "Workspace":
      if (route.name == "workspace-management") {
        return "#065695";
      } else {
        return "grey";
      }
    case "Meeting":
      if (route.name == "meeting-management") {
        return "#065695";
      } else {
        return "grey";
      }
    case "Document":
      if (route.name == "document-management") {
        return "#065695";
      } else {
        return "grey";
      }
    default:
      return "grey";
  }
};
</script>

<style scoped>
:deep(.v-img__img--contain) {
  width: auto !important;
}

.cursor-pointer {
  cursor: pointer;
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.cursor-pointer:hover {
  transform: scale(1.05);
  opacity: 0.9;
}

.cursor-pointer:active {
  transform: scale(0.98);
}

.download-image {
  width: 140px !important;
  height: 45px !important;
  max-width: 140px;
  max-height: 45px;
}

.download-container {
  display: flex;
  justify-content: start;
  gap: 8px;
  align-items: center;
}

.download-span {
  display: inline-block;
}

.download-button {
  width: 120;
  height: 38;
  opacity: 1;
  border-radius: 6px;
}
</style>
