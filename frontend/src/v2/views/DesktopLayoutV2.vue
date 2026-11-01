<template>
  <v-app class="main-app overflow-visible">
    <v-layout>
      <v-app-bar app color="white">
        <v-icon @click.stop="rail = !rail" class="ml-6" size="large">
          mdi-menu
        </v-icon>

        <img
          class="ml-6"
          :src="require('@/v2/assets/frame/logo_dwp_new.svg')"
          @click="router.push({ name: 'v2.home' })"
        />

        <v-spacer />

        <v-chip class="mr-3" variant="flat" color="white">
          <p class="font-weight-bold text-newBlack mr-3">Back to the Old DWP</p>
          <template v-slot:append>
            <v-switch
              class="gd-switch"
              v-model="toggle"
              inset
              @click="gotoOldDWP"
            >
            </v-switch>
          </template>
        </v-chip>

        <v-progress-circular
          v-if="isLoading"
          indeterminate
          color="#267dc2"
          size="24"
        />
        <rainbow-button v-if="isValidRole" />

        <notification-toggle />
        <account-toggle />
      </v-app-bar>

      <v-navigation-drawer
        v-model="drawer"
        :rail="rail"
        :width="330"
        permanent
        :image="require('@v2/assets/frame/sidebar.svg')"
      >
        <list-main-menu />

        <template v-slot:append>
          <back-button-app :rail="rail" />
        </template>
      </v-navigation-drawer>
      <v-main style="height: 100vh; overflow-y: auto">
        <div>
          <img
            :src="require('@v2/assets/frame/batik_header.webp')"
            style="position: absolute; right: 0; z-index: -99; max-width: 600px"
          />
        </div>
        <div>
          <router-view />
        </div>
      </v-main>
    </v-layout>
    <v-footer app class="footer footer-with-pattern"> </v-footer>
  </v-app>
</template>
<script setup lang="ts">
import { ref, onMounted } from "vue";
import RainbowButton from "@/v2/components/frame/RainbowButton.vue";
import NotificationToggle from "@/v2/components/frame/NotificationToggle.vue";
import AccountToggle from "@/v2/components/frame/AccountToggle.vue";
import ListMainMenu from "@/v2/components/frame/ListMainMenu.vue";
import BackButtonApp from "@/v2/components/frame/BackButtonApp.vue";

import { useStore } from "vuex";
import { useRouter } from "vue-router";

const drawer = ref(true);
const rail = ref(true);
const toggle = ref(true);
const router = useRouter();
const store = useStore();
const isLoading = ref(false);
const isValidRole = ref(false);

const gotoOldDWP = () => {
  router.push({ name: "app" });
};

const createEventRole = () => {
  isLoading.value = true;
  store.dispatch("userStore/createEventRole").then((res) => {
    isLoading.value = false;
    isValidRole.value = res.responseData.isCreate || false;
  });
};

function getTokenCkEditor() {
  store.dispatch("userStore/fetchCKEditorToken");
}

function getTokenCKBox() {
  store.dispatch("userStore/fetchCKBoxToken");
}

const getTokenDocumentCKEditor = () => {
  store.dispatch("userStore/fetchDocumentToken");
};

onMounted(() => {
  createEventRole();
  getTokenCkEditor();
  getTokenCKBox();
  getTokenDocumentCKEditor();
});
</script>

<style scoped>
:deep(.v-app-bar.v-toolbar:not(.v-toolbar--flat)) {
  box-shadow: 0px -7px 18px 0px #b3b3b340 !important;
}
:deep(.v-switch__thumb) {
  height: 18px;
  width: 18px;
}

:deep(.v-switch__track) {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  opacity: 1;
  height: 25px;
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
  background-image: url("@v2/assets/frame/batik_footer.webp");
  background-repeat: repeat-x;
  background-size: auto 60px;
  background-position: center bottom;
  min-height: 60px;
}

:deep(.v-img__img) {
  width: 56%;
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

:deep(.v-list-item--active > .v-list-item__overlay) {
  opacity: 0;
}
</style>
