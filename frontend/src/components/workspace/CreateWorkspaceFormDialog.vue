<template>
  <v-dialog
    persistent
    v-model="dialog"
    content-class="overflowyhid"
    :max-width="workspaceWidth"
  >
    <v-card class="rounded-lg">
      <v-card-title class="d-flex justify-center align-center">
        <div class="text-18 text-blueTheme fw-500 mt-2 mb-2">
          Create Workspace
        </div>
        <v-btn
          class="mr-2"
          style="position: absolute; right: 0"
          variant="text"
          icon="mdi-close"
          @click="dialog = false"
        ></v-btn>
      </v-card-title>
      <div class="separatorHorizontalGradient"></div>
      <v-card-text class="pb-4">
        <v-row class="my-1">
          <v-col cols="12" class="py-1" v-if="!formData.idWorkspaceType">
            <div class="text-15 text-blueTheme fw-500">Workspace</div>
            <v-select
              item-title="workspaceGrupName"
              item-value="id"
              variant="solo"
              density="comfortable"
              placeholder="Choose Workspace"
              v-model="formData.idWorkspaceGroup"
              single-line
              :items="workspaceGroupItems"
              :loading="loading[2]"
            >
              <template v-slot:no-data>
                <span
                  class="d-flex align-item-center ma-2 pa-1 select-empty"
                  @click="getworkSpaceGroup()"
                >
                  <v-icon class="mr-2">mdi-reload</v-icon>
                  Reload Data
                </span>
              </template>
            </v-select>
          </v-col>
          <v-col
            cols="12"
            class="py-1"
            v-if="formData.idWorkspaceGroup"
            :md="isPredefinedWpc ? '6' : '12'"
          >
            <div
              v-if="formData.idWorkspaceType"
              class="text-15 text-blueTheme fw-500"
            >
              Workspace Type
            </div>
            <v-select
              item-title="workspaceTypeName"
              item-value="id"
              variant="solo"
              density="comfortable"
              placeholder="Choose Workspace"
              v-model="formData.idWorkspaceType"
              single-line
              :items="workspaceTypeItems"
              @blur="v$.formData.idWorkspaceType.$touch"
              :error-messages="e(v$.formData.idWorkspaceType)"
            ></v-select>
          </v-col>
        </v-row>
        <v-row class="my-1" v-if="isPredefinedWpc">
          <v-col cols="12" md="6" class="py-1">
            <div class="text-15 text-blueTheme fw-500 mt-6">Nama</div>
            <v-text-field
              variant="solo"
              :value="workspaceNameComputed"
              :placeholder="placeholderComputed"
              readonly
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6" class="py-1">
            <div class="text-15 text-blueTheme fw-500">Periode</div>
            <v-row>
              <v-col v-if="formData.idWorkspaceType == 4">
                <div class="text-15 text-blueTheme fw-500">Minggu</div>
                <v-select
                  item-title="label"
                  item-value="label"
                  variant="solo"
                  placeholder="M1"
                  append-inner-icon="mdi-calendar-today"
                  single-line
                  v-model="formData.weekPeriod"
                  @blur="v$.formData.weekPeriod.$touch"
                  :items="weeks"
                  :error-messages="e(v$.formData.weekPeriod)"
                ></v-select>
              </v-col>
              <v-col>
                <div class="text-15 text-blueTheme fw-500">
                  Bulan<span style="color: red">*</span>
                </div>
                <v-select
                  item-title="label"
                  item-value="label"
                  variant="solo"
                  placeholder="MM"
                  append-inner-icon="mdi-calendar-today"
                  single-line
                  v-model="formData.monthPeriod"
                  @blur="v$.formData.monthPeriod.$touch"
                  :items="months"
                  :error-messages="e(v$.formData.monthPeriod)"
                >
                </v-select>
              </v-col>
              <v-col>
                <div class="text-15 text-blueTheme fw-500">
                  Tahun<span style="color: red">*</span>
                </div>
                <v-select
                  variant="solo"
                  placeholder="YYYY"
                  append-inner-icon="mdi-calendar-today"
                  single-line
                  v-model="formData.yearPeriod"
                  @blur="v$.formData.yearPeriod.$touch"
                  :items="years"
                  :error-messages="e(v$.formData.yearPeriod)"
                ></v-select>
              </v-col>
            </v-row>
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-500">
              Deskripsi<span style="color: red">*</span>
            </div>
            <v-textarea
              rows="3"
              max-rows="5"
              placeholder="Masukan deskripsi workspace"
              v-model="formData.descriptions"
              variant="solo"
              @blur="v$.formData.descriptions.$touch"
              :error-messages="e(v$.formData.descriptions)"
            ></v-textarea>
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-500">Due Date</div>
            <v-row>
              <v-col cols="6">
                <div class="text-15 text-blueTheme fw-500">
                  Start<span style="color: red">*</span>
                </div>
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
                    >(Tanggal maksimal semua proses harus selesai)</small> -->
                  <span style="color: red">*</span>
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
        </v-row>
        <v-row class="my-1" v-else-if="isCustomWpc">
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-500">Nama</div>
            <v-text-field
              v-model="formData.workspaceName"
              variant="solo"
              :placeholder="placeholderComputed"
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
              v-model="formData.descriptions"
              variant="solo"
              @blur="v$.formData.descriptions.$touch"
              :error-messages="e(v$.formData.descriptions)"
            ></v-textarea>
          </v-col>
          <v-col cols="12" class="py-1" v-if="isSatkerWpc">
            <div class="text-15 text-blueTheme fw-500">Satker Pembuat</div>
            <v-text-field
              disabled
              variant="solo"
              :value="userSatker"
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
                      @change="v$.formData.endDate.$touch"
                      @blur="v$.formData.endDate.$touch"
                      :error-messages="e(v$.formData.endDate)"
                      :value="
                        $filters.formatTimeEngToIndNoDays(formData.endDate)
                      "
                    ></v-text-field>
                  </template>
                </VueDatePicker>
              </v-col>
            </v-row>
          </v-col>
          <v-col cols="12" class="py-1">
            <v-row>
              <v-col cols="12" class="text-15 text-blueTheme fw-500 py-0">
                PS
              </v-col>
              <v-col cols="6" class="pt-1">
                <v-row>
                  <v-col
                    v-for="(item, idx) in psList"
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
            <v-select
              variant="solo"
              item-title="name"
              item-value="username"
              v-model="formData.userApproval"
              placeholder="Pilih Pimpinan Satker"
              @blur="v$.formData.userApproval.$touch"
              :items="pimList"
              :error-messages="e(v$.formData.userApproval)"
              :loading="loading[3]"
            >
              <template v-slot:no-data>
                <span
                  class="d-flex align-item-center ma-2 pa-1 select-empty"
                  @click="getPimpinanSatkerBySatker()"
                >
                  <v-icon class="mr-2">mdi-reload</v-icon>
                  Reload Data
                </span>
              </template>
            </v-select>
          </v-col>
        </v-row>
        <v-row
          class="my-0 text-center"
          v-else-if="this.formData.idWorkspaceType && isUnderDevelopment"
        >
          Under Development
        </v-row>
      </v-card-text>
      <v-card-actions
        v-if="!isUnderDevelopment"
        class="justify-end pr-6 pt-0 pb-4"
      >
        <v-btn class="btn-action btn-action-close" @click="dialog = false">
          Close
        </v-btn>
        <v-btn
          class="btn-action btn-action-create"
          @click="process(1)"
          :loading="loading[1]"
          :disabled="loading[1]"
        >
          Create
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <modal-response ref="dialog" @close-modal="closeModalHendle"></modal-response>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { required, helpers } from "@vuelidate/validators";
import { getErrorMessages, isError } from "@/library/ValidationHelper";
import client from "@/library/ApiClient";
import ModalResponse from "../utils/ModalResponse.vue";

