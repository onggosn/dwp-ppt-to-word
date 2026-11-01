<template>
  <v-dialog
    persistent
    v-model="dialog"
    content-class="overflowyhid"
    :max-width="dialogWidth"
  >
    <v-card>
      <v-card-title class="d-flex justify-center align-center pa-4">
        <div class="text-18 text-blueTheme fw-700">Create Assignment</div>
        <v-btn
          class="mr-2"
          style="position: absolute; right: 0"
          variant="text"
          icon="mdi-close"
          @click="hide()"
        ></v-btn>
      </v-card-title>
      <div class="separatorHorizontalGradient"></div>
      <v-card-text class="pb-4 pt-0">
        <v-row v-if="step == 0" class="mt-3">
          <v-col cols="12" class="py-1" v-if="!formData.idAssignmentType">
            <div class="text-15 text-blueTheme fw-600">Assignment</div>
            <v-select
              single-line
              item-title="value"
              item-value="id"
              variant="solo"
              placeholder="Choose Assignment"
              v-model="formData.idAssignmentType"
              :items="list.assignmentTypes"
            >
              <template v-slot:no-data>
                <span
                  class="d-flex align-item-center ma-2 pa-1 select-empty"
                  @click="getAssignmentType()"
                >
                  <!-- <v-icon class="mr-2">mdi-reload</v-icon> -->
                  Data tidak ditemukan
                </span>
              </template>
            </v-select>
          </v-col>
          <template v-else>
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-600">
                Workspace Type <span class="text-redTheme">*</span>
              </div>
              <v-select
                single-line
                item-title="rdgType"
                item-value="idEventSubtypeList"
                variant="solo"
                density="comfortable"
                placeholder="Choose Workspace"
                v-model="formData.idWorkspaceType"
                :items="list.workspaceTypes"
                :error-messages="e(v$.formData.idWorkspaceType)"
              >
                <template v-slot:no-data>
                  <span
                    class="d-flex align-item-center ma-2 pa-1 select-empty"
                    @click="getWorkspaceType()"
                  >
                    <!-- <v-icon class="mr-2">mdi-reload</v-icon> -->
                    Data tidak ditemukan
                  </span>
                </template>
              </v-select>
            </v-col>
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-600">
                Tanggal Pelaksanaan RDG
              </div>
              <VueDatePicker
                auto-apply
                v-model="formData.tanggalPelaksanaan"
                :month-change-on-scroll="false"
                :enable-time-picker="false"
                @update:model-value="getWorkspaceName()"
                :disabled="true"
              >
                <template #trigger>
                  <v-text-field
                    readonly
                    variant="solo"
                    placeholder="DD/MM/YYYY"
                    append-inner-icon="mdi-calendar-today"
                    class="cursor-pointer"
                    @blur="v$.formData.tanggalPelaksanaan.$touch"
                    :error-messages="e(v$.formData.tanggalPelaksanaan)"
                    :value="
                      formData?.tanggalPelaksanaan
                        ? formatTimeEngToIndNoDays(formData.tanggalPelaksanaan)
                        : ''
                    "
                    :disabled="true"
                  ></v-text-field>
                </template>
              </VueDatePicker>
            </v-col>
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-600">
                Workspace Name <span class="text-redTheme">*</span>
              </div>
              <v-autocomplete
                return-object
                single-line
                item-title="event"
                item-value="idEvent"
                variant="solo"
                density="comfortable"
                placeholder="Choose Workspace"
                v-model="formData.idWorkspace"
                :items="list.workspaces"
                :error-messages="e(v$.formData.idWorkspace)"
                :menu-props="{ maxWidth: 200 }"
                :loading="loading[1]"
                @update:model-value="getListAdg($event)"
              >
                <template v-slot:no-data>
                  <span class="d-flex align-item-center ma-2 pa-1 select-empty">
                    <!-- <v-icon class="mr-2">mdi-reload</v-icon> -->
                    Data tidak ditemukan
                  </span>
                </template>
              </v-autocomplete>
            </v-col>
          </template>
        </v-row>
        <v-row v-else-if="step == 1" class="mt-3">
          <v-col
            cols="12"
            class="pb-4"
            v-if="editIdx == null && formData.assignments.length"
          >
            <div class="d-flex justify-end">
              Assignment {{ totalAssignment + 1 }} of {{ totalAssignment + 1 }}
            </div>
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-600">
              Topik Penugasan <span class="text-redTheme">*</span>
            </div>
            <v-text-field
              variant="solo"
              placeholder="Please Input Topik Penugasan"
              v-model="formAssigment.namaPenugasan"
              :error-messages="e(v$.formAssigment.namaPenugasan)"
              :counter="1000"
            ></v-text-field>
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-600">Isi Penugasan</div>
            <v-textarea
              variant="solo"
              placeholder="Please Input Isi Penugasan"
              v-model="formAssigment.deskripsiPenugasan"
              :error-messages="e(v$.formAssigment.deskripsiPenugasan)"
            ></v-textarea>
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-600">
              Tipe Penugasan <span class="text-redTheme">*</span>
            </div>
            <v-select
              single-line
              item-title="TipePenugasan"
              item-value="idTipePenugasan"
              variant="solo"
              density="comfortable"
              placeholder="Please Choose Tipe Penugasan"
              v-model="formAssigment.idTipePenugasan"
              :items="list.typePenugasans"
              :error-messages="e(v$.formAssigment.idTipePenugasan)"
            >
              <template v-slot:no-data>
                <span
                  class="d-flex align-item-center ma-2 pa-1 select-empty"
                  @click="getTypePenugasan()"
                >
                  <!-- <v-icon class="mr-2">mdi-reload</v-icon> -->
                  Data tidak ditemukan
                </span>
              </template>
            </v-select>
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-600">
              Satker Koordinator <span class="text-redTheme">*</span>
            </div>
            <v-autocomplete
              hide-selected
              chips
              multiple
              item-title="value"
              item-value="id"
              variant="solo"
              density="comfortable"
              id="koordinator"
              closable-chips
              placeholder="Please Input Satker Koordinator"
              @update:modelValue="updateKoordinator"
              v-model="formAssigment.listSatkerKoordinator"
              :items="satkerKoordinators"
              :error-messages="e(v$.formAssigment.listSatkerKoordinator)"
            >
              <template v-slot:chip="{ props, item }">
                <!-- Hanya tampilkan badge jika satker TIDAK memiliki isPimpinanAndPICExist = true -->
                <v-badge
                  v-if="!item.raw.isPimpinanAndPICExist"
                  location="top right"
                  color="error"
                  content="!"
                  class="mr-2"
                >
                  <v-chip variant="flat" v-bind="props" class="chip-red">{{
                    item.raw.value
                  }}</v-chip>
                  <v-tooltip
                    activator="parent"
                    location="bottom"
                    content-class="custom-tooltip"
                  >
                    The PIC and the Coordinating Work Unit Head have not been
                    selected. Please select them first
                  </v-tooltip>
                </v-badge>

                <v-chip
                  v-else
                  variant="flat"
                  v-bind="props"
                  class="chip-blue mr-2"
                  >{{ item.raw.value }}</v-chip
                >
              </template>
            </v-autocomplete>
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-600">Satker Pendukung</div>
            <v-autocomplete
              hide-selected
              chips
              closable-chips
              multiple
              item-title="value"
              item-value="id"
              variant="solo"
              density="comfortable"
              id="pendukung"
              @update:modelValue="updatePendukung"
              placeholder="Please Input Satker Pendukung"
              v-model="formAssigment.listSatkerPendukung"
              :items="satkerPendukungs"
              :error-messages="e(v$.formAssigment.listSatkerPendukung)"
            >
              <template v-slot:no-data>
                <span
                  class="d-flex align-item-center ma-2 pa-1 select-empty"
                  @click="getSatker()"
                >
                  <!-- <v-icon class="mr-2">mdi-reload</v-icon> -->
                  Data tidak ditemukan
                </span>
              </template>
            </v-autocomplete>
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-600">Ditugaskan Kepada</div>
            <v-autocomplete
              return-object
              hide-selected
              chips
              closable-chips
              multiple
              item-title="value"
              variant="solo"
              density="comfortable"
              placeholder="Please Input Ditugaskan Kepada"
              id="ditugaskan"
              @update:modelValue="updateDitugaskan"
              v-model="formAssigment.listDitugaskanKepada"
              v-model:search="formAssigment.searchDitugaskanKepada"
              :items="list.ditugaskanKepadas"
              :error-messages="e(v$.formAssigment.listDitugaskanKepada)"
              @update:search="onChangeSearchFilter"
            >
              <template v-slot:no-data>
                <span class="d-flex align-item-center ma-2 pa-1">
                  ketikan nama user atau group
                </span>
              </template>
              <template v-slot:item="{ props, item }">
                <v-list-item v-bind="props" :title="''" class="py-2">
                  <span style="color: #3a416f">{{ item.raw.value }}</span>
                  <br />
                  <span class="text-12 text-grey">{{
                    item.raw.inputEmail
                  }}</span>
                </v-list-item>
              </template>
            </v-autocomplete>
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-600">
              ADG yang Membawahi <span class="text-redTheme">*</span>
            </div>
            <v-autocomplete
              hide-selected
              chips
              closable-chips
              multiple
              item-title="value"
              item-value="id"
              variant="solo"
              density="comfortable"
              placeholder="Please Input Ditugaskan Oleh"
              id="adgbidang"
              @update:modelValue="updateAdgBidang"
              v-model="formAssigment.listADGBidang"
              :items="list.adgBidangs"
              :error-messages="e(v$.formAssigment.listADGBidang)"
            >
              <template v-slot:no-data>
                <span class="d-flex align-item-center ma-2 pa-1 select-empty">
                  Data tidak ditemukan
                </span>
              </template>
            </v-autocomplete>
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-600">Batas Waktu</div>
            <VueDatePicker
              auto-apply
              v-model="formAssigment.batasWaktu"
              :month-change-on-scroll="false"
              :enable-time-picker="false"
              :disabled="isArahan"
              :class="isArahan ? 'disabled-input' : ''"
            >
              <template #trigger>
                <v-text-field
                  readonly
                  variant="solo"
                  placeholder="DD/MM/YYYY"
                  append-inner-icon="mdi-calendar-today"
                  class="cursor-pointer"
                  @blur="v$.formAssigment.batasWaktu.$touch"
                  :error-messages="e(v$.formAssigment.batasWaktu)"
                  :value="
                    formAssigment?.batasWaktu
                      ? formatTimeEngToIndNoDays(formAssigment?.batasWaktu)
                      : ''
                  "
                ></v-text-field>
              </template>
            </VueDatePicker>
          </v-col>
          <v-col cols="12" class="py-1">
            <div class="text-15 text-blueTheme fw-600">Periode Reminder</div>
            <v-select
              single-line
              item-title="periode"
              item-value="id"
              variant="solo"
              density="comfortable"
              placeholder="Choose Periode"
              id="periode"
              @update:modelValue="updatePeriode"
              v-model="formAssigment.periodeReminder"
              :items="list.periodes"
              :disabled="isArahan"
              :error-messages="
                e(v$.formAssigment.periodeReminder, {
                  moreThan: 'Opps!, periode tidak boleh melebihi batas waktu',
                })
              "
            >
              <template v-slot:no-data>
                <span
                  class="d-flex align-item-center ma-2 pa-1 select-empty"
                  @click="getPeriodeReminder()"
                >
                  <!-- <v-icon class="mr-2">mdi-reload</v-icon> -->
                  Data tidak ditemukan
                </span>
              </template>
            </v-select>
          </v-col>
          <v-col cols="12" class="py-1" v-if="editIdx == null">
            <v-btn class="btn-action btn-action-create" @click="addMore()">
              + Add More Assignment
            </v-btn>
          </v-col>
        </v-row>
        <v-row v-else-if="step == 2" class="mt-3">
          <v-col cols="12">
            <v-table
              fixed-header
              class="tableAssignment pb-3"
              density="comfortable"
            >
              <thead>
                <tr>
                  <th width="60%" class="text-center txt-header">
                    Assignment Name
                  </th>
                  <th width="20%" class="text-center txt-header">Type</th>
                  <th width="20%" class="text-center txt-header">Action</th>
                </tr>
              </thead>
              <tbody>
                <template v-if="totalAssignment">
                  <tr v-for="(item, idx) in formData.assignments" :key="idx">
                    <td class="text-row">
                      {{ serializedAssignmentName(item.namaPenugasan) }}
                    </td>
                    <td class="text-row">
                      {{ getTypePenugasanName(item.idTipePenugasan) }}
                    </td>
                    <td class="text-center">
                      <v-btn
                        class="rounded-lg mx-1"
                        size="x-small"
                        icon="mdi-pencil"
                        color="#065695"
                        variant="outlined"
                        @click="editMore(idx)"
                      >
                        <v-icon> mdi-pencil</v-icon>
                        <v-tooltip activator="parent" location="top"
                          >Edit Assignment</v-tooltip
                        >
                      </v-btn>
                      <v-btn
                        class="rounded-lg mx-1"
                        size="x-small"
                        icon="mdi-delete-forever"
                        color="#065695"
                        variant="outlined"
                        @click="deleteMore(idx)"
                      >
                        <v-icon> mdi-delete-forever</v-icon>
                        <v-tooltip activator="parent" location="top"
                          >Delete Assignment</v-tooltip
                        >
                      </v-btn>
                    </td>
                  </tr>
                </template>
                <tr v-else>
                  <td colspan="3" class="text-center text-15">
                    Data Assignment Belum Ada
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions
        class="justify-end pr-6 pt-3 pb-4"
        v-if="formData.idAssignmentType"
      >
        <v-btn class="btn-action btn-action-close" @click="hide()">
          Cancel
        </v-btn>
        <v-btn
          v-if="step == 2"
          class="btn-action btn-action-create"
          @click="process()"
          :loading="loading[0]"
          :disabled="disabled"
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

