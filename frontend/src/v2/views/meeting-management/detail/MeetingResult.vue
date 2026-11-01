<template>
  <div>
    <v-row no-gutters justify="space-between">
      <p class="font-weight-bold text-h6 text-darkBlue">Hasil Pembahasan</p>
      <v-spacer />
      <DownloadAllDocument :id="idEvent" :selected="selected" type="result" />
      <AddHasilPembahasan
        v-if="canCreateResult"
        title="+ Add Document"
        @onSuccess="getMeetingResult()"
      />
    </v-row>

    <v-row no-gutters v-if="!items.length && !isLoading">
      <img
        :src="require('@/v2/assets/empty/no_available_state.svg')"
        class="img-no-available"
      />
    </v-row>

    <v-row v-else no-gutters class="mt-10">
      <v-col cols="12">
        <paragraph-shimmer
          v-if="isLoading"
          :is-loading="true"
          :lines="4"
          :random-size="true"
        />
        <v-table
          v-else
          style="
            width: 100%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 12px 12px 0px 0px;
          "
        >
          <thead class="blue-background">
            <tr>
              <th class="text-center" style="width: 15px; font-weight: 800">
                <v-checkbox
                  v-if="canSelectDownloadAll"
                  v-model="selectAll"
                  color="success"
                  @update:model-value="selectAllDownload($event)"
                />
              </th>
              <th
                class="text-center txt-header"
                style="width: 150px; font-weight: 800"
              >
                No
              </th>
              <th class="text-left txt-header" style="font-weight: 800">
                Name
              </th>
              <th class="text-center txt-header" style="font-weight: 800">
                Type
              </th>
              <th
                class="text-center txt-header"
                style="width: 15%; font-weight: 800"
              >
                Size
              </th>
              <th
                class="text-center txt-header"
                style="width: 15%; font-weight: 800"
              >
                Upload Date
              </th>
              <th
                class="text-center txt-header"
                style="width: 20%; font-weight: 800"
              >
                Action
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(item, idx) in items"
              :key="item.id"
              style="font-size: 13px"
              :class="{ 'active-row': selected.includes(item.id) }"
            >
              <td class="text-center" style="font-weight: 800px">
                <v-checkbox
                  v-if="item.materialAction.isDownload"
                  v-model="selected"
                  :value="item.id"
                  hide-details
                  color="success"
                />
              </td>
              <td class="text-center txt-data">{{ getNumber(idx + 1) }}</td>
              <td class="text-left txt-data">
                {{ item.materialName || "-" }}
              </td>
              <td style="text-align: center">
                <v-img
                  v-if="item.materialExt === '.pdf'"
                  :src="require('@/v2/assets/icon/docImage/iconPdf.svg')"
                  alt="Icon"
                  width="40"
                  height="40"
                  style="display: inline-block; vertical-align: middle"
                ></v-img>
                <v-img
                  v-else-if="
                    item.materialExt === '.doc' || item.materialExt === '.docx'
                  "
                  :src="require('@/v2/assets/icon/doc.png')"
                  alt="Icon"
                  width="40"
                  height="40"
                  style="display: inline-block; vertical-align: middle"
                ></v-img>
                <v-img
                  v-else-if="
                    item.materialExt === '.ppt' || item.materialExt === '.pptx'
                  "
                  :src="require('@/v2/assets/icon/ppt.png')"
                  alt="Icon"
                  width="40"
                  height="40"
                  style="display: inline-block; vertical-align: middle"
                ></v-img>
              </td>
              <td class="text-center txt-data">
                {{ (item.materialSize / (1024 * 1024)).toFixed(2) }}
                MB
              </td>
              <td class="text-center txt-data">
                {{ convertTimestamp(item.timeStamp).date }}
                {{ convertTimestamp(item.timeStamp).time }}
              </td>
              <td class="text-center txt-data">
                <BtnAccess
                  v-if="item.materialAction.isAccess"
                  :idEventHasilPembahasan="item.id"
                  @onSuccess="getMeetingResult()"
                ></BtnAccess>
                <v-btn
                  v-if="item.materialAction.isRead"
                  variant="text"
                  class="pa-1"
                  min-width="0"
                  @click="openPreview(item)"
                >
                  <v-icon
                    class="table-content-center"
                    color="#267DC2"
                    small
                    style="
                      border: 1px solid;
                      border-radius: 4px;
                      padding: 13px;
                      cursor: pointer;
                    "
                  >
                    mdi-file-document-outline</v-icon
                  >
                  <v-tooltip activator="parent" location="top"
                    >Preview</v-tooltip
                  >
                </v-btn>
                <download-document
                  v-if="item.materialAction.isDownload"
                  :id="item.id"
                  :filename="item.materialName"
                />
                <BtnDeleteResult
                  v-if="item.materialAction.isDelete"
                  @onSuccess="getMeetingResult()"
                  :id="item.id"
                />
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-col>
    </v-row>

    <div class="text-center mt-5">
      <v-pagination
        v-if="canChangePage"
        v-model="currentPage"
        :length="pagination?.totalPage"
        @update:modelValue="changePage"
      ></v-pagination>
    </div>
  </div>
  <v-dialog
    v-model="openModal"
    transition="dialog-bottom-transition"
    fullscreen
    v-if="documentItem"
  >
    <v-card>
      <v-toolbar class="pa-4 bg-white" style="border-bottom: solid 2px #e4e4e4">
        <div class="d-block">
          <v-btn
            variant="outlined"
            size="large"
            icon="mdi-arrow-left"
            class="ml-5 ml-md-0"
            color="#045695"
            style="border: 0.01px solid #d3d3d3; color: white !important"
            elevation="2"
            @click="openModal = false"
            ><v-icon icon="mdi-arrow-left" color="#045695"> </v-icon>
          </v-btn>
          <span class="view-title ml-2">{{ documentItem.materialName }}</span>
        </div>
      </v-toolbar>
      <view-document
        :document="documentItem"
        :size="documentItem.materialSize"
        type="result"
      />
    </v-card>
  </v-dialog>
