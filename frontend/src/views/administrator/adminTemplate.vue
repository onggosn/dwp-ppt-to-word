<template>
  <div v-if="hasil.isEmpty">
    <v-img
      src="/images/no_document_available.svg"
      style="display: block; margin: 0 auto; width: 450px; margin-top: 80px"
    />
  </div>
  <admin-template-component
    ref="hasil"
    :items="hasil.list"
    :loading="hasil.isLoading"
    :pagination="hasil.pagination"
    @reloadPage="reloadPage()"
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
      @update:modelValue="getUserList()"
    />
  </div>
</template>
<script>
import AdminTemplateComponent from "@/components/administrator/AdminTemplateComponent.vue";
import { mGetListTemplate } from "@/models/Administrator";
export default {
  name: "AdminTemplate",
  emits: ["subTabChange", "dataLoading"],
  components: {
    AdminTemplateComponent,
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
          entriesPerPage: 10,
        },
      },
    };
  },
  methods: {
    reloadPage() {
      this.hasil.pagination.page = 1;
      this.getUserList();
    },
    getUserList() {
      this.hasil.isLoading = true;
      this.$emit("dataLoading", true);
      this.hasil.isEmpty = false;
      this.hasil.list = [];

      let checkbox = this.filter.filter ?? {};
      let sort = this.filter.sort ?? {};

      let requestData = {
        pageNo: this.hasil.pagination.page,
        entriesPerPage: this.hasil.pagination.entriesPerPage,
        username: this.$store.state.username,

        searchKeyword: this.filter.searchKeyword ?? "",

        category: checkbox.category ?? [],
        workspacetype: checkbox.workspacetype ?? [],
        year: checkbox.year ?? [],
        month: checkbox.month ?? [],

        sortName: sort.sortName ?? "",
        sortType: sort.sortType ?? "",
        sortTime: sort.sortTime ?? "",
      };

      mGetListTemplate(requestData.pageNo, requestData.entriesPerPage)
        .then((res) => {
          if (res.error == 0) {
            let result = res.list.plainData.responseData ?? {};
            this.hasil.pagination.total = result.info.totalPage ?? 0;

            let hasilList = result.data ?? [];
            this.hasil.list = hasilList;
            this.hasil.isEmpty = hasilList.length == 0;
          } else {
            throw new Error(res.error);
          }
        })
        .catch((err) => {
          if (err?.message === "403") {
            this.$root.toast.show({
              message: "tidak memiliki akses ke halaman ini",
              color: "warning",
              timeout: 3000,
            });
            this.$router.push({
              name: "home",
            });
          }
          this.hasil.isEmpty = true;
        })
        .finally(() => {
          this.$emit("dataLoading", false);
          this.hasil.isLoading = false;
        });
    },
  },
  created() {
    this.getUserList();
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
</style>