<script setup lang="ts">
import {
  ref,
  reactive,
  computed,
  watch,
  onMounted,
  getCurrentInstance,
} from "vue";
import { useStore } from "vuex";
import useVuelidate from "@vuelidate/core";
import { required, maxLength, helpers } from "@vuelidate/validators";
import { getErrorMessages } from "@/library/ValidationHelper";
import { dateDiff } from "@/helpers/date";
import { convertDate } from "@v2/helpers/DateHelper";
import client from "@/library/ApiClient";
import { uniqueOptions } from "@/helpers/utils";
// const alphaNumCustom = helpers.regex(/^[a-zA-Z0-9\-_()\s]+$/i);
import { formatTimeEngToIndNoDays } from "@/helpers/date";
import { debounce } from "lodash";
import clientv2 from "@v2/library/ApiClient";
const emit = defineEmits(["afterInsert"]);

const store = useStore();
const { root } = getCurrentInstance() as any;

// Custom validator untuk satker koordinator
const satkerKoordinatorValid = helpers.withMessage(
  "Satker koordinator yang dipilih harus memiliki Pimpinan dan PIC",
  (value: number[]) => {
    if (!value || value.length === 0) return true; // Let required handle empty validation

    // Check if all selected satker have isPimpinanAndPICExist = true
    return value.every((selectedId: number) => {
      const satker = list.satkers.find((item: any) => item.id === selectedId);
      return satker?.isPimpinanAndPICExist === true;
    });
  }
);

