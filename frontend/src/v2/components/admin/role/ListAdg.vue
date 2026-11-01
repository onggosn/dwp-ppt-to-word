<template>
  <!-- Custom skeleton matching expansion panel layout -->
  <div v-if="loadingList" class="skeleton-list mt-5">
    <div
      v-for="i in 5"
      :key="i"
      class="skeleton-panel"
      :style="{ animationDelay: `${(i - 1) * 0.07}s` }"
    >
      <div class="skeleton-panel-body">
        <div class="sk-block sk-title"></div>
        <div class="sk-block sk-meta"></div>
        <div class="sk-block sk-chevron"></div>
      </div>
    </div>
  </div>
  <template v-else>
    <div v-if="hasList" class="my-8">
      <div
        v-for="(item, idx) in list"
        :key="item.idFormasi"
        class="adg-panel-wrapper"
        :style="{ animationDelay: `${idx * 0.07}s` }"
      >
        <AccordionPanel
          :items="item"
          @on-droped="(value) => getDetailADG(value)"
        >
          <template #title>
            <v-row style="cursor: pointer !important" class="pl-4">
              <v-col cols="8" style="padding: 0 !important">
                <p class="font-weight-bold ellipsis-1">
                  {{ item.name }}
                </p>
              </v-col>
              <v-col
                cols="4"
                style="
                  padding: 2px !important;
                  display: flex;
                  justify-content: start;
                "
              >
                <span class="item-information font-italic"
                  >Last modified by: {{ item.lastUpdatedBy || " - " }}
                  <span style="font-style: normal">|</span> Date:
                  {{
                    reformatDateEngWithMonthLong(item.lastUpdatedDate) || " - "
                  }}
                  <span style="font-style: normal">|</span> Time:
                  {{ reformatTimes(item.lastUpdatedDate) || " - " }} WIB</span
                >
              </v-col>
            </v-row>
          </template>
          <template #body>
            <div
              v-if="loadingDetail && processedADGId === item.idFormasi"
              class="skeleton-inner"
            >
              <div
                v-for="i in 3"
                :key="i"
                class="skeleton-inner-row"
                :style="{ animationDelay: `${(i - 1) * 0.08}s` }"
              >
                <div class="sk-block sk-inner-name"></div>
                <div class="sk-block sk-inner-meta"></div>
              </div>
            </div>
            <div v-else>
              <div class="d-flex justify-end pr-2">
                <btn-delete
                  :title="'Delete Formasi ADG'"
                  :is-icon-button="false"
                  :subtitle="'Are you sure you want to delete this ADG Formation? '"
                  :description="''"
                  :append-icon="true"
                  :btn-color="'#d6212a'"
                  :btn-icon-color="'#d6212a'"
                  :btn-title="'Delete Formasi'"
                  :disabled="list.length > 1 ? false : true"
                  btn-class="font-weight-bold"
                  @update="deleteADG(item.idFormasi)"
                >
                </btn-delete>
                <div class="px-2 py-3 ml-2">
                  <EditAdgDialog
                    :form-data="item?.detailADG?.responseData"
                    :id-formasi="item.idFormasi"
                    @refresh-data="handleRefreshData"
                  />
                </div>
              </div>
              <div class="my-5 mx-2 elevation-2 rounded-lg pa-8">
                <v-row>
                  <v-col cols="6">
                    <div class="image-container">
                      <label class="label">Banner Event Detail</label>
                      <div class="image-card">
                        <img :src="require('@/v2/assets/icon/image.svg')" />
                        <label>{{
                          item?.detailADG?.responseData
                            ?.bannerEventDetailExtention
                        }}</label>
                        <span class="dot ml-2 mr-2">●</span>
                        <span
                          style="cursor: pointer"
                          class="preview"
                          @click="
                            handlePreviewEventDetail(
                              item?.detailADG?.responseData?.bannerEventDetail
                            )
                          "
                        >
                          Preview
                        </span>
                      </div>
                    </div>

                    <div class="image-container">
                      <label class="label">Homepage Event Banner*</label>
                      <div class="image-card">
                        <img :src="require('@/v2/assets/icon/image.svg')" />
                        <label>{{
                          item?.detailADG?.responseData
                            ?.homepageEventBannerExtention
                        }}</label>
                        <span class="dot ml-2 mr-2">●</span>
                        <span
                          style="cursor: pointer"
                          class="preview"
                          @click="
                            handlePreviewHomepage(
                              item?.detailADG?.responseData?.homepageEventBanner
                            )
                          "
                        >
                          Preview
                        </span>
                      </div>
                    </div>
                  </v-col>
                  <v-col cols="2" class="align-self-end">
                    <div class="status-container">
                      <label class="label">Effective Date </label>
                      <label>{{
                        formatTimeEngToIndNoDays(
                          item?.detailADG?.responseData?.effectiveDate
                        )
                      }}</label>
                    </div>
                    <div class="status-container">
                      <label class="label"> Status </label>
                      <label>
                        <v-icon
                          :color="item.isActive ? '#4CAF50' : '#9E9E9E'"
                          size="8"
                          class="mr-2"
                        >
                          mdi-circle
                        </v-icon>
                        {{ item?.detailADG?.responseData?.status }}
                      </label>
                    </div>
                  </v-col>
                </v-row>
                <v-row
                  v-if="item?.detailADG?.responseData?.detailADG"
                  class="mt-8"
                >
                  <v-col
                    cols="12"
                    v-for="(element, idE) in item.detailADG.responseData
                      .detailADG"
                    :key="idE"
                  >
                    <v-card
                      class="list-user"
                      elevation="0"
                      style="
                        border-radius: 10px;
                        padding: 20px 20px;
                        background-image: url('data:image/svg+xml,%3csvg width=\'100%25\' height=\'100%25\' xmlns=\'http://www.w3.org/2000/svg\'%3e%3crect width=\'100%25\' height=\'100%25\' fill=\'none\' rx=\'10\' ry=\'10\' stroke=\'%23404040\' stroke-width=\'1\' stroke-dasharray=\'10%2c 10\' stroke-dashoffset=\'0\' stroke-linecap=\'square\'/%3e%3c/svg%3e');
                      "
                    >
                      <v-row>
                        <v-col cols="6">
                          <label>Nama</label>
                          <p>{{ element.namaAdg }}</p>
                        </v-col>
                        <v-col cols="6">
                          <label>Email</label>
                          <p>{{ element.email }}</p>
                        </v-col>
                        <v-col cols="6">
                          <label>Jabatan</label>
                          <p>{{ element.jabatan }}</p>
                        </v-col>
                        <v-col cols="6">
                          <label>ADG Bidang</label>
                          <p>{{ element.adgBidang }}</p>
                        </v-col>
                        <v-col cols="6">
                          <label>Pangkat</label>
                          <p>{{ element.pangkat }}</p>
                        </v-col>
                      </v-row>
                    </v-card>
                  </v-col>
                </v-row>
              </div>
            </div>
          </template>
        </AccordionPanel>
      </div>

      <div class="text-center mt-7">
        <v-pagination
          v-if="list?.length"
          rounded="1"
          elevation="2"
          size="small"
          v-model="currentPage"
          :length="pagination.totalPage"
          :total-visible="1"
          @update:model-value="changePage"
        />
      </div>
    </div>
    <div v-else class="empty-illustration">
      <img
        :src="require('@/v2/assets/empty/no_available_state.svg')"
        class="img-no-available"
      />
    </div>
    <preview-dialog
      v-model="showPreviewEventDetail"
      :img-src="fileImg"
      @close="showPreviewEventDetail = false"
    />
    <previewHomepageDialog
      v-model="showPreviewHomepageDetail"
      :img-src="fileImg"
      @close="showPreviewHomepageDetail = false"
    />
  </template>
