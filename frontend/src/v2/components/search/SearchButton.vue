<template>
  <v-menu
    transition="slide-y-transition"
    bottom
    :close-on-content-click="false"
  >
    <template #activator="{ props }">
      <v-btn v-if="roundedBtn" icon size="small" v-bind="props">
        <img src="/images/task/searchMagnifier.svg" width="21" height="21" />
      </v-btn>
      <v-btn
        v-else
        class="btn-dropdown"
        variant="outlined"
        dark
        v-bind="props"
        style="overflow: hidden"
      >
        <img src="/images/task/searchMagnifier.svg" width="21" height="21" />
        <span class="ml-2"> Search </span>
      </v-btn>
    </template>

    <v-card min-width="300">
      <v-form ref="form" @submit.prevent="searchEvent">
        <v-list>
          <v-list-item>
            <v-text-field
              v-model="keyword"
              hide-details="auto"
              placeholder="search"
              variant="outlined"
              clearable
              autofocus
              style="border-radius: 10px"
            />
          </v-list-item>

          <v-list-item>
            <v-list-item-title class="text-right">
              <v-btn class="btn-primary blue-gradient mb-2" type="submit">
                Search
              </v-btn>
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-form>
    </v-card>
  </v-menu>
</template>

<script lang="ts" setup>
import { ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

defineProps({
  roundedBtn: {
    type: Boolean,
    default: false,
  },
});

const keyword = ref<string>("");
const route = useRoute();
const store = useStore();

const emit = defineEmits(["update"]);

function searchEvent() {
  if (keyword.value === null) {
    keyword.value = "";
  }
  store.commit("globalStore/setSearch", keyword.value);
  emit("update", true);
}

watch(
  () => route.path,
  () => {
    keyword.value = "";
    store.commit("globalStore/setSearch", "");
    emit("update", false);
  }
);
</script>

<style scoped>
.blue-gradient {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: white !important;
  border-radius: 10px;
}
.btn-dropdown {
  color: #065695;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
}
</style>