const dialog = ref(false);
const loading = reactive([false, false]);
const step = ref(0);
const editIdx = ref<number | null>(null);

const formData = reactive({
  idAssignmentType: null as number | null,
  idWorkspaceType: null as number | null,
  documentDate: null as string | null,
  tanggalPelaksanaan: null as string | null,
  idWorkspace: null as number | null,
  assignments: [] as Array<any>,
});

const formAssigment = reactive({
  namaPenugasan: null as string | null,
  deskripsiPenugasan: null as string | null,
  idTipePenugasan: null as number | null,
  listSatkerKoordinator: [] as number[],
  listSatkerPendukung: [] as number[],
  listDitugaskanKepada: [] as any[],
  listADGBidang: [] as number[],
  batasWaktu: null as string | null,
  periodeReminder: null as number | null,
  searchDitugaskanKepada: undefined as string | undefined,
});

const list = reactive({
  assignmentTypes: [] as any[],
  workspaceTypes: [] as any[],
  workspaces: [] as any[],
  tasks: [] as any[],
  typePenugasans: [] as any[],
  satkers: [] as any[],
  ditugaskanKepadas: [] as any[],
  adgBidangs: [] as any[],
  periodes: [] as any[],
});

const isArahan = computed(() => {
  return (
    (formAssigment.idTipePenugasan && formAssigment.idTipePenugasan != 1) ||
    false
  );
});

