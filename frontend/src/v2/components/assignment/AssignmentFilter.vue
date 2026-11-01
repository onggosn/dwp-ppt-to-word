<template>
  <v-menu
    transition="slide-y-transition"
    bottom
    :close-on-content-click="false"
    :max-height="600"
    :width="450"
    v-model="menu"
  >
    <template v-slot:activator="{ props }">
      <v-btn v-if="roundedBtn" icon="" size="small" v-bind="props">
        <img src="/images/task/filter.svg" :width="20" :height="20" />
      </v-btn>
      <v-btn
        v-else
        class="btn-dropdown"
        variant="outlined"
        dark
        v-bind="props"
        style="overflow: hidden"
      >
        <v-icon icon="mdi-tune" color="#065695"></v-icon>
        <span class="ml-2"> Filter </span>
      </v-btn>
    </template>
    <v-card style="overflow-x: hidden; border-radius: 10px" width="400">
      <v-row class="mb-0">
        <v-col>
          <div class="my-3" v-if="list.length">
            <p class="text-title ml-5" style="margin-bottom: 0px !important">
              Filter By
            </p>
            <div v-for="(item, idx) in list" :key="idx">
              <p class="text-title mt-0 ml-5">
                {{ item.title }}
              </p>
              <v-list v-if="item.title !== 'Satker Koordinator'">
                <div
                  v-for="(val, idx) in expandedItems[item.name]
                    ? item.value
                    : item.value.slice(0, 5)"
                  :key="idx"
                >
                  <v-list-item
                    style="height: 5px; font-size: 11px; font-weight: 900"
                  >
                    <v-checkbox
                      :label="val.value"
                      :value="val.id"
                      v-model="checkedOptions[item.name]"
                      color="#05aa59"
                      style="margin-right: 0px"
                      density="compact"
                      hide-details
                    />
                  </v-list-item>
                </div>
                <v-btn
                  v-if="item.value.length > 5"
                  variant="text"
                  class="font-italic text-decoration-underline pa-0 ml-5"
                  color="blue"
                  @click="toggleExpand(item.name)"
                  style="font-size: 10px"
                >
                  {{ expandedItems[item.name] ? "See Less" : "See All" }}
                </v-btn>
              </v-list>
              <v-list v-else>
                <div class="ml-5 mr-5">
                  <SearchBar
                    :isAdmin="true"
                    accessType="role"
                    type="satker"
                    :placeHolderSearch="'Search Satker Koordinator here'"
                    @selected="handleSatkerSelected"
                    hide-details
                  />
                  <div
                    v-if="selectedSatker.length > 0"
                    class="d-flex flex-wrap mt-2"
                  >
                    <v-chip
                      v-for="item in selectedSatker"
                      :key="item.id"
                      closable
                      @click:close="removeSatker(item)"
                      class="mr-2 mt-2"
                      color="#6EB3EA"
                      style="border: 1px solid #007bff; border-radius: 6px"
                    >
                      <span style="color: #065391; font-size: 12px">
                        {{ item.value }}
                      </span>
                      <template v-slot:close>
                        <v-icon color="#065391">mdi-close</v-icon>
                      </template>
                    </v-chip>
                  </div>
                </div>
              </v-list>
            </div>
          </div>
          <div class="mx-4 mb-5">
            <v-btn
              block
              class="primary-gradient"
              style="border-radius: 10px"
              @click="applyFilter"
              >Apply</v-btn
            >
          </div>
        </v-col>
      </v-row>
    </v-card>
  </v-menu>
</template>
<script lang="ts" setup>
import { ref, onMounted, watch } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import { TResponseSearchByName } from "@v2/Type";
import SearchBar from "../collaboration/SearchBar.vue";

const props = defineProps({
  subFilter: {
    type: String,
    default: "",
  },
  roundedBtn: {
    type: Boolean,
    default: false,
  },
});

const store = useStore();
const route = useRoute();
const list = ref<any>([]);
const isLoading = ref<boolean>(false);
const checkedOptions = ref<any>({});
const lastAppliedCheckedOptions = ref<any>({});
const expandedItems = ref<Record<string, boolean>>({});
const menu = ref<any>(null);

const selectedSatker = ref<TResponseSearchByName[]>([]);
const lastAppliedSatker = ref<TResponseSearchByName[]>([]);