</template>
<script setup lang="ts">
import { ref, onMounted, computed, watchEffect } from "vue";
import { convertTimestamp } from "@v2/helpers/datetime";
import { TMaterialList, TInfoPage } from "@/v2/Type";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
// import ViewDocument from "@v2/components/meeting/meetingResult/ViewDocument.vue";
import ViewDocument from "@v2/components/meeting/meetingMaterial/ViewDocument.vue";
import DownloadDocument from "@v2/components/meeting/meetingResult/DownloadDocResult.vue";
import DownloadAllDocument from "@v2/components/meeting/meetingMaterial/DownloadAllDocument.vue";
import BtnDeleteResult from "@v2/components/meeting/meetingResult/BtnDeleteResult.vue";
import AddHasilPembahasan from "@v2/components/meeting/meetingMaterial/AddHasilPembahasan.vue";
import BtnAccess from "@v2/components/meeting/meetingResult/EditAccessResult.vue";

const route = useRoute();
const store = useStore();
const idEvent = route.params.idEvent as string;
defineEmits<{
  refresh: [];
}>();

const isLoading = ref<boolean>(false);
const selectAll = ref<boolean>(false);
const selected = ref<string[]>([]);
const items = ref<TMaterialList[]>([]);
const pagination = ref<TInfoPage | null>(null);
const currentPage = ref<number>(1);
const openModal = ref<boolean>(false);
const canCreateResult = ref<boolean>(false);
const documentItem = ref();

const canSelectDownloadAll = computed((): boolean => {
  const result = items.value.some((item) => item.materialAction.isDownload);
  return result;
});

const canChangePage = computed((): boolean => {
  if (pagination.value?.totalData && pagination.value?.totalData >= 5)
    return true;

  return false;
});

const getMeetingResult = () => {
  isLoading.value = true;
  const request = {
    idEvent: idEvent,
    entriesPerPage: 5,
    pageNo: currentPage.value,
  };
  store
    .dispatch("meetingStore/getMeetingResult", request)
    .then(({ responseData }) => {
      items.value = responseData.data;
      canCreateResult.value = responseData.isCreateMaterial;
      pagination.value = {
        pageNo: currentPage.value,
        entriesPerPage: responseData.infoPage.entriesPerPage,
        totalData: responseData.infoPage.totalData,
        totalPage: responseData.infoPage.totalPage,
        nextPageNo: responseData.infoPage.nextPageNo,
        prevPageNo: responseData.infoPage.prevPageNo,
      };
    })

    .finally(() => {
      isLoading.value = false;
    });
};

function selectAllDownload(value: boolean) {
  if (value)
    selected.value = items.value
      .filter((item: TMaterialList) => {
        return item.materialAction?.isDownload === true;
      })
      .map((item: TMaterialList) => item.id);
  else selected.value = [];
}

function openPreview(data: TMaterialList) {
  openModal.value = true;
  documentItem.value = data;
}

function getNumber(index: number) {
  let pageNo = currentPage.value;
  let entriesPerPage = 5;
  let number = index + (pageNo - 1) * entriesPerPage;

  return number;
}

watchEffect(() => {
  const maxLength = items.value.filter((item: TMaterialList) => {
    return item.materialAction?.isDownload === true;
  }).length;

  if (selected.value?.length === maxLength) selectAll.value = true;
  else selectAll.value = false;
});

onMounted(() => {
  getMeetingResult();
});

const changePage = (newPage: number) => {
  currentPage.value = newPage;
  selected.value = [];
  getMeetingResult();
};
</script>
<style scoped>
tr:hover td {
  background: #e0efff;
}

.active-row {
  background: #e0efff;
}
.blue-background {
  border-radius: 12px 12px 0px 0px;
  background: #f7fbfe;
}

.btn-create {
  color: #065695;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
}

.txt-header {
  text-align: center;
  font-family: Poppins;
  font-size: 17px;
  font-style: normal;
  font-weight: 800;
  line-height: normal;
  background: var(
    --Gradient-CTA,
    linear-gradient(92deg, #065695 -46.47%, #267dc2 157.9%)
  );
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.txt-data {
  color: var(--Black, #4b4b4b);
  font-family: Poppins;
  font-size: 17px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
}

.img-no-available {
  margin-top: 5vh;
  width: 100%;
  height: 20vh;
  margin-bottom: 5vh;
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
.view-title {
  font-family: Poppins;
  font-size: 20px;
  font-weight: 700;
  line-height: 30px;
  color: #3a416f;
  margin-left: 17px;
}
</style>