const disabled = computed(() => {
  return loading[0] || !formData.assignments.length;
});

const rules = computed(() => {
  let formDataRules: any = {
    idAssignmentType: { required },
    idWorkspaceType: { required },
    tanggalPelaksanaan: {},
    idWorkspace: { required },
  };

  if (![1, 2, 3, 4].includes(formData.idWorkspaceType as number)) {
    formDataRules.tanggalPelaksanaan = { required };
  }

  let formAss: any = {
    namaPenugasan: {},
    deskripsiPenugasan: {},
    idTipePenugasan: {},
    listSatkerKoordinator: {},
    listSatkerPendukung: {},
    listDitugaskanKepada: {},
    listADGBidang: {},
    batasWaktu: {},
    periodeReminder: {},
  };

  if (step.value == 1) {
    formAss = {
      namaPenugasan: { required, maxLength: maxLength(1000) },
      // Add custom validation for satker koordinator
      listSatkerKoordinator: {
        required,
        satkerKoordinatorValid,
      },
      listADGBidang: { required },
      batasWaktu: {},
      periodeReminder: {},
    };

    if (!isArahan.value) {
      formAss.batasWaktu = { required };
      formAss.periodeReminder = {
        required,
        moreThan: (val: any, vm: any) => {
          let periode = list.periodes.find((e) => e.id == val);
          if (periode && vm.batasWaktu) {
            let date = new Date(vm.batasWaktu);
            let now = new Date();
            [now, date].forEach((d) => d.setHours(0, 0, 0, 0));
            return parseInt(periode.periode) <= dateDiff(now, date);
          }
          return true;
        },
      };
    }
  }

  return { formData: formDataRules, formAssigment: formAss };
});

