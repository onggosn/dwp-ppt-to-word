<template>
  <div class="d-flex justify-space-between">
    <v-tabs v-model="tab" bg-color="transparent">
      <v-tab class="tab-header" value="materi"> MATERI PEMBAHASAN </v-tab>
      <v-tab class="tab-header" value="hasil"> HASIL PEMBAHASAN </v-tab>
    </v-tabs>
    <free-style-shimmer
      v-if="
        (tab == 'hasil' && hasil.isLoading) ||
        (tab == 'materi' && materi.isLoading)
      "
      height="35px"
      width="140px"
      border-radius="10px"
      color="#d3d3d3"
    />
    <v-btn v-else class="btn-download" @click="download(tab)"
      >Download .xls</v-btn
    >
  </div>
  <v-window v-model="tab" class="mt-2">
    <v-window-item value="materi">
      <div v-if="materi.isEmpty">
        <img
          src="/images/no_document_available.svg"
          style="display: block; margin: 0 auto; width: 450px; margin-top: 80px"
        />
      </div>
      <dash-doc-component
        ref="materi"
        :items="materi.list"
        :loading="materi.isLoading"
        :pagination="materi.pagination"
        v-else
      />
      <div class="text-center mt-7">
        <v-pagination
          rounded="1"
          elevation="2"
          size="small"
          v-model="materi.pagination.page"
          :length="materi.pagination.total"
          :total-visible="materi.pagination.visible"
          @update:modelValue="getMateri()"
        />
      </div>
    </v-window-item>
    <v-window-item value="hasil">
      <div v-if="hasil.isEmpty">
        <img
          src="/images/no_document_available.svg"
          style="display: block; margin: 0 auto; width: 450px; margin-top: 80px"
        />
      </div>
      <dash-doc-component
        ref="hasil"
        :items="hasil.list"
        :loading="hasil.isLoading"
        :pagination="hasil.pagination"
        v-else
      />
      <div class="text-center mt-7">
        <v-pagination
          rounded="1"
          elevation="2"
          size="small"
          v-model="hasil.pagination.page"
          :length="hasil.pagination.total"
          :total-visible="hasil.pagination.visible"
          @update:modelValue="getHasil()"
        />
      </div>
    </v-window-item>
  </v-window>
  <custom-loading
    v-if="materi.isDownload"
    :title="materi.titleLoading"
    :progress="materi.downloadProgress"
    :totalProgress="materi.documentSize"
    :hasProgress="true"
  />
  <custom-loading
    v-if="hasil.isDownload"
    :title="hasil.titleLoading"
    :progress="hasil.downloadProgress"
    :totalProgress="hasil.documentSize"
    :hasProgress="true"
  />
</template>

<script>
import client from "@/library/ApiClient";
import DashDocComponent from "@/components/dashboard/DashDocComponent.vue";
import CustomLoading from "@/components/CustomLoading.vue";

