<template>
  <api-loader
    ref="listNotif"
    :apiMethod="getNotification"
    loadingMessage="Memuat Notifikasi..."
    :hasOverlay="false"
    @loadingEnded="handleLoadingEnded"
  >
    <template v-slot:default="">
      <v-menu location="bottom" max-height="300" max-width="500">
        <template v-slot:activator="{ props }">
          <v-btn icon v-bind="props" @click="resetNotif">
            <v-tooltip location="bottom">
              <template v-slot:activator="{ props }">
                <v-icon color="#1266a6" v-bind="props">mdi-bell</v-icon>
                <span v-if="$store.state.isNotifNew == true" class="badge-red"
                  >&nbsp;</span
                >
                <span v-else class="badge-brown">&nbsp;</span>
              </template>
              <span>Lihat daftar notifikasi</span>
            </v-tooltip>
          </v-btn>
        </template>
        <v-list>
          <v-list-item v-if="$store.state.notifList.length == 0">
            You dont have notification
          </v-list-item>
          <template v-else>
            <v-list-item v-for="item in $store.state.notifList" :key="item.id">
              <row-notification :item="item" />
            </v-list-item>
          </template>
        </v-list>
      </v-menu>
    </template>
  </api-loader>
</template>

<script>
import client from "@/library/ApiClient";
import ApiLoader from "@/components/ApiLoader.vue";
import RowNotification from "./RowNotification.vue";

export default {
  components: { ApiLoader, RowNotification },
  methods: {
    resetNotif() {
      this.$store.dispatch("updateNotif");
    },
    handleLoadingEnded({ success, response }) {
      if (success) {
        if (
          !this.$store.state.notifNumber ||
          !this.$store.state.notifList.length > 0
        ) {
          this.$store.dispatch("createNewNotif", {
            totalNotification: response.plainData.totalNotification,
            notificationViewList: response.plainData.notificationViewList,
          });
        }
      }
    },
    getNotification() {
      return client.getNotificationLimitViewAndTotalNotifByUsername({
        store: this.$store,
        data: {
          username: this.$store.state.username,
        },
      });
    },
  },
};
</script>

<style scoped>
:deep(.v-menu__content) {
  overflow-y: hidden;
}
.badge-red {
  position: absolute;
  top: 13px;
  right: 10px;
  padding: 5px;
  border-radius: 50%;
  background: red;
  color: white;
  height: 13px;
  width: 13px;
}

.badge-brown {
  display: none;
}
</style>