const v$ = useVuelidate(rules, { formData, formAssigment });

const e = getErrorMessages;

const serializedAssignmentName = (name: string) => {
  if (formData.documentDate) return `${formData.documentDate}_${name}`;
};

const updateKoordinator = () => {
  document.getElementById("koordinator")?.blur();

  // Trigger validation setelah update
  setTimeout(() => {
    v$.value.formAssigment.listSatkerKoordinator.$touch();
  }, 100);
};

const updatePendukung = () => document.getElementById("pendukung")?.blur();
const updateDitugaskan = () => document.getElementById("ditugaskan")?.blur();
const updateAdgBidang = () => document.getElementById("adgbidang")?.blur();
const updatePeriode = () => document.getElementById("periode")?.blur();

const hide = () => {
  dialog.value = false;
  resetForm("all");
  localStorage.setItem(keyCache.value, "");
};

const next = () => {
  v$.value.$validate().then((res: boolean) => {
    if (res) {
      if (step.value == 1) addMore();
      ++step.value;
    } else {
      // Show specific error for invalid satker koordinator
      if (v$.value.formAssigment.listSatkerKoordinator.$error) {
        const invalidSatkers = formAssigment.listSatkerKoordinator
          .filter((selectedId) => {
            const satker = list.satkers.find(
              (item: any) => item.id === selectedId
            );
            return satker?.isPimpinanAndPICExist === false;
          })
          .map((selectedId) => {
            const satker = list.satkers.find(
              (item: any) => item.id === selectedId
            );
            return satker?.value || "Unknown";
          });

        if (invalidSatkers.length > 0) {
          root.refs.toast.show({
            message: `Satker ${invalidSatkers.join(
              ", "
            )} belum memiliki Pimpinan dan PIC. Silakan pilih satker lain.`,
            color: "warning",
            timeout: 5000,
          });
        }
      }
    }
  });
};

