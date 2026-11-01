<template>
  <v-list density="compact" nav class="mt-3">
    <template v-for="item in listMenu" :key="item">
      <v-list-item
        :to="{
          name: `v2.${item.route}`,
        }"
      >
        <p class="ml-3">{{ item.label }}</p>
        <template v-slot:prepend>
          <template v-if="currentRoute?.includes(item.route)">
            <img
              class="pt-2"
              :src="require(`@/v2/assets/icon/menu/${item.iconName}Active.svg`)"
            />
          </template>
          <template v-else>
            <img
              class="pt-2"
              :src="require(`@/v2/assets/icon/menu/${item.iconName}.svg`)"
            />
          </template>
        </template>
        <v-tooltip activator="parent" location="bottom" scroll-strategy="close">
          {{ item.tooltip }}
        </v-tooltip>
      </v-list-item>
    </template>
    <v-list-item
      :to="{
        name: `v2.help`,
      }"
    >
      <p class="ml-3">Help</p>
      <template v-slot:prepend>
        <template v-if="currentRoute?.includes('help')">
          <img
            class="pt-2"
            :src="require(`@/v2/assets/icon/menu/helpActive.svg`)"
          />
        </template>
        <template v-else>
          <img class="pt-2" :src="require(`@/v2/assets/icon/menu/help.svg`)" />
        </template>
      </template>
      <v-tooltip activator="parent" location="bottom" scroll-strategy="close">
        Help
      </v-tooltip>
    </v-list-item>
  </v-list>
</template>

<script lang="ts" setup>
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

const router = useRouter();
const store = useStore();
const currentRoute = ref(router.currentRoute.value.path);
const listMenu = ref();

watch(
  () => router.currentRoute.value.path,
  (value) => {
    currentRoute.value = value;
  }
);

store.dispatch("userStore/fetchMenuList").then((data) => {
  // debugger;
  listMenu.value = data.roleMenuList;
});
</script>

<style scoped>
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