export default {
  name: "dhsDocument",
  emits: ["subTabChange", "dataLoading"],
  components: {
    DashDocComponent,
    CustomLoading,
  },
  props: {
    filter: {
      type: Object,
      default: function () {
        return {};
      },
    },
  },
  data() {
    return {
      tab: null,
      hasil: {
        isLoading: true,
        isEmpty: false,
        list: [],
        pagination: {
          page: 1,
          total: 0,
          visible: 10,
        },
        blob: {},
        isDownload: false,
        titleLoading: "Waiting for server respond",
        downloadProgress: 0,
        fileSize: 0,
      },
      materi: {
        isLoading: true,
        isEmpty: false,
        list: [],
        pagination: {
          page: 1,
          total: 0,
          visible: 10,
        },
        blob: {},
        isDownload: false,
        titleLoading: "Waiting for server respond",
        downloadProgress: 0,
        fileSize: 0,
      },
    };
  },
  methods: {
    reloadPage() {
      if (this.tab == "hasil") {
        this.hasil.pagination.page = 1;
        this.getHasil();
      } else if (this.tab == "materi") {
        this.materi.pagination.page = 1;
        this.getMateri();
      }
    },
    setFilter(type = "materi", page = true) {
      // debugger;
      let checkbox = this.filter.filter ?? {};
      let sort = this.filter.sort ?? {};
      let additionalFilter,
        pageFilter = {};
      let pages, pageSizes;

      pages = this.hasil.pagination.page;
      pageSizes = this.hasil.pagination.visible;

      if (type == "materi") {
        additionalFilter = {
          processBusiness: checkbox.processBusiness ?? [],
        };
        pages = this.materi.pagination.page;
        pageSizes = this.materi.pagination.visible;
      }

      if (page) {
        pageFilter = {
          page: pages,
          pageSize: pageSizes,
        };
      }

      let requestData = {
        username: this.$store.state.username,

        category: checkbox.category ?? [],
        workspaceType: checkbox.workspacetype ?? [],
        year: checkbox.year ?? [],
        month: checkbox.month ?? [],
        documentType: checkbox.documentType ?? [],
        satkerPembuat: checkbox.satkerPembuat ?? [],

        sortName: sort.sortName ?? "",
        sortType: sort.sortType ?? "",
        sortTime: sort.sortTime ?? "",
        ...additionalFilter,
        ...pageFilter,
      };

      return requestData;
    },
    getHasil() {
      this.hasil.isLoading = true;
      this.$emit("dataLoading", true);
      this.hasil.isEmpty = false;
      this.hasil.list = [];

      let requestData = this.setFilter(this.tab, true);

      client
        .getListDocumentByUsername({
          store: this.$store,
          data: requestData,
        })
        .then((res) => {
          let result = res.plainData.responseData ?? {};
          this.hasil.pagination.total = result.infoPage?.totalPage ?? 0;

          let hasilList = result.data ?? [];
          this.hasil.list = hasilList;
          this.hasil.isEmpty = hasilList.length == 0;
        })
        .catch(() => {
          this.hasil.isEmpty = true;
        })
        .finally(() => {
          this.$emit("dataLoading", false);
          this.hasil.isLoading = false;
        });
    },
    getMateri() {
      // debugger;
      this.materi.isLoading = true;
      this.$emit("dataLoading", true);
      this.materi.isEmpty = false;
      this.materi.list = [];

      let requestData = this.setFilter(this.tab, true);

      client
        .getListDocumentSupportByUsername({
          store: this.$store,
          data: requestData,
        })
        .then((res) => {
          let result = res.plainData.responseData ?? {};
          this.materi.pagination.total = result.infoPage?.totalPage ?? 0;

          let materiList = result.data ?? [];
          this.materi.list = materiList;
          this.hasil.isEmpty = materiList.length == 0;
        })
        .catch(() => {
          this.hasil.isEmpty = true;
        })
        .finally(() => {
          this.$emit("dataLoading", false);
          this.materi.isLoading = false;
        });
    },
    download(tab) {
      if (tab == "materi") {
        this.downloadExcelMateri();
      } else {
        this.downloadExcelHasil();
      }
    },
    downloadExcelMateri() {
      // debugger;
      this.materi.isDownload = true;
      let requestData = this.setFilter(this.tab, false);

      client
        .downloadDocumentMateriExcel({
          store: this.$store,
          data: requestData,
          onDownloadProgress: (progressEvent) => {
            this.materi.titleLoading =
              "Download progress: " + this.formatBytes(progressEvent.loaded);
            this.materi.downloadProgress = progressEvent.loaded;
            this.materi.fileSize = progressEvent.loaded;
          },
        })
        .then((res) => {
          const link = document.createElement("a");
          link.href = window.URL.createObjectURL(new Blob([res.data]));
          link.setAttribute("download", "Materi_Pembahasan.xlsx");
          document.body.appendChild(link);
          link.click();
        })
        .catch(() => {
          this.materi.isDownload = false;
        })
        .finally(() => {
          this.materi.titleLoading = "Waiting for server respond";
          this.materi.isDownload = false;
          this.materi.downloadProgress = 0;
          this.materi.fileSize = 0;
        });
    },
    downloadExcelHasil() {
      // debugger;
      this.hasil.isDownload = true;
      let requestData = this.setFilter(this.tab, false);

      client
        .downloadDocumentHasilExcel({
          store: this.$store,
          data: requestData,
          onDownloadProgress: (progressEvent) => {
            this.hasil.titleLoading =
              "Download progress: " + this.formatBytes(progressEvent.loaded);
            this.hasil.downloadProgress = progressEvent.loaded;
            this.hasil.fileSize = progressEvent.loaded;
          },
        })
        .then((res) => {
          const link = document.createElement("a");
          link.href = window.URL.createObjectURL(new Blob([res.data]));
          link.setAttribute("download", "Hasil_Pembahasan.xlsx");
          document.body.appendChild(link);
          link.click();
        })
        .catch(() => {
          this.hasil.isDownload = false;
        })
        .finally(() => {
          this.hasil.titleLoading = "Waiting for server respond";
          this.hasil.isDownload = false;
          this.hasil.downloadProgress = 0;
          this.hasil.fileSize = 0;
        });
    },
    formatBytes(bytes, decimals = 2) {
      if (!+bytes) return "0.00 Bytes";

      const k = 1024;
      const dm = decimals < 0 ? 0 : decimals;
      const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];

      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
    },
  },
  created() {
    // this.getHasil();
    this.getMateri();
    this.$emit("subTabChange", null);
  },
  watch: {
    tab(value) {
      this.$emit("subTabChange", value);
    },
    filter() {
      this.reloadPage();
    },
  },
};
</script>

<style scoped>
:deep(.tab-header.v-slide-group-item--active) {
  background: none !important;
  color: red !important;
  border: none !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: red !important;
}

:deep(.v-btn.v-tab) {
  font-weight: 600;
  background: -webkit-linear-gradient(#065695, #267dc2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
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
}
:deep(.v-pagination__next) {
  color: #065695;
}
:deep(.v-pagination__prev) {
  color: #065695;
}
.btn-download {
  border-radius: 10px;
  background: var(
    --Greent-Text,
    linear-gradient(0deg, #639b4e 0%, #639b4e 100%)
  );
  color: white;
  margin-top: 20px;
}
</style>