const resetForm = (tag = "other") => {
  if (tag == "all") {
    step.value = 0;
    formData.idAssignmentType = null;
    formData.idWorkspaceType = null;
    formData.tanggalPelaksanaan = null;
    formData.idWorkspace = null;
    formData.assignments = [];
  }

  formAssigment.namaPenugasan = null;
  formAssigment.deskripsiPenugasan = null;
  formAssigment.idTipePenugasan = null;
  formAssigment.listSatkerKoordinator = [];
  formAssigment.listSatkerPendukung = [];
  formAssigment.listDitugaskanKepada = [];
  formAssigment.listADGBidang = [];
  formAssigment.batasWaktu = null;
  formAssigment.periodeReminder = null;

  v$.value.$reset();
};

// Enhanced addMore dengan validasi tambahan
const addMore = () => {
  v$.value.$validate().then((res: boolean) => {
    if (res) {
      if (editIdx.value === null) {
        formData.assignments.push({ ...formAssigment });
      } else {
        formData.assignments[editIdx.value] = { ...formAssigment };
      }
      editIdx.value = null;
      resetForm();
      localStorage.setItem(keyCache.value, JSON.stringify(formData));
    } else {
      // Show validation error for satker koordinator
      if (v$.value.formAssigment.listSatkerKoordinator.$error) {
        root.refs.toast.show({
          message:
            "Tidak dapat menambah assignment. Pastikan semua satker koordinator memiliki Pimpinan dan PIC.",
          color: "error",
          timeout: 5000,
        });
      }
    }
  });
};

const editMore = (idx: number) => {
  editIdx.value = idx;
  Object.assign(formAssigment, formData.assignments[idx] ?? {});
  step.value = 1;
};

const deleteMore = (idx: number) => formData.assignments.splice(idx, 1);

// Enhanced process dengan final validation
const process = () => {
  // Final check untuk semua assignments
  const hasInvalidSatkers = formData.assignments.some((assignment: any) => {
    return assignment.listSatkerKoordinator.some((selectedId: number) => {
      const satker = list.satkers.find((item: any) => item.id === selectedId);
      return satker?.isPimpinanAndPICExist === false;
    });
  });

  if (hasInvalidSatkers) {
    root.refs.toast.show({
      message:
        "Tidak dapat membuat assignment. Ada satker koordinator yang belum memiliki Pimpinan dan PIC.",
      color: "error",
      timeout: 5000,
    });
    return;
  }

  loading[0] = true;
  const {
    idWorkspace: { idEvent },
    idWorkspaceType: idEventSubtypeList,
  } = formData as any;

  let requestData = formData.assignments.map((el: any) => ({
    ...el,
    ...formData,
  }));
  requestData = requestData.map((el: any) => {
    delete el.assignments;
    delete el.idWorkspace;
    delete el.idWorkspaceType;
    let assignmentName = el.namaPenugasan;
    let description = el.deskripsiPenugasan;
    delete el.namaPenugasan;
    delete el.deskripsiPenugasan;

    el.listDitugaskanKepada?.map((elm: any) => {
      delete elm.id;
      delete elm.title;
      return elm;
    });

    return {
      ...el,
      assignmentName,
      description,
      idEvent,
      idEventSubtypeList,
      idAssignmentType: formData.idAssignmentType,
    };
  });

  client
    .insertAssignmentNew({ store, data: requestData })
    .then((res: any) => {
      const { responseCode, responseMessage } = res.plainData;

      if (responseCode == "011000") {
        root.refs.toast.show({
          message: "Successfully Create",
          color: "success",
          timeout: 3000,
        });
        emit("afterInsert");
      } else {
        root.toast.show({ message: responseMessage, color: "warning" });
      }
    })
    .catch(() => {
      root.toast.show({
        message: "internal server error",
        color: "warning",
      });
    })
    .finally(() => {
      loading[0] = false;
      dialog.value = false;
    });

  localStorage.setItem(keyCache.value, "");
};

