<template>
  <v-dialog
    persistent
    v-model="dialog"
    content-class="overflowyhid"
    :max-width="600"
  >
    <v-card>
      <v-card-title class="d-flex justify-center align-center">
        <div class="text-18 text-blueTheme fw-500">Edit Participant</div>
        <v-btn
          class="mr-2"
          style="position: absolute; right: 0"
          variant="text"
          icon="mdi-close"
          @click="hide()"
        ></v-btn>
      </v-card-title>
      <v-card-text class="pb-4">
        <div
          class="separatorHorizontalGradient"
          style="margin-top: -16px"
        ></div>
        <v-row class="my-3">
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-500 mb-1">
              Pimpinan Satker
            </div>
            <v-autocomplete
              single-line
              item-title="name"
              item-value="username"
              variant="solo"
              density="comfortable"
              placeholder="Choose Pimpinan Satker"
              clearable
              hide-selected
              closable-chips
              v-model="formData.pimpinanSatker"
              :items="itemsPimpinanSatker"
              :error-messages="e(v$.formData.pimpinanSatker)"
              :menu-props="{ 'max-width': 200 }"
              :loading="loading[1]"
            >
              <template v-slot:no-data>
                <span class="d-flex align-item-center ma-2 pa-1 select-empty">
                  <!-- <v-icon class="mr-2">mdi-reload</v-icon> -->
                  Data tidak ditemukan
                </span>
              </template>
            </v-autocomplete>
          </v-col>
          <v-col cols="12" class="py-1" v-if="!item.isWorkspaceTopical">
            <div class="text-15 text-blueTheme fw-500 mb-1">Project Leader</div>
            <v-autocomplete
              single-line
              item-title="name"
              item-value="username"
              variant="solo"
              density="comfortable"
              placeholder="Choose Project Leader"
              clearable
              hide-selected
              closable-chips
              v-model="formData.projectLeader"
              :items="itemsProjectLeader"
              :error-messages="e(v$.formData.projectLeader)"
              :menu-props="{ 'max-width': 200 }"
              :loading="loading[1]"
            >
              <template v-slot:no-data>
                <span class="d-flex align-item-center ma-2 pa-1 select-empty">
                  <!-- <v-icon class="mr-2">mdi-reload</v-icon> -->
                  Data tidak ditemukan
                </span>
              </template>
            </v-autocomplete>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions class="justify-end pr-6 pt-0 pb-4">
        <v-btn class="btn-action btn-action-close" @click="hide()">
          Cancel
        </v-btn>
        <v-btn
          class="btn-action btn-action-create"
          @click="process()"
          :loading="loading[4]"
          :disabled="loading[4]"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { required } from "@vuelidate/validators";
import { getErrorMessages, isError } from "@/library/ValidationHelper";
import client from "@/library/ApiClient";

export default {
  name: "editParticipantDialog",
  emits: ["submit"],
  components: {},
  setup: () => ({ v$: useVuelidate() }),
  validations() {
    let formData = {
      pimpinanSatker: { required },
    };
    return { formData };
  },
  data() {
    return {
      dialog: false,
      loading: [],
      taskId: null,
      item: {},
      formData: {
        id: null,
        pimpinanSatker: null,
        projectLeader: null,
      },
      itemsPimpinanSatker: [],
      itemsProjectLeader: [],
    };
  },
  methods: {
    e: getErrorMessages,
    isError: isError,
    show(item) {
      this.item = item;
      this.getMasterData();
      this.dialog = true;
    },
    hide() {
      this.dialog = false;
    },
    process() {
      this.v$.$validate().then((res) => {
        if (res) {
          this.loading[4] = true;
          let data = {
            id: this.item.id,
            pimpinanSatker: this.formData.pimpinanSatker,
            projectLeader: this.formData.projectLeader,
          };
          client
            .updatePimpinanSatkerByIdWorkspaceCustomandUsername({
              store: this.$store,
              data: data,
            })
            .then((res) => {
              this.$root.toast.show({
                message: res.plainData.responseData.description,
                color:
                  res.plainData.responseCode == "011000" ? "success" : "error",
                timeout: 5000,
              });
              this.hide();
              this.$emit("submit");
            })
            .catch((err) => {
              this.$root.toast.show({
                message: err.message ?? "Maaf, terjadi kesalahan sistem",
                color: "error",
                timeout: 500000,
              });
            })
            .finally(() => {
              this.loading[4] = false;
            });
        }
      });
    },
    getMasterData() {
      this.loading[1] = true;
      client
        .getListPimpinanSatkerAndProjectLeader({
          store: this.$store,
          data: { id: this.item.id },
        })
        .then((res) => {
          // debugger;
          this.itemsPimpinanSatker = res.plainData.responseData.pimpinanSatker;
          this.itemsProjectLeader = res.plainData.responseData.projectLeader;
          this.formData.pimpinanSatker =
            this.itemsPimpinanSatker.length > 0
              ? this.item.pimpinanSatker[0].value
              : "";
          this.formData.projectLeader =
            this.itemsProjectLeader.length > 0
              ? this.item.projectLeader[0].value
              : "";
        })
        .finally(() => {
          this.loading[1] = false;
        });
    },
  },
  computed: {},
  watch: {},
};
</script>

<style scoped>
.overflowyhid {
  overflow-y: hidden;
  padding-bottom: 5px;
}

.select-empty {
  cursor: pointer;
}
:deep(.cursor-pointer input) {
  cursor: pointer !important;
}
:deep(.v-field--disabled) {
  background-color: rgb(168 160 160) !important;
}
:deep(.v-autocomplete__selection .v-chip) {
  background: #267dc2 !important;
  color: white !important;
}
</style>
