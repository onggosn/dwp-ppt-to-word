<template>
  <v-sheet class="my-3">
    <v-expansion-panels v-model="panel">
      <v-expansion-panel :value="item.docID">
        <v-expansion-panel-title>
          <v-row align="center" style="cursor: pointer !important">
            <v-col cols="6" style="padding: 0 !important">
              <p class="font-weight-bold ellipsis-1">
                {{ item.docName }}
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
              <v-chip :style="matchChipStyle(documentStatus) as StyleValue">
                {{ documentStatus }}
              </v-chip>
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
                >Last modified by: {{ modifiedData?.modifiedBy || " - " }}
                <span style="font-style: normal">|</span> Date:
                {{ modifiedData?.date || " - " }}
                <span style="font-style: normal">|</span> Time:
                {{ modifiedData?.time || " - " }}
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
            <v-row v-if="!isBuku2D">
              <v-col>
                <template v-if="isRisalahRDG">
                  <p class="mb-2 mt-3 text-gradient-grey text-15">Penyusun</p>
                  <div class="d-flex align-center">
                    <text-ellipsis
                      :text="participantsBPOnGoing.value?.penyusunDoc ?? '-'"
                    />
                  </div>
                </template>
                <template v-if="canSeePengaju">
                  <p class="mb-2 text-gradient-grey text-15">Pengaju</p>
                  <div class="d-flex align-center">
                    <text-ellipsis :text="pengaju.name ?? '-'" />
                    <div class="ml-2">
                      <edit-approval
                        v-if="pengaju.isEdit"
                        :itemDialog="pengaju"
                        :item="item"
                        :label-dialog="'Edit Pengaju'"
                        @onSuccess="reloadContent"
                      />
                    </div>
                  </div>
                </template>
                <p class="mb-2 mt-3 text-gradient-grey text-15">Penyetuju</p>
                <div class="d-flex align-center">
                  <text-ellipsis :text="penyetuju.name ?? '-'" />
                  <div class="ml-2">
                    <edit-approval
                      v-if="penyetuju.isEdit"
                      :itemDialog="penyetuju"
                      :item="item"
                      :label-dialog="'Edit Pengaju'"
                      @onSuccess="reloadContent"
                    />
                  </div>
                </div>
                <v-btn
                  class="rounded-lg font-weight-semibold mt-4 reset-approval-btn"
                  min-width="0"
                  color="#065695"
                  variant="outlined"
                  :disabled="!participantsBPOnGoing?.buttonReset"
                  @click="handleResetApproval(item.docID)"
                >
                  Reset Approval
                </v-btn>
              </v-col>
              <v-col>
                <p class="mb-2 text-gradient-grey text-15">Penyusun</p>
                <text-ellipsis :text="penyusun" />
                <p class="mb-2 mt-3 text-gradient-grey text-15">
                  Dokumen Final
                </p>
                <text-ellipsis :text="docFinal" />
                <div v-if="timTeknis != ''">
                  <p class="mb-2 mt-3 text-gradient-grey text-15">Tim Teknis</p>
                  <text-ellipsis :text="timTeknis" />
                </div>
              </v-col>
            </v-row>
            <v-row v-else>
              <v-col cols="6">
                <p class="mb-2 text-gradient-grey text-15">Penyusun</p>
                <text-ellipsis :text="penyusun" />
              </v-col>

              <v-col cols="6">
                <p class="mb-2 text-gradient-grey text-15">Dokumen Final</p>
                <text-ellipsis :text="docFinal" />
              </v-col>

              <v-col cols="12" class="mt-3">
                <buku2d-detail
                  :item="participantsBPOnGoing.sectorApprovals"
                  :docID="item.docID"
                  :on-reset-approval="handleResetApproval"
                  @onSuccess="reloadContent"
                />
              </v-col>
            </v-row>

            <!-- List Section -->
            <list-section
              :document="item"
              :items="participantsBPOnGoing.listSection"
              @update-list="getDetailBPDocOnGoing(item.docID)"
              :buttonAddSection="participantsBPOnGoing.buttonAddSection"
              :buttonChangeOrderSection="
                participantsBPOnGoing.buttonChangeOrderSection
              "
            />
          </template>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

    <!-- Reset Approval Confirmation Modal -->
    <modal-confirm
      ref="modalResetApproval"
      :form-config="resetApprovalConfig"
      @actionConfirm="confirmResetApproval"
      :isLoading="resetApprovalLoading"
    >
      <template v-slot:icon-img>
        <v-avatar
          size="80"
          style="margin-top: -54px; filter: drop-shadow(#9b9b9b 2px 2px 3px)"
        >
          <img src="/images/icon/iconWarning.png" style="width: 80px" />
        </v-avatar>
      </template>
    </modal-confirm>
  </v-sheet>
</template>
<script setup lang="ts">
/* eslint-disable */
import TextEllipsis from "@/v2/components/admin/TextEllipsis.vue";
import EditApproval from "@/v2/components/admin/content/EditApproval.vue";
import Buku2dDetail from "./Buku2dDetail.vue";
import ListSection from "@/v2/components/admin/content/ListSection.vue";
import ModalConfirm from "@/v2/components/utils/modal/ModalConfirm.vue";
import { matchChipStyle } from "@/v2/helpers/color";
import {
  reformatTimes,
  formatTimeEngToMonthInd,
} from "@/v2/helpers/DateHelper";
import { useStore } from "vuex";
import { ref, watch, computed, StyleValue, getCurrentInstance } from "vue";
import type { TModalConfirm } from "@/v2/Type";

