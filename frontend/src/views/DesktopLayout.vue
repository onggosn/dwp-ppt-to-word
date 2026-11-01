<template>
  <v-app class="main-app">
    <v-layout>
      <v-app-bar app color="white">
        <v-icon @click.stop="rail = !rail" class="ml-6" size="large">
          mdi-menu
        </v-icon>

        <router-link :to="{ name: 'home' }">
          <img
            class="ml-6"
            :src="require('@/v2/assets/frame/logo_dwp_new.svg')"
          />
        </router-link>

        <v-spacer />

        <v-chip class="mr-3" variant="flat" color="white">
          <p class="font-weight-bold text-newBlack mr-3">Try the new DWP</p>
          <template v-slot:append>
            <v-switch
              class="gd-switch"
              v-model="toggle"
              inset
              @click="gotoNewDWP"
            >
            </v-switch>
          </template>
        </v-chip>

        <rainbow-button
          @click="showModal"
          label="Create Workspace"
          v-if="canCreateWorkspace"
        />
        <notification-menu />

        <v-menu transition="slide-y-transition">
          <template v-slot:activator="{ props }">
            <v-btn color="#3A416F" v-bind="props" class="font-weight-bold">
              Hi, {{ store.state.fullname }}
              <template v-slot:append>
                <v-icon>mdi-chevron-down</v-icon>
              </template>
            </v-btn>
          </template>
          <v-list>
            <v-list-item
              :title="store.state.fullname"
              subtitle="see profile"
              style="cursor: pointer; color: black"
              :to="{
                name: 'profile',
              }"
            >
              <template v-slot:prepend>
                <v-avatar>
                  <v-icon color="#267dc2">mdi-account</v-icon>
                </v-avatar>
              </template>
            </v-list-item>
            <v-list-item
              title="Logout"
              style="cursor: pointer; color: black"
              @click="doLogout"
            >
              <template v-slot:prepend>
                <v-avatar>
                  <v-icon color="#267dc2">mdi-logout</v-icon>
                </v-avatar>
              </template>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-app-bar>

      <v-navigation-drawer
        v-model="drawer"
        :rail="rail"
        :width="330"
        permanent
        :image="require('@/v2/assets/frame/sidebar.svg')"
      >
        <list-main-menu @createWorkspace="createWorkspace" />
        <template v-slot:append>
          <back-button-app :rail="rail" />
        </template>
      </v-navigation-drawer>
      <v-main style="height: 100vh; overflow-y: auto">
        <div>
          <img
            :src="require('@v2/assets/frame/batik_header.webp')"
            style="position: absolute; right: 0; max-width: 600px"
          />
        </div>
        <router-view />
      </v-main>
    </v-layout>

    <create-workspace-form-dialog ref="dialog" />
    <v-overlay :model-value="isLoading" class="align-center justify-center">
      <v-progress-circular
        color="#065695"
        indeterminate
        size="68"
        width="6"
      ></v-progress-circular>
    </v-overlay>
    <v-footer app class="footer footer-with-pattern"> </v-footer>
  </v-app>
</template>
<script setup lang="ts">
import { ref } from "vue";
import RainbowButton from "@/components/workspace/RainbowButton.vue";
import NotificationMenu from "@/components/notification/NotificationMenu.vue";
import CreateWorkspaceFormDialog from "@/components/workspace/CreateWorkspaceFormDialog.vue";
import ListMainMenu from "@/components/ListMainMenu.vue";
import BackButtonApp from "@/v2/components/frame/BackButtonApp.vue";
import store from "@/store";
import { useRouter } from "vue-router";
import { useMsal } from "@/v2/composables/useMsal";
import { redirectToBisa } from "@/v2/helpers/utils";

const drawer = ref(true);
const rail = ref(false);
const toggle = ref(false);
const router = useRouter();
const isLoading = ref(false);
const dialog = ref();
const canCreateWorkspace = ref(false);
const { logoutMsal } = useMsal();

const gotoNewDWP = () => {
  router.push({ path: "/app/v2/home" });
};

const createWorkspace = (value) => (canCreateWorkspace.value = value);

const showModal = () => {
  dialog.value.start();
};

const doLogout = async () => {
  isLoading.value = true;
  store
    .dispatch("logout")
    .then(async () => {
      if (process.env.VUE_APP_MFA_STATUS === "true") {
        window.location.href =
          process.env.VUE_APP_MW_AUTH_BISA + "/auth/logout";
      } else {
        await logoutMsal("redirect");
        redirectToBisa();
      }
    })
    .finally(() => {
      isLoading.value = false;
    });
};
</script>

<style scoped>
:deep(.v-app-bar.v-toolbar:not(.v-toolbar--flat)) {
  box-shadow: 0px -7px 18px 0px #b3b3b340 !important;
}
:deep(.v-switch__thumb) {
  height: 30px;
  width: 30px;
  box-shadow: 1px 1px 4px 1px grey;
}

:deep(.v-switch__track) {
  /* background: linear-gradient(92.09deg, grey 0%, -46.47%, grey 157.9%); */
  opacity: 1;
  height: 25px;
  background: #efefef;
  box-shadow: 0.1px 0.1px 3px 0.1px grey;
}
.main-app {
  background-color: #f5f5f5;
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
}

.text-newBlack {
  color: #4b4b4b;
}

.footer {
  background-color: #f5f5f5;
  z-index: 1 !important;
  padding: 0 !important;
}

.footer-with-pattern {
  background-image: url("~@/v2/assets/frame/batik_footer.webp");
  background-repeat: repeat-x;
  background-size: auto 60px; /* Tinggi gambar 40px, lebar otomatis */
  background-position: center bottom;
  min-height: 60px;
}

/* :deep(.v-navigation-drawer__img) {
  background: url("@/v2/assets/frame/sidebar.png") !important;
} */

:deep(.v-img__img) {
  /* width: 56%; */
}
:deep(.v-input__details) {
  grid-area: auto;
}

:deep(.v-navigation-drawer) {
  background: #f5f5f5 !important;
  box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.1) !important;
  border: 0px !important;
}

:deep(.v-navigation-drawer--rail) {
  width: 80px !important;
}

:deep(.v-list-item--active) {
  background-color: transparent;
}

:deep(.v-list-item--variant-text) {
  color: #fff;
}

:deep(.v-list-item--nav .v-list-item-title) {
  font-size: 13px;
  font-weight: 500;
  letter-spacing: normal;
  line-height: 1rem;
  text-align-last: left;
  margin-left: 1vw;
}

:deep(.v-list .v-list-item--nav:not(:only-child)) {
  margin-bottom: 10px;
}
:deep(.v-list-item--active > .v-list-item__overlay) {
  opacity: 0;
}
</style>
