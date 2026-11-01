<template>
  <v-dialog
    persistent
    v-model="dialog"
    content-class="overflowyhid"
    :max-width="1200"
  >
    <v-card>
      <v-card-title class="d-flex justify-center align-center">
        <div class="text-18 text-blueTheme fw-500">Add Task</div>
        <v-btn
          class="mr-2"
          style="position: absolute; right: 0"
          variant="text"
          icon="mdi-close"
          @click="hide()"
        ></v-btn>
      </v-card-title>
      <v-sheet
        elevation="0"
        class="d-block separatorHorizontal"
        style="cursor: none"
      />
      <v-sheet
        style="align-self: center; margin-top: 0px"
        v-if="stepNumber == 2"
      >
        <v-timeline direction="horizontal" style="width: 30vw">
          <v-timeline-item
            icon-color="white"
            icon="mdi-check"
            dot-color="#065695"
            size="small"
          >
            <template v-slot:opposite>
              <div>Step 1</div>
            </template>
          </v-timeline-item>
          <v-timeline-item
            icon-color="white"
            icon="mdi-check"
            dot-color="#065695"
            size="small"
          >
            <template v-slot:opposite> </template>
            <div>Step 2</div>
          </v-timeline-item>
        </v-timeline>
      </v-sheet>
      <v-card-text class="pt-0 pb-4">
        <v-row class="my-1">
          <template v-if="stepNumber == 1">
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-500 mb-1">
                Task Name<span class="text-redTheme">*</span>
              </div>
              <v-text-field
                variant="solo"
                style="font-size: 15px"
                placeholder="Masukan Nama Task"
                v-model="formData.taskName"
                :error-messages="e(v$.formData.taskName)"
                :hide-details="isError(v$.formData.taskName)"
              />
            </v-col>
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-500 mb-1">
                Task Description
              </div>
              <v-textarea
                variant="solo"
                rows="3"
                row-height="5"
                placeholder="Masukan Deskripsi Task"
                v-model="formData.descriptions"
                :error-messages="e(v$.formData.descriptions)"
                :hide-details="isError(v$.formData.descriptions)"
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
                <v-col
                  cols="12"
                  class="pt-0"
                  v-if="!isError(v$.formData.listPS)"
                >
                  <span class="text-danger ps-3" style="font-size: 12px">
                    {{ e(v$.formData.listPS).toString() }}
                  </span>
                </v-col>
              </v-row>
            </v-col>
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-500">
                Task Type<span class="text-redTheme">*</span>
              </div>
              <div>
                <v-select
                  variant="solo"
                  item-title="value"
                  item-value="id"
                  placeholder="Pilih Tipe Task"
                  v-model="formData.idTaskType"
                  :items="list.tt"
                  :error-messages="e(v$.formData.idTaskType)"
                  :hide-details="isError(v$.formData.idTaskType)"
                  @update:modelValue="getPenyetujuByTaskType()"
                />
              </div>
            </v-col>
            <template v-if="isAssesment">
              <v-col cols="12">
                <div class="text-15 text-blueTheme fw-500">
                  Satker <span class="text-redTheme">*</span>
                </div>
                <div>
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
                </div>
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
                            $filters.formatTimeEngToIndNoDays(
                              formData.startDate
                            )
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
          </template>
          <template v-else-if="stepNumber == 2 && (isKomite || isRDGB)">
            <v-col cols="12" v-if="isKomite">
              <div class="text-15 text-blueTheme fw-500">
                Komite <span class="text-redTheme">*</span>
                <v-select
                  variant="solo"
                  item-title="value"
                  item-value="id"
                  placeholder="Pilih Komite"
                  v-model="formData.komite.idMKomite"
                  :items="list.komites"
                  :error-messages="e(v$.formData.komite.idMKomite)"
                  :hide-details="isError(v$.formData.komite.idMKomite)"
                  @update:modelValue="getListPenyetujuByKomite()"
                />
              </div>
            </v-col>
            <v-col cols="12" v-if="isRDGB">
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
                </div>
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
                  <v-col
                    cols="12"
                    class="pt-0"
                    v-if="!isError(v$.formData.rdgm.listMAdg)"
                  >
                    <span class="text-danger ps-3" style="font-size: 12px">
                      {{ e(v$.formData.rdgm.listMAdg).toString() }}
                    </span>
                  </v-col>
                </v-row>
              </v-col>
            </template>
            <v-col cols="12">
              <div class="text-15 text-blueTheme fw-500">
                Penyetuju <span class="text-redTheme">*</span>
                <v-select
                  variant="solo"
                  item-title="name"
                  item-value="value"
                  placeholder="Pilih Penyetuju"
                  v-model="formData.komite.userApproval"
                  :items="list.penyetujus"
                  :error-messages="e(v$.formData.komite.userApproval)"
                  :hide-details="isError(v$.formData.komite.userApproval)"
                />
              </div>
            </v-col>
          </template>
          <template v-else-if="this.formData.idTaskType">
            <v-col class="text-center text-24"> In Development </v-col>
          </template>
        </v-row>
      </v-card-text>
      <v-card-actions class="justify-end pr-6 pt-0 pb-4">
        <v-btn
          v-if="stepNumber == 1"
          class="btn-action btn-action-close"
          @click="hide()"
        >
          Cancel
        </v-btn>
        <v-btn v-else class="btn-action btn-action-close" @click="previews()">
          Back
        </v-btn>
        <v-btn
          v-if="stepNumber == 2 || (stepNumber == 1 && isAssesment)"
          class="btn-action btn-action-create"
          @click="process()"
          :loading="loading[1]"
          :disabled="loading[1]"
        >
          Create
        </v-btn>
        <v-btn v-else class="btn-action btn-action-create" @click="next()">
          Next
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
  name: "addTaskDialog",
  components: {
    SelectMemberComponent,
  },
  props: {
    satkerId: null,
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

    if (this.stepNumber == 1 && this.isAssesment) {
      delete formData.startTime;
      delete formData.endTime;

      formData = {
        ...formData,
        asesment: asesment,
      };
    } else if (this.stepNumber == 2 && this.isKomite) {
      formData = {
        ...formData,
        komite: komite,
      };
    } else if (this.stepNumber == 2 && this.isRDGB) {
      delete komite.idMKomite;
      formData = {
        ...formData,
        asesment: asesment,
        komite: komite,
        rdgm: rdgm,
      };
    } else {
      formData.startDate = {};
      formData.endDate = {};
      formData.startTime = {};
      formData.endTime = {};
    }

    return { formData };
  },
  data() {
    return {
      dialog: false,
      loading: [],
      stepNumber: 1,
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
          idDestinationStatement: null,
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
    resetForm(tag = "all") {
      if (tag == "all") {
        this.formData.listPS = [];
        this.formData.idTaskType = null;
        this.formData.descriptions = null;
        this.formData.taskName = null;
      }

      this.formData.startDate = null;
      this.formData.endDate = null;
      this.formData.startTime = null;
      this.formData.endTime = null;

      this.formData.asesment = {
        idMSatker: null,
      };

      this.formData.komite = {
        idMKomite: null,
        idMWeek: null,
        idMMonth: null,
        yearPeriod: null,
        duration: 0,
        userApproval: null,
      };

      this.formData.rdgm = {
        idDestinationStatement: null,
        listSatkerPenyaji: [],
        listSatkerDiundang: [],
        listMAdg: [],
      };
    },
    show(item) {
      this.item = item;
      this.dialog = true;
      this.v$.$reset();
      this.resetForm();
      this.getTaskTypeByActivity(item.idActivityType);
    },
    hide() {
      this.dialog = false;
    },
    next() {
      this.v$.$validate().then((res) => {
        if (res) {
          this.v$.$reset();
          this.resetForm("next");
          this.stepNumber = 2;
        } else {
          this.stepNumber = 1;
          return 0;
        }
      });
    },
    previews() {
      this.v$.$reset();
      this.formData.idTaskType = null;
      this.stepNumber = 1;
    },
    process() {
      this.v$.$validate().then((res) => {
        if (res) {
          this.loading[1] = true;
          let data = {
            ...this.formData,
            startDate: this.startDateTime,
            endDate: this.endDateTime,
            idActivity: this.item.id,
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
            doAction = this.insertAsesment(data);
          } else if (this.isKomite) {
            doAction = this.insertKomite(data);
          } else if (this.isRDGB) {
            doAction = this.insertRDGM(data);
          }

          doAction
            .then((res) => {
              if (res.plainData.responseCode == "011000") {
                let msg =
                  "Successfully Submit <br /> Please wait for task approval";
                if (this.isAssesment) msg = "Successfully Created";
                this.$root.toast.show({
                  message: msg,
                  color: "success",
                  timeout: 3000,
                });
              } else {
                this.$root.toast.show({
                  message: res.plainData.responseMessage,
                  color: "error",
                  timeout: 3000,
                });
              }
              this.$emit("submit");
            })
            .finally(() => {
              this.loading[1] = false;
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
    getListPenyetujuByKomite() {
      let komiteId = this.formData.komite.idMKomite;
      client
        .getListPegawaiByKomite({ store: this.$store, data: { id: komiteId } })
        .then((res) => {
          this.list.penyetujus = res.plainData.responseData;
        });
    },
    getPenyetujuByTaskType() {
      if (this.isRDGB) {
        client.getListPegawaiByIdRole({ store: this.$store }).then((res) => {
          this.list.penyetujus = res.plainData.responseData;
        });
      } else {
        this.list.penyetujus = [];
      }
    },
    insertAsesment(data = {}) {
      delete data.asesment;
      delete data.komite;
      delete data.rdgm;

      data = {
        ...data,
        ...this.formData.asesment,
      };

      return client.postTaskAsesmen({
        store: this.$store,
        data: data,
      });
    },
    insertKomite(data = {}) {
      delete data.asesment;
      delete data.komite;
      delete data.rdgm;

      data = {
        ...data,
        ...this.formData.komite,
      };

      return client.postTaskKomite({
        store: this.$store,
        data: data,
      });
    },
    insertRDGM(data = {}) {
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

      return client.postTaskRDG({
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
      return (
        this.formData.idTaskType && [1, 5].includes(this.formData.idTaskType)
      );
    },
    isKomite() {
      return this.formData.idTaskType && [2].includes(this.formData.idTaskType);
    },
    isRDGB() {
      return (
        this.formData.idTaskType && [3, 4].includes(this.formData.idTaskType)
      );
    },
    isSatker() {
      return this.formData.idTaskType && [5].includes(this.formData.idTaskType);
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
    "formData.idTaskType": {
      handler(val) {
        if ([2, 3, 4].includes(val)) {
          this.next();
        } else {
          if (val == 5) {
            this.formData.asesment.idMSatker = this.satkerId;
          }
          this.stepNumber = 1;
        }
      },
    },
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
.separatorHorizontal {
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
  height: 1.2px;
  width: 100%;
}
.blueText {
  color: #3a416f;
}

:deep(
    .v-timeline--horizontal.v-timeline
      .v-timeline-item:nth-child(2n + 1)
      .v-timeline-item__opposite
  ) {
  padding-top: 5px;
}

/* :deep(
    .v-timeline--horizontal.v-timeline
      .v-timeline-item:nth-child(2n)
      .v-timeline-item__body
  ) {
  padding-top: 5px;
}

:deep(.cursor-pointer input) {
  cursor: pointer !important;
} */
:deep(.v-timeline-item__body) {
  padding: 0 !important;
}

:deep(.v-timeline-item__opposite) {
  padding: 0 !important;
}

:deep(
    .v-timeline--horizontal.v-timeline
      .v-timeline-item:first-child
      .v-timeline-divider
  ) {
  padding-inline-start: 0 !important;
}

:deep(.v-overlay__content.v-select__content) {
  position: fixed;

  --v-overlay-anchor-origin: bottom left;

  transform-origin: left top;
}
:deep(
    .v-timeline--horizontal.v-timeline
      .v-timeline-item:last-child
      .v-timeline-divider
  ) {
  padding-inline-end: 0 !important;
}
.v-timeline--align-center {
  --v-timeline-line-size-base: 100%;
  --v-timeline-line-size-offset: 0px;
}
</style>
