<template>
  <v-container>
    <div class="mx-6 my-3">
      <v-row>
        <v-col cols="12">
          <v-card v-if="!modeSearch" class="card-non-outline">
            <v-card-text>
              <DashboardSummary />
            </v-card-text>
          </v-card>
          <v-card v-if="!modeSearch" class="card-non-outline my-3">
            <v-card-text class="py-2">
              <div class="d-flex justify-space-between align-center">
                <v-tabs v-model="tab" bg-color="white">
                  <v-tab
                    v-for="(item, idx) in listMenu"
                    :key="idx"
                    class="menu-list"
                    slider-color="transparent"
                    :value="item.name"
                    :to="{ name: item.name }"
                  >
                    {{ item.label }}
                  </v-tab>
                </v-tabs>

                <div v-if="tab === 'dashboard.assignment.v2'">
                  <AssignmentFilter />
                  <AssignmentSorting
                    :tab="currentTabType"
                    @update="setSorting"
                    :rounded-btn="false"
                  />
                  <SearchButton @update="updateSearchFilter" />
                </div>

                <div v-if="tab === 'dashboard.document.v2'">
                  <DocumentFilter />
                  <DocumentSorting
                    @update="setDocumentSorting"
                    :rounded-btn="false"
                  />
                  <SearchButton @update="updateSearchFilter" />
                </div>
                <div v-if="tab === 'dashboard.workspace.v2'">
                  <AssignmentFilter />
                  <WorkspaceSorting
                    @update="setWorkspaceSorting"
                    :rounded-btn="false"
                  />
                  <SearchButton @update="updateSearchFilter" />
                </div>
              </div>
            </v-card-text>
          </v-card>
          <router-view />
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import { TSortData, TMenuItem } from "@v2/Type";

import DashboardSummary from "@v2/components/dashboard/DashboardSummary.vue";
import AssignmentFilter from "@/v2/components/assignment/AssignmentFilter.vue";
import AssignmentSorting from "@/v2/components/assignment/AssignmentSorting.vue";
import DocumentFilter from "@/v2/components/document/DocumentFilter.vue";
import DocumentSorting from "@/v2/components/document/DocumentSorting.vue";
import WorkspaceSorting from "@/v2/components/workspace/WorkspaceSort.vue";

import { SearchRouteName } from "@/v2/enum/Search";
import SearchButton from "@/v2/components/search/SearchButton.vue";

const modeSearch = computed(() => store.getters["globalStore/getStatusSearch"]);

const currentTabType = computed(() => {
  const routeName = route.name as string;
  if (routeName?.includes("arahan")) {
    return "arahan";
  } else if (routeName?.includes("penugasan")) {
    return "penugasan";
  }
  return "penugasan"; // default
});

const tab = ref<string | null>(null);
const route = useRoute();
const router = useRouter();
const store = useStore();

const listMenu: TMenuItem[] = [
  {
    name: "dashboard.workspace.v2",
    label: "Workspace",
  },
  {
    name: "dashboard.document.v2",
    label: "Document",
  },
  {
    name: "dashboard.assignment.v2",
    label: "Assignment",
  },
];

const setSorting = (modelValue: TSortData): void => {
  store.commit("assignmentStore/setItemsSort", modelValue);
};

const setDocumentSorting = (modelValue: TSortData): void => {
  store.commit("documentsStore/setItemsSort", modelValue);
};

const setWorkspaceSorting = (val: TSortData): void => {
  store.commit("documentsStore/setItemsSort", val);
};

function updateSearchFilter(item) {
  const routeName = route.name ? SearchRouteName[route.name] : undefined;
  if (item && routeName) {
    router.push({ name: routeName });
  }
  store.commit("globalStore/setStatusSearch", item);
}

watch(
  () => route.path,
  (path) => {
    store.commit("globalStore/setStatusSearch", path.includes("search"));
  },
  { immediate: true }
);

onMounted(() => {
  if (route.name === "dashboard.v2") {
    router.replace({
      name: "dashboard.workspace.v2",
    });
  }
});
</script>

<style scoped>
.v-container {
  max-width: 100%;
}

.card-non-outline {
  border-radius: 15px;
  box-shadow: 0px 4px 18px 0px rgba(192, 192, 192, 0.25);
}

.menu-list {
  text-transform: capitalize;
  letter-spacing: -0.2px !important;
  font-style: normal;
  font-weight: 600;
  font-size: 13px;
  color: #267dc2;
  height: 35px;
}

:deep(.v-slide-group__container) {
  align-items: center !important;
  justify-content: space-between !important;
}

:deep(.menu-list.v-tab--selected) {
  background: linear-gradient(180deg, #d6212a 0%, #ff000d 100%);
  color: #fff !important;
  font-weight: 600 !important;
  border-radius: 15px !important;
}

:deep(.v-tab) {
  letter-spacing: 0.1px;
}

.blue-gradient {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: white !important;
  border-radius: 10px;
}

.text-grey-theme {
  color: rgba(121, 121, 121, 0.9);
}
</style>
