<template>
  <v-dialog
    persistent
    v-model="dialog"
    content-class="overflowyhid"
    :max-width="1200"
  >
    <v-card>
      <v-card-title class="d-flex justify-center align-center">
        <div class="text-18 text-blueTheme fw-500">Edit Task</div>
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
        <v-row class="my-1">
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-500">
              Task Name <span class="text-redTheme">*</span>
            </div>
            <v-text-field
              placeholder="Masukan Nama Task"
              variant="solo"
              v-model="formData.taskName"
              :error-messages="e(v$.formData.taskName)"
              @blur="v$.formData.taskName.$touch"
            />
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-500">
              Task Deskription <span class="text-redTheme">*</span>
            </div>
            <v-textarea
              placeholder="Masukan Deskripsi Task"
              variant="solo"
              rows="3"
              v-model="formData.descriptions"
              :error-messages="e(v$.formData.descriptions)"
              @blur="v$.formData.descriptions.$touch"
            />
          </v-col>
          <v-col cols="12" class="py-1 mb-6">
            <v-row>
              <v-col cols="12" class="text-15 text-blueTheme fw-500 py-4">
                PS
              </v-col>
              <v-col cols="8" class="pt-1">
                <v-row>
                  <v-col
                    v-for="(item, idx) in list.ps"
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
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-500">
              Task Type <span class="text-redTheme">*</span>
            </div>
            <v-text-field disabled variant="solo" :value="item.taskTypeName" />
          </v-col>
          <!-- FORM ASSESMEN -->
          <template v-if="isAssesment">
            <v-col cols="12">
              <div class="text-15 text-blueTheme fw-500">
                Satker <span class="text-redTheme">*</span>
              </div>
              <v-select
                variant="solo"
                item-title="value"
                item-value="id"
                placeholder="Pilih Satker"
                v-model="formData.asesment.idMSatker"
                :items="list.satkers"
                :error-messages="e(v$.formData.asesment.idMSatker)"
                :hide-details="isError(v$.formData.asesment.idMSatker)"
                :disabled="isSatker"
              />
            </v-col>
            <v-col cols="12">
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
                    end
                    <!-- <small class="text-12"
                      >(Tanggal maksimal semua proses harus selesai)</small
                    > -->
                    <span class="text-redTheme">*</span>
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
          </template>
          <template v-else>
            <v-col cols="12" v-if="isKomite">
              <div class="text-15 text-blueTheme fw-500">
                Komite <span class="text-redTheme">*</span>
              </div>
              <v-text-field
                disabled
                variant="solo"
                :value="item.idMKomiteName"
              />
            </v-col>
            <v-col cols="12">
              <div class="text-15 text-blueTheme fw-500">
                Detail Periode <span class="text-redTheme">*</span>
              </div>
              <v-row>
                <v-col>
                  <div class="text-15 text-blueTheme fw-500">Minggu</div>
                  <v-select
                    variant="solo"
                    item-title="value"
                    item-value="id"
                    placeholder="M1"
                    append-inner-icon="mdi-calendar-today"
                    style="border-radius: 10px"
                    v-model="formData.komite.idMWeek"
                    :items="list.weeks"
                    :error-messages="e(v$.formData.komite.idMWeek)"
                    :hide-details="isError(v$.formData.komite.idMWeek)"
                  />
                </v-col>
                <v-col>
                  <div class="text-15 text-blueTheme fw-500">Bulan</div>
                  <v-select
                    single-line
                    variant="solo"
                    item-title="value"
                    item-value="id"
                    placeholder="MM"
                    append-inner-icon="mdi-calendar-today"
                    style="border-radius: 10px"
                    v-model="formData.komite.idMMonth"
                    :items="list.months"
                    :error-messages="e(v$.formData.komite.idMMonth)"
                    :hide-details="isError(v$.formData.komite.idMMonth)"
                  />
                </v-col>
                <v-col>
                  <div class="text-15 text-blueTheme fw-500">Tahun</div>
                  <v-select
                    variant="solo"
                    item-title="value"
                    item-value="id"
                    placeholder="YYYY"
                    append-inner-icon="mdi-calendar-today"
                    v-model="formData.komite.yearPeriod"
                    :items="list.years"
                    :error-messages="e(v$.formData.komite.yearPeriod)"
                    :hide-details="isError(v$.formData.komite.yearPeriod)"
                  />
                </v-col>
              </v-row>
            </v-col>
            <v-col cols="12">
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
                    end
                    <!-- <small class="text-12"
                      >(Tanggal maksimal semua proses harus selesai)</small
                    > -->
                    <span class="text-redTheme">*</span>
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
            <v-col cols="12">
              <div class="text-15 text-blueTheme fw-500">
                Estimasi Waktu Pembahasan<span class="text-redTheme">*</span>
              </div>
              <v-row>
                <v-col cols="6">
                  <div class="text-15 text-blueTheme fw-500">Start</div>
                  <v-select
                    variant="solo"
                    placeholder="Choose Time"
                    append-inner-icon="mdi-timer"
                    v-model="formData.startTime"
                    @blur="v$.formData.startTime.$touch"
                    :error-messages="e(v$.formData.startTime)"
                    :items="list.times"
                  />
                </v-col>
                <v-col cols="6">
                  <div class="text-15 text-blueTheme fw-500">
                    end
                    <!-- <small class="text-12"
                      >(Waktu maksimal pembahasan harus selesai)</small
                    > -->
                    <span class="text-redTheme">*</span>
                  </div>
                  <v-select
                    variant="solo"
                    placeholder="Choose Time"
                    append-inner-icon="mdi-timer"
                    v-model="formData.endTime"
                    @blur="v$.formData.endTime.$touch"
                    :error-messages="e(v$.formData.endTime)"
                    :items="list.times"
                  />
                </v-col>
              </v-row>
            </v-col>
            <v-col cols="12">
              <div class="text-15 text-blueTheme fw-500">
                Duration <span class="text-redTheme">*</span>
              </div>
              <v-text-field
                type="number"
                variant="solo"
                @blur="v$.formData.komite.duration.$touch"
                :value="formData.komite.duration"
                :error-messages="e(v$.formData.komite.duration)"
              />
            </v-col>
            <template v-if="isRDGB">
              <v-col cols="12">
                <div class="text-15 text-blueTheme fw-500">
                  Destination Statement <span class="text-redTheme">*</span>
                </div>
                <v-select
                  variant="solo"
                  item-title="value"
                  item-value="id"
                  placeholder="Pilih Destination Statement"
                  v-model="formData.rdgm.idDestinationStatement"
                  :items="list.destinations"
                  :error-messages="e(v$.formData.rdgm.idDestinationStatement)"
                  :hide-details="
                    isError(v$.formData.rdgm.idDestinationStatement)
                  "
                  :menu-props="{ 'max-width': 200 }"
                />
              </v-col>
              <v-col cols="12">
                <div class="text-15 text-blueTheme fw-500">
                  Satker Penyaji <span class="text-redTheme">*</span>
                  <select-member-component
                    key="satker_penyaji"
                    title="Satker Penyaji"
                    searchPlacheHolder="masukan nama satker"
                    :items="list.penyajis"
                    :selected="formData.rdgm.listSatkerPenyaji"
                    :errorMsg="e(v$.formData.rdgm.listSatkerPenyaji)"
                  />
                </div>
              </v-col>
              <v-col cols="12">
                <div class="text-15 text-blueTheme fw-500">
                  Satker Diundang <span class="text-redTheme">*</span>
                  <select-member-component
                    key="satker_diundang"
                    title="Satker Diundang"
                    searchPlacheHolder="masukan nama satker"
                    :items="list.diundangs"
                    :selected="formData.rdgm.listSatkerDiundang"
                    :errorMsg="e(v$.formData.rdgm.listSatkerDiundang)"
                  />
                </div>
              </v-col>
              <v-col cols="12" class="py-1">
                <v-row>
                  <v-col cols="12" class="text-15 text-blueTheme fw-500 py-4">
                    ADG <span class="text-redTheme">*</span>
                  </v-col>
                  <v-col cols="12" class="pt-1">
                    <v-row>
                      <v-col
                        v-for="(item, idx) in list.adgs"
                        :key="idx"
                        cols="3"
                        class="px-2 py-0"
                      >
                        <v-checkbox
                          :label="item.value"
                          :value="item.id"
                          color="#05aa59"
                          class="my-0 py-0"
                          density="compact"
                          v-model="formData.rdgm.listMAdg"
                          hide-details
                          multiple
                        />
                      </v-col>
                    </v-row>
                  </v-col>
                  <span
                    class="text-danger"
                    v-if="!isError(v$.formData.rdgm.listMAdg)"
                  >
                    {{ e(v$.formData.rdgm.listMAdg).toString() }}
                  </span>
                </v-row>
              </v-col>
            </template>
            <v-col cols="12">
              <div class="text-15 text-blueTheme fw-500">
                Penyetuju <span class="text-redTheme">*</span>
              </div>
              <v-select
                disabled
                variant="solo"
                item-title="name"
                item-value="value"
                placeholder="Pilih Penyetuju"
                v-model="formData.komite.userApproval"
                :items="list.penyetujus"
                :error-messages="e(v$.formData.komite.userApproval)"
                :hide-details="isError(v$.formData.komite.userApproval)"
              />
            </v-col>
          </template>
          <template v-if="!(isAssesment || isKomite || isRDGB)">
            <v-col class="text-center text-24"> In Development </v-col>
          </template>
        </v-row>
      </v-card-text>
      <v-card-actions class="justify-end pr-6 pt-0 pb-4">
        <v-btn class="btn-action btn-action-close" @click="hide()">
          Close
        </v-btn>
        <v-btn
          class="btn-action btn-action-create"
          @click="process()"
          :loading="loading"
          :disabled="loading"
        >
          Update
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { required, helpers, minValue } from "@vuelidate/validators";
import { getErrorMessages, isError } from "@/library/ValidationHelper";
import { addHours } from "date-fns";
import { diffMinute } from "@/library/DateHelper";
import SelectMemberComponent from "../utils/SelectMemberComponent.vue";
import client from "@/library/ApiClient";