// Watch untuk auto-clear validation ketika satker valid dipilih
watch(
  () => formAssigment.listSatkerKoordinator,
  (newValue) => {
    // Check if all selected satkers are now valid
    const allValid = newValue.every((selectedId) => {
      const satker = list.satkers.find((item: any) => item.id === selectedId);
      return satker?.isPimpinanAndPICExist === true;
    });

    // Clear validation error if all satkers are now valid
    if (allValid && v$.value.formAssigment.listSatkerKoordinator.$error) {
      setTimeout(() => {
        v$.value.formAssigment.listSatkerKoordinator.$reset();
      }, 100);
    }
  },
  { deep: true }
);

const getTypePenugasanName = (id: number) =>
  list.typePenugasans.find((e) => e.idTipePenugasan == id)?.TipePenugasan;
const getAssignmentType = () =>
  client
    .getAssignmentType({ store })
    .then((res: any) => (list.assignmentTypes = res.plainData.responseData));
const getPeriodeReminder = () =>
  client
    .getAssignmentReminderPeriode({ store })
    .then((res: any) => (list.periodes = res.plainData.responseData));
const getSatker = () =>
  client.MSatkerPembuat({ store }).then((res: any) => {
    list.satkers = res.plainData.responseData;
  });
const getWorkspaceType = () =>
  client
    .getWorkspaceTypesNew({ store })
    .then((res: any) => (list.workspaceTypes = res.plainData.responseData));

const getWorkspaceName = () => {
  const { idWorkspaceType } = formData as any;
  if (
    [1, 2, 3, 4, 6].includes(idWorkspaceType) ||
    (idWorkspaceType && formData.tanggalPelaksanaan)
  ) {
    loading[1] = true;
    const requestData = { idSubTypeList: idWorkspaceType };
    formData.idWorkspace = null;
    client
      .getWorkspaceNameNew({ store, data: requestData })
      .then((res: any) => (list.workspaces = res.plainData.responseData))
      .finally(() => {
        loading[1] = false;
      });
  }
};

const getTypePenugasan = () => {
  const { idAssignmentType } = formData as any;
  client
    .getTipePenugasanByAssignmentType({ store, data: { idAssignmentType } })
    .then((res: any) => (list.typePenugasans = res.plainData.responseData));
};

const getDocumentDate = () => {
  const data = { idEvent: (formData.idWorkspace as any).idEvent };
  client.getPreviewDocumentDate({ store, data }).then((res: any) => {
    const { responseData } = res.plainData;
    const { tglRDG, tglRDGH2 } = responseData;
    formData.documentDate = tglRDGH2;
    formData.tanggalPelaksanaan = convertDate(tglRDG) as unknown as string;
  });
};

const getListAdg = (data) => {
  list.adgBidangs = data.listADG.map((item: any) => ({
    id: item.id,
    value: item.displayName,
  }));
};

