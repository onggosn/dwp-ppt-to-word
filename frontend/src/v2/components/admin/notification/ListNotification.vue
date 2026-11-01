<template>
  <p class="font-weight-bold mb-3" style="font-size: 18px; color: #065695">
    List Notification
  </p>

  <div class="notification-list my-5 mx-2 elevation-3 rounded-lg pa-5 bg-white">
    <!-- Loading Shimmer -->
    <div v-if="isLoading" class="mb-6">
      <v-table class="notification-table">
        <thead>
          <tr>
            <th
              class="table-header table-header-index"
              style="text-align: center !important"
            >
              No
            </th>
            <th class="table-header" style="text-align: left !important">
              Fitur
            </th>
            <th class="table-header" style="text-align: left !important">
              Trigger
            </th>
            <th class="table-header" style="text-align: left !important">
              Status
            </th>
            <th class="table-header" style="text-align: left !important">
              Action
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="n in 3" :key="n" class="shimmer-row">
            <td class="table-index">
              <div class="shimmer-text shimmer"></div>
            </td>
            <td><div class="shimmer-text shimmer"></div></td>
            <td><div class="shimmer-text shimmer"></div></td>
            <td><div class="shimmer-text shimmer"></div></td>
            <td><div class="shimmer-chip shimmer"></div></td>
          </tr>
        </tbody>
      </v-table>
    </div>

    <!-- Actual Content -->
    <div v-else class="mb-6">
      <v-table class="notification-table">
        <thead>
          <tr>
            <th
              class="table-header table-header-index"
              style="text-align: center !important"
            >
              No
            </th>
            <th class="table-header" style="text-align: left !important">
              Fitur
            </th>
            <th class="table-header" style="text-align: left !important">
              Trigger
            </th>

            <th class="table-header" style="text-align: left !important">
              Status
            </th>
            <th class="table-header" style="text-align: left !important">
              Action
            </th>
          </tr>
        </thead>
        <tbody>
          <template
            v-for="(item, index) in list"
            :key="item.idNotificationType"
          >
            <tr
              class="notification-row"
              :class="{
                'expanded-parent': isExpanded(item.idNotificationType),
              }"
              @click="toggleRow(item.idNotificationType)"
              style="cursor: pointer"
            >
              <td class="table-index" style="text-align: center">
                {{ (currentPage - 1) * pagination.entriesPerPage + index + 1 }}
              </td>
              <td class="notification-title">
                <div
                  class="title-notification"
                  style="
                    text-align: left !important;
                    justify-content: left !important;
                    align-items: left !important;
                    font-weight: 500;
                  "
                >
                  {{ item.fitur }}
                </div>
              </td>
              <td style="text-align: left">
                <div class="title-content">
                  {{ item.trigger }}
                </div>
              </td>
              <td style="text-align: left">
                <div class="d-flex align-center justify-start">
                  <v-icon
                    :color="item.isActive ? '#4CAF50' : '#9E9E9E'"
                    size="8"
                    class="mr-2"
                  >
                    mdi-circle
                  </v-icon>
                  <span>{{ item.isActive ? "Active" : "In Active" }}</span>
                </div>
              </td>

              <td style="text-align: left">
                <div class="action-buttons">
                  <v-btn
                    :icon="
                      isExpanded(item.idNotificationType)
                        ? 'mdi-chevron-up'
                        : 'mdi-chevron-right'
                    "
                    size="x-small"
                    variant="text"
                    color="#267DC2"
                    @click.stop="toggleRow(item.idNotificationType)"
                  >
                    <v-icon
                      class="table-content-center"
                      color="#267DC2"
                      small
                      style="border-radius: 4px; padding: 13px; cursor: pointer"
                    >
                      {{
                        isExpanded(item.idNotificationType)
                          ? "mdi-chevron-up"
                          : "mdi-chevron-right"
                      }}
                    </v-icon>
                    <v-tooltip activator="parent" location="top">
                      {{
                        isExpanded(item.idNotificationType)
                          ? "Hide Details"
                          : "View Details"
                      }}
                    </v-tooltip>
                  </v-btn>
                </div>
              </td>
            </tr>
            <tr v-if="isExpanded(item.idNotificationType)" class="details-row">
              <td colspan="5" class="px-5">
                <div
                  v-if="isLoadingDetail[item.idNotificationType]"
                  class="pa-4"
                >
                  <v-row>
                    <v-col cols="6">
                      <div
                        class="shimmer mb-3"
                        style="height: 20px; width: 100px"
                      ></div>
                      <div class="mb-4">
                        <div
                          class="shimmer mb-2"
                          style="height: 14px; width: 120px"
                        ></div>
                        <div
                          class="shimmer"
                          style="height: 18px; width: 180px"
                        ></div>
                      </div>
                      <div
                        class="shimmer mb-3 mt-6"
                        style="height: 20px; width: 100px"
                      ></div>
                      <div
                        class="shimmer mb-2"
                        style="height: 14px; width: 60px"
                      ></div>
                      <div
                        class="shimmer mb-4"
                        style="height: 18px; width: 90%"
                      ></div>
                    </v-col>
                    <v-col cols="6">
                      <div
                        class="shimmer mb-3"
                        style="height: 20px; width: 100px"
                      ></div>
                      <div
                        class="shimmer mb-2"
                        style="height: 14px; width: 60px"
                      ></div>
                      <div
                        class="shimmer mb-6"
                        style="height: 100px; width: 100%"
                      ></div>
                      <div
                        class="shimmer mb-3"
                        style="height: 20px; width: 100px"
                      ></div>
                      <div
                        class="shimmer"
                        style="height: 16px; width: 80%"
                      ></div>
                    </v-col>
                  </v-row>
                </div>
                <div
                  v-else-if="detailsMap[item.idNotificationType]"
                  class="pa-4"
                >
                  <v-row>
                    <v-col cols="6">
                      <p class="detail-title">Receiver</p>
                      <template
                        v-for="r in detailsMap[item.idNotificationType]
                          .listReceiver"
                        :key="r.receiverId"
                      >
                        <p class="detail-label mb-1">{{ r.receiverName }}</p>
                        <p class="text-14 font-weight-medium mb-3">
                          {{ getReceiverChannels(r) }}
                        </p>
                      </template>

                      <p class="detail-title mt-6">Wording</p>
                      <p class="detail-label mb-1">Push</p>
                      <div
                        class="text-14 mb-4 wording-content"
                        v-html="detailsMap[item.idNotificationType].pushWording"
                      ></div>

                      <p class="detail-label mb-1">InApp</p>
                      <div
                        class="text-14 mb-4 wording-content"
                        v-html="
                          detailsMap[item.idNotificationType].loncengWording
                        "
                      ></div>
                    </v-col>
                    <v-col cols="6">
                      <p class="detail-title">Wording</p>
                      <p class="detail-label mb-1">Email</p>
                      <div
                        class="text-14 mb-6 wording-content email-wording"
                        v-html="
                          detailsMap[item.idNotificationType].wordingEmail
                        "
                      ></div>

                      <p class="detail-title">Log</p>
                      <div
                        class="text-13 mt-2 font-italic text-grey-darken-1"
                        style="font-family: inherit"
                      >
                        Last modified by:
                        {{
                          detailsMap[item.idNotificationType].lastModifiedBy ||
                          "-"
                        }}
                        |
                        {{
                          formatDate(
                            detailsMap[item.idNotificationType].lastModifiedDate
                          )
                        }}
                      </div>
                    </v-col>
                  </v-row>
                  <v-row class="mt-4">
                    <v-col cols="12">
                      <v-btn
                        width="100%"
                        class="bg-gradient-darkblue font-weight-medium rounded-lg"
                        elevation="4"
                        size="large"
                        height="35"
                        style="color: white"
                        @click="openEditDialog(item.idNotificationType)"
                      >
                        Edit
                      </v-btn>
                    </v-col>
                  </v-row>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </v-table>
    </div>

    <!-- Empty State -->
    <div
      v-if="!isLoading && list.length === 0"
      class="empty-state text-center py-8"
    >
      <v-icon
        icon="mdi-bell-off-outline"
        size="64"
        color="grey-lighten-1"
      ></v-icon>
      <div class="empty-text mt-4">No Notifications found</div>
    </div>

    <!-- Pagination -->
    <div v-if="!isLoading && list.length > 0" class="pagination-container mt-4">
      <v-pagination
        v-model="currentPage"
        :length="pagination.totalPage"
        :total-visible="5"
        @update:model-value="changePage"
        class="custom-pagination"
      ></v-pagination>
    </div>
  </div>

  <EditNotificationDialog ref="editNotif" @on-save="refreshList" />
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from "vue";
import EditNotificationDialog from "./EditNotificationDialog.vue";
import { useStore } from "vuex";

