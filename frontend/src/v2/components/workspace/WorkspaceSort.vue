<template>
  <v-menu :close-on-content-click="false" v-model="menu" width="400">
    <template v-slot:activator="{ props }">
      <!-- CLASS mr-2 HANYA SEMENTARA SAMPAI BUTTON SORT DI-REFACTOR -->
      <v-btn
        v-if="roundedBtn"
        class="ml-2 mr-2"
        density="default"
        icon="mdi-swap-vertical"
        size="small"
        variant="text"
        style="background-color: #fff; border-radius: 50px"
        elevation="2"
        color="#267DC2"
        v-bind="props"
      ></v-btn>

      <!-- CLASS mr-2 HANYA SEMENTARA SAMPAI BUTTON SORT DI-REFACTOR -->
      <v-btn
        v-else
        class="ml-2 mr-2 btn-dropdown"
        variant="outlined"
        dark
        v-bind="props"
        style="overflow: hidden"
      >
        <v-icon icon="mdi-swap-vertical" color="#065695"></v-icon>
        <span class="ml-2"> Sort </span>
      </v-btn>
    </template>

    <v-list>
      <v-sheet class="pa-3 rounded-lg">
        <p class="mb-2 font-weight-bold text-newBlack text-12">Sort By</p>
        <v-row>
          <v-col
            :cols="isShortContent ? 9 : 6"
            style="
              padding-top: 15px;
              padding-left: 10px;
              padding-right: 2px;
              padding-bottom: 0px;
            "
          >
            <v-select
              class="custom-select-height"
              variant="outlined"
              :items="itemsFilter"
              item-title="value"
              color="#e4e4e4"
              item-value="id"
              placeholder="Sort Based"
              v-model="sortField"
            />
          </v-col>
          <v-col
            :cols="isShortContent ? 3 : 6"
            style="
              padding-top: 15px;
              padding-left: 2px;
              padding-right: 10px;
              padding-bottom: 0px;
            "
          >
            <v-select
              class="custom-select-height m-n5"
              variant="outlined"
              :items="sortDirections"
              item-title="value"
              item-value="id"
              placeholder="A-Z"
              color="#e4e4e4"
              v-model="sortOrder"
            />
          </v-col>
        </v-row>
      </v-sheet>
    </v-list>
  </v-menu>
</template>

<script setup lang="ts">
import useDashboard from "@/v2/composables/workspaces/useDashboard";
import { DashboardSort } from "@/v2/enum/Enum";
import { computed, ref, watch } from "vue";

defineProps({
  roundedBtn: {
    type: Boolean,
    default: false,
  },
});

const { itemsFilter } = useDashboard();

const emit = defineEmits(["update"]);

const menu = ref(false);

const sortField = ref<string | null>(null);
const sortOrder = ref<string | null>(null);

const errorMessage = ref("");

const sortDirections = ref([
  { id: "ascending", value: "A-Z" },
  { id: "descending", value: "Z-A" },
]);

const isShortContent = computed(() => {
  return sortField.value !== DashboardSort.TanggalRDG;
});

watch(sortField, (newField) => {
  if (!newField) {
    errorMessage.value = "Please select a sorting option first.";
    return;
  }

  errorMessage.value = "";

  if (newField === DashboardSort.TanggalRDG) {
    sortDirections.value = [
      { id: "descending", value: "Newest to Oldest" },
      { id: "ascending", value: "Oldest to Newest" },
    ];
    sortOrder.value = "descending";
  }

  emit("update", {
    sortName: sortField.value,
    sortType: sortOrder.value,
  });
});

watch(sortOrder, (newOrder) => {
  emit("update", {
    sortName: sortField.value,
    sortType: newOrder,
  });
});
</script>

<style scoped>
.sortButton {
  border: 2px solid #e4e4e4;
  color: #797979;
  font-weight: 900;
  height: 48px;
}

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
  border-radius: 6px;
  /* height: 45px;*/
}

:deep(
    .custom-select-height .v-input__control,
    .custom-select-height .v-field__input
  ) {
  min-height: 45px !important; /* Or whatever height you want */
  height: 45px !important;
  font-size: 14px;
  border-radius: 14px !important;
}

:deep(.custom-select-height .v-field .v-field__append-inner) {
  height: 40px !important;
}

:deep(.custom-select-height .v-field) {
  --v-field-input-padding-top: 8px !important;
  font-size: 14px;
  border-radius: 12px;
}

:deep(.custom-select-height .v-select__selection .v-field) {
  --v-field-input-padding-top: 0px !important;
  --v-field-input-padding-bottom: 0px !important;
  font-size: 14px;
}

:deep(.v-select__selection) {
  display: block;
}
</style>
