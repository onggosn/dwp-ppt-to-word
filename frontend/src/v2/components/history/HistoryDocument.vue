<template>
  <div class="document-history-list my-5 mx-2 elevation-3 rounded-lg pa-5">
    <p class="item-label mb-5" style="font-size: 18px">List Document</p>

    <!-- Loading Shimmer -->
    <div v-if="loading" class="mb-6">
      <v-table class="document-table">
        <thead>
          <tr>
            <th class="table-header table-header-index">No</th>
            <th class="table-header">Name</th>
            <th class="table-header">Task Name</th>
            <th class="table-header">Type</th>
            <th class="table-header">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="n in 3" :key="n" class="shimmer-row">
            <td class="table-index">
              <div class="shimmer-text shimmer"></div>
            </td>
            <td><div class="shimmer-text shimmer"></div></td>
            <td><div class="shimmer-chip shimmer"></div></td>
            <td><div class="shimmer-chip shimmer"></div></td>
            <td><div class="shimmer-text shimmer"></div></td>
          </tr>
        </tbody>
      </v-table>
    </div>

    <!-- Actual Content -->
    <div v-else class="mb-6">
      <v-table class="document-table">
        <thead>
          <tr>
            <th class="table-header table-header-index">No</th>
            <th class="table-header" style="text-align: left !important">
              Name
            </th>
            <th class="table-header">Task Name</th>
            <th class="table-header">Type</th>
            <th class="table-header">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(item, index) in items"
            :key="item.documentId"
            class="document-row"
          >
            <td class="table-index" style="text-align: center">
              {{ (currentPage - 1) * pageSize + index + 1 }}
            </td>
            <td class="document-title">
              <div
                class="title-document"
                style="
                  text-align: left !important;
                  justify-content: left !important;
                  align-items: left !important;
                  font-weight: 500;
                "
              >
                {{ item.documentName }}
              </div>
            </td>
            <td style="text-align: center">
              <div class="title-content">
                {{ item.taskName }}
              </div>
            </td>
            <td style="text-align: center">
              <div class="title-content">
                {{ item.documentType }}
              </div>
            </td>

            <td style="text-align: center">
              <div class="action-buttons" v-if="item.isPreview">
                <v-btn
                  v-if="item.isPreview"
                  icon="mdi-file-document-outline"
                  size="x-small"
                  variant="text"
                  color="#267DC2"
                  @click="viewDocument(item)"
                >
                  <v-icon
                    class="table-content-center"
                    color="#267DC2"
                    small
                    style="border-radius: 4px; padding: 13px; cursor: pointer"
                  >
                    mdi-file-document-outline
                  </v-icon>
                  <v-tooltip activator="parent" location="top">
                    Preview Document
                  </v-tooltip>
                </v-btn>
                <v-btn
                  v-if="item.isDownload"
                  icon="mdi-file-document-outline"
                  size="x-small"
                  variant="text"
                  color="#267DC2"
                  @click="downloadDocument(item)"
                >
                  <v-icon
                    class="table-content-center"
                    color="#267DC2"
                    small
                    style="border-radius: 4px; padding: 13px; cursor: pointer"
                  >
                    mdi-cloud-download
                  </v-icon>
                  <v-tooltip activator="parent" location="top">
                    Download Document
                  </v-tooltip>
                </v-btn>
              </div>
            </td>
          </tr>
        </tbody>
      </v-table>
    </div>

    <!-- Empty State -->
    <div
      v-if="!loading && items.length === 0"
      class="empty-state text-center py-8"
    >
      <v-icon
        icon="mdi-clipboard-text-off"
        size="64"
        color="grey-lighten-1"
      ></v-icon>
      <div class="empty-text mt-4">No Documents found</div>
    </div>

    <!-- Pagination -->
    <div v-if="!loading && items.length > 0" class="pagination-container mt-4">
      <v-pagination
        v-model="currentPage"
        :length="totalPages"
        :total-visible="5"
        @update:model-value="handlePageChange"
        class="custom-pagination"
      ></v-pagination>

      <!-- Page Info -->
      <!-- <div class="page-info mt-2 text-center">
        <span class="page-info-text">
          Showing {{ startItem }} to {{ endItem }} of {{ totalItems }} documents
        </span>
      </div> -->
    </div>
  </div>
  <download-dialog
    v-if="loadingDownload"
    :titleLoading="titleLoading"
    :progress="downloadProgress"
    :total-progress="fileSize"
  />
