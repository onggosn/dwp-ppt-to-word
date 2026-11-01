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
        :class="route.name === 'dashboard.document.v2.hasil' ? 'mr-2' : ''"
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
                <b v-if="route.name === 'dashboard.document.v2.materi'">
                  {{ item.title }}
                </b>
                <b v-else>
                  {{ item.title !== "Document Type" ? item.title : "" }}
                </b>
              </p>
              <v-list v-if="item.title !== 'Document Type'">
                <div
                  v-for="(val, idx) in item.name === 'status' &&
                  route.name === 'dashboard.document.v2.hasil'
                    ? item.value.slice(-1)
                    : expandedItems[item.name]
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
                <div
                  class="ml-5 mr-5"
                  v-if="route.name === 'dashboard.document.v2.materi'"
                >
                  <SearchBar
                    :isAdmin="true"
                    accessType="role"
                    type="doctype"
                    :placeHolderSearch="'Search Document Type here'"
                    @selected="handleDoctypeSelected"
                    hide-details
                  />
                  <div
                    v-if="selectedDocType.length > 0"
                    class="d-flex flex-wrap mt-2"
                  >
                    <v-chip
                      v-for="item in selectedDocType"
                      :key="item.id"
                      closable
                      @click:close="removeDoctype(item)"
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
import { TResponseSearchByDocType } from "@v2/Type";
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

const selectedDocType = ref<TResponseSearchByDocType[]>([]);
const lastAppliedDocType = ref<TResponseSearchByDocType[]>([]);

function getFilter() {
  isLoading.value = true;
  let requestData = {};

  store
    .dispatch("documentsStore/getDocumentFilter", requestData)
    .then((resp) => {
      list.value = resp.responseData.data.filter;
      initializeCheckedOptions();
    })
    .finally(() => (isLoading.value = false));
}

function toggleExpand(name: string) {
  expandedItems.value[name] = !expandedItems.value[name];
}

function handleDoctypeSelected(item) {
  if (!selectedDocType.value.some((existing) => existing.id === item.id)) {
    selectedDocType.value.push(item);
  }
}

function removeDoctype(item) {
  selectedDocType.value = selectedDocType.value.filter((s) => {
    return s.id !== item.id;
  });
}

function resetToLastAppliedState() {
  checkedOptions.value = JSON.parse(
    JSON.stringify(lastAppliedCheckedOptions.value)
  );
  selectedDocType.value = [...lastAppliedDocType.value];
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
  lastAppliedDocType.value = [...selectedDocType.value];
}

function applyFilter() {
  menu.value = false;
  list.value.forEach((item: any) => {
    expandedItems.value[item.name] = false;
  });

  if (selectedDocType.value.length) {
    checkedOptions.value.documentType = selectedDocType.value.map(
      (doctype) => doctype.id
    );
  } else {
    checkedOptions.value.documentType = [];
  }

  // Save current state as last applied state
  lastAppliedCheckedOptions.value = JSON.parse(
    JSON.stringify(checkedOptions.value)
  );
  lastAppliedDocType.value = [...selectedDocType.value];

  const filter = JSON.parse(JSON.stringify(checkedOptions.value));

  store.commit("documentsStore/setItemsFilter", filter);
}

onMounted(() => {
  getFilter();
});

watch(
  () => [route.name, props.subFilter],
  () => {
    getFilter();
    selectedDocType.value = [];
    store.commit("documentsStore/setItemsFilter", {});
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
