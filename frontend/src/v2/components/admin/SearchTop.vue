<template>
  <v-sheet class="bg-transparent px-7">
    <v-row>
      <v-col cols="9">
        <v-sheet class="d-flex flex-row align-start bg-transparent">
          <v-btn
            icon="mdi-arrow-left"
            style="
              color: rgba(38, 125, 194, 1);
              box-shadow: 10px 4px 10px rgba(255, 255, 255, 1);
            "
            elevation="0"
            @click="back"
          ></v-btn>
          <div style="margin-left: 30px; padding-top: 12px">
            <p
              style="
                color: rgba(38, 125, 194, 1);
                font-size: 28px;
                font-weight: 600;
                line-height: 23px;
              "
            >
              {{ labelSearch }}
            </p>
            <p style="color: #4b4b4b; margin-top: 16px">
              Search results displayed
              {{ searchResultDisplayed }}
              (total relevant results
              {{ totalDataCount }})
            </p>
          </div>
        </v-sheet>
      </v-col>
      <v-col cols="3">
        <v-text-field
          v-model="localKeyword"
          density="compact"
          hide-details="auto"
          clearable
          placeholder="Search"
          variant="solo"
          @keyup.enter="getList"
          @click:clear="handleClear"
          :autofocus="true"
        >
          <template v-slot:prepend-inner>
            <img src="/images/task/searchMagnifier.svg" /></template
        ></v-text-field>
      </v-col>
    </v-row>
  </v-sheet>
</template>

<script setup lang="ts">
import { defineProps } from "vue";

import { ref, onMounted, computed, watch } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

const props = defineProps({
  keyword: {
    type: String,
    default: "",
  },
  item: {
    type: Object,
    default: null,
  },
});

const store = useStore();
const route = useRoute();
const emit = defineEmits(["update", "back"]);

const localKeyword = ref(props.keyword);

const totalData = computed(() => store.getters["adminStore/getTotalData"]);

const totalDataDocMateri = computed(
  () => store.getters["documentsStore/getTotalDataMateri"]
);
const totalDataHistory = computed(
  () => store.getters["historyStore/getTotalData"]
);
const totalDataDocHasil = computed(
  () => store.getters["documentsStore/getTotalDataHasil"]
);

const totalDataWorkspace = computed(
  () => store.getters["documentsStore/getTotalDataWorkspace"]
);

const totalWorkspacePerPage = computed(
  () => store.getters["documentsStore/getTotalWorkspacePerPage"]
);

const searchResultDisplayed = computed(() => {
  if (route.path.includes("admin-management")) {
    return totalData.value.tShow;
  } else if (route.name === "mydashboard-documentmateri-search") {
    return totalDataDocMateri.value.totalData;
  } else if (route.name === "mydashboard-documenthasil-search") {
    return totalDataDocHasil.value.totalData;
  } else if (route.path.includes("/history/search")) {
    return totalDataHistory.value.tShow;
  } else if (route.path.includes("mydashboard/workspace/search")) {
    return totalWorkspacePerPage.value ?? 0;
  } else {
    return 0;
  }
});

const totalDataCount = computed(() => {
  if (route.path.includes("admin-management")) {
    return totalData.value.totalData;
  } else if (route.name === "mydashboard-documentmateri-search") {
    return totalDataDocMateri.value.totalData;
  } else if (route.name === "mydashboard-documenthasil-search") {
    return totalDataDocHasil.value.totalData;
  } else if (route.path.includes("/history/search")) {
    return totalDataHistory.value.totalData;
  } else if (route.path.includes("mydashboard/workspace/search")) {
    return totalDataWorkspace.value ? totalDataWorkspace.value.totalData : 0;
  } else {
    return 0;
  }
});

