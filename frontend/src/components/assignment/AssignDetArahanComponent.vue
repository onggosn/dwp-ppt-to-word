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
            {{ item.workspaceTypeName ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Satker Koordinator</div>
          <div class="text-black-theme text-13">
            {{ item.listSatkerKoordinator ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Workspace Name</div>
          <div class="text-black-theme text-13">
            {{ item.workspaceName ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Satker Pendukung</div>
          <div class="text-black-theme text-13">
            {{ item.listSatkerPendukung ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Task Name</div>
          <div class="text-black-theme text-13">
            {{ item.taskName ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Ditugaskan Kepada</div>
          <div class="text-black-theme text-13">
            {{ item.listDitugaskanKepada ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Tanggal Pelaksanaan</div>
          <div class="text-black-theme text-13">
            {{
              item.workDate != null
                ? formatTimeEngToMonthInd(item.workDate)
                : "-"
            }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">ADG yang Membawahi</div>
          <div class="text-black-theme text-13">
            {{ item.listADGBidang ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Topik Penugasan</div>
          <div class="text-black-theme text-13">
            {{ item.assignmentName ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Created By</div>
          <div class="text-black-theme text-13">
            {{
              item.createdDate != ""
                ? formatTimeEngToMonthandTimeInd(item.createdDate)
                : "-"
            }}
            ;
            {{ item.name != "" ? setName(item.name) : "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Isi Penugasan</div>
          <div class="text-black-theme text-13">
            {{ item.description ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0"></v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Tipe Penugasan</div>
          <div class="text-black-theme text-13">
            {{ item.tipePenugasan ?? "-" }}
          </div>
        </v-col>
      </v-row>
    </v-col>
    <v-col cols="3" class="mt-2 text-right">
      <template v-if="item.listApproval && item.listApproval.length">
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

  <modal-edit-metadata
    ref="modal_edit_metadata"
    @onSuccessEdit="reloadPage"
    tag="arahan_metadata"
  />

  <edit-access-assignment-dialog
    ref="modal_edit_assignment_member"
    @closeModal="getArahan"
  />
</template>

<script>
import client from "@/library/ApiClient";
import ModalEditMetadata from "./EditMetadataAssignment.vue";
import ModalConfirmComponent from "../utils/ModalConfirmComponent.vue";
import EditAccessAssignmentDialog from "../assignment/EditAccessAssignmentDialog.vue";
import {
  formatTimeEngToMonthInd,
  formatTimeEngToMonthandTimeInd,
} from "@/helpers/date";

export default {
  name: "assignDetArahanComponent",
  emits: ["reloadPage"],
  props: {
    idAssignment: {
      type: String,
      default: null,
      required: true,
    },
  },
  components: {
    ModalEditMetadata,
    ModalConfirmComponent,
    EditAccessAssignmentDialog,
  },
  data() {
    return {
      tab: null,
      isLoading: false,
      item: {},
      formConfirm: {
        title: "Delete Arahan",
        width: 500,
        btnSubmitLabel: "Delete",
        icon: {
          code: "mdi-close-circle-outline",
          color: "red",
        },
        message: `<div class="text-center">Deleting assignment will permanently remove all data and document. Are you sure ? </div>`,
      },
    };
  },
  methods: {
    formatTimeEngToMonthInd: formatTimeEngToMonthInd,
    formatTimeEngToMonthandTimeInd: formatTimeEngToMonthandTimeInd,
    getArahan() {
      this.isLoading = true;
      client
        .getAssignmentDetail({
          store: this.$store,
          data: {
            id: this.idAssignment,
          },
        })
        .then((result) => {
          let plainData = result.plainData.responseData;
          this.item = plainData;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getColorBtn(label) {
      label = label.toLowerCase();
      const color = {
        "view assignment": "#1976d2",
        "go to task": "#1976d3",
        edit: "success",
        delete: "red",
        close: "red",
      };
      return color[label] ?? "success";
    },
    setName() {
      let createdByName = this.item.name;
      let splitName = createdByName.toLowerCase().split(" ");
      for (var i = 0; i < splitName.length; i++) {
        splitName[i] =
          splitName[i].charAt(0).toUpperCase() + splitName[i].substring(1);
      }
      return splitName.join(" ") ?? "-";
    },
    action(row) {
      row.idArahan = this.item.id;
      let label = row.label.toLowerCase();

      // go to assignment
      if (label == "view assignment") {
        this.$router.push({
          name: "assignment-detail",
          params: {
            id: this.item.id,
          },
        });
      }
      // go to task
      else if (label == "go to task") {
        this.$router.push({
          name: "task-description",
          params: {
            taskId: this.item.idTask,
            workspaceId: this.item.idWorkspace,
          },
        });
      }
      if (label == "edit metadata") {
        this.$refs.modal_edit_metadata.show(this.item);
      }
      // edit
      else if (label == "edit") {
        this.$refs.modal_edit_arahan.show(this.item.id);
      }
      // edit access
      else if (label == "edit access") {
        this.$refs.modal_edit_assignment_member.show(this.item.id);
      }
      // delete
      else if (label == "delete") {
        this.formConfirm = {
          title: "Delete Assignment",
          width: 500,
          btnSubmitLabel: "Delete",
          icon: {},
          message: `<div class="text-center">Deleting assignment will permanently remove all data
          and document. Are you sure ?</div>`,
        };
        let count = 0;
        if (row.nextApproval === 0) {
          count = 10;
        }
        this.$refs.modal_confirm.start(row, count);
      }
    },
    doAction(data = {}) {
      let requestData = {
        idAssignment: data.idAssignment,
        idTipePenugasan: data.idTipePenugasan,
        currentStatus: data.currentStatus,
        nextApproval: data.nextApproval,
      };
      client
        .deleteAssignment({
          store: this.$store,
          data: requestData,
        })
        .then(() => {
          this.reloadPage();
          let msg = "Successfully Deleted";
          this.$root.toast.show({
            message: msg,
            color: "success",
            timeout: 3000,
          });
        })
        .catch(() => {
          this.$root.toast.show({
            message: "Error Deleted Arahan",
            color: "danger",
            timeout: 3000,
          });
        });
    },
    reloadPage() {
      this.$emit("reloadPage");
    },
  },
  created() {
    this.getArahan();
  },
};
</script>

<style scoped>
.text-danger {
  background: -webkit-linear-gradient(90.85deg, #d6212a 15.38%, #ff000d 81.89%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.text-waring {
  background: -webkit-linear-gradient(90.05deg, #c45b10 0.05%, #fe7411 99.96%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.text-success {
  background: -webkit-linear-gradient(180deg, #00783e 0%, #02aa59 100%);
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