const store = useStore();

const list = ref<any[]>([]);
const pagination = ref({
  totalData: 0,
  pageNo: 1,
  totalPage: 1,
  entriesPerPage: 10,
});
const searchMode = computed(() => store.getters["globalStore/getStatusSearch"]);
const searchValue = computed(() => store.getters["globalStore/getSearch"]);
const isLoading = ref<boolean>(false);
const isLoadingDetail = ref<Record<number, boolean>>({});
const detailsMap = ref<Record<number, any>>({});
const currentPage = ref<number>(1);
const expandedRows = ref<number[]>([]);
const editNotif = ref();

function formatDate(date: string) {
  if (!date) return "-";
  const d = new Date(date);
  if (isNaN(d.getTime())) return date;

  const datePart = new Intl.DateTimeFormat("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
  }).format(d);

  const timePart = new Intl.DateTimeFormat("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  }).format(d);

  return `Date: ${datePart} | Time: ${timePart} WIB`;
}

function getReceiverChannels(r: any) {
  const channels: string[] = [];
  if (r.isPush) channels.push("Push");
  if (r.isLonceng) channels.push("In App");
  if (r.isEmail) channels.push("Email");
  return channels.length > 0 ? channels.join(", ") : "-";
}

function highlightMarkers(text: string) {
  if (!text) return "-";
  // Replace {0}, {1}, etc with highlighted spans
  let processed = text.replace(
    /\{(\d+)\}/g,
    '<span class="marker-highlight">{$1}</span>'
  );
  // Optional: replace *bold* with <b> tags if you want to support markdown-like bolding
  processed = processed.replace(/\*(.*?)\*/g, "<b>$1</b>");
  return processed;
}

