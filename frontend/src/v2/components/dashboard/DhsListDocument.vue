<template>
  <v-sheet class="my-3">
    <v-expansion-panels v-model="panel">
      <v-expansion-panel :value="item.idBPDocument">
        <v-expansion-panel-title>
          <v-tooltip activator="parent" location="top left">
            {{ item.bpDocumentName }}
          </v-tooltip>
          <v-row align="center" style="cursor: pointer !important">
            <v-col cols="5" style="padding: 0 !important">
              <p class="font-weight-bold ellipsis-1">
                {{ item.bpDocumentName }}
              </p>
            </v-col>
            <v-col
              cols="2"
              style="
                padding: 2px !important;
                display: flex;
                justify-content: start;
              "
            >
              <v-chip
                :style="chipStyles[item?.status?.toLocaleLowerCase()] as StyleValue"
              >
                {{ item.status }}
              </v-chip>
            </v-col>
            <v-col
              cols="5"
              style="
                padding: 2px !important;
                display: flex;
                justify-content: start;
              "
            >
              <span class="item-information font-italic"
                >Last modified by: {{ item.lastModifiedBy || " - " }}
                <span style="font-style: normal">|</span> Date:
                {{ item.date ? formatTimeEngToMonthInd(item.date) : " - " }}
                <span style="font-style: normal">|</span> Time:
                {{ item.date ? reformatTimes(item.date) : " - " }}
                WIB</span
              >
            </v-col>
          </v-row>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-row v-if="loadingBPOnGoing" class="mx-5 my-5">
            <v-col v-for="i in 3" :key="i" cols="12">
              <free-style-shimmer
                width="100%"
                height="40px"
                border-radius="10px"
                color="#d3d3d3"
              />
            </v-col>
          </v-row>

          <template v-else>
            <v-row class="mx-2">
              <v-col cols="6" class="mt-2">
                <v-row>
                  <v-col
                    v-show="isRisalahRDG || isDocument2D"
                    cols="12"
                    class="px-0"
                  >
                    <div class="text-grey-theme fw-600 text-13">Penyusun</div>
                    <div class="text-black-theme text-13">
                      <text-ellipsis
                        :text="isDocument2D ? penyusunAll : penyusun"
                      />
                    </div>
                  </v-col>
                  <v-col v-show="!isDocument2D" cols="12" class="px-0">
                    <div class="text-grey-theme fw-600 text-13">Pengaju</div>
                    <div class="text-black-theme text-13">
                      <text-ellipsis :text="pengaju" />
                    </div>
                  </v-col>
                  <v-col v-show="!isDocument2D" cols="12" class="px-0">
                    <div class="text-grey-theme fw-600 text-13">Penyetuju</div>
                    <div class="text-black-theme text-13">
                      <text-ellipsis :text="penyetuju" />
                    </div>
                  </v-col>
                </v-row>
              </v-col>
              <v-col cols="4" class="mt-2">
                <v-row>
                  <v-col v-show="!isDocument2D" cols="12" class="px-0">
                    <div class="text-grey-theme fw-600 text-13">Penyusun</div>
                    <div class="text-black-theme text-13">
                      <text-ellipsis :text="penyusunAll" />
                    </div>
                  </v-col>
                  <v-col cols="12" class="px-0">
                    <div class="text-grey-theme fw-600 text-13">
                      Dokumen Final
                    </div>
                    <div class="text-black-theme text-13">
                      <text-ellipsis :text="docFinalAll" />
                    </div>
                  </v-col>
                  <v-col v-show="isRisalahRDG" cols="12" class="px-0">
                    <div class="text-grey-theme fw-600 text-13">Tim Teknis</div>
                    <div class="text-black-theme text-13">
                      <text-ellipsis :text="timTeknisAll" />
                    </div>
                  </v-col>
                  <v-col cols="12" class="px-0">
                    <div class="text-grey-theme fw-600 text-13">Organizer</div>
                    <div class="text-black-theme text-13">
                      <text-ellipsis :text="organizerAll" />
                    </div>
                  </v-col>
                </v-row>
              </v-col>
              <v-col cols="2" class="mt-2 text-right">
                <v-btn
                  color="#1976d3"
                  density="comfortable"
                  width="auto"
                  height="auto"
                  variant="outlined"
                  class="btn-outline-rounded pa-1 pl-2 pr-2"
                  @click="goToContent()"
                >
                  Go To Content
                </v-btn>
              </v-col>
            </v-row>
            <div v-if="item.idDocumentType === 8">
              <dhs-list-sector
                v-for="(sector, index) in workspaceDetail?.sectorApprovals"
                :key="index"
                class="mt-5"
                :item="sector"
              ></dhs-list-sector>
            </div>
          </template>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-sheet>