const props = defineProps({
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
});

const store = useStore();
const { root } = getCurrentInstance() as any;
const panel = ref<number[]>([]);
const loadingBPOnGoing = ref<boolean>(false);
const participantsBPOnGoing = ref();
const modalResetApproval = ref<InstanceType<typeof ModalConfirm> | null>(null);
const resetApprovalDocID = ref<{
  idBpDocument: string;
  idSector: number | null;
} | null>(null);
const resetApprovalLoading = ref<boolean>(false);
const documentStatus = ref<string>(props.item.docStatus);
const modifiedData = ref(
  formatModifiedData(props.item?.docModifiedBy, props.item?.docModifiedDate)
);
const resetApprovalConfig = ref<TModalConfirm>({
  title: "Are you sure you want reset the approval?",
  message:
    "If you reset the approval, the status will return to the initial stage and require re-approval",
  width: 500,
  btnSubmitLabel: "Yes",
  btnSubmitColor: "primary-gradient",
  showIcon: true,
});

watch(panel, (newValue) => {
  if (newValue) getDetailBPDocOnGoing(newValue);
});

const pengaju = computed(() => {
  return participantsBPOnGoing.value?.pengaju ?? {};
});

const penyetuju = computed(() => {
  return participantsBPOnGoing.value?.penyetuju ?? {};
});

const penyusun = computed(() => {
  return participantsBPOnGoing.value?.penyusun ?? "-";
});

const docFinal = computed(() => {
  return participantsBPOnGoing.value?.docFinal ?? "-";
});

const timTeknis = computed(() => {
  return participantsBPOnGoing.value?.timTeknis ?? "";
});

const isBuku2D = computed(() => {
  // Buku 4 = 21
  return [8, 20, 21].includes(props.item.idDocumentType);
});

const isRisalahRDG = computed(() => {
  return props.item.idDocumentType === 9;
});

const canSeePengaju = computed(() => {
  return participantsBPOnGoing.value?.isShowPengaju ?? false;
});

function formatModifiedData(modifiedBy?: string, modifiedDate?: string) {
  return {
    modifiedBy: modifiedBy || null,
    date: modifiedDate ? formatTimeEngToMonthInd(modifiedDate) : "",
    time: modifiedDate ? reformatTimes(modifiedDate) : "",
  };
}

function getDetailBPDocOnGoing(docID: number | number[]) {
  loadingBPOnGoing.value = true;
  store
    .dispatch("adminStore/getDetailBPDocOnGoing", {
      idBPDocument: docID,
    })
    .then((res: any) => {
      participantsBPOnGoing.value = res.responseData;
      if (res.responseData?.statusDoc) {
        documentStatus.value = res.responseData?.statusDoc ?? "Unknown";
      }
      if (
        res.responseData?.lastModifiedBy ||
        res.responseData?.lastModifiedDate
      ) {
        modifiedData.value = formatModifiedData(
          res.responseData?.lastModifiedBy,
          res.responseData?.lastModifiedDate
        );
      }
    })
    .finally(() => {
      loadingBPOnGoing.value = false;
    });
}

const reloadContent = (value: any) => {
  getDetailBPDocOnGoing(value);
};

function handleResetApproval(docID: string, sectorId?: number) {
  resetApprovalDocID.value = {
    idBpDocument: docID,
    idSector: sectorId ?? null,
  };
  if (modalResetApproval.value) {
    modalResetApproval.value.show(resetApprovalDocID.value);
  }
}

function confirmResetApproval() {
  if (!resetApprovalDocID.value) return;

  resetApprovalLoading.value = true;
  store.commit("adminStore/setLoading", true);
  store
    .dispatch("adminStore/resetApproval", {
      idBpDocument: resetApprovalDocID.value.idBpDocument,
      idSector: resetApprovalDocID.value.idSector,
    })
    .then((res: any) => {
      root.refs.toast.show({
        message: res?.responseMessage ?? "Successfully reset the approval",
        color: "success",
        timeout: 3000,
      });
      reloadContent(resetApprovalDocID.value?.idBpDocument);
      modalResetApproval.value?.hide();
    })
    .catch((error: any) => {
      root.refs.toast.show({
        message: error?.message ?? "Failed to reset approval",
        color: "error",
        timeout: 3000,
      });
      console.error("Error resetting approval:", error);
    })
    .finally(() => {
      resetApprovalLoading.value = false;
      store.commit("adminStore/setLoading", false);
      resetApprovalDocID.value = null;
    });
}
</script>
<style scoped>
.item-information {
  color: #797979e5;
  font-size: 13px;
  line-height: 19.5px;
}

.reset-approval-btn:disabled {
  background-color: #d9d9d9 !important;
  color: #9e9e9e !important;
  opacity: 1 !important;
  border: none;
}
</style>