</template>

<script lang="ts" setup>
import { ref, defineProps, onMounted, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { toSlug } from "@/v2/helpers/utils";
import downloadDialog from "@/v2/components/utils/dialog/LoadingDownload.vue";
import { insertLog } from "@/models/log";
import { formatBytes } from "@/v2/helpers/utils";
import { getFileExtension } from "@/v2/helpers/utils";
import client from "@/library/ApiClient";
import { v4 as uuidv4 } from "uuid";

const store = useStore();
const items = ref<DocumentItem[]>([]);
const router = useRouter();
const loadingDownload = ref(false);

const props = defineProps<{ id: string }>();
const loading = ref(true);

// Pagination variables
const currentPage = ref(1);
const pageSize = ref(5);
const totalItems = ref(0);
const totalPages = ref(0);

const payload = computed(() => ({
  workspaceId: props.id,
  page: currentPage.value,
  pageSize: pageSize.value,
}));

const timeStart = ref(0);
const timeEnd = ref(0);
const traceId = ref("");
const titleLoading = ref("");
const downloadProgress = ref(0);
const fileSize = ref(0);

onMounted(() => {
  fetchDocumentList();
});

const fetchDocumentList = () => {
  loading.value = true;
  store
    .dispatch("historyStore/getHistoryDocumentList", payload.value)
    .then((res) => {
      if (res.responseCode == "011000") {
        if (res.responseData.data) {
          items.value = res.responseData.data;
          totalItems.value =
            res.responseData.totalData || res.responseData.total || 0;
        } else {
          items.value = res.responseData;
          totalItems.value = res.responseData.length || 0;
        }
        totalPages.value = res.responseData.infoPage.totalPage;
      }
      loading.value = false;
    })
    .catch(() => {
      loading.value = false;
    });
};

// Handle page change
const handlePageChange = (page: number) => {
  currentPage.value = page;
  fetchDocumentList();
};

interface DocumentItem {
  documentId: string;
  documentName: string;
  taskName: string;
  documentType: string;
  isPreview: string;
  isDownload: string;
  workspaceId?: string;
  taskId?: string;
}

const downloadDocument = (item: DocumentItem) => {
  if (toSlug(item.documentType) === "hasilpembahasan") {
    doDownloadDocument(
      item,
      getFileExtension(item.documentName),
      client.DownloadDocumentById.bind(client),
      "Download Hasil Pembahasan Document"
    );
  } else {
    doDownloadDocument(
      item,
      getFileExtension(item.documentName),
      client.DownloadDocument.bind(client),
      "Download Support Document"
    );
  }
};

const doDownloadDocument = (
  item: DocumentItem,
  type,
  downloadMethod,
  logMessage
) => {
  traceId.value = uuidv4();
  loadingDownload.value = true;
  timeStart.value = performance.now();

  downloadMethod({
    store: store,
    data: {
      id: item?.documentId,
      typeDocument: type,
      traceId: traceId.value,
    },
    onDownloadProgress: (progressEvent) => {
      titleLoading.value =
        "Download progress: " + formatBytes(progressEvent.loaded);
      downloadProgress.value = progressEvent.loaded;
      fileSize.value = progressEvent.loaded;
    },
  })
    .then((response) => {
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      const documentDownloadName =
        item?.documentName.split(".")[0] + "." + type;

      link.href = url;
      link.setAttribute("download", documentDownloadName);
      document.body.appendChild(link);
      link.click();

      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      timeEnd.value = performance.now();
      insertLog(
        traceId.value,
        item.documentId,
        documentDownloadName,
        fileSize.value,
        timeStart.value,
        timeEnd.value,
        logMessage
      );
    })
    .catch((error) => {
      void error;
    })
    .finally(() => {
      loadingDownload.value = false;
    });
};

const viewDocument = (item: DocumentItem) => {
  const routeData = router.resolve({
    name:
      toSlug(item.documentType) === "hasilpembahasan"
        ? "preview-document"
        : "preview-document-support",
    params: {
      pageId: 1,
      workspaceId: item?.workspaceId,
      documentId: item.documentId,
      taskId: item?.taskId,
    },
  });
  window.open(routeData.href, "_blank");
};
</script>

<style scoped>
.line-dashed {
  width: 100%;
  height: 1px;
  border-top: 1.5px dashed #065695;
  background-color: transparent;
}

.item-content-information {
  color: #4b4b4b;
  font-size: 13px;
  line-height: 19.5px;
}

.item-content-label {
  color: #a6abc7;
  font-size: 13px;
  line-height: 19.5px;
  font-weight: 600;
}

.item-information {
  color: #797979e5;
  font-size: 14px;
  line-height: 19.5px;
}

.item-label {
  color: #4b4b4b;
  font-size: 11px;
  line-height: 24px;
  font-weight: 800;
}

.comment-item {
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #065695;
}

.comment-header {
  margin-bottom: 8px;
}

.comment-author {
  font-weight: 600;
  color: #4b4b4b;
  font-size: 13px;
}

.comment-date {
  color: #a6abc7;
  font-size: 12px;
}

.comment-text {
  color: #4b4b4b;
  font-size: 13px;
  line-height: 18px;
}

.empty-state {
  color: #a6abc7;
}

.empty-text {
  font-size: 16px;
  color: #797979e5;
}

/* Shimmer Loading Styles */
.shimmer-item {
  background: white;
  border-radius: 10px;
  box-shadow: 0px 2px 4px 0px #0000001f;
  padding: 16px;
  min-height: 60px;
}

.shimmer-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.shimmer {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 4px;
}

.shimmer-text-long {
  height: 20px;
  flex: 1;
  max-width: 300px;
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

/* Document Table Styles */
.document-table {
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
  text-align: center !important;
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

.document-row {
  transition: all 0.2s ease;
  border-bottom: 1px solid #f0f0f0;
}

.document-row:hover {
  background-color: #f8f9fa;
}

.document-row td {
  padding: 16px 12px !important;
  vertical-align: top;
}

.document-title {
  max-width: 300px;
}

.title-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 14px;
}

.title-content .item-label {
  font-size: 14px !important;
  font-weight: 800;
  color: #4b4b4b;
  line-height: 24px;
  margin-bottom: 4px;
}

.item-description {
  font-size: 12px;
  color: #797979e5;
  line-height: 16px;
  margin-top: 4px;
}

.action-buttons {
  display: flex;
  gap: 4px;
  justify-content: center;
}

.action-buttons :deep(.v-btn) {
  border: 1px solid #267dc2 !important;
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

.custom-pagination :deep(.v-pagination__item) {
  font-weight: 600;
  color: #267dc2;
  box-shadow: #4b4b4b1a 0px 2px 4px 0px;
}

.custom-pagination :deep(.v-pagination__item--is-active) {
  background-color: #267dc2 !important;
  color: white !important;
}

.custom-pagination :deep(.v-pagination__prev),
.custom-pagination :deep(.v-pagination__next) {
  color: #267dc2;
  background: white;
  box-shadow: #4b4b4b1a 0px 2px 4px 0px;
}

.custom-pagination :deep(.v-pagination__prev:hover),
.custom-pagination :deep(.v-pagination__next:hover) {
  background-color: #f7fbfe;
}

.page-info {
  margin-top: 12px;
}

.page-info-text {
  color: #797979e5;
  font-size: 14px;
  font-weight: 500;
}
</style>
