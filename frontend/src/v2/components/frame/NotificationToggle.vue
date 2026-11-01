<template>
  <v-menu location="bottom" max-height="300" max-width="500">
    <template v-slot:activator="{ props }">
      <v-badge v-if="showBadge" color="red">
        <v-icon
          v-bind="props"
          color="#267DC2"
          size="large"
          @click="handleOpenNotification"
        >
          mdi-bell
        </v-icon>
      </v-badge>
      <v-icon
        v-else
        v-bind="props"
        color="#267DC2"
        size="large"
        @click="handleOpenNotification"
      >
        mdi-bell
      </v-icon>
    </template>
    <v-list class="border-radius-dwp">
      <template v-if="items?.length == 0">
        <v-list-item>
          <div class="d-flex py-1">
            <div class="my-auto">
              <v-avatar
                rounded="0"
                image="/images/notif/Puzzle.png"
                size="55"
              ></v-avatar>
            </div>
            <div class="d-flex flex-column ml-4">
              <span class="text-body-2 mb-1">Not Available</span>
              <p class="text-caption text--secondary mb-0">
                There is no notification available
              </p>
            </div>
          </div>
        </v-list-item>
      </template>
      <template v-else>
        <notification-item
          v-for="(item, idx) in items"
          @read-local="read"
          :key="idx"
          :item="item"
        />
      </template>
    </v-list>
  </v-menu>
</template>
<script setup lang="ts">
import { useStore } from "vuex";

import { TNotificationItem } from "@/v2/Type";
import { ref, computed } from "vue";
import { onMounted } from "vue";
import NotificationItem from "@v2/components/frame/NotificationItem.vue";
const store = useStore();
const items = ref<Array<TNotificationItem>>([]);
const showBadge = computed(() => {
  return items.value.some((item) => item.seenByUser === false);
});
const hasOpen = ref<boolean>(false);
function getNotification() {
  const payload = {
    info: {
      pageNo: 1,
      entriesPerPage: 20,
    },
  };
  store
    .dispatch("userStore/getNotificationViewByUsernameNew", { payload })
    .then((resp: any) => {
      items.value = resp;
    });
}

function handleOpenNotification() {
  hasOpen.value = true;
}

function read(id: string) {
  const item = items.value.find((el) => el.id == id);
  if (item) {
    item.seenByUser = true;
  }
}

onMounted(() => {
  getNotification();
});
</script>
