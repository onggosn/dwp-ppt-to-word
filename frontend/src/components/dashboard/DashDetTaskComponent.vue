<template>
  <v-row class="mx-2 my-1">
    <!-- start custom wpc dan satker wpc -->
    <v-col cols="10" v-if="[null, 0].includes(item.idTaskType)">
      <v-row>
        <v-col cols="12" sm="6" class="py-2">
          <div class="text-grey-theme fw-600 text-13">Workspace Name</div>
          <div class="text-black-theme text-13">
            {{ item.workspaceName ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" sm="6" class="py-2">
          <div class="text-grey-theme fw-600 text-13">
            Destination Statement
          </div>
          <div class="text-black-theme text-13">
            {{ item.destinationStatement ?? "-" }}
          </div>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" sm="6" class="py-2">
          <div class="text-grey-theme fw-600 text-13">Task Description</div>
          <div class="text-black-theme text-13">
            {{ item.descriptions ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" sm="6" class="py-2">
          <div class="text-grey-theme fw-600 text-13">Program Strategis</div>
          <div class="text-black-theme text-13">
            {{ item.programStrategis ?? "-" }}
          </div>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" sm="6" class="py-2">
          <div class="text-grey-theme fw-600 text-13">Task Type</div>
          <div class="text-black-theme text-13">
            {{ item.taskType ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" sm="6" class="py-2">
          <div class="text-grey-theme fw-600 text-13">Pengaju</div>
          <div class="text-black-theme text-13">
            {{ !item.pengaju ? "-" : item.pengaju }}
          </div>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" sm="6" class="py-2">
          <div class="text-grey-theme fw-600 text-13">Detail Periode</div>
          <div class="text-black-theme text-13">
            {{ item.detailPeriode ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" sm="6" class="py-2">
          <div class="text-grey-theme fw-600 text-13">Penyetuju</div>
          <div class="text-black-theme text-13">
            {{ !item.penyetuju ? "-" : item.penyetuju }}
          </div>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" sm="6" class="py-2">
          <div class="text-grey-theme fw-600 text-13">Tanggal Pelaksanaan</div>
          <div class="text-black-theme text-13">
            {{ item.tanggalPelaksanaan ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" sm="6" class="py-2">
          <div class="text-grey-theme fw-600 text-13">Satker Pengusul</div>
          <div class="text-black-theme text-13">
            {{ item.satkerPengusul ?? "-" }}
          </div>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" sm="6" class="py-2">
          <div class="text-grey-theme fw-600 text-13">Waktu Pembahasan</div>
          <div class="text-black-theme text-13">
            {{ item.waktuPembahasan ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" sm="6" class="py-2">
          <div class="text-grey-theme fw-600 text-13">
            Anggota Dewan Gubernur
          </div>
          <div class="text-black-theme text-13">
            {{ item.anggotaDewanGubernur ?? "-" }}
          </div>
        </v-col>
      </v-row>
    </v-col>
    <!-- end custom wpc dan satker wpc -->
    <v-col cols="10" v-else>
      <!-- START ASSESMENT -->
      <template v-if="[1, 5].includes(item.idTaskType)">
        <v-row>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Workspace Name</div>
            <div class="text-black-theme text-13">
              {{ item.workspaceName ?? "-" }}
            </div>
          </v-col>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Satker</div>
            <div class="text-black-theme text-13">
              {{ item.satker != "" ? item.satker : "-" }}
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Task Description</div>
            <div class="text-black-theme text-13">
              {{ item.descriptions ?? "-" }}
            </div>
          </v-col>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Due Date</div>
            <div class="text-black-theme text-13">
              {{
                !item.startDate ? "-" : formatTimeEngToIndNoDays(item.startDate)
              }}
              -
              {{ !item.endDate ? "-" : formatTimeEngToIndNoDays(item.endDate) }}
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">PS</div>
            <div class="text-black-theme text-13">
              {{ item.ps != "" ? item.ps : "-" }}
            </div>
          </v-col>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Pengaju</div>
            <div class="text-black-theme text-13">
              {{ item.pengaju ? item.pengaju : "-" }}
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Task Type</div>
            <div class="text-black-theme text-13">
              {{ item.TaskTypeName ?? item.taskTypeName }}
            </div>
          </v-col>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Penyetuju</div>
            <div class="text-black-theme text-13">
              {{ item.penyetuju ? item.penyetuju : "-" }}
            </div>
          </v-col>
        </v-row>
      </template>
      <!-- END ASSESMENT -->
      <!-- START KOMITE -->
      <template v-if="item.idTaskType == 2">
        <v-row>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Workspace Name</div>
            <div class="text-black-theme text-13">
              {{ item.workspaceName ?? "-" }}
            </div>
          </v-col>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Pengaju</div>
            <div class="text-black-theme text-13">
              {{ item.pengaju != "" ? item.pengaju : "-" }}
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Task Description</div>
            <div class="text-black-theme text-13">
              {{ item.descriptions ?? "-" }}
            </div>
          </v-col>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Penyetuju</div>
            <div class="text-black-theme text-13">
              {{ item.penyetuju != "" ? item.penyetuju : "-" }}
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">PS</div>
            <div class="text-black-theme text-13">
              {{ item.ps != "" ? item.ps : "-" }}
            </div>
          </v-col>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Periode</div>
            <div class="text-black-theme text-13">
              {{ item.detailPeriod ? item.detailPeriod : "-" }}
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Task Type</div>
            <div class="text-black-theme text-13">
              {{ item.TaskTypeName ?? item.taskTypeName }}
            </div>
          </v-col>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">
              Tanggal Pelaksanaan
            </div>
            <div class="text-black-theme text-13">
              {{
                !item.startDate ? "-" : formatTimeEngToIndNoDays(item.startDate)
              }}
              -
              {{ !item.endDate ? "-" : formatTimeEngToIndNoDays(item.endDate) }}
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Komite</div>
            <div class="text-black-theme text-13">
              {{ item.komite != "" ? item.komite : "-" }}
            </div>
          </v-col>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Waktu</div>
            <div class="text-black-theme text-13">
              {{ !item.startDate ? "-" : formatTimeAmPm(item.startDate) }}
              -
              {{ !item.endDate ? "-" : formatTimeAmPm(item.endDate) }}
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6" class="py-2"></v-col>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Durasi</div>
            <div class="text-black-theme text-13">
              {{ item.duration != null ? item.duration + " menit" : "-" }}
            </div>
          </v-col>
        </v-row>
      </template>
      <!-- END KOMITE-->
      <!-- START RDGM -->
      <template v-if="[3, 4].includes(item.idTaskType)">
        <v-row>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Workspace Name</div>
            <div class="text-black-theme text-13">
              {{ item.workspaceName ?? "-" }}
            </div>
          </v-col>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">
              Destination Statement
            </div>
            <div class="text-black-theme text-13">
              {{ item.destinationStatement ? item.destinationStatement : "-" }}
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Task Description</div>
            <div class="text-black-theme text-13">
              {{ item.descriptions ?? "-" }}
            </div>
          </v-col>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">PS</div>
            <div class="text-black-theme text-13">
              {{ item.ps != "" ? item.ps : "-" }}
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Task Type</div>
            <div class="text-black-theme text-13">
              {{ item.TaskTypeName ?? item.taskTypeName }}
            </div>
          </v-col>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Pengaju</div>
            <div class="text-black-theme text-13">
              {{ item.pengaju ? item.pengaju : "-" }}
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Detail Periode</div>
            <div class="text-black-theme text-13">
              {{ item.detailPeriod ? item.detailPeriod : "-" }}
            </div>
          </v-col>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Penyetuju</div>
            <div class="text-black-theme text-13">
              {{ item.penyetuju ? item.penyetuju : "-" }}
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">
              Tanggal Pelaksanaan
            </div>
            <div class="text-black-theme text-13">
              {{
                !item.startDate ? "-" : formatTimeEngToIndNoDays(item.startDate)
              }}
              -
              {{ !item.endDate ? "-" : formatTimeEngToIndNoDays(item.endDate) }}
            </div>
          </v-col>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Satker Penyaji</div>
            <div class="text-black-theme text-13">
              {{ item.satkerPenyaji != "" ? item.satkerPenyaji : "-" }}
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Waktu</div>
            <div class="text-black-theme text-13">
              {{ !item.startDate ? "-" : formatTimeAmPm(item.startDate) }}
              -
              {{ !item.endDate ? "-" : formatTimeAmPm(item.endDate) }}
            </div>
          </v-col>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Satker Diundang</div>
            <div class="text-black-theme text-13">
              {{ item.satkerDiundang != "" ? item.satkerDiundang : "-" }}
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">Durasi</div>
            <div class="text-black-theme text-13">
              {{ item.duration ? item.duration + " menit" : "-" }}
            </div>
          </v-col>
          <v-col cols="12" sm="6" class="py-2">
            <div class="text-grey-theme fw-600 text-13">ADG</div>
            <div class="text-black-theme text-13">
              {{ item.adg != "" ? item.adg : "-" }}
            </div>
          </v-col>
        </v-row>
      </template>
      <!-- END RDGM-->
    </v-col>
    <v-col cols="2" class="mt-2 text-right">
      <template v-if="item.listApproval && item.listApproval.length">
        <div v-for="(row, idx) in item.listApproval" :key="idx">
          <v-btn
            v-if="row.label == 'Go To Task'"
            density="comfortable"
            color="#1976d2"
            width="auto"
            height="auto"
            variant="outlined"
            class="btn-outline-rounded pa-1 pl-2 pr-2"
            :to="{
              name: 'task-description',
              params: {
                taskId: item.idTask,
                workspaceId: item.idWorkspace,
              },
            }"
          >
            {{ row.label }}
          </v-btn>
          <v-btn
            v-else
            :color="getColorBtn(row.label)"
            width="auto"
            height="auto"
            variant="outlined"
            class="btn-outline-rounded pa-1"
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

  <edit-task-dialog ref="modal_edit_task" @submit="reloadPage" />
</template>

<script>
import { formatTimeEngToIndNoDays, formatTimeAmPm } from "@/helpers/date";
import ModalConfirmComponent from "../utils/ModalConfirmComponent.vue";
import EditTaskDialog from "../task/EditTaskDialog.vue";
import client from "@/library/ApiClient";

export default {
  name: "dashDetTaskComponent",
  emits: ["reloadPage"],
  props: {
    item: {
      type: Object,
      required: true,
      default: function () {
        return {};
      },
    },
  },
  components: {
    ModalConfirmComponent,
    EditTaskDialog,
  },
  data() {
    return {
      isLoading: true,
      formConfirm: {
        title: "Delete Task",
        width: 500,
        btnSubmitLabel: "Delete",
        icon: {
          code: "mdi-close-circle-outline",
          color: "red",
        },
        message: `<div class="text-center">Are you sure delete this task ?</div>`,
      },
    };
  },
  created() {
    setTimeout(() => (this.isLoading = false), 300);
  },
  methods: {
    formatTimeEngToIndNoDays: formatTimeEngToIndNoDays,
    formatTimeAmPm: formatTimeAmPm,
    getColorBtn(label) {
      label = label?.toLowerCase();
      const color = {
        "go to task": "#1976d2",
        approve: "#1976d2",
        reject: "red",
        edit: "success",
        delete: "red",
        cancel: "warning",
        close: "red",
      };
      return color[label] ?? "success";
    },
    action(row) {
      row.idTask = this.item.id;
      row.nextApproval = row.nextApproval ?? 0;
      row.currentStatus = row.currentStatus ?? 0;
      row.commentDelete = null;

      let label = row.label.toLowerCase();

      if (label == "edit") {
        this.$refs.modal_edit_task.show(this.item.id, this.item.idTaskType);
      }
      // delete
      else if (label == "delete") {
        this.formConfirm = {
          title: "Delete Task",
          width: 500,
          btnSubmitLabel: "Delete",
          icon: {},
          message: `
            <div class="text-center">
              Deleting task will permanently remove all data <br />
              from your task. Are you sure ?
            </div>
          `,
        };

        let count = 0;
        if (row.nextApproval === 0) {
          count = 10;
        }
        this.$refs.modal_confirm.start(row, count);
      }
      // approval create
      else if (this.item.idNextApproval == 15) {
        if (label == "reject") {
          this.formConfirm = {
            title: "Reject Task",
            width: 500,
            btnSubmitLabel: "Reject",
            icon: {
              code: "mdi-close-circle-outline",
              color: "red",
            },
            message: `<div class="text-center">Are you sure reject this task ?</div>`,
          };
          this.$refs.modal_confirm.start(row, 10);
        } else {
          this.doAction(row);
        }
      }
      // approval delete
      else if (this.item.idNextApproval == 18) {
        if (label == "reject") {
          this.doAction(row);
        } else {
          this.formConfirm = {
            title: "Delete Task",
            width: 500,
            btnSubmitLabel: "Delete",
            icon: {
              code: "mdi-close-circle-outline",
              color: "red",
            },
            message: `<div class="text-center">Are you sure delete this task ?</div>`,
          };
          this.$refs.modal_confirm.start(row, 10);
        }
      }
    },
    doAction(data = {}) {
      let label = data.label;
      // delete data.label;

      if (label.toLowerCase() == "delete") {
        client
          .taskSubmission({
            store: this.$store,
            data: data,
          })
          .then(() => {
            this.reloadPage();
            let msg = `Successfully Submit <br/> Please wait for approval to delete`;
            if (data.nextApproval === 0) msg = `Successfully deleted`;
            this.$root.toast.show({
              message: msg,
              color: "success",
              timeout: 3000,
            });
          })
          .catch(() => {
            this.$root.toast.show({
              message: "error deleted workspace",
              color: "danger",
              timeout: 3000,
            });
          });
      } else {
        client
          .tasksApproval({
            store: this.$store,
            data: data,
          })
          .then((response) => {
            if (response.plainData.responseCode != "011000") {
              this.$root.toast.show({
                message: response.plainData.responseMessage,
                color: "error",
                timeout: 3000,
              });
            } else {
              this.$root.toast.show({
                message: `Successfully ${label}`,
                color: "success",
                timeout: 3000,
              });
              this.reloadPage();
            }
          })
          .catch(() => {
            this.$root.toast.show({
              message: `Failed to ${label}`,
              color: "error",
              timeout: 3000,
            });
          });
      }
    },
    reloadPage() {
      this.$emit("reloadPage");
    },
  },
};
</script>

<style scoped>
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
