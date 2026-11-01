<template>
  <div>
    <v-row no-gutters>
      <p class="text-left font-weight-bold text-h6 text-darkBlue">Material</p>
      <v-card v-if="linkMaterial.idEvent" class="link-material-card">
        <v-btn
          class="link-btn-material"
          variant="text"
          style="width: fit-content; margin-bottom: 12px"
          @click="
            goToCollaboration(
              linkMaterial.idParent,
              linkMaterial.idBPDocument,
              linkMaterial.rdgType
            )
          "
        >
          <span class="text-material text-gradient-blue">{{
            linkMaterial.materialName
          }}</span>
          <template #append>
            <img :src="require('@/v2/assets/icon/link.svg')" />
          </template>
        </v-btn>
      </v-card>
      <img
        v-else
        :src="require('@/v2/assets/empty/no_available_state.svg')"
        class="img-no-available"
      />
    </v-row>
    <v-row no-gutters justify="space-between">
      <p class="font-weight-bold text-h6 text-darkBlue">
        Presentation Material
      </p>
      <v-spacer />
      <DownloadAllDocument :id="idEvent" :selected="selected" />
      <AddMaterialPersentation
        @onSuccess="getMeetingMaterial"
        title="+ Add Material"
        v-if="isCreateMaterial"
      />
    </v-row>
    <v-row no-gutters v-if="paginationPage?.totalData === 0">
      <img
        :src="require('@/v2/assets/empty/no_available_state.svg')"
        class="img-no-available"
      />
    </v-row>
    <v-row no-gutters v-else class="mt-10">
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
              <th class="text-left txt-header" style="font-weight: 800">
                List Document
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
                style="width: 15%; font-weight: 800"
              >
                Action
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(item, indx) in itemMaterial"
              :key="indx"
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
              <td class="text-center txt-data">{{ getNumber(indx + 1) }}</td>
              <td class="text-left txt-data">
                {{ item.materialName || "-" }}
              </td>
              <td class="text-left txt-data">
                {{ item.materialListDoc || "-" }}
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
                {{ (item.materialSize / (1024 * 1024)).toFixed(2) }} MB
              </td>
              <td class="text-center txt-data">
                {{ convertTimestamp(item.timeStamp).date }}
                {{ convertTimestamp(item.timeStamp).time }}
              </td>
              <td class="text-center txt-data">
                <BtnAccess
                  v-if="item.materialAction.isAccess"
                  :idEventPresentationMaterial="item.id"
                  :idListMaterial="item.materialListDocId"
                  @onSuccess="getMeetingMaterial($event)"
                ></BtnAccess>
                <v-btn
                  v-if="item.materialAction.isRead"
                  variant="text"
                  class="pa-1"
                  min-width="0"
                  :to="{
                    name: 'v2.meeting-detail-material-preview',
                    params: { idEvent: idEvent, idMaterial: item.id },
                    query: { size: item.materialSize },
                  }"
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
                    mdi-file-document-outline
                  </v-icon>
                  <v-tooltip activator="parent" location="top">
                    Preview
                  </v-tooltip>
                </v-btn>
                <download-document
                  v-if="item.materialAction.isDownload"
                  :id="item.id"
                  :filename="item.materialName"
                  :type="item.materialExt"
                  :initialDocument="item.initialDocument"
                  :initialDocumentExt="item.initialDocumentExt"
                />
                <BtnDeleteMaterial
                  v-if="item.materialAction.isDelete"
                  @onSuccess="getMeetingMaterial($event)"
                  :id="item.id"
                />
                <BtnMetadata
                  v-if="item.materialAction.isMetadata"
                  :id="item.id"
                />
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-col>
    </v-row>
    <div v-if="!isLoading && itemMaterial.length" class="text-center mt-5">
      <v-pagination
        v-if="canChangePage"
        v-model="currentPage"
        :length="paginationPage?.totalPage"
        @update:modelValue="changePage"
      ></v-pagination>
    </div>

    <PreviewDocument :key="route.fullPath" />
  </div>
</template>

<script setup lang="ts">
import AddMaterialPersentation from "@v2/components/meeting/meetingMaterial/AddMaterialPersentation.vue";
import BtnDeleteMaterial from "@v2/components/meeting/meetingMaterial/BtnDeleteMaterial.vue";
import DownloadDocument from "@v2/components/meeting/meetingMaterial/DownloadDocument.vue";
import DownloadAllDocument from "@v2/components/meeting/meetingMaterial/DownloadAllDocument.vue";
import { convertTimestamp } from "@v2/helpers/datetime";
import BtnAccess from "@v2/components/meeting/meetingMaterial/EditAccessMaterial.vue";
import BtnMetadata from "@v2/components/meeting/meetingMaterial/BtnMetadata.vue";
import PreviewDocument from "@v2/components/meeting/PreviewDocument.vue";

