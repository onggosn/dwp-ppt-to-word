<template>
  <v-dialog
    persistent
    v-model="dialog"
    content-class="overflowyhid"
    :max-width="800"
  >
    <v-card>
      <v-card-title class="d-flex justify-center align-center">
        <div class="text-18 text-blueTheme fw-500">Edit Workspace</div>
        <v-btn
          class="mr-2"
          style="position: absolute; right: 0"
          variant="text"
          icon="mdi-close"
          @click="hide()"
        ></v-btn>
      </v-card-title>
      <div class="separatorHorizontalGradient"></div>
      <v-card-text>
        <v-row class="my-1">
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-500">Workspace</div>
            <v-text-field
              readonly
              variant="solo"
              :value="item.workspaceTypeName"
            ></v-text-field>
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-500">Nama</div>
            <v-text-field
              variant="solo"
              placeholder="Masukan Nama Workspace"
              v-model="formData.workspaceName"
              :error-messages="e(v$.formData.workspaceName)"
              @blur="v$.formData.workspaceName.$touch"
            ></v-text-field>
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-500">Deskripsi</div>
            <v-textarea
              rows="3"
              max-rows="5"
              placeholder="Masukan deskripsi workspace"
              variant="solo"
              v-model="formData.descriptions"
              @blur="v$.formData.descriptions.$touch"
              :error-messages="e(v$.formData.descriptions)"
            ></v-textarea>
          </v-col>
          <v-col cols="12" class="py-1" v-if="isSatkerWpc">
            <div class="text-15 text-blueTheme fw-500">Satker Pembuat</div>
            <v-text-field
              variant="solo"
              :value="item.organizationName"
            ></v-text-field>
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-500">Due Date</div>
            <v-row>
              <v-col cols="6">
                <div class="text-15 text-blueTheme fw-500">Start</div>
                <VueDatePicker
                  auto-apply
                  v-model="formData.startDate"
                  :enable-time-picker="false"
                  :month-change-on-scroll="false"
                >
                  <template #trigger>
                    <v-text-field
                      readonly
                      variant="solo"
                      placeholder="DD/MM/YYYY"
                      append-inner-icon="mdi-calendar-today"
                      class="cursor-pointer"
                      @change="v$.formData.startDate.$touch"
                      @blur="v$.formData.startDate.$touch"
                      :error-messages="e(v$.formData.startDate)"
                      :value="
                        $filters.formatTimeEngToIndNoDays(formData.startDate)
                      "
                    ></v-text-field>
                  </template>
                </VueDatePicker>
              </v-col>
              <v-col cols="6">
                <div class="text-15 text-blueTheme fw-500">
                  End
                  <!-- <small class="text-11"
                    >(Tanggal maksimal semua proses harus selesai)</small
                  > -->
                </div>
                <VueDatePicker
                  auto-apply
                  v-model="formData.endDate"
                  :enable-time-picker="false"
                  :month-change-on-scroll="false"
                >
                  <template #trigger>
                    <v-text-field
                      readonly
                      variant="solo"
                      placeholder="DD/MM/YYYY"
                      append-inner-icon="mdi-calendar-today"
                      class="cursor-pointer"
                      :value="
                        $filters.formatTimeEngToIndNoDays(formData.endDate)
                      "
                      :error-messages="e(v$.formData.endDate)"
                      @change="v$.formData.endDate.$touch"
                      @blur="v$.formData.endDate.$touch"
                    ></v-text-field>
                  </template>
                </VueDatePicker>
              </v-col>
            </v-row>
          </v-col>
          <v-col cols="12" class="py-1">
            <v-row>
              <v-col cols="12" class="text-15 text-blueTheme fw-500 py-4">
                PS
              </v-col>
              <v-col cols="9" class="pt-1">
                <v-row>
                  <v-col
                    v-for="(item, idx) in item.listPS"
                    :key="idx"
                    cols="2"
                    class="px-2 py-0"
                  >
                    <v-checkbox
                      :label="item.value"
                      :value="item.id"
                      color="#05aa59"
                      class="my-0 py-0"
                      density="compact"
                      v-model="formData.listPS"
                      hide-details
                      multiple
                    />
                  </v-col>
                </v-row>
              </v-col>
              <span class="text-danger" v-if="!isError(v$.formData.listPS)">
                {{ e(v$.formData.listPS).toString() }}
              </span>
            </v-row>
          </v-col>
          <v-col cols="12" class="mt-4 pb-0">
            <div class="text-15 text-blueTheme fw-500">Pimpinan Satker</div>
            <v-text-field
              readonly
              variant="solo"
              :value="item.userApprovalName"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions class="justify-end pr-6 pt-0 pb-4">
        <v-btn class="btn-action btn-action-close" @click="dialog = false">
          Close
        </v-btn>
        <v-btn
          class="btn-action btn-action-create"
          @click="process()"
          :loading="loading"
          :disabled="loading"
        >
          Create
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
  name: "editWorkspaceDialog",

  setup: () => ({ v$: useVuelidate() }),
  validations() {
    let formData = {
      workspaceName: { required },
      descriptions: { required },
      startDate: { required },
      endDate: { required },
      listPS: { required },
    };

    return {
      formData,
    };
  },
  data() {
    return {
      dialog: false,
      loading: false,
      userSatker: null,
      item: {
        listPS: [],
      },
      formData: {
        workspaceName: null,
        descriptions: null,
        startDate: null,
        endDate: null,
        userApproval: null,
        listPS: [],
      },
    };
  },
  methods: {
    e: getErrorMessages,
    isError: isError,
    show(workspaceId) {
      this.dialog = true;
      this.getWorkspaceById(workspaceId);
    },
    hide() {
      this.dialog = false;
    },
    process() {
      this.v$.$validate().then((res) => {
        if (res) {
          client
            .updateWorkspace({
              store: this.$store,
              data: {
                id: this.item.id,
                ...this.formData,
              },
            })
            .then(() => {
              this.$root.toast.show({
                message: "Workspace successfully change",
                color: "success",
                timeout: 3000,
              });
              this.$emit("afterProsess");
            })
            .catch(() => {
              this.$root.toast.show({
                message: "Failed to Change Workspace",
                color: "error",
                timeout: 3000,
              });
            });
        }
      });
    },
    getWorkspaceById(workspaceId) {
      client
        .getWorkspaceById({
          store: this.$store,
          data: {
            id: workspaceId,
          },
        })
        .then((response) => {
          let data = response.plainData.responseData;
          this.item = data;
          this.formData.workspaceName = data.workspaceName;
          this.formData.descriptions = data.descriptions;
          this.formData.startDate = data.startDate.substring(0, 10);
          this.formData.endDate = data.endDate.substring(0, 10);
          this.formData.listPS = data.listPS
            .filter((e) => e.selected == true)
            .map((e) => e.id);

          if (this.isSatkerWpc) {
            this.formData.organizationName = data.organizationName;
          }
        })
        .catch(() => {
          this.$root.toast.show({
            message: "Error Ketika Request Data Edit",
            color: "error",
            timeout: 3000,
          });
        });
    },
  },
  computed: {
    isSatkerWpc() {
      return this.item.idWorkspaceType == 7;
    },
  },
};
</script>

<style scoped>
.btn-action {
  border-radius: 10px;
  padding-left: 15px;
  padding-right: 15px;
  font-weight: 800;
  box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
}

.btn-action-create {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: white !important;
}

.btn-action-close {
  background: linear-gradient(92.09deg, #fff -46.47%, #fff 157.9%);
  color: red !important;
}

.overflowyhid {
  overflow-y: hidden;
  padding-bottom: 5px;
}

input[type="date"]::-webkit-inner-spin-button,
input[type="date"]::-webkit-calendar-picker-indicator {
  display: none;
  -webkit-appearance: none;
}

.select-empty {
  cursor: pointer;
}
:deep(.cursor-pointer input) {
  cursor: pointer !important;
}
</style>
