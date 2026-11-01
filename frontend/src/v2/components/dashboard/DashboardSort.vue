<template>
  <div class="text-center mx-1">
    <v-menu :close-on-content-click="false" v-model="showMenu">
      <template v-slot:activator="{ props }">
        <v-btn icon="" size="small" v-bind="props" style="margin-left: 8px">
          <img
            :src="require('@/v2/assets/icon/sort.svg')"
            :width="20"
            :height="20"
          />
        </v-btn>
      </template>
      <v-card min-width="300">
        <p class="text-title ml-5 mt-1">Sort by</p>
        <v-sheet class="pa-3 rounded-lg">
          <v-select
            style="border: 1px red !important"
            variant="outlined"
            :items="filterData"
            item-title="value"
            color="#e4e4e4"
            item-value="id"
            placeholder="Sort Based"
            v-model="selectedItem"
          ></v-select>
        </v-sheet>
      </v-card>
    </v-menu>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";

const emit = defineEmits(["update"]);

const filterData = ref([
  "status",
  "workspace name",
  "nama penugasan",
  "batas waktu",
]);

const selectedItem = ref();

const showMenu = ref(false);

const applyFilter = () => {
  emit("update", selectedItem.value);
  showMenu.value = false;
};
</script>
<style scoped>
.blue-gradient {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: white !important;
  border-radius: 10px;
}
.text-grey-theme {
  color: rgba(121, 121, 121, 0.9);
}
</style>
