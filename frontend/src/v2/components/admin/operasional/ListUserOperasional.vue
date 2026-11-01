<template>
  <p
    v-if="!searchMode"
    class="font-weight-bold mb-3 mt-3 ml-1"
    style="font-size: 18px; color: #065695"
  >
    List User
  </p>
  <div>
    <v-card class="rounded-lg pa-4 mb-4" v-if="!searchMode">
      <div class="toggle-section text-right">
        <div class="d-flex justify-end">
          <div class="custom-switch-container">
            <template v-if="isLoadingToggle">
              <v-progress-circular
                color="#085391"
                :width="6"
                :size="25"
                indeterminate
              ></v-progress-circular>
            </template>
            <template v-else>
              <div
                class="custom-switch"
                :class="{ active: enableAllMFA }"
                @click="toggleSwitch"
              >
                <div class="switch-thumb"></div>
              </div>
            </template>

            <span class="switch-label">
              {{ enableAllMFA == true ? "Disable" : "Enable" }} MFA</span
            >
          </div>
        </div>
      </div>
    </v-card>

    <!-- Custom skeleton matching user card layout -->
    <div v-if="isLoading" class="skeleton-list">
      <div
        v-for="i in 5"
        :key="i"
        class="skeleton-user-card"
        :style="{ animationDelay: `${(i - 1) * 0.07}s` }"
      >
        <div class="sk-block sk-name"></div>
        <div class="sk-block sk-satker"></div>
        <div class="sk-block sk-jabatan"></div>
        <div class="sk-block sk-checkbox"></div>
        <div class="sk-block sk-checkbox"></div>
      </div>
    </div>

    <template v-if="!isLoading">
      <list-user-item
        v-for="(item, idx) in list"
        :is-loading="isLoading"
        :key="idx"
        class="mt-3"
        :item="item"
        :delay="`${idx * 0.07}s`"
      ></list-user-item>
    </template>

    <div class="text-center mt-7">
      <v-pagination
        v-if="list?.length && !isLoading"
        rounded="1"
        elevation="2"
        size="small"
        v-model="currentPage"
        :length="pagination.totalPage"
        :total-visible="10"
        @update:model-value="changePage"
      />
    </div>

    <div v-if="!list?.length && !isLoading" class="empty-illustration">
      <img
        :src="require('@/v2/assets/empty/no_available_state.svg')"
        class="img-no-available"
      />
    </div>
  </div>

  <!-- Confirmation Dialog -->
  <v-dialog v-model="showConfirmDialog" max-width="500" persistent>
    <v-card class="pa-5 rounded-lg">
      <v-card-title class="text-h6 font-weight-bold dialog-title">
        <v-btn
          class="close-btn"
          icon
          size="small"
          variant="text"
          @click="cancelConfirmation"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <div class="font-weight-bold text-center mt-5 text-20">
        {{ confirmationTitle }}
      </div>
      <v-card-text class="confirmation-text">
        <p v-html="confirmationMessage"></p>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          class="cancel-btn rounded-lg"
          color="white"
          variant="flat"
          elevation="2"
          @click="cancelConfirmation"
        >
          Cancel
        </v-btn>
        <v-btn
          class="confirm-btn rounded-lg"
          variant="flat"
          elevation="3"
          @click="proceedWithToggle"
        >
          {{ getConfirmButtonLabel() }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { TInfoPage } from "@/v2/Type";
import { ref, onMounted, watch, computed, getCurrentInstance } from "vue";
import ListUserItem from "@/v2/components/admin/operasional/ListUserItem.vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";

const store = useStore();
const route = useRoute();
const instance: any = getCurrentInstance()?.root.refs;

const list = ref<any[]>([]);
const pagination = ref<TInfoPage>({
  totalData: 0,
  prevPageNo: 0,
  pageNo: 1,
  nextPageNo: 2,
  totalPage: 1,
  entriesPerPage: 10,
});
const isLoading = ref<boolean>(false);
const currentPage = ref<number>(1);
const enableAllMFA = ref<boolean>(false);
const isLoadingToggle = ref<boolean>(false);

// Dialog state
const showConfirmDialog = ref(false);
const confirmationTitle = ref("");
const confirmationMessage = ref("");
const previousToggleValue = ref(false);

const searchMode = computed(() => store.getters["globalStore/getStatusSearch"]);
const searchValue = computed(() => store.getters["globalStore/getSearch"]);
const filterValue = computed(() => store.getters["adminStore/getItemsFilter"]);
const refreshList = computed(() => store.getters["adminStore/getRefreshList"]);

function getList() {
  store.commit("documentStore/setOnLoadingButtonState", true);
  isLoading.value = true;

  let payload = {
    sortBy: searchMode.value
      ? 0
      : parseInt((route.query.userSort as string) ?? 0),
    orderBy: "",
    pageSize: pagination.value.entriesPerPage,
    pageNumber: pagination.value.pageNo ?? 1,
    searchUserName: searchValue.value,
  };

  store
    .dispatch("adminStore/getListUsername", payload)
    .then((res: any) => {
      enableAllMFA.value = res.responseData?.data?.isEnableMFA === 1 || false;
      list.value = res.responseData?.data.users;
      pagination.value.pageNo = res.responseData.data.infoPage?.pageNo ?? 1;
      pagination.value.totalData =
        res.responseData.data.infoPage?.totalData ?? 10;
      pagination.value.totalPage =
        res.responseData.data.infoPage?.totalPage ?? 10;
      const totalData = res.responseData.data.infoPage?.totalData;
      const totalDataPerPage =
        res.responseData.data.infoPage?.entriesPerPage || 0;
      store.commit("globalStore/setTotalData", totalData);
      store.commit("globalStore/setTotalDataPerPage", totalDataPerPage);
    })
    .finally(() => {
      isLoading.value = false;
    });
}

function changePage(curr: number) {
  pagination.value.pageNo = curr;
  getList();
}

function toggleSwitch() {
  // Store the previous value before showing dialog
  previousToggleValue.value = enableAllMFA.value;

  // Toggle the value to show what the new state would be
  enableAllMFA.value = !enableAllMFA.value;

  confirmationTitle.value = enableAllMFA.value
    ? "Enable MFA Feature"
    : "Disable MFA Feature";

  if (enableAllMFA.value) {
    confirmationMessage.value = `Are you sure you want to enable <b>Multi-Factor Authentication (MFA)</b> feature?\nThis will require selected user to verify their identity using MFA when logging in.`;
  } else {
    confirmationMessage.value = `Are you sure you want to disable <b>Multi-Factor Authentication (MFA)</b> feature?\nThis will remove the MFA requirement for selected user when logging in`;
  }

  showConfirmDialog.value = true;
}

// Cancel confirmation and revert toggle
const cancelConfirmation = () => {
  enableAllMFA.value = previousToggleValue.value;
  showConfirmDialog.value = false;
};

// Get dynamic confirm button label
const getConfirmButtonLabel = () => {
  return enableAllMFA.value ? "Yes, Enable" : "Yes, Disable";
};

// Proceed with the toggle change
const proceedWithToggle = async () => {
  showConfirmDialog.value = false;
  isLoadingToggle.value = true;

  try {
    await store
      .dispatch("adminStore/updateToggleMFA", {
        isEnableMFA: enableAllMFA.value === true ? 1 : 0,
      })
      .then((result) => {
        instance.toast.show({
          message:
            result.responseMessage ?? "Successfully " + confirmationTitle.value,
          color: "success",
          timeout: 3000,
        });
        showConfirmDialog.value = false;
      })
      .catch((error) => {
        instance.toast.show({
          message: error.message ?? "Failed " + confirmationTitle.value,
          color: "error",
          timeout: 3000,
        });
      })
      .finally(() => {
        isLoadingToggle.value = false;
        getList();
      });
  } catch (err) {
    enableAllMFA.value = previousToggleValue.value;
    instance.toast.show({
      message: "Failed " + confirmationTitle.value,
      color: "error",
      timeout: 3000,
    });
    isLoadingToggle.value = false;
  }
};

watch([route, refreshList], () => {
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

onMounted(() => {
  getList();
});
</script>

<style scoped>
:deep(.v-card--variant-elevated) {
  box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.12) !important;
}

.empty-illustration {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}

.toggle-section {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

:deep(.v-switch .v-selection-control__input) {
  color: #065391;
}

:deep(.v-switch .v-label) {
  font-weight: 600;
  font-size: 16px;
  color: #065695;
}

:deep(.v-switch .v-label) {
  color: black;
  font-size: 14px;
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

/* ── Skeleton user cards ─────────────────────────── */
.skeleton-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.skeleton-user-card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
  padding: 14px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  animation: fadeSlideUp 0.4s ease-out both;
}

.sk-block {
  border-radius: 6px;
  background: #e8e8e8;
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
}

.sk-block::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.7) 50%,
    transparent 100%
  );
  background-size: 200% 100%;
  animation: shimmerSweep 1.4s ease-in-out infinite;
}