const toggleRow = (id: number) => {
  const index = expandedRows.value.indexOf(id);
  if (index > -1) {
    expandedRows.value.splice(index, 1);
  } else {
    expandedRows.value.push(id);
    getDetail(id);
  }
};

const isExpanded = (id: number) => expandedRows.value.includes(id);

function getDetail(id: number) {
  if (detailsMap.value[id]) return;

  isLoadingDetail.value[id] = true;
  store
    .dispatch("adminStore/getListNotificationDetail", {
      idNotificationType: id,
    })
    .then((res: any) => {
      if (res.responseData) {
        detailsMap.value[id] = res.responseData;
      }
    })
    .finally(() => {
      isLoadingDetail.value[id] = false;
    });
}

function getList() {
  isLoading.value = true;

  store
    .dispatch("adminStore/getListNotification", {
      search: searchMode.value ? searchValue.value : "",
      pageNo: currentPage.value,
      pageSize: pagination.value.entriesPerPage,
    })
    .then((res: any) => {
      if (res.responseCode === "011000") {
        list.value = res.responseData.data || [];
        pagination.value.totalData = res.responseData.infoPage?.totalData ?? 0;
        pagination.value.totalPage = res.responseData.infoPage?.totalPage ?? 1;
        const totalData = res.responseData.infoPage?.totalData;
        const totalDataPerPage = res.responseData.data?.length || 0;
        store.commit("globalStore/setTotalData", totalData);
        store.commit("globalStore/setTotalDataPerPage", totalDataPerPage);
      }
    })
    .finally(() => {
      isLoading.value = false;
    });
}