</template>

<script setup lang="ts">
import {
  computed,
  getCurrentInstance,
  nextTick,
  onMounted,
  ref,
  toRaw,
} from "vue";
import { useStore } from "vuex";
import previewDialog from "./previewDialog.vue";
import {
  type ListADG,
  type ParamsListADG,
  type PaginationADG,
} from "@/v2/Type";
import AccordionPanel from "@/v2/components/accordion/AccordionPanel.vue";
import previewHomepageDialog from "./previewHomepageDialog.vue";
import EditAdgDialog from "./EditAdgDialog.vue";
import {
  reformatTimes,
  reformatDateEngWithMonthLong,
  formatTimeEngToIndNoDays,
} from "@/v2/helpers/DateHelper";
import BtnDelete from "@/v2/components/utils/dialog/DeleteEventDialog.vue";
const showPreviewEventDetail = ref<boolean>(false);
const showPreviewHomepageDetail = ref<boolean>(false);
const fileImg = ref<string | undefined>("");

const store = useStore();

const loadingDetail = ref<boolean>(false);
const processedADGId = ref<string | null | undefined>("");

const hasList = computed(() => list.value.length > 0);

const currentPage = computed<number>({
  get() {
    return store.state.adminStore.currentPageADG;
  },
  set(newValue) {
    store.commit("adminStore/setADGPage", newValue);
  },
});

const list = computed<ListADG[]>(() => store.getters["adminStore/getListADG"]);

const pagination = computed<PaginationADG>(
  () => store.getters["adminStore/getPaginationADG"]
);

const params = computed<ParamsListADG>(
  () => store.getters["adminStore/getParamsListADG"]
);

const loadingList = computed<boolean>(
  () => store.getters["adminStore/getLoadingADG"]
);