/* mirrors md-3 name | md-3 satker | md-3 jabatan | md-1 MFA | md-2 Lock */
.sk-name {
  flex: 1;
  height: 13px;
  max-width: 22%;
}
.sk-satker {
  flex: 1;
  height: 13px;
  max-width: 22%;
}
.sk-jabatan {
  flex: 1;
  height: 13px;
  max-width: 22%;
}
.sk-checkbox {
  width: 60px;
  height: 24px;
  border-radius: 999px;
}

.sk-satker::after {
  animation-delay: 0.08s;
}
.sk-jabatan::after {
  animation-delay: 0.16s;
}
.sk-checkbox:nth-child(4)::after {
  animation-delay: 0.24s;
}
.sk-checkbox:nth-child(5)::after {
  animation-delay: 0.32s;
}

@keyframes shimmerSweep {
  from {
    background-position: -200% 0;
  }
  to {
    background-position: 200% 0;
  }
}

@keyframes fadeSlideUp {
  from {
    opacity: 0;
    translate: 0 16px;
  }
  to {
    opacity: 1;
    translate: 0 0;
  }
}

/* Custom Switch Styles */
.custom-switch-container {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-direction: row;
}

.switch-label {
  font-size: 14px;
  font-weight: 400;
  color: #000000;
}

