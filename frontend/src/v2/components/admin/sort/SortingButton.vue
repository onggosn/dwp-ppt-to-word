<template>
  <div class="text-center">
    <v-menu :close-on-content-click="false" v-model="menu">
      <template v-slot:activator="{ props }">
        <v-btn
          color="#065695"
          class="rounded-lg font-weight-bold"
          v-bind="props"
          prepend-icon="mdi-swap-vertical"
          variant="outlined"
          style="font-size: 16px"
        >
          Sort
        </v-btn>
      </template>

      <v-list>
        <v-sheet class="pa-3 rounded-lg" style="width: 250px">
          <p class="mb-2 font-weight-bold text-newBlack">Sort By</p>

          <v-select
            style="border: 1px red !important"
            variant="outlined"
            :items="items"
            item-title="value"
            color="#e4e4e4"
            item-value="id"
            placeholder="Sort Based"
            v-model="selectedItem"
          ></v-select>
          <v-btn class="mt-n5 w-100 blue-gradient" @click="updateSort"
            >Apply</v-btn
          >
        </v-sheet>
      </v-list>
    </v-menu>
  </div>
</template>

<script lang="ts" setup>
import { PropType, ref, computed, onUpdated } from "vue";
import { TListSortingType } from "@/v2/Type";
import { useRoute } from "vue-router";

const props = defineProps({
  items: {
    type: Array as PropType<TListSortingType[]>,
    default: () => [],
  },
  title: {
    type: String,
    default: "",
  },
  initalData: Object,
});

const emit = defineEmits(["update", "update:title"]);
const route = useRoute();
const menu = ref(false);
const selectedItem = ref<TListSortingType>();
const currentSortingId = computed(() => {
  const eventSort = route.query.eventSort;
  return eventSort ? parseInt(eventSort as string, 10) : null;
});

const updateSort = () => {
  emit("update", selectedItem.value);
  menu.value = false;
};

onUpdated(() => {
  selectedItem.value = props.items.find(
    (item) => item.id === currentSortingId.value
  );
});
</script>
<style scoped>
.btn-dropdown {
  color: #065695;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
}

.blue-gradient {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: white !important;
  border-radius: 10px;
}

:deep(.v-list.v-theme--light.v-list--density-default.v-list--one-line) {
  margin-top: 10px;
  border-radius: 8px;
}
:deep(.v-input__control) {
  border: 2px solid #e4e4e4;
  border-radius: 4px;
  /* height: 45px;*/
}
</style>