const onChangeSearchFilter = debounce((val: string) => {
  if (val) {
    const trimmedSearch = val
      .replace(/"/g, "")
      .split(";")
      .map((part) => {
        if (part.trim() === "") return; // Skip empty parts
        const regex = /<[^>]*@[^>]*>/;
        const matchingMail = part.match(regex);
        if (matchingMail !== null) {
          return matchingMail[0].slice(1, -1);
        } else {
          return part.trim();
        }
      })
      .filter((v): v is string => !!v);

    const reqData = {
      name: trimmedSearch,
      isEvent: false, // mengikuti parameter di edit Event (?)
    };
    clientv2.SearchUserAndGroupNew({ data: reqData }).then((res: any) => {
      if (Array.isArray(res) && res.length > 0) {
        const taskMember = [
          ...res.map((item: any) => {
            item.groupName = item.isGroup ? item.value : null;
            return item;
          }),
        ];
        list.ditugaskanKepadas = taskMember;
        val.includes(";") && (formAssigment.listDitugaskanKepada = taskMember);
        val.includes(";") && (formAssigment.searchDitugaskanKepada = ""); // Clear the search input after getting results
      }
    });
  } else {
    list.ditugaskanKepadas = [];
  }
}, 300);

const dialogWidth = computed(() => (formData.idAssignmentType ? "800" : "600"));
const keyCache = computed(() => store.state.username + "_form_assignment");
const totalAssignment = computed(() => formData.assignments.length);
const satkerKoordinators = computed(() =>
  uniqueOptions(list.satkers, formAssigment.listSatkerPendukung)
);
const satkerPendukungs = computed(() =>
  uniqueOptions(list.satkers, formAssigment.listSatkerKoordinator)
);

watch(
  () => formData.idWorkspaceType,
  () => {
    if (formData.idWorkspaceType) {
      getTypePenugasan();
      getWorkspaceName();
    }
  }
);

watch(
  () => formData.idWorkspace,
  () => {
    if (formData.idWorkspace) getDocumentDate();
  }
);

watch(
  () => isArahan.value,
  (val: any) => {
    if (val) {
      formAssigment.periodeReminder = null;
      formAssigment.batasWaktu = null;
    }
  }
);

const show = () => {
  dialog.value = true;
  resetForm("all");
};

defineExpose({
  show,
});

const load = () => {
  getAssignmentType();
  getSatker();
  getWorkspaceType();
  getPeriodeReminder();
};

onMounted(() => {
  load();
});
</script>

<style scoped lang="scss">
:deep(.custom-tooltip) {
  background-color: #ffffff !important;
  color: rgb(10, 10, 10) !important;
  opacity: 1 !important;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
}
.table {
  width: 100%;
}

.table tr {
  line-height: 20px;
  height: 20px;
}

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

.select-empty {
  cursor: pointer;
}

:deep(
    .v-timeline--horizontal.v-timeline
      .v-timeline-item:nth-child(2n + 1)
      .v-timeline-item__opposite
  ) {
  padding-top: 10px;
}

:deep(
    .v-timeline--horizontal.v-timeline
      .v-timeline-item:nth-child(2n)
      .v-timeline-item__body
  ) {
  padding-top: 10px;
}
:deep(.cursor-pointer input) {
  cursor: pointer !important;
}

:deep(.arahan .v-field__outline) {
  background-color: #dfdfdf;
}

.tableAssignment {
  background: rgba(247, 251, 254, 1) !important;
  border-radius: 15px;
  border: none !important;
}
.tableAssignment thead th {
  background: rgba(247, 251, 254, 1) !important;
  border: none !important;
}
.txt-header {
  font-weight: bold !important;
  font-size: 15px !important;
  color: rgba(58, 65, 111, 1) !important;
}
.text-row {
  /* font-weight: bold !important; */
  font-size: 15px !important;
}

:deep(.v-theme--light) {
  --v-border-color: none !important;
}
:deep(.v-chip.v-chip--size-small) {
  --v-chip-size: 0.75rem;
  --v-chip-height: 30px;
  font-size: 0.8rem;
  padding: 0 10px;
  background: rgba(38, 125, 194, 1) !important;
  color: white;
}
:deep(.v-field--disabled) {
  background-color: rgb(168 160 160) !important;
}
.disabled-input {
  :deep(.v-field--variant-solo) {
    background-color: rgb(222 219 219 / 80%) !important;
  }
}
:deep(.v-chip.v-chip--density-default) {
  height: calc(var(--v-chip-height) + 0px);
  border-radius: 5px;
  background: #e9f5ff !important;
  border: 1px solid #6eb3ea;
  color: #065391;
  padding: 10px;
  margin-right: 5px;
  margin-bottom: 5px;
}
:deep(.bg-error) {
  background-color: #ffebe9 !important;
  border: 1px solid #d6212a;
  color: #d6212a !important;
}

.chip-red {
  background-color: #ffebe9 !important;
  border: 1px solid #d6212a !important;
  color: #d6212a !important;
}

.chip-blue {
  background-color: #e3f2fd !important;
  border: 1px solid #1976d2 !important;
  color: #1976d2 !important;
}

:deep(.v-field .v-chip.chip-blue) {
  background-color: #e3f2fd !important;
  color: #1976d2 !important;
}

:deep(.v-field .v-chip.chip-red) {
  background-color: #ffebe9 !important;
  color: #d6212a !important;
}
</style>