.custom-switch {
  width: 48px;
  height: 24px;
  background-color: #e0e0e0;
  border-radius: 12px;
  position: relative;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.custom-switch.active {
  background-color: #065391;
}

.switch-thumb {
  width: 20px;
  height: 20px;
  background-color: white;
  border-radius: 50%;
  position: absolute;
  top: 2px;
  left: 2px;
  transition: transform 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.custom-switch.active .switch-thumb {
  transform: translateX(24px);
}

/* Confirmation Dialog Styles */
.dialog-title {
  text-align: center !important;
  justify-content: center !important;
  position: relative !important;
}

.close-btn {
  position: absolute !important;
  right: 8px !important;
  top: 50% !important;
  transform: translateY(-50%) !important;
  color: #666 !important;
}

.close-btn:hover {
  color: #333 !important;
  background-color: rgba(0, 0, 0, 0.04) !important;
}

.confirmation-text {
  font-family: Poppins !important;
  font-weight: 400 !important;
  font-style: normal !important;
  font-size: 16px !important;
  line-height: 140% !important;
  letter-spacing: 0% !important;
  background: linear-gradient(
    92.72deg,
    rgba(121, 121, 121, 0.9) 0%,
    rgba(187, 187, 187, 0.9) 152.21%
  ) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  background-clip: text !important;
  text-align: left !important;
  white-space: pre-line !important;
  margin-bottom: 10px;
}

.confirm-btn {
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%) !important;
  color: white !important;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2) !important;
  font-weight: 800;
}

.confirm-btn:hover {
  background: linear-gradient(180deg, #054a82 0%, #2070b0 100%) !important;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3) !important;
}

.cancel-btn {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15) !important;
  color: #065695 !important;
  font-weight: 800;
}

.cancel-btn:hover {
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2) !important;
  color: #054a82 !important;
}
</style>