const labelSearch = computed(() => {
  //admin management
  if (route.path.includes("admin-management/content")) return "List Content";
  if (route.path.includes("admin-management/meeting")) return "List Meeting";
  if (route.path.includes("admin-management/role")) return "List Role";

  //my dashboard
  if (route.path.includes("mydashboard/assignment/search"))
    return "List Penugasan";
  if (route.path.includes("mydashboard/arahan/search")) return "List Arahan";
  if (route.path.includes("mydashboard/documentmateri/search"))
    return "List Document";
  if (route.path.includes("mydashboard/documenthasil/search"))
    return "List Document";

  //assignment-management
  if (route.path.includes("/assignmentmanagement-new/assignment/search"))
    return "List Penugasan";

  if (route.path.includes("/assignmentmanagement-new/arahan/search"))
    return "List Arahan";

  if (route.path.includes("mydashboard/workspace")) {
    return "List Workspace";
  }
  //history
  if (route.path.includes("/history/search")) return "List Event";

  // default item
  return "List";
});

const getRouteType = () => {
  if (route.path.includes("admin-management")) return "admin";
  if (route.path.includes("mydashboard")) return "mydashboard";
  if (route.path.includes("assignmentmanagement-new")) return "assignment";
  if (route.path.includes("history")) return "history";
  return null;
};

const commitSearchValue = (value: string) => {
  const routeType = getRouteType();

  switch (routeType) {
    case "admin": {
      store.commit("adminStore/setSearchAdmin", value);
      break;
    }
    case "mydashboard": {
      if (
        route.path.includes("mydashboard/assignment/search") ||
        route.path.includes("mydashboard/arahan/search")
      ) {
        const myDashboardData =
          store.getters["assignmentStore/getStatusSearch"];
        myDashboardData.detail.searchKeyword = value;
        store.commit("assignmentStore/setStatusSearch", myDashboardData);
      } else {
        const myDashboardData = store.getters["documentsStore/getStatusSearch"];
        myDashboardData.detail.searchKeyword = value;
        store.commit("documentsStore/setStatusSearch", myDashboardData);
      }
      break;
    }
    case "assignment": {
      const assignmentData = store.getters["assignmentStore/getStatusSearch"];
      assignmentData.searchKeyword = value;
      store.commit("assignmentStore/setStatusSearch", assignmentData);
      break;
    }
    case "history": {
      store.commit("historyStore/setSearchHistory", value);
      break;
    }
  }
};

const getSearchValueFromStore = () => {
  const routeType = getRouteType();

  switch (routeType) {
    case "admin":
      return store.getters["adminStore/getSearchAdmin"];
    case "mydashboard":
      return route.path.includes("mydashboard/assignment/search") ||
        route.path.includes("mydashboard/arahan/search")
        ? store.getters["assignmentStore/getStatusSearch"]?.detail
            ?.searchKeyword || ""
        : store.getters["documentsStore/getStatusSearch"]?.detail
            ?.searchKeyword || "";
    case "assignment":
      return (
        store.getters["assignmentStore/getStatusSearch"]?.searchKeyword || ""
      );
    case "history":
      return store.getters["historyStore/getSearchHistory"];
    default:
      return "";
  }
};

function back() {
  emit("back", route.path);
}

function handleClear() {
  commitSearchValue("");
}

function getList() {
  commitSearchValue(localKeyword.value);
}
onMounted(() => {
  localKeyword.value = getSearchValueFromStore();
});

watch(
  () => localKeyword.value,
  (value) => {
    if (value === "" || value === null || value === undefined) {
      commitSearchValue("");
    }
  }
);
</script>

<style scoped>
.empty-illustration {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}
:deep(.v-field) {
  border-radius: 15px;
}
:deep(.v-input--horizontal) {
  display: contents;
}
:deep(.v-pagination__item--is-active) {
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%) !important;
  color: white !important;
  border-radius: 10px;
}
:deep(.v-pagination .v-btn) {
  border-radius: 10px;
  font-size: 15px;
  font-weight: bold;
}
:deep(.v-pagination__item) {
  color: #065695;
  border-radius: 10px;
  background: white;
}
:deep(.v-pagination__next) {
  color: #065695;
  border-radius: 10px;
  background: white;
}
:deep(.v-pagination__prev) {
  color: #065695;
  border-radius: 10px;
  background: white;
}
</style>
