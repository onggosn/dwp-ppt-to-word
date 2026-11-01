<template>
  <div class="d-flex justify-space-between align-center">
    <p class="font-weight-bold mb-3" style="font-size: 18px; color: #065695">
      List Pegawai
    </p>
  </div>

  <div class="user-list my-5 mx-2 elevation-3 rounded-lg pa-5 bg-white">
    <!-- Loading Shimmer -->
    <div v-if="isLoading" class="mb-6">
      <v-table class="user-table">
        <thead>
          <tr>
            <th
              class="table-header table-header-index"
              style="text-align: center !important"
            >
              No
            </th>
            <th class="table-header" style="text-align: left !important">
              User
            </th>
            <th class="table-header" style="text-align: left !important">
              Satker
            </th>
            <th class="table-header" style="text-align: left !important">
              Jabatan
            </th>
            <th class="table-header" style="text-align: left !important">
              Role
            </th>
            <th class="table-header" style="text-align: left !important">
              Action
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="n in 5" :key="n" class="shimmer-row">
            <td><div class="shimmer-text shimmer"></div></td>
            <td><div class="shimmer-text shimmer"></div></td>
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
      <v-table class="user-table">
        <thead>
          <tr>
            <th
              class="table-header table-header-index"
              style="text-align: center !important"
            >
              No
            </th>
            <th class="table-header" style="text-align: left !important">
              User
            </th>
            <th class="table-header" style="text-align: left !important">
              Satker
            </th>
            <th class="table-header" style="text-align: left !important">
              Jabatan
            </th>
            <th class="table-header" style="text-align: left !important">
              Role
            </th>
            <th class="table-header" style="text-align: left !important">
              Action
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in list" :key="item.id" class="user-row">
            <td style="text-align: center">
              {{ (currentPage - 1) * pagination.entriesPerPage + index + 1 }}
            </td>
            <td class="user-name">
              <div
                class="title-user"
                style="
                  text-align: left !important;
                  justify-content: left !important;
                  align-items: left !important;
                  font-weight: 500;
                "
              >
                {{ item.name || "-" }}
              </div>
            </td>
            <td style="text-align: left">
              <div class="title-content">
                {{ item.satkerName || "-" }}
              </div>
            </td>
            <td style="text-align: left">
              <div class="title-content">
                {{ item.jabatanName || "-" }}
              </div>
            </td>
            <td style="text-align: left">
              {{ item.combinedRoleName || "-" }}
            </td>
            <td style="text-align: left">
              <div class="action-buttons">
                <v-btn
                  icon="mdi-pencil"
                  size="x-small"
                  color="#267DC2"
                  @click="editUser(item)"
                  variant="outlined"
                  class="rounded-lg px-2 py-2"
                >
                  <v-icon class="table-content-center" color="#267DC2" small>
                    mdi-pencil
                  </v-icon>
                  <v-tooltip activator="parent" location="top">
                    Edit User
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
      v-if="!isLoading && list.length === 0"
      class="empty-state text-center py-8"
    >
      <v-icon
        icon="mdi-account-off-outline"
        size="64"
        color="grey-lighten-1"
      ></v-icon>
      <div class="empty-text mt-4">No Users found</div>
    </div>

    <!-- Pagination -->
    <div v-if="!isLoading && list.length > 0" class="mt-4">
      <v-pagination
        v-model="currentPage"
        :length="pagination.totalPage"
        :total-visible="8"
        @update:model-value="changePage"
        rounded="1"
        elevation="2"
        size="small"
      ></v-pagination>
    </div>
  </div>

  <EditUserDialog ref="editUserDialog" @onClose="getList" />
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch, getCurrentInstance } from "vue";
import EditUserDialog from "./EditUserDialog.vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";

const store = useStore();
const route = useRoute();
const { root } = getCurrentInstance() as any;

const list = ref<any[]>([]);
const pagination = ref({
  totalData: 0,
  pageNo: 1,
  totalPage: 1,
  entriesPerPage: 10,
});
const searchMode = computed(() => store.getters["globalStore/getStatusSearch"]);
const searchValue = computed(() => store.getters["globalStore/getSearch"]);
const filterValue = computed(() => store.getters["adminStore/getItemsFilter"]);
const isLoading = ref<boolean>(false);
const currentPage = ref<number>(1);
const editUserDialog = ref();

function getList() {
  isLoading.value = true;
  let payload = {
    searchKeyword: searchMode.value ? searchValue.value : "",
    pageNumber: currentPage.value,
    satkerFilter: searchMode.value ? [] : filterValue.value.satkerFilter || [],
    jabatanFilter: searchMode.value
      ? []
      : filterValue.value.jabatanFilter || [],
    roleFilter: searchMode.value ? [] : filterValue.value.roleFilter || [],
    sortBy: searchMode.value
      ? 0
      : parseInt((route.query.eventSort as string) ?? 0),
    pageSize: 10,
  };

  store
    .dispatch("adminStore/getListMUserAndRole", payload)
    .then((res: any) => {
      if (res.responseCode === "011000") {
        list.value = res.responseData.listMUserAndRoles || [];
        pagination.value.totalData = res.responseData.info?.totalData ?? 0;
        pagination.value.totalPage = res.responseData.info?.totalPage ?? 1;
        const totalData = res.responseData.info?.totalData;
        const totalDataPerPage =
          res.responseData.listMUserAndRoles?.length || 0;
        store.commit("globalStore/setTotalData", totalData);
        store.commit("globalStore/setTotalDataPerPage", totalDataPerPage);
      }
    })
    .catch(() => {
      root.refs.toast.show({
        message: "Failed to fetch users. Please try again later.",
        color: "error",
        timeout: 5000,
      });
    })
    .finally(() => {
      isLoading.value = false;
    });
}

function changePage(curr: number) {
  currentPage.value = curr;
  pagination.value.pageNo = curr;
  getList();
}

function editUser(item: any) {
  editUserDialog.value.show(item);
}

onMounted(() => {
  getList();
});

watch(
  () => JSON.stringify(filterValue.value),
  (newValue, oldValue) => {
    if (!searchMode.value && newValue !== oldValue) {
      pagination.value.pageNo = 1;
      currentPage.value = 1;
      getList();
    }
  }
);

watch(
  [searchValue, route],
  () => {
    if (searchMode.value) {
      pagination.value.pageNo = 1;
      currentPage.value = 1;
    }
    getList();
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

/* User Table Styles */
.user-table {
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

.user-row {
  transition: all 0.2s ease;
  border-bottom: 1px solid #f0f0f0;
}

.user-row:hover {
  background-color: #f8f9fa;
}

.user-row td {
  padding: 16px 12px !important;
  vertical-align: middle;
}

.user-name {
  max-width: 200px;
}

.title-content {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
  font-size: 14px;
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