const alphaNumCustom = helpers.regex(/^[a-zA-Z0-9\-_()\s]+$/i);

export default {
  name: "createWorkspace",
  components: {
    ModalResponse,
  },
  setup: () => ({ v$: useVuelidate() }),
  validations() {
    let formData = {
      idWorkspaceGroup: { required },
      idWorkspaceType: { required },
      weekPeriod: {},
      monthPeriod: {},
      yearPeriod: {},
      descriptions: { required },
      startDate: { required },
      endDate: {
        required,
        moreThanStartDate: (value, vm) => {
          return value && value > vm.startDate;
        },
      },

      workspaceName: {},
      userApproval: {},
      listPS: {},
    };

    if (this.isCustomWpc || this.isSatkerWpc) {
      formData.workspaceName = { required, alphaNumCustom };
      formData.userApproval = { required };
      formData.listPS = { required };
    } else {
      formData.monthPeriod = { required };
      formData.yearPeriod = { required };

      if (this.formData.idWorkspaceType == 4) {
        formData.weekPeriod = { required };
      }
    }

    return {
      formData,
    };
  },
  data() {
    const today = new Date();
    const currentYear = today.getFullYear();
    let years = [];
    for (let i = currentYear - 2; i < currentYear + 8; i++) {
      years.push(i.toString());
    }

    return {
      loading: [],
      workspaceGroupItems: [],
      dialog: false,
      formData: {
        // for global
        idWorkspaceGroup: null,
        idWorkspaceType: null,
        weekPeriod: null,
        monthPeriod: null,
        yearPeriod: null,
        descriptions: null,
        startDate: null,
        endDate: null,

        // for custom
        workspaceName: "",
        listPS: [],
        userApproval: null,
      },
      months: [
        { id: 1, label: "Januari" },
        { id: 2, label: "Februari" },
        { id: 3, label: "Maret" },
        { id: 4, label: "April" },
        { id: 5, label: "Mei" },
        { id: 6, label: "Juni" },
        { id: 7, label: "Juli" },
        { id: 8, label: "Agustus" },
        { id: 9, label: "September" },
        { id: 10, label: "Oktober" },
        { id: 11, label: "November" },
        { id: 12, label: "Desember" },
      ],
      weeks: [
        { id: 1, label: "M1" },
        { id: 2, label: "M2" },
        { id: 3, label: "M3" },
        { id: 4, label: "M4" },
        { id: 5, label: "M5" },
      ],
      years,
      //for custom
      userSatker: null,
      psList: [], //program strategis list
      pimList: [], //pimpinan satker list
    };
  },
  methods: {
    e: getErrorMessages,
    isError: isError,
    start() {
      this.dialog = true;
      this.formData = {
        idWorkspaceGroup: null,
        idWorkspaceType: null,
        weekPeriod: null,
        monthPeriod: null,
        yearPeriod: null,
        descriptions: null,
        startDate: null,
        endDate: null,
        workspaceName: null,
        listPS: [],
        userApproval: null,
      };
      this.v$.$reset();
    },
    process(i) {
      this.v$.$validate().then((res) => {
        if (res) {
          this.loading[i] = true;
          let reqData = {
            ...this.formData,
            createdBy: this.$store.state.username,
          };

          if (this.isPredefinedWpc) {
            reqData.workspaceName = this.workspaceNameComputed;
          }

          if (this.isSatkerWpc) {
            reqData.organizationName = this.userSatker;
          }

          if (this.isPredefinedWpc) {
            this.insertPredefine(reqData, i);
          } else if (this.isCustomWpc || this.isSatkerWpc) {
            this.insertCustom(reqData, i);
          } else {
            this.$refs.dialog.openModal("Under Development", true);
          }
        }
      });
    },
    insertPredefine(data, loadingIdx) {
      client
        .createPredefinedWorkspaceActivityAndTask({
          store: this.$store,
          data: data,
        })
        .then((res) => {
          this.dialog = false;
          this.$root.toast.show({
            message: "Successfully Submit",
            color: "success",
            timeout: 3000,
          });
          this.$router.push({
            name: "workspace-detail",
            params: { workspaceId: res.plainData.id },
          });
          return Promise.resolve(res);
        })
        .catch((e) => {
          // this.dialog = false;
          let msg = e.response.data.message;
          this.$refs.dialog.openModal(msg, true);
          return Promise.reject(e);
        })
        .finally(() => {
          this.loading[loadingIdx] = false;
        });
    },
    insertCustom(data, loadingIdx) {
      client
        .createWorkspaceCustom({
          store: this.$store,
          data: data,
        })
        .then((res) => {
          this.dialog = false;
          this.$root.toast.show({
            message:
              "Successfully Submit <br /> Please wait for workspace approval",
            color: "success",
            timeout: 3000,
          });
          this.$router.push({
            name: "workspace-detail",
            params: { workspaceId: res.plainData.responseData.id },
          });
          return Promise.resolve(res);
        })
        .catch((e) => {
          // this.dialog = false;
          let msg = "internal server error";
          try {
            msg = JSON.parse(e.response.data.message).responseMessage;
          } catch (e) {
            undefined;
          }
          this.$refs.dialog.openModal(msg, true);
          return Promise.reject(e);
        })
        .finally(() => {
          this.loading[loadingIdx] = false;
        });
    },
    getworkSpaceGroup() {
      this.loading[2] = true;
      client
        .getWorkspaceTypeByUsername({ store: this.$store })
        .then((res) => {
          this.workspaceGroupItems = res.plainData;
        })
        .finally(() => {
          this.loading[2] = false;
        });
    },
    getPimpinanSatkerBySatker() {
      this.loading[3] = true;
      client
        .MUserListPimpinanSatkerbySatker({ store: this.$store })
        .then((res) => {
          this.pimList = res.plainData.responseData;
        })
        .finally(() => {
          this.loading[3] = false;
        });
    },
    getMasterData() {
      client.MProgramStrategis({ store: this.$store }).then((res) => {
        this.psList = res.plainData.responseData;
      });

      client
        .GetOrganizationNameByUsername({ store: this.$store })
        .then((res) => {
          this.userSatker = res.plainData.responseData.organizationName;
        });
    },
    closeModalHendle() {
      this.v$.$reset();
    },
  },
  created() {
    this.getworkSpaceGroup();
    this.getPimpinanSatkerBySatker();
    this.getMasterData();
  },
  computed: {
    workspaceWidth() {
      if (this.formData.idWorkspaceType) {
        if ([6, 7].includes(this.formData.idWorkspaceType)) {
          return "1200";
        }
        return "800";
      } else {
        return "600";
      }
    },
    workspaceTypeItems() {
      let rowGroup =
        this.workspaceGroupItems.find(
          (e) => e.id == this.formData.idWorkspaceGroup
        ) ?? {};
      return rowGroup.workspaceTypes;
    },
    workspaceNameComputed() {
      if (!this.formData.monthPeriod || !this.formData.yearPeriod) return null;
      let periodName = `${this.formData.weekPeriod ?? ""} ${
        this.formData.monthPeriod
      } ${this.formData.yearPeriod}`;

      switch (this.formData.idWorkspaceType) {
        case 1:
          return `RDG Bulanan${periodName}`;
        case 2:
          return `RDGM Triwulanan Kelembagaan${periodName}`;
        case 3:
          return `RDGB Cakupan Triwulanan${periodName}`;
        case 4:
          return `RDGM - Laporan Evaluasi Pelaksanaan Kebijakan${periodName}`;
        case 5:
          return `Production Test [Warning] -${periodName}`;
        default:
          return "workspace not found";
      }
    },
    placeholderComputed() {
      switch (this.formData.idWorkspaceType) {
        case 1:
          return `ex. RDG Bulanan Januari 2022`;
        case 2:
          return `ex. RDGM Triwulanan Kelembagaan`;
        case 3:
          return `ex. RDGB Triwulanan`;
        case 4:
          return `ex. RDGM - Laporan Evaluasi Pelaksanaan Kebijakan M1 September 2022`;
        case 5:
          return `ex. Workspace Name`;
        default:
          return `Masukan Nama Workspace`;
      }
    },
    isPredefinedWpc() {
      return (
        this.formData.idWorkspaceType &&
        [1, 2, 3, 4].includes(this.formData.idWorkspaceType)
      );
    },
    isCustomWpc() {
      return (
        this.formData.idWorkspaceType &&
        [6, 7].includes(this.formData.idWorkspaceType)
      );
    },
    isSatkerWpc() {
      return (
        this.formData.idWorkspaceType && this.formData.idWorkspaceType == 7
      );
    },
    isUnderDevelopment() {
      return ![1, 2, 3, 4, 6, 7].includes(this.formData.idWorkspaceType);
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