import { ref, onMounted, toRefs, computed, watchEffect } from "vue";
import { TMaterialList, TInfoPage, TLinkMaterialResponse } from "@/v2/Type";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const store = useStore();
const idEvent = route.params.idEvent as string;
const { itemMaterial, paginationPage, currentPage, isCreateMaterial } = toRefs({
  itemMaterial: ref<TMaterialList[]>([]),
  paginationPage: ref<TInfoPage | null>(null),
  currentPage: ref<number>(1),
  isCreateMaterial: ref<boolean>(false),
});

const isLoading = ref<boolean>(false);
const linkMaterial = ref<TLinkMaterialResponse>({
  materialName: "",
  idEvent: "",
  idBPDocument: "",
  idParent: null,
  idMEventSubTypeList: 1,
  rdgType: "",
});

const canSelectDownloadAll = computed((): boolean => {
  const result = itemMaterial.value.some(
    (item) => item.materialAction.isDownload
  );
  return result;
});

const canChangePage = computed((): boolean => {
  if (paginationPage.value?.totalData && paginationPage.value?.totalData >= 5)
    return true;

  return false;
});

const getMeetingMaterial = (fromDelete?: boolean) => {
  if (fromDelete && itemMaterial.value.length === 1) {
    currentPage.value = 1;
  }

  isLoading.value = true;
  const request = {
    idEvent: idEvent,
    entriesPerPage: 5,
    pageNo: currentPage.value,
  };
  return store
    .dispatch("meetingStore/getMaterialByMeetingId", request)
    .then(({ responseData }) => {
      itemMaterial.value = responseData.data;
      isCreateMaterial.value = responseData.isCreateMaterial;
      paginationPage.value = {
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

function getLinkBukuDigitalMeeting() {
  const request = { id: idEvent };

  return store.dispatch("eventStore/getLinkMaterial", request).then((res) => {
    linkMaterial.value = res;
  });
}
function getNumber(index: number) {
  let pageNo = currentPage.value;
  let entriesPerPage = 5;
  let number = index + (pageNo - 1) * entriesPerPage;

  return number;
}

const changePage = (newPage: number) => {
  currentPage.value = newPage;
  selected.value = [];
  getMeetingMaterial();
};

function goToCollaboration(idEvent, idDoc, typeRDG) {
  let routeName = "";
  if (typeRDG === "RDGM") {
    routeName = "om.rdg-collaboration";
  } else {
    routeName = "v2.rdg-collaboration";
  }
  router.push({
    name: routeName,
    params: {
      typeRDG: typeRDG,
      idEvent: idEvent,
      idDoc: idDoc,
    },
  });
}

const selectAll = ref<boolean>(false);
const selected = ref<string[]>([]);
function selectAllDownload(value: boolean) {
  if (value)
    selected.value = itemMaterial.value
      .filter((item) => {
        return item.materialAction?.isDownload === true;
      })
      .map((item) => item.id);
  else selected.value = [];
}

watchEffect(() => {
  const maxLength = itemMaterial.value.filter((item) => {
    return item.materialAction?.isDownload === true;
  }).length;

  if (selected.value?.length === maxLength) selectAll.value = true;
  else selectAll.value = false;
});

function load() {
  getMeetingMaterial();
  getLinkBukuDigitalMeeting();
}

onMounted(() => {
  load();
});
</script>

<style scoped>
tr:hover td {
  background: #e0efff;
}

.active-row {
  background: #e0efff;
}

.link-material-card {
  margin-top: 18px;
  margin-bottom: 36px;
  width: 100%;
  padding: 12px 24px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
}
.text-material {
  font-size: 18px;
  text-align: left;
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
.text-darkBlue {
  color: var(--Black-NEW-VERSION, #4b4b4b);
  font-family: Poppins;
  font-size: 24px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
}
.blue-background {
  border-radius: 12px 12px 0px 0px;
  background: #f7fbfe;
}
.btn-detail-view.v-btn--size-default {
  min-width: initial;
  padding: 5px;
}
.img-no-available {
  margin-top: 5vh;
  width: 100%;
  height: 20vh;
  margin-bottom: 5vh;
}
:deep(
    v-table--density-default > .v-table__wrapper > table > tbody > tr > th,
    .v-table--density-default > .v-table__wrapper > table > thead > tr > th,
    .v-table--density-default > .v-table__wrapper > table > tfoot > tr > th
  ) {
  border-top: thin solid #e0e0e0 !important;
}
.txt-data {
  color: var(--Black, #4b4b4b);
  font-family: Poppins;
  font-size: 17px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
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
  font-weight: 800;
  line-height: 30px;
  color: #3a416f;
  margin-left: 17px;
}
.v-btn.link-btn-material {
  text-decoration-line: underline !important;
  text-decoration-color: #065695;
  text-underline-offset: 4px;
}
</style>