function changePage(curr: number) {
  pagination.value.pageNo = curr;
  getList();
}

function openEditDialog(id: number) {
  editNotif.value.show(id);
}

function refreshList() {
  expandedRows.value = [];
  detailsMap.value = {};
  getList();
}

onMounted(() => {
  getList();
});

watch(
  () => searchValue.value,
  () => {
    if (searchMode.value) {
      pagination.value.pageNo = 1;
      currentPage.value = 1;
      getList();
    }
  },
  { deep: true }
);
</script>

<style scoped>
.item-label {
  color: #4b4b4b;
  font-size: 11px;
  line-height: 24px;
  font-weight: 800;
}

.empty-state {
  color: #a6abc7;
}

.empty-text {
  font-size: 16px;
  color: #797979e5;
}

/* Shimmer Loading Styles */
.shimmer {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 4px;
}

.shimmer-chip {
  height: 24px;
  width: 60px;
  border-radius: 12px;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* Notification Table Styles */
.notification-table {
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0px 2px 8px 0px rgba(0, 0, 0, 0.1);
}

:deep(.v-table) {
  background-color: white;
}

:deep(.v-table__wrapper) {
  border-radius: 10px;
}

.table-header {
  background-color: #f7fbfe !important;
  color: #267dc2 !important;
  font-weight: 700 !important;
  font-size: 14px !important;
  padding: 16px 12px !important;
  border-bottom: 2px solid #e9ecef !important;
  text-align: left !important;
}

.table-header-index {
  width: 60px !important;
  text-align: center !important;
}

.table-index {
  width: 60px;
  text-align: center;
  font-weight: 600;
  color: #6c757d;
  font-size: 14px;
}

.notification-row {
  transition: all 0.2s ease;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
}

.notification-row:hover {
  background-color: #f8f9fa;
}

.details-row {
  background-color: #f7fbfe;
}

.details-row td {
  border-bottom: 1px solid #e9ecef !important;
}

.bg-light-blue-lighten-5 {
  background-color: #f7fbfe;
}

.bg-gradient-darkblue {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
}

.notification-row td {
  padding: 16px 12px !important;
  vertical-align: middle;
}

.notification-title {
  max-width: 300px;
}

.title-content {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
  font-size: 14px;
}

.action-buttons {
  display: flex;
  gap: 4px;
  justify-content: flex-start;
}

.action-buttons :deep(.v-btn) {
  border: none !important;
  border-radius: 6px !important;
}

.action-buttons :deep(.v-btn:hover) {
  border-color: currentColor !important;
}

/* Shimmer styles for table */
.shimmer-row td {
  padding: 16px 12px !important;
}

.shimmer-text {
  height: 16px;
  width: 100%;
  max-width: 120px;
  border-radius: 4px;
}

/* Pagination Styles */
.pagination-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
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

.detail-title {
  color: #757575;
  font-size: 15px;
  font-weight: 500;
  margin-bottom: 12px;
}

.detail-label {
  color: #9e9e9e;
  font-size: 14px;
  font-weight: 500;
}

.wording-content {
  line-height: 1.6;
  color: #4b4b4b;
}

.email-wording :deep(table) {
  border-collapse: collapse;
  width: 100%;
}

.email-wording :deep(td) {
  padding: 2px 0;
}

.email-wording :deep(a) {
  pointer-events: none;
  cursor: default;
  text-decoration: none;
  color: black; /* Keep the color so it still looks like a link */
}

:deep(.marker-highlight) {
  background-color: #f7fb35;
  color: #000;
  font-weight: bold;
  padding: 0 4px;
  border-radius: 4px;
  display: inline-block;
  line-height: 1.4;
}
</style>
