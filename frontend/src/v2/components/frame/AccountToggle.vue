<template>
  <v-menu location="bottom">
    <template v-slot:activator="{ props }">
      <v-btn
        variant="text"
        v-bind="props"
        class="mr-10 ml-5 text-darkBlue font-weight-bold"
      >
        Hi, {{ store.state.fullname }}
        <template v-slot:append>
          <v-icon>mdi-chevron-down</v-icon>
        </template>
      </v-btn>
    </template>

    <v-list density="compact" nav>
      <v-list-item
        :to="{
          name: 'home.profile',
        }"
        :title="store.state.fullname"
        subtitle="see profile"
        class="text-black font-weight-bold text-left text-subtitle-2 pt-2 pb-2 pl-5 pr-10"
      >
        <template v-slot:prepend>
          <v-icon color="#267DC2" size="large" style="opacity: 1"
            >mdi-account</v-icon
          >
        </template>
      </v-list-item>
      <v-divider class="pr-4 pl-4" />
      <v-list-item
        title="Logout"
        class="text-black font-weight-bold text-left text-subtitle-2 pt-2 pb-2 pr-10 pl-5"
        @click="doLogout"
      >
        <template v-slot:prepend>
          <v-icon color="#267DC2" size="large" style="opacity: 1"
            >mdi-logout</v-icon
          >
        </template>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script setup lang="ts">
import { useStore } from "vuex";
import { useMsal } from "@/v2/composables/useMsal";
import { redirectToBisa } from "@/v2/helpers/utils";
const store = useStore();
const { logoutMsal } = useMsal();

const doLogout = async () => {
  const isMfa = process.env.VUE_APP_MFA_STATUS === "true";
  store.dispatch("logout").then(async () => {
    if (!isMfa) {
      window.location.href = process.env.VUE_APP_MW_AUTH_BISA + "/auth/logout";
    } else {
      await logoutMsal("redirect");
      redirectToBisa();
    }
  });
};
</script>