function getFilter() {
  isLoading.value = true;
  let requestData = {
    filterType: "assignment",
  };

  store
    .dispatch("assignmentStore/getAssignmentFilter", requestData)
    .then((resp) => {
      list.value = resp.responseData.data.filter;
      initializeCheckedOptions();
    })
    .finally(() => (isLoading.value = false));
}

function getFilterWorkspace() {
  isLoading.value = true;

  store
    .dispatch("assignmentStore/getWorkspaceFilter")
    .then((resp) => {
      list.value = resp.responseData.data;
      initializeCheckedOptions();
    })
    .finally(() => (isLoading.value = false));
}

function toggleExpand(name: string) {
  expandedItems.value[name] = !expandedItems.value[name];
}

function handleSatkerSelected(item) {
  if (!selectedSatker.value.some((existing) => existing.id === item.id)) {
    selectedSatker.value.push(item);
  }
}

function removeSatker(item) {
  selectedSatker.value = selectedSatker.value.filter((s) => {
    return s.id !== item.id;
  });
}

function resetToLastAppliedState() {
  checkedOptions.value = JSON.parse(
    JSON.stringify(lastAppliedCheckedOptions.value)
  );
  selectedSatker.value = [...lastAppliedSatker.value];
}

function initializeCheckedOptions() {
  list.value.forEach((item: any) => {
    checkedOptions.value[item.name] = [];
    expandedItems.value[item.name] = false;
  });

  // Save as last applied state (initial state)
  lastAppliedCheckedOptions.value = JSON.parse(
    JSON.stringify(checkedOptions.value)
  );
  lastAppliedSatker.value = [...selectedSatker.value];
}

function applyFilter() {
  menu.value = false;
  list.value.forEach((item: any) => {
    expandedItems.value[item.name] = false;
  });

  if (selectedSatker.value.length) {
    checkedOptions.value.satkerKoordinator = selectedSatker.value.map(
      (satker) => satker.id
    );
  }

  // Save current state as last applied state
  lastAppliedCheckedOptions.value = JSON.parse(
    JSON.stringify(checkedOptions.value)
  );
  lastAppliedSatker.value = [...selectedSatker.value];

  const filter = JSON.parse(JSON.stringify(checkedOptions.value));
  store.commit("assignmentStore/setItemsFilter", filter);
}

onMounted(() => {
  if (route.name === "dashboard.workspace.v2") {
    getFilterWorkspace();
  } else {
    getFilter();
  }
});

watch(
  () => [route.name, props.subFilter],
  () => {
    if (route.name === "dashboard.workspace.v2") {
      getFilterWorkspace();
    } else {
      getFilter();
    }
    selectedSatker.value = [];
    store.commit("assignmentStore/setItemsFilter", {});
  }
);

watch(menu, (newVal, oldVal) => {
  if (oldVal === true && newVal === false) {
    // Menu was closed, reset to last applied state
    resetToLastAppliedState();
  }
});
</script>
<style scoped>
.text-title {
  font-size: 13px;
  font-weight: 900;
}
.cheeckbox-custom {
  margin-top: 10px;
  font-size: 1.5vh;
  font-weight: bold;
  opacity: 0.7;
  display: grid;
  grid-template-columns: 1em auto;
  gap: 1em;
}
.cheeckbox-custom input[type="checkbox"] {
  width: 2vh;
  height: 2vh;
  accent-color: #05aa59;
}
.checkbox-spacing {
  margin: -15px -10px 0px -10px;
  height: 40px;
}

.v-list-item {
  min-height: 25px !important;
}
:deep(.v-application) {
  color: #05aa59 !important;
}
:deep(.v-list-item__title) {
  font-size: 15px;
  font-weight: 900;
  color: #4b4b4b;
}

:deep(.v-select__selection--comma) {
  font-weight: 900;
  color: #4b4b4b;
}
:deep .v-label {
  font-size: 13px;
  font-weight: 900;
}
.v-messages {
  flex: 1 1 auto;
  font-size: 12px;
  min-height: 14px;
  min-width: 1px;
  opacity: var(--v-medium-emphasis-opacity);
  position: relative;
}
.btn-dropdown {
  color: #065695;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
}
</style>
