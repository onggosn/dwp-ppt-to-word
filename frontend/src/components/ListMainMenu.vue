<template>
  <v-list density="comfortable" nav>
    <template v-for="item in listMenu" :key="item.value">
      <template v-if="item.subMenu.length > 0">
        <v-list-group :value="item.value">
          <template v-slot:activator="{ props }">
            <v-list-item
              color="white"
              style="color: white; font-size: 1 rem !important"
              v-bind="props"
              :title="item.label"
            >
              <v-tooltip activator="parent" location="bottom">
                {{ item.tooltip }}
              </v-tooltip>
              <template v-slot:prepend>
                <img
                  aspect-ratio="1/1"
                  :width="50"
                  :src="
                    currentRoute?.includes(item.route)
                      ? item.iconActive
                      : item.icon
                  "
                  class="pt-2 pr-3"
                />
              </template>
            </v-list-item>
          </template>
          <v-list-item
            color="white"
            style="color: white; font-size: 1 rem !important"
            v-for="subMenus in item.subMenu"
            :key="subMenus.value"
            :value="subMenus.value"
            :to="{
              name: subMenus.route,
            }"
          >
            <v-tooltip activator="parent" location="bottom">
              {{ subMenus.tooltip }}
            </v-tooltip>
            <v-list-item-title
              :class="[
                currentRoute?.includes(subMenus.route) ? 'selected' : '',
              ]"
              >{{ subMenus.label }}</v-list-item-title
            >
          </v-list-item>
        </v-list-group>
      </template>
      <template v-else>
        <v-list-item
          :title="item.label"
          :value="item.value"
          :to="{
            name: item.route,
          }"
          color="white"
          style="color: white; font-size: 1 rem !important"
        >
          <v-tooltip activator="parent" location="bottom">
            {{ item.label }}
          </v-tooltip>
          <template v-slot:prepend>
            <img
              aspect-ratio="1/1"
              :width="50"
              :src="
                currentRoute?.includes(item.route) ? item.iconActive : item.icon
              "
              class="pt-2 pr-3"
            />
          </template>
        </v-list-item>
      </template>
    </template>
  </v-list>
</template>

<script setup lang="ts">
import { ref, watch, defineEmits } from "vue";
import { useRouter } from "vue-router";
import { mGetMenu } from "@/models/menu";

const emits = defineEmits(["createWorkspace"]);
const router = useRouter();
const currentRoute = ref(router.currentRoute.value.path);

const listMenu = ref();
const createworkspace = ref(false);
mGetMenu().then((res) => {
  listMenu.value = res.menus;
  createworkspace.value = res.createworkspace;
  emits("createWorkspace", createworkspace.value);
});

watch(
  () => router.currentRoute.value.path,
  (value) => {
    currentRoute.value = value;
  }
);
</script>
<style scoped>
.selected {
  background: linear-gradient(180deg, #d6212a 0%, #ff000d 100%);
  width: fit-content;
  border-radius: 12px;
  padding: 10px;
}
</style>
