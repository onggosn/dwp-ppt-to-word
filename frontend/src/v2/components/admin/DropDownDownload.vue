<template>
  <div class="text-center">
    <v-menu>
      <template v-slot:activator="{ props }">
        <v-btn
          class="btn-dropdown w-100"
          variant="outlined"
          dark
          v-bind="props"
          prepend-icon="mdi-cloud-download"
          append-icon="mdi-chevron-down"
        >
          Download
        </v-btn>
      </template>

      <v-list>
        <v-list-item v-for="(item, index) in listDownload" :key="index">
          <v-list-item-title
            style="cursor: pointer"
            @click.prevent="download(item)"
            >{{ item.value }}</v-list-item-title
          >
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
  <LoadingDownload
    v-if="downloadLoading"
    :title="bandwidthSpend"
  ></LoadingDownload>
</template>
<script lang="ts" setup>
import { ref, getCurrentInstance, computed } from "vue";
import { useStore } from "vuex";
import LoadingDownload from "@/v2/components/utils/dialog/LoadingDownload.vue";
import { TListDownload } from "@/v2/Type";
import { useRoute } from "vue-router";
import { useDownloadBlob } from "@/v2/composables/useDownloadBlob";

const store = useStore();
const route = useRoute();
const { root } = getCurrentInstance() as any;
const downloadLoading = ref(false);
const listDownload = ref<TListDownload[]>([]);

const bandwidthSpend = computed(
  () => store.getters["adminStore/getLabelProgress"]
);

const DOWNLOAD_CONFIGS = [
  {
    path: "admin-management/role",
    isRole: true,
    filename: (type) => `DWP_User_Role.${type}`,
    totalSheetKey: "totalSheetRole",
    downloadAction: "adminStore/downloadRole",
  },
  {
    path: "admin-management/content",
    isRole: false,
    filename: (type, sheet, timestamp) =>
      type === "csv"
        ? sheet === 1
          ? `PredefinedContentPD_${timestamp}.${type}`
          : `PredefinedSTPMapping_${timestamp}.${type}`
        : `PredefinedContent_${timestamp}.${type}`,
    totalSheetKey: "totalSheet",
    downloadAction: "adminStore/download",
  },
];

function getDownloadConfig(currentPath) {
  return DOWNLOAD_CONFIGS.find((cfg) => currentPath.includes(cfg.path));
}

const download = async (param) => {
  const config = getDownloadConfig(route.path);
  if (!config) return;

  const totalSheet = param[config.totalSheetKey] || 1;

  if (param.type === "csv" && !config.isRole) {
    for (let index = 1; index <= totalSheet; index++) {
      await downloadFile(param, index, config);
    }
  } else {
    await downloadFile(param, totalSheet, config);
  }
};

const buildPayload = (param, sheet) => {
  const itemsFilter = store.getters["adminStore/getItemsFilter"];
  const searchAdmin = store.getters["adminStore/getSearchAdmin"] ?? "";
  if (route.path.includes("role")) {
    return {
      satkerFilter:
        store.getters["adminStore/getItemsFilter"].satkerFilter ?? [],
      gradeFilter: store.getters["adminStore/getItemsFilter"].gradeFilter ?? [],
      type: param.type,
      sortBy: parseInt((route.query.eventSort as string) ?? 0),
      roleSearching: searchAdmin,
    };
  } else {
    return {
      type: param.type,
      sheet,
      eventSearching: searchAdmin,
      eventTypeFilter: [1],
      eventSubTypeListFilter: itemsFilter.eventSubTypeListFilter,
      sectorFilter: itemsFilter.sector,
      dateSince: itemsFilter.dateSince === "" ? null : itemsFilter.dateSince,
      dateTo: itemsFilter.dateTo === "" ? null : itemsFilter.dateTo,
      eventSort: route.query.eventSort ?? null,
    };
  }
};

const downloadFile = async (param, sheet, config) => {
  try {
    downloadLoading.value = true;
    const payload = buildPayload(param, sheet);
    let res;
    let filename = "";
    // Generate timedatenow
    const now = new Date();
    const pad = (n: number) => n.toString().padStart(2, "0");
    const timestamp = `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(
      now.getDate()
    )}_${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`;

    filename = config.filename(param.type, sheet, timestamp);
    res = await store.dispatch(config.downloadAction, payload);
    useDownloadBlob(res.data, filename);
  } catch (error) {
    root.refs.toast.show({
      message: "Download file expired",
      color: "error",
      timeout: 5000,
    });
  } finally {
    downloadLoading.value = false;
  }
};

store.dispatch("adminStore/getListDownload").then((res) => {
  listDownload.value = res.responseData;
});
</script>
<style scoped>
.btn-dropdown {
  color: #065695;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
}
</style>
