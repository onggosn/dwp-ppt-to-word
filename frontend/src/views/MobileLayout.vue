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
        <p style="text-align: justify; font-size: 12px">
          <b>"Hello, {{ $store.state.fullname }}</b>
        </p>
        <p style="text-align: justify; font-size: 12px" class="mt-1 mb-1">
          We apologize for any inconvenience, but it seems that the feature
          you're looking for is not currently available on the mobile app
          browser. We're actively working on bringing this feature to the mobile
          app in the future. In the meantime, we recommend using the web desktop
          version to access this feature seamlessly. You can access it by
          visiting on your desktop or laptop computer. Thank you for your
          understanding, and we appreciate your patience as we work to improve
          your experience. If you have any questions or need further assistance,
          please feel free to reach out to our support team."
        </p>
        <p style="text-align: justify; font-size: 12px"><b>Best regards</b></p>

        <router-link :to="{ name: 'home' }">
          <v-btn
            class="text-none text-subtitle-1 text-white mt-10 rounded-xl"
            color="#065695"
            size="small"
            variant="flat"
          >
            Back to Home
          </v-btn>
        </router-link>
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
import { defineComponent } from "vue";
import NotificationMenu from "@/components/notification/NotificationMenu.vue";
import { useRoute, useRouter } from "vue-router";

defineComponent({
  components: {
    NotificationMenu,
  },
});

const route = useRoute();
const router = useRouter();

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
</style>
