<template>
  <template v-if="isLoading">
    <paragraph-shimmer :is-loading="true" :lines="4" :random-size="true" />
  </template>
  <v-row v-else class="mx-2">
    <v-col cols="9" class="mt-2">
      <v-row>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Workspace Type</div>
          <div class="text-black-theme text-13">
            {{ item?.eventSubTypeLIst ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Satker Koordinator</div>
          <div class="text-black-theme text-13">
            {{ item?.satkerKoordinatorList ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Workspace Name</div>
          <div class="text-black-theme text-13">
            {{ item?.eventName ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Satker Pendukung</div>
          <div class="text-black-theme text-13">
            {{ item?.satkerPendukungList ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Tanggal Pelaksanaan</div>
          <div class="text-black-theme text-13">
            {{
              item?.workDate != null
                ? formatTimeEngToMonthInd(item?.workDate)
                : "-"
            }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Ditugaskan Kepada</div>
          <div class="text-black-theme text-13">
            {{
              !!item?.listDitugaskanKepada ? item?.listDitugaskanKepada : "-"
            }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Topik Penugasan</div>
          <div class="text-black-theme text-13">
            {{ item?.assignmentName ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">ADG yang Membawahi</div>
          <div class="text-black-theme text-13">
            {{ item?.adgBidangList ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Isi Penugasan</div>
          <div class="text-black-theme text-13">
            {{ !!item?.description ? item?.description : "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Batas Waktu</div>
          <div class="text-black-theme text-13">
            {{ item?.dueDate ? formatTimeEngToMonthInd(item?.dueDate) : "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Tipe Penugasan</div>
          <div class="text-black-theme text-13">
            {{ item?.tipePenugasan ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Periode Reminder</div>
          <div class="text-black-theme text-13">
            {{ item?.periode ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0"></v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Created By</div>
          <div class="text-black-theme text-13">
            {{
              item?.createdDate
                ? formatTimeEngToMonthandTimeInd(item?.createdDate)
                : "-"
            }}
            ;
            {{ item?.name ? setName(item?.name) : "-" }}
          </div>
        </v-col>
      </v-row>
    </v-col>
    <v-col cols="3" class="mt-2 text-right">
      <template v-if="item?.listApproval && item?.listApproval.length">
        <div v-for="(row, idx) in item.listApproval" :key="idx">
          <v-btn
            :color="getColorBtn(row.label)"
            density="comfortable"
            width="auto"
            height="auto"
            variant="outlined"
            class="btn-outline-rounded pa-1 pl-2 pr-2"
            @click="action(row)"
          >
            {{ row.label }}
          </v-btn>
        </div>
      </template>
    </v-col>
  </v-row>

  <modal-confirm-component
    :formConfirm="formConfirm"
    ref="modal_confirm"
    @action-confirm="doAction"
  />
  <modal-edit-metadata ref="modal_edit_metadata" @onSuccessEdit="reloadPage" />
  <EditAccessAssignment
    :idDoc="item?.id"
    title="Edit Access"
    @onSuccessEdit="getPenugasan"
    ref="modal_edit_assignment_member"
    :key="store.getters['collaborationStore/getDocumentFlowCheck']"
  />
</template>

<script setup lang="ts">
import { ref, getCurrentInstance, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import { TModalConfirm } from "@v2/Type.d";

import {
  formatTimeEngToMonthInd,
  formatTimeEngToMonthandTimeInd,
} from "@/helpers/date";

import ModalConfirmComponent from "@/components/utils/ModalConfirmComponent.vue";
import ModalEditMetadata from "./EditMetadataAssignment.vue";
import EditAccessAssignment from "../collaboration/EditAccessAssignment.vue";
import { ListAssignment, ListApproval } from "@v2/Type";

import ActionApproval from "@/v2/enum/ActionApproval";

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
  isDashboard: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits<{ (e: "reloadPage", value: unknown): void }>();
const router = useRouter();
const store = useStore();
const isLoading = ref<boolean>(false);

const modal_edit_penugasan = ref();
const modal_edit_assignment_member = ref();
const modal_edit_metadata = ref();
const modal_confirm = ref();
const instance = ref<any>(getCurrentInstance()?.root.refs);
const formConfirm = ref<TModalConfirm>({
  title: "Delete Penugasan",
  width: 500,
  btnSubmitLabel: "Delete",
  icon: {
    code: "mdi-close-circle-outline",
    color: "red",
  },
  message: `<div class="text-center">Deleting assignment will permanently remove all data and document. Are you sure ? </div>`,
});

const item = ref<ListAssignment>();

function getPenugasan() {
  isLoading.value = true;
  const payload = {
    id: props.id,
  };

  if (props.isDashboard) {
    Object.assign(payload, { source: "dashboard-assignment" });
  }

  store
    .dispatch("assignmentStore/getDetailAssignmentById", payload)
    .then((result) => {
      item.value = result.responseData;
    })
    .finally(() => {
      isLoading.value = false;
    });
}

function getColorBtn(label: string) {
  const color = {
    "go to penugasan": "#1976d3",
    "view assignment": "#1976d2",
    "go to workspace": "#1976d3",
    edit: "success",
    delete: "red",
    close: "red",
  };
  return color[label.toLowerCase()] ?? "success";
}

function setName(name: any) {
  let createdByName = name;
  let splitName = createdByName?.toLowerCase().split(" ");
  for (var i = 0; i < splitName.length; i++) {
    splitName[i] =
      splitName[i].charAt(0).toUpperCase() + splitName[i].substring(1);
  }
  return splitName.join(" ") ?? "-";
}

function action(row: ListApproval) {
  row.idPenugasan = item.value?.id;
  let label = row.label.toLowerCase();

  // go to assignment
  if (label == ActionApproval.viewAssignment) {
    router.push({
      name: "assignment-detail-new",
      params: {
        id: item.value?.id,
      },
    });
  }
  // go to workspace
  else if (label == ActionApproval.goToWorkspace) {
    if (item.value?.eventName.includes("RDGM")) {
      router.push({
        name: "om.workspace-management-rdgm-detail",
        params: { typeRDG: "rdgm", idEvent: item.value?.idEvent },
      });
    } else {
      router.push({
        name: "v2.workspace-rdg-detail",
        params: { typeRDG: "rdgb", idEvent: item.value?.idEvent },
      });
    }
  }
  // edit
  else if (label == ActionApproval.edit) {
    modal_edit_penugasan.value.show(item.value?.id);
  }
  // edit access
  else if (label == ActionApproval.editAccess) {
    modal_edit_assignment_member.value.openDialog();
  }
  if (label == ActionApproval.editMetadata) {
    modal_edit_metadata.value.show(item.value);
  }
  // delete
  else if (label == ActionApproval.delete) {
    formConfirm.value = {
      title: "Delete Assignment",
      width: 500,
      btnSubmitLabel: "Delete",
      icon: {},
      message: `<div class="text-center" style="color: #BBBBBB">Deleting assignment will permanently remove all data
          and document. Are you sure ?</div>`,
    };
    let count = 0;
    if (row.nextApproval === 0) {
      count = 10;
    }
    modal_confirm.value.start(row, count);
  }
  // close
  else if (label == ActionApproval.close) {
    doAction(row);
  }
}

function doAction(data: any = {}) {
  if (data.label === "Delete") {
    store
      .dispatch("assignmentStore/deleteAssignment", data)
      .then((res) => {
        if (res.responseCode == "011000") {
          instance.value.toast.show({
            message: res.responseMessage,
            color: "success",
            timeout: 3000,
            icon: "mdi-check",
          });
        } else {
          instance.value.toast.show({
            message: res.responseMessage,
            color: "error",
            timeout: 3000,
            icon: "mdi-check",
          });
        }
      })
      .catch(() => {
        instance.value.toast.show({
          message: "Fail deleting assignment",
          color: "error",
          timeout: 3000,
          icon: "mdi-check",
        });
      })
      .finally(() => {
        reloadPage();
      });
  }
}

onMounted(() => {
  getPenugasan();
});

function reloadPage() {
  emit("reloadPage", true);
}
</script>

<style scoped>
.text-danger {
  background: -webkit-linear-gradient(90.85deg, #d6212a 15.38%, #ff000d 81.89%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.text-waring {
  background: -webkit-linear-gradient(90.05deg, #c45b10 0.05%, #fe7411 99.96%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.text-success {
  background: -webkit-linear-gradient(180deg, #00783e 0%, #02aa59 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.text-grey-theme {
  color: #a6abc7;
}
.text-black-theme {
  color: #4b4b4b;
}

.text-gradient-blue {
  background: -webkit-linear-gradient(#065695, #267dc2);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 900;
  font-size: 15px;
}

.btn-outline-rounded {
  border-radius: 10px;
  letter-spacing: -0.5px;
}
.dotted {
  border: 2px dashed #065695;
  border-style: none none dashed;
  color: #fff;
  background-color: #fff;
}
:deep(.tab-header.v-slide-group-item--active) {
  color: #065695;
  background: transparent;
  border: 0px;
  border-radius: 0px;
  border-bottom: 1.2px solid;
}
</style>
