<template>
  <template v-if="isLoading">
    <paragraph-shimmer :is-loading="true" :lines="4" :random-size="true" />
  </template>
  <v-row v-else class="mx-2">
    <v-col cols="10" class="mt-2">
      <v-row>
        <v-col cols="12" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Deskripsi</div>
          <div class="text-black-theme text-13">
            {{ item.descriptions ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Tipe</div>
          <div class="text-black-theme text-13">
            {{ item.workspaceTypeName ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Pengaju</div>
          <div class="text-black-theme text-13">
            {{ item.pengaju ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Due Date</div>
          <div class="text-black-theme text-13">
            {{
              item.startDate != "" ? formatTimeEngtoInd(item.startDate) : "-"
            }}
            -
            {{ item.endDate != "" ? formatTimeEngtoInd(item.endDate) : "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Penyetuju</div>
          <div class="text-black-theme text-13">
            {{ item.penyetuju ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" md="6" class="px-0">
          <div class="text-grey-theme fw-600 text-13">PS</div>
          <div class="text-black-theme text-13">
            {{ item.ps ?? "-" }}
          </div>
        </v-col>
        <!-- show command in delete and cancel -->
        <v-col
          cols="12"
          class="px-0"
          v-if="
            item.commentDelete &&
            (([12, 13].includes(item.idNextApproval) && tag == 'persetujuan') ||
              tag == 'pengajuan')
          "
        >
          <v-alert
            color="red"
            variant="outlined"
            icon="mdi-information-outline"
            prominent
          >
            <p class="mb-1 text-grey-theme fw-600 text-13">
              {{
                [12, null].includes(item.idNextApproval)
                  ? "Delete Workspace"
                  : "Cancel Workspace"
              }}
            </p>
            <p class="text-black-theme text-13 label">
              "{{ item.commentDelete }}"
            </p>
          </v-alert>
        </v-col>
      </v-row>
    </v-col>
    <v-col cols="2" class="mt-2 text-right">
      <template v-if="item.listApproval && item.listApproval.length">
        <div v-for="(row, idx) in item.listApproval" :key="idx">
          <v-btn
            v-if="row.label == 'Go To Workspace'"
            density="comfortable"
            color="#1976d2"
            variant="outlined"
            class="btn-outline-rounded"
            :to="{
              name: 'workspace-detail',
              params: { workspaceId: item.id },
            }"
          >
            {{ row.label }}
          </v-btn>
          <v-btn
            v-else
            density="comfortable"
            :color="getColorBtn(row.label)"
            style="width: 5vw"
            variant="outlined"
            class="btn-outline-rounded"
            @click="action(row)"
          >
            {{ row.label }}
          </v-btn>
        </div>
      </template>
    </v-col>
  </v-row>
  <template v-if="tag == 'workspace'">
    <hr style="margin-top: 40px" class="dotted" />
    <div class="mt-4" v-if="isLoading">
      <paragraph-shimmer :is-loading="true" :lines="4" :random-size="true" />
    </div>
    <div class="mx-2 mb-1">
      <v-row class="mt-2">
        <v-col cols="12">
          <div class="text-gradient-blue text-15">List Activity & Task</div>
        </v-col>
      </v-row>
      <template v-if="listItem.activityViewList.length">
        <v-tabs v-model="tab">
          <div
            v-for="itemActivity in listItem.activityViewList"
            :key="itemActivity.id"
          >
            <v-tab :value="itemActivity.activityName" class="tab-header">
              <p class="pt-4">
                {{ itemActivity.activityName.toUpperCase() }}
              </p>
            </v-tab>
          </div>
        </v-tabs>
        <v-window v-model="tab" class="mt-2">
          <v-window-item
            v-for="itemActivity in listItem.activityViewList"
            :key="itemActivity.id"
            :value="itemActivity.activityName"
          >
            <v-row>
              <v-col cols="12">
                <v-table style="width: 100%">
                  <template v-slot:default>
                    <thead>
                      <tr>
                        <th class="text-center label-header" width="5%">No</th>
                        <th width="30%" class="text-center label-header">
                          Task
                        </th>
                        <th width="40%" class="text-center label-header">
                          Description
                        </th>
                        <th width="15%" class="text-center label-header">
                          Status
                        </th>
                        <th class="text-center" width="10%"></th>
                      </tr>
                    </thead>
                    <tbody>
                      <!-- Start Pengulanan untuk render task -->
                      <tr
                        class="text-13"
                        v-for="(
                          itemTab, i
                        ) in itemActivity.tasksWithMemberViews"
                        :key="itemTab.id"
                      >
                        <td width="5%" class="text-center">{{ i + 1 }}</td>
                        <td width="30%">
                          {{ itemTab.taskName }}
                        </td>
                        <td width="40%">
                          {{ itemTab.descriptions }}
                        </td>
                        <td width="15%">
                          <span
                            class="font-weight-bold"
                            :class="'text-' + getColor(itemTab.status)"
                          >
                            {{ itemTab.statusName }}
                          </span>
                        </td>
                        <td width="10%"></td>
                      </tr>
                      <!-- End Pengulanan untuk render task -->
                    </tbody>
                  </template>
                </v-table>
              </v-col>
            </v-row>
          </v-window-item>
        </v-window>
      </template>
      <template v-else>
        <div class="text-black-theme text-13 mt-2">Data masih kosong</div>
      </template>
    </div>
  </template>

  <modal-confirm-component
    :formConfirm="formConfirm"
    ref="modal_confirm"
    @action-confirm="doAction"
  />

  <modal-confirm-component
    :formConfirm="formConfirm"
    ref="modal_confirm_two_factor_1"
  >
    <template v-slot:btn-action-confirm="slot">
      <v-btn
        class="ml-2 rounded-lg btn btn-danger"
        @click="nextAction(slot.modalData)"
      >
        Next
      </v-btn>
    </template>
  </modal-confirm-component>

  <modal-confirm-component
    @action-confirm="doAction"
    :formConfirm="formConfirm"
    ref="modal_confirm_two_factor_2"
  >
    <v-textarea
      variant="outlined"
      rows="3"
      max-rows="3"
      class="mt-3"
      v-model="description.value"
      :placeholder="description.placeholder"
      :error-messages="description.error"
      :hide-details="description.error.length == 0"
    />
  </modal-confirm-component>

  <edit-workspace-dialog
    ref="modal_edit_workspace"
    @afterProsess="reloadPage"
  />
</template>

<script>
import client from "@/library/ApiClient";
import ModalConfirmComponent from "../utils/ModalConfirmComponent.vue";
import EditWorkspaceDialog from "../workspace/EditWorkspaceDialog.vue";
import { formatTimeEngtoInd } from "@/helpers/date";

export default {
  name: "dashDetWorkspaceComponent",
  emits: ["reloadPage"],
  props: {
    item: {
      type: Object,
      default: function () {
        return {};
      },
    },
    tag: {
      type: String,
      default: "workspace",
    },
  },
  components: {
    ModalConfirmComponent,
    EditWorkspaceDialog,
  },
  data() {
    return {
      tab: null,
      isLoading: false,
      listItem: {
        activityViewList: [],
      },
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
      description: {
        placeholder: "Masukkan alasan Anda menghapus workspace ini",
        value: null,
        error: [],
      },
    };
  },
  methods: {
    formatTimeEngtoInd: formatTimeEngtoInd,
    getWorkspace() {
      this.isLoading = true;
      client
        .getListActivityAndTaskByTaskMemberandIdWorkspace({
          store: this.$store,
          data: {
            id: this.item.id,
            username: this.$store.state.username,
          },
        })
        .then((result) => {
          let plainData = result.plainData;
          this.listItem = plainData;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getColor(statusId) {
      let colorStatus = {
        1: "danger",
        2: "warning",
        3: "success",
        8: "warning",
        9: "danger",
        10: "warning",
        11: "success",
        12: "danger",
        13: "danger",
        14: "warning",
        15: "danger",
        16: "warning",
        17: "success",
        18: "danger",
      };
      return colorStatus[statusId] ?? "danger";
    },
    getColorBtn(label) {
      label = label.toLowerCase();
      const color = {
        "go to workspace": "#1976d3",
        approve: "#1976d2",
        reject: "red",
        edit: "success",
        delete: "red",
        cancel: "warning",
        close: "red",
      };
      return color[label] ?? "success";
    },
    isOwner() {
      return this.$store.state.divisiDewa.includes(this.$store.state.divisi);
    },
    action(row) {
      row.idWorkspace = this.item.id;
      row.nextApproval = row.nextApproval ?? 0;
      row.currentStatus = row.currentStatus ?? 0;

      let label = row.label.toLowerCase();

      if (label == "edit") {
        this.$refs.modal_edit_workspace.show(this.item.id);
      }
      // delete
      else if (label == "delete") {
        this.formConfirm = {
          title: "Delete Workspace",
          width: 500,
          btnSubmitLabel: "Submit",
          icon: {},
          message: `<div class="text-center">Are you sure delete this workspace ?</div>`,
        };
        this.description.placeholder =
          "Masukkan alasan Anda menghapus workspace ini";
        this.$refs.modal_confirm_two_factor_1.start(row, 0);
      }
      // close
      else if (label == "close") {
        this.description.value = null;
        this.doAction(row);
      }
      // cancel
      else if (label == "cancel") {
        this.formConfirm = {
          title: "Cancel Workspace",
          width: 500,
          btnSubmitLabel: "Submit",
          icon: {},
          message: `<div class="text-center">Are you sure cancel this workspace ?</div>`,
        };
        this.description.placeholder =
          "Masukkan alasan Anda membatalkan workspace ini";
        this.$refs.modal_confirm_two_factor_1.start(row, 0);
      }
      // approval create
      else if (this.item.idNextApproval == 9) {
        if (label == "reject") {
          this.formConfirm = {
            title: "Reject Workspace",
            width: 500,
            btnSubmitLabel: "Reject",
            icon: {
              code: "mdi-close-circle-outline",
              color: "red",
            },
            message: `Rejecting workspace will permanently remove <br />
            workspace proposal from your dashboard. <br />
            Are you sure ?`,
          };
          this.$refs.modal_confirm.start(row, 10);
        } else {
          this.doAction(row);
        }
      }
      // approval close
      else if (this.item.idNextApproval == 11) {
        if (label == "reject") {
          this.formConfirm = {
            title: "Reject to Close Workspace",
            width: 500,
            btnSubmitLabel: "Reject",
            icon: {
              code: "mdi-close-circle-outline",
              color: "red",
            },
            message: `Rejecting to close the workspace will keep <br />
            the workspace running on your dashboard. <br />
            Are you sure?`,
          };
          this.$refs.modal_confirm.start(row);
        } else {
          this.formConfirm = {
            title: "Close Workspace",
            width: 500,
            btnSubmitLabel: "Close",
            icon: {
              code: "mdi-close-circle-outline",
              color: "green",
            },
            message: `Approve close workspace will permanently finish your <br />
            workspace from your dashboard. Are you sure ?`,
          };
          this.$refs.modal_confirm.start(row, 10);
        }
      }
      // approval delete
      else if (this.item.idNextApproval == 12) {
        if (label == "reject") {
          this.formConfirm = {
            title: "Reject to Delete Workspace",
            width: 500,
            btnSubmitLabel: "Reject",
            icon: {
              code: "mdi-close-circle-outline",
              color: "red",
            },
            message: `Rejecting to delete the workspace will keep <br />
            the workspace running on your dashboard. <br />
            Are you sure?`,
          };
          this.$refs.modal_confirm.start(row);
        } else {
          this.formConfirm = {
            title: "Delete Workspace",
            width: 500,
            btnSubmitLabel: "Delete",
            icon: {},
            message: `<div class="text-center">Are you sure delete this workspace ?</div>`,
          };
          this.$refs.modal_confirm.start(row, 10);
        }
      }
      // approval cancel
      else if (this.item.idNextApproval == 13) {
        if (label == "reject") {
          this.formConfirm = {
            title: "Cancel Workspace",
            width: 500,
            btnSubmitLabel: "Reject",
            icon: {
              code: "mdi-close-circle-outline",
              color: "red",
            },
            message: `<div class="text-center">Are you sure to Reject for cancel this workspace ?</div>`,
          };
          this.$refs.modal_confirm.start(row, 10);
        } else {
          this.formConfirm = {
            title: "Cancel Workspace",
            width: 500,
            btnSubmitLabel: "Approve",
            icon: {
              code: "mdi-close-circle-outline",
              color: "red",
            },
            message: `<div class="text-center">Are you sure cancel this workspace ?</div>`,
          };
          this.$refs.modal_confirm.start(row, 10);
        }
      }
    },
    nextAction(data) {
      this.description.error = [];
      this.$refs.modal_confirm_two_factor_1.hide();
      this.$refs.modal_confirm_two_factor_2.start(data);
    },
    doAction(data = {}) {
      let label = data.label.toLowerCase();
      data.commentDelete = this.description.value;

      if (
        ["delete", "cancel"].includes(label) &&
        (data.commentDelete == "" || data.commentDelete == null)
      ) {
        this.description.error = ["wajib diisi"];
        this.$refs.modal_confirm_two_factor_2.open();
        return 0;
      }

      client
        .workspaceApproval({
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
              message: response.plainData.responseData.description,
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
    },
    reloadPage() {
      this.$emit("reloadPage");
    },
  },
  created() {
    if (this.tag == "workspace") {
      this.getWorkspace();
    } else {
      this.isLoading = false;
    }
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
  font-weight: 600 !important;
}
.label-header {
  font-size: 13px;
  font-weight: 600 !important;
}
.tab-header {
  color: #3a416f !important;
}
</style>
