<template>
  <v-row class="ml-1 mt-2">
    <v-col cols="10">
      <v-row>
        <v-col cols="12" class="py-2">
          <div class="text-grey-theme fw-600 text-13">Workspace Type</div>
          <div class="text-black-theme text-13">
            {{ item.workspaceTypeName ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" class="py-2">
          <div class="text-grey-theme fw-600 text-13">Nama</div>
          <div class="text-black-theme text-13">
            {{ item.name ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" class="py-2">
          <div class="text-grey-theme fw-600 text-13">Deskripsi</div>
          <div class="text-black-theme text-13">
            {{ item.descriptions ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" class="py-2">
          <div class="text-grey-theme fw-600 text-13">Pimpinan Satker</div>
          <div class="text-black-theme text-13">
            {{ getNameFromArray(item.pimpinanSatker) ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" class="py-2" v-if="item.isWorkspaceTopical">
          <div class="text-grey-theme fw-600 text-13">PIC Satker</div>
          <div class="text-black-theme text-13">
            {{ getNameFromArray(item.picSatker) ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" class="py-2" v-else>
          <div class="text-grey-theme fw-600 text-13">Project Leader</div>
          <div class="text-black-theme text-13">
            {{ getNameFromArray(item.projectLeader) ?? "-" }}
          </div>
        </v-col>
      </v-row>
    </v-col>
    <v-col cols="2" class="mt-2 text-right">
      <v-btn
        color="#1976d2"
        variant="outlined"
        class="btn-outline-rounded pa-1 pl-2 pr-2"
        @click="action"
      >
        Edit Participant
      </v-btn>
    </v-col>
  </v-row>

  <modal-confirm-component
    :formConfirm="formConfirm"
    ref="modal_confirm"
    @action-confirm="doAction"
  />

  <edit-participant-dialog ref="modal_edit_participant" @submit="reloadPage" />
</template>

<script>
import ModalConfirmComponent from "../utils/ModalConfirmComponent.vue";
import EditParticipantDialog from "@/components/administrator/EditParticipantDialog.vue";
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
    EditParticipantDialog,
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
    action() {
      this.$refs.modal_edit_participant.show(this.item);
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
    getNameFromArray(items) {
      let arryName = [];
      if (items) {
        items.map((el) => {
          arryName.push(el.name);
        });
      }

      return arryName.length > 0 ? arryName.join(", ") : "-";
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
