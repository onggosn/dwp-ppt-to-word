<template>
  <v-menu :close-on-content-click="false" v-model="menu" width="400">
    <template v-slot:activator="{ props }">
      <v-btn
        v-if="roundedBtn"
        class="ml-2"
        density="default"
        icon="mdi-swap-vertical"
        size="small"
        variant="text"
        style="background-color: #fff; border-radius: 50px"
        elevation="2"
        color="#267DC2"
        v-bind="props"
      ></v-btn>
      <!-- CLASS mr-2 CUMA SEMENTARA SAMPAI SORT DI-REFACTOR -->
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
              :items="filteredSortingList"
              item-title="value"
              color="#e4e4e4"
              item-value="id"
              placeholder="Sort Based"
              v-model="sortField"
              :error="!!errorMessage"
              :error-messages="errorMessage"
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

<script lang="ts" setup>
import { ref, watch, PropType, computed, onMounted } from "vue";
import { TSortingData } from "@/v2/Type";
import { useStore } from "vuex";
import { useRoute } from "vue-router";

const store = useStore();
const route = useRoute();
const props = defineProps({
  items: {
    type: Array as PropType<TSortingData[]>,
    default: () => [],
  },
  roundedBtn: {
    type: Boolean,
    default: false,
  },
  tab: {
    type: String,
    default: "penugasan",
  },
});

const emit = defineEmits(["update"]);
const menu = ref(false);
const sortField = ref<string | null>(null);
const sortOrder = ref<string>("ascending");
const errorMessage = ref("");

const sortDirections = ref<TSortingData[]>([
  { id: "ascending", value: "A-Z" },
  { id: "descending", value: "Z-A" },
]);

const isShortContent = computed(() => {
  return sortField.value !== "batasWaktu" && sortField.value !== "status";
});

const sortingList = ref<TSortingData[]>();

const filteredSortingList = computed(() => {
  if (!sortingList.value) return [];

  if (props.tab === "arahan") {
    return sortingList.value.filter(
      (item) => item.id !== "batasWaktu" && item.id !== "status"
    );
  }

  return sortingList.value;
});

const getSortingListType = () => {
  store
    .dispatch("assignmentStore/getAssignmentFilter", {
      filterType: "assignment",
    })
    .then((res) => {
      if (res.responseCode == "011000") {
        let result = res.responseData ?? {};
        sortingList.value = result.data.sort ?? [];
      }
    });
};

onMounted(() => {
  getSortingListType();
});

watch(sortField, (newField) => {
  if (!newField) {
    errorMessage.value = "Please select a sorting option first.";
    return;
  }

  errorMessage.value = "";

  if (newField === "status") {
    sortDirections.value = [
      { id: "ascending", value: "In Progress-Done" },
      { id: "descending", value: "Done-In Progress" },
    ];
    sortOrder.value = "ascending";
  } else if (newField === "batasWaktu") {
    sortDirections.value = [
      { id: "descending", value: "Oldest-Newest" },
      { id: "ascending", value: "Newest-Oldest" },
    ];
    sortOrder.value = "ascending";
  } else {
    sortDirections.value = [
      { id: "ascending", value: "A-Z" },
      { id: "descending", value: "Z-A" },
    ];
    sortOrder.value = "ascending";
  }

  emit("update", {
    sortName: sortField.value,
    sortType: sortOrder.value,
  });
});

watch(sortOrder, () => {
  if (sortField.value) {
    emit("update", {
      sortName: sortField.value,
      sortType: sortOrder.value,
    });
  }
});

watch(
  () => route.name,
  () => {
    store.commit("assignmentStore/setItemsSort", {});
    sortField.value = null;
    sortOrder.value = "";
  }
);
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

.sortButton {
  border: 2px solid #e4e4e4;
  color: #797979;
  font-weight: 900;
  height: 48px;
}
</style>