const alphaNumCustom = helpers.regex(/^[a-zA-Z0-9\-_()\s]+$/i);

export default {
  name: "editTaskDialog",
  components: {
    SelectMemberComponent,
  },
  setup: () => ({ v$: useVuelidate() }),
  validations() {
    let formData = {
      taskName: { required, alphaNumCustom },
      descriptions: { required },
      listPS: { required },
      idTaskType: { required },

      startDate: { required },
      endDate: {
        required,
        moreThanStartDate: (value, vm) => {
          if (this.isAssesment) return new Date(value) > new Date(vm.startDate);
          return new Date(value) >= new Date(vm.startDate);
        },
      },
      startTime: { required },
      endTime: {
        required,
        moreThanStartTime: (value, vm) => {
          if (!vm.startDate || !vm.endDate) return true;
          return !helpers.req(value) || vm.komite.duration > 0;
        },
      },

      asesment: {
        idMSatker: {},
      },

      komite: {
        idMKomite: {},
        idMWeek: {},
        idMMonth: {},
        yearPeriod: {},
        duration: {},
        userApproval: {},
      },

      rdgm: {
        idDestinationStatement: {},
        listSatkerPenyaji: {},
        listSatkerDiundang: {},
        listMAdg: {},
      },
    };

    let asesment = {
      idMSatker: { required },
    };

    let komite = {
      idMKomite: { required },
      idMWeek: { required },
      idMMonth: { required },
      yearPeriod: { required },
      duration: {
        required,
        minValue: minValue(30),
      },
      userApproval: { required },
    };

    let rdgm = {
      idDestinationStatement: { required },
      listSatkerPenyaji: { required },
      listSatkerDiundang: { required },
      listMAdg: { required },
    };

    if (this.isAssesment) {
      delete formData.startTime;
      delete formData.endTime;

      formData = {
        ...formData,
        asesment: asesment,
      };
    } else if (this.isKomite) {
      formData = {
        ...formData,
        komite: komite,
      };
    } else if (this.isRDGB) {
      delete komite.idMKomite;
      delete asesment.idMSatker;
      formData = {
        ...formData,
        komite: komite,
        rdgm: rdgm,
      };
    }

    return { formData };
  },
  data() {
    return {
      dialog: false,
      loading: false,
      taskId: null,
      item: {},
      formData: {
        listPS: [],
        idTaskType: null,
        descriptions: null,
        taskName: null,

        startDate: null,
        endDate: null,
        startTime: "00:00",
        endTime: "00:00",

        asesment: {
          idMSatker: null,
        },

        komite: {
          idMKomite: null,
          idMWeek: null,
          idMMonth: null,
          yearPeriod: null,
          duration: 0,
          userApproval: null,
        },

        rdgm: {
          idDestinationStatement: 0,
          listSatkerPenyaji: [],
          listSatkerDiundang: [],
          listMAdg: [],
        },
      },
      list: {
        tt: [],
        ps: [],
        satkers: [],
        komites: [],
        weeks: [],
        months: [],
        years: [],
        adgs: [],
        penyajis: [],
        diundangs: [],
        destinations: [],
        penyetujus: [],
        times: [
          "00:00",
          "00:30",
          "01:00",
          "01:30",
          "02:00",
          "02:30",
          "03:00",
          "03:30",
          "04:00",
          "04:30",
          "05:00",
          "05:30",
          "06:00",
          "06:30",
          "07:00",
          "07:30",
          "08:00",
          "08:30",
          "09:00",
          "09:30",
          "10:00",
          "10:30",
          "11:00",
          "11:30",
          "12:00",
          "12:30",
          "13:00",
          "13:30",
          "14:00",
          "14:30",
          "15:00",
          "15:30",
          "16:00",
          "16:30",
          "17:00",
          "17:30",
          "18:00",
          "18:30",
          "19:00",
          "19:30",
          "20:00",
          "20:30",
          "21:00",
          "21:30",
          "22:00",
          "22:30",
          "23:00",
          "23:30",
        ],
      },
    };
  },
  created() {
    this.getMasterData();
  },
  methods: {
    e: getErrorMessages,
    isError: isError,
    show(taskId, taskTypeId) {
      this.formData.idTaskType = taskTypeId;
      this.taskId = taskId;

      if (this.isAssesment) {
        this.getTaskAssesment(taskId);
      } else if (this.isKomite) {
        this.getTaskKomite(taskId);
      } else if (this.isRDGB) {
        this.getTaskRDGB(taskId);
      }

      this.dialog = true;
    },
    hide() {
      this.dialog = false;
    },
    process() {
      this.v$.$validate().then((res) => {
        if (res) {
          this.loading = true;
          let data = {
            ...this.formData,
            startDate: this.startDateTime,
            endDate: this.endDateTime,
            idTask: this.taskId,
          };

          let doAction = new Promise((resolve, reject) => {
            let res = {
              response: {
                plainData: {
                  responseMessage: "under development",
                },
              },
            };
            reject(res);
          });

          if (this.isAssesment) {
            doAction = this.updateAsesment(data);
          } else if (this.isKomite) {
            doAction = this.updateKomite(data);
          } else if (this.isRDGB) {
            doAction = this.updateRDGM(data);
          }

          doAction
            .then((res) => {
              this.$root.toast.show({
                message: res.plainData.responseMessage,
                color:
                  res.plainData.responseCode == "011000" ? "success" : "error",
                timeout: 3000,
              });
              this.$emit("submit");
            })
            .finally(() => {
              this.loading = false;
            });
        }
      });
    },
    getMasterData() {
      client.MProgramStrategis({ store: this.$store }).then((res) => {
        this.list.ps = res.plainData.responseData;
      });

      client.MSatkerPembuat({ store: this.$store }).then((res) => {
        this.list.satkers = res.plainData.responseData;
      });

      client.getMKomiteList({ store: this.$store }).then((res) => {
        this.list.komites = res.plainData.responseData;
      });

      client.getListWeekMonthYear({ store: this.$store }).then((res) => {
        this.list.weeks = res.plainData.responseData.mWeek;
        this.list.months = res.plainData.responseData.mMonth;
        this.list.years = res.plainData.responseData.mYear;
      });

      client.getMAdgList({ store: this.$store }).then((res) => {
        this.list.adgs = res.plainData.responseData;
      });

      client.MSatkerPembuat({ store: this.$store }).then((res) => {
        this.list.penyajis = res.plainData.responseData;
        this.list.diundangs = res.plainData.responseData;
      });

      client.getMDestinationStatement({ store: this.$store }).then((res) => {
        this.list.destinations = res.plainData.responseData;
      });
    },
    getTaskTypeByActivity(activityTypeId) {
      client
        .getMTaskTypeByActivityType({
          store: this.$store,
          data: {
            id: activityTypeId,
          },
        })
        .then((res) => {
          this.list.tt = res.plainData.responseData;
        });
    },
    getListPenyetujuByKomite(komiteId) {
      client
        .getListPegawaiByKomite({ store: this.$store, data: { id: komiteId } })
        .then((res) => {
          this.list.penyetujus = res.plainData.responseData;
        });
    },
    getListPenyetujuByUsername() {
      client.getListPegawaiByIdRole({ store: this.$store }).then((res) => {
        this.list.penyetujus = res.plainData.responseData;
      });
    },
    getTaskAssesment(taskId) {
      client
        .getTaskAsesmentById({
          store: this.$store,
          data: {
            id: taskId,
          },
        })
        .then((res) => {
          let response = res.plainData.responseData;
          this.formData.descriptions = response.descriptions;
          this.formData.taskName = response.taskName;
          this.formData.startDate = response.startDate.substring(0, 10);
          this.formData.endDate = response.endDate.substring(0, 10);
          this.formData.listPS = response.listPS.map((e) => e.id);

          this.formData.asesment.idMSatker = response.idMSatker;

          this.item = response;
        });
    },
    getTaskKomite(taskId) {
      client
        .getTaskKomiteById({
          store: this.$store,
          data: {
            id: taskId,
          },
        })
        .then((res) => {
          let response = res.plainData.responseData;
          this.formData.descriptions = response.descriptions;
          this.formData.taskName = response.taskName;
          this.formData.startDate = response.startDate.substring(0, 10);
          this.formData.endDate = response.endDate.substring(0, 10);
          this.formData.startTime = response.startDate.substring(11, 16);
          this.formData.endTime = response.endDate.substring(11, 16);
          this.formData.listPS = response.listPS.map((e) => e.id);

          this.formData.komite.idMKomite = response.idMKomite;
          this.formData.komite.idMWeek = response.idMWeek;
          this.formData.komite.idMMonth = response.idMMonth;
          this.formData.komite.yearPeriod = response.yearPeriod;
          this.formData.komite.userApproval = response.userApproval;
          this.formData.komite.duration = response.duration;

          this.item = response;

          this.getListPenyetujuByKomite(response.idMKomite);
        });
    },
    getTaskRDGB(taskId) {
      client
        .getTaskRDGById({
          store: this.$store,
          data: {
            id: taskId,
          },
        })
        .then((res) => {
          let response = res.plainData.responseData;
          this.formData.descriptions = response.descriptions;
          this.formData.taskName = response.taskName;
          this.formData.startDate = response.startDate.substring(0, 10);
          this.formData.endDate = response.endDate.substring(0, 10);
          this.formData.startTime = response.startDate.substring(11, 16);
          this.formData.endTime = response.endDate.substring(11, 16);
          this.formData.listPS = response.listPS.map((e) => e.id);

          this.formData.komite.idMWeek = response.idMWeek;
          this.formData.komite.idMMonth = response.idMMonth;
          this.formData.komite.yearPeriod = response.yearPeriod;
          this.formData.komite.userApproval = response.userApproval;
          this.formData.komite.duration = response.duration;

          this.formData.rdgm.idDestinationStatement =
            response.idDestinationStatement;

          let satkerPenyaji = response.listSatkerPenyaji ?? [];
          this.formData.rdgm.listSatkerPenyaji = satkerPenyaji.map((e) => e.id);

          let satkerDiundang = response.listSatkerDiundang ?? [];
          this.formData.rdgm.listSatkerDiundang = satkerDiundang.map(
            (e) => e.id
          );

          let adg = response.listAdg ?? [];
          this.formData.rdgm.listMAdg = adg.map((e) => e.id);

          this.item = response;

          this.getListPenyetujuByUsername();
        });
    },
    updateAsesment(data = {}) {
      delete data.asesment;
      delete data.komite;
      delete data.rdgm;
      data = {
        ...data,
        ...this.formData.asesment,
      };

      return client.updateTaskAsesmen({
        store: this.$store,
        data: data,
      });
    },
    updateKomite(data = {}) {
      delete data.asesment;
      delete data.komite;
      delete data.rdgm;

      data = {
        ...data,
        ...this.formData.komite,
      };

      return client.updateTaskKomite({
        store: this.$store,
        data: data,
      });
    },
    updateRDGM(data = {}) {
      delete data.komite.idMKomite;

      data = {
        ...data,
        ...data.asesment,
        ...data.komite,
        ...data.rdgm,
      };

      delete data.asesment;
      delete data.komite;
      delete data.rdgm;

      return client.updateTaskRDG({
        store: this.$store,
        data: data,
      });
    },
    formatYmd(stringDate) {
      const dates = new Date(stringDate);
      const month = dates.getMonth() + 1;
      const year = dates.getFullYear();

      const strDate =
        dates.getDate() < 10 ? "0" + dates.getDate() : dates.getDate();
      const strMonth = month < 10 ? "0" + month : month;

      return year + "-" + strMonth + "-" + strDate;
    },
  },
  computed: {
    isAssesment() {
      return [1, 5].includes(this.formData.idTaskType);
    },
    isKomite() {
      return [2].includes(this.formData.idTaskType);
    },
    isRDGB() {
      return [3, 4].includes(this.formData.idTaskType);
    },
    isSatker() {
      return [5].includes(this.formData.idTaskType);
    },
    startDateTime() {
      let startTime = "00:00";
      let startDate = this.formatYmd(this.formData.startDate);
      if (this.isKomite || this.isRDGB) {
        startTime = this.formData.startTime;
      }
      return addHours(new Date(startDate + "T" + startTime + ":00"), 7);
    },
    endDateTime() {
      let endTime = "00:00";
      let endDate = this.formatYmd(this.formData.endDate);
      if (this.isKomite || this.isRDGB) {
        endTime = this.formData.endTime;
      }
      return addHours(new Date(endDate + "T" + endTime + ":00"), 7);
    },
    duration() {
      if (
        !this.formData.startTime ||
        !this.formData.endTime ||
        !this.formData.startDate ||
        !this.formData.endDate
      )
        return 0;

      let startTime = this.startDateTime;
      let endTime = this.endDateTime;

      let duration = diffMinute(startTime, endTime);
      return duration;
    },
  },
  watch: {
    duration(val) {
      this.formData.komite.duration = val;
    },
  },
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
</style>