</template>
<script setup lang="ts">
import TextEllipsis from "@/v2/components/admin/TextEllipsis.vue";
import { chipStyles } from "@/v2/helpers/color";
import {
  reformatTimes,
  formatTimeEngToMonthInd,
} from "@/v2/helpers/DateHelper";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { ref, watch, computed, StyleValue } from "vue";
import DhsListSector from "@v2/components/dashboard/DhsListSector.vue";

const props = defineProps({
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
});

const store = useStore();
const router = useRouter();
const panel = ref<number[]>([]);
const loadingBPOnGoing = ref<boolean>(false);
const workspaceDetail = ref();

watch(panel, (newValue) => {
  if (newValue) GetListWorkspaceDetail(newValue);
});

const penyusun = computed(() => {
  return workspaceDetail.value?.penyusun || "-";
});

const pengaju = computed(() => {
  return workspaceDetail.value?.pengaju || "-";
});

const penyetuju = computed(() => {
  return workspaceDetail.value?.penyetuju || "-";
});

const penyusunAll = computed(() => {
  return workspaceDetail.value?.penyusunAll || "-";
});

const docFinalAll = computed(() => {
  return workspaceDetail.value?.dokumenFinalAll || "-";
});

const timTeknisAll = computed(() => {
  return workspaceDetail.value?.timTeknisAll || "-";
});

const organizerAll = computed(() => {
  return workspaceDetail.value?.organizerAll || "-";
});

const isDocument2D = computed(() => {
  return props.item.idDocumentType === 8;
});

const isRisalahRDG = computed(() => {
  return props.item.idDocumentType === 9;
});

function GetListWorkspaceDetail(docID: number | number[]) {
  loadingBPOnGoing.value = true;
  store
    .dispatch("documentsStore/GetListWorkspaceDetail", {
      idBPDocument: docID,
      idDocumentType: props.item.idDocumentType,
    })
    .then((res: any) => {
      workspaceDetail.value = res.responseData;
    })
    .finally(() => {
      loadingBPOnGoing.value = false;
    });
}

function goToContent() {
  let routeName = "";
  let typeRDG = "";
  if (workspaceDetail.value.eventSubTypeList === "RDGB Cakupan Bulanan") {
    routeName = "v2.rdg-collaboration";
    typeRDG = "rdgb";
  } else if (workspaceDetail.value.eventSubTypeList === "RDGTK") {
    routeName = "v2.rdg-collaboration";
    typeRDG = "rdgtk";
  } else {
    routeName = "om.rdg-collaboration";
    typeRDG = "rdgm";
  }
  router.push({
    name: routeName,
    params: {
      typeRDG: typeRDG,
      idEvent: workspaceDetail.value.idEvent,
      idDoc: workspaceDetail.value.idBPDocument,
    },
  });
}
</script>
<style scoped>
.item-information {
  color: #797979e5;
  font-size: 13px;
  line-height: 19.5px;
}
.text-grey-theme {
  color: #a6abc7;
}
.text-black-theme {
  color: #4b4b4b;
}
.btn-outline-rounded {
  border-radius: 10px;
  letter-spacing: -0.5px;
}
</style>