const vm = getCurrentInstance() as any;

const getDetailADG = async (id?: string) => {
  if (!id) return;
  loadingDetail.value = true;
  processedADGId.value = id;
  try {
    await store.dispatch("adminStore/getListADGDetail", id);
  } finally {
    loadingDetail.value = false;
  }
};

const showToast = async (opts: {
  message: string;
  color: string;
  timeout?: number;
}) => {
  await nextTick();
  vm?.root?.refs?.toast?.show?.({ timeout: 3000, ...opts });
};

function handleRefreshData(temp) {
  getDetailADG(temp);
}

function handlePreviewEventDetail(item) {
  fileImg.value = item;
  showPreviewEventDetail.value = true;
}
function handlePreviewHomepage(item) {
  fileImg.value = item;
  showPreviewHomepageDetail.value = true;
}
function changePage(curr: number) {
  pagination.value.pageNo = curr;
  store.dispatch("adminStore/getListADG", params.value);
}
async function deleteADG(id?: string) {
  try {
    store.commit("adminStore/setLoadingADG", true);
    await store.dispatch("adminStore/deleteADG", id);
    await store.dispatch("adminStore/getListADG", params.value);
    await showToast({ message: "Successfully Deleted", color: "success" });
  } catch (e) {
    await showToast({ message: "Sorry, failed Delete", color: "error" });
  } finally {
    store.commit("adminStore/setLoadingADG", false);
  }
}

onMounted(() => {
  store.dispatch("adminStore/getListADG", params.value);
});
</script>

<style scoped>
.section-title {
  font-weight: 700;
  margin-bottom: 12px;
  font-size: 18px;
  color: #065695;
}
.item-information {
  color: #797979e5;
  font-size: 13px;
  line-height: 19.5px;
}
.dot {
  color: #767676;
}
:deep(
    .v-expansion-panel-title--active > .v-expansion-panel-title__overlay,
    .v-expansion-panel-title[aria-haspopup="menu"][aria-expanded="true"]
      > .v-expansion-panel-title__overlay
  ) {
  opacity: 0 !important;
}
:deep(.v-expansion-panel) {
  border-radius: 16px;
}
:deep(.v-expansion-panel__shadow) {
  box-shadow: 0px 2px 4px 0px #0000001f !important;
}
:deep(.v-expansion-panel-title) {
  min-height: 60px;
}

.image-container {
  margin-bottom: 8px;
}

.image-card {
  background-color: #f2f4f7;
  padding: 12px 14px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: start;
  height: 48px;
  width: 60%;
}

.image-card label,
.image-card img {
  margin-left: 4px;
  margin-right: 4px;
}
.image-card .preview {
  color: #005fad;
  cursor: pointer;
}

.status-container,
.image-container {
  display: flex;
  flex-direction: column;
  margin-top: 20px;
  justify-content: end;
}

.empty-illustration {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}

.status-container .label,
.image-container .label,
.list-user label {
  color: #a6abc7;
}

/* ── Skeleton panels (outer list) ────────────────── */
.skeleton-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skeleton-panel {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.12);
  padding: 0 16px;
  height: 64px;
  display: flex;
  align-items: center;
  animation: fadeSlideUp 0.4s ease-out both;
}

.skeleton-panel-body {
  display: flex;
  align-items: center;
  width: 100%;
  gap: 12px;
}

/* col-8 name */
.sk-title {
  flex: 1;
  height: 13px;
  border-radius: 6px;
  background: #e8e8e8;
  max-width: 50%;
  position: relative;
  overflow: hidden;
}

/* col-4 metadata */
.sk-meta {
  flex: 1;
  height: 12px;
  border-radius: 6px;
  background: #e8e8e8;
  position: relative;
  overflow: hidden;
}

.sk-chevron {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #e8e8e8;
  position: relative;
  overflow: hidden;
  margin-left: auto;
  flex-shrink: 0;
}

/* Shimmer sweep */
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
.sk-meta::after {
  animation-delay: 0.12s;
}
.sk-chevron::after {
  animation-delay: 0.24s;
}

/* ── Skeleton inner rows (detail body) ──────────── */
.skeleton-inner {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 16px 20px;
}

.skeleton-inner-row {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #fafafa;
  border-radius: 10px;
  padding: 12px 16px;
  animation: fadeSlideUp 0.35s ease-out both;
}

.sk-inner-name {
  flex: 1;
  height: 12px;
  border-radius: 6px;
}
.sk-inner-meta {
  flex: 1;
  height: 12px;
  border-radius: 6px;
  max-width: 55%;
}

.sk-inner-meta::after {
  animation-delay: 0.12s;
}

/* AccordionPanel entrance */
.adg-panel-wrapper {
  animation: fadeSlideUp 0.45s ease-out both;
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
</style>
