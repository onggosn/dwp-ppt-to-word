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
                item-title="workspaceTypeName"
                item-value="id"
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
                @update:model-value="getWorkspaceAndTask()"
                :disabled="formData.idWorkspaceType != 6"
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
                      $filters.formatTimeEngToIndNoDays(
                        formData.tanggalPelaksanaan
                      )
                    "
                    :disabled="formData.idWorkspaceType != 6"
                  ></v-text-field>
                </template>
              </VueDatePicker>
            </v-col>
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-600">
                Workspace Name <span class="text-redTheme">*</span>
              </div>
              <v-autocomplete
                single-line
                item-title="value"
                item-value="id"
                variant="solo"
                density="comfortable"
                placeholder="Choose Workspace"
                v-model="formData.idWorkspace"
                :items="list.workspaces"
                :error-messages="e(v$.formData.idWorkspace)"
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
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-600">
                Task Name <span class="text-redTheme">*</span>
              </div>
              <v-autocomplete
                single-line
                item-title="value"
                item-value="id"
                variant="solo"
                density="comfortable"
                placeholder="Choose Task"
                v-model="formData.idTask"
                :items="taskWorkspace"
                :error-messages="e(v$.formData.idTask)"
                :loading="loading[1]"
              >
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
              closable-chips
              multiple
              item-title="value"
              item-value="id"
              variant="solo"
              density="comfortable"
              id="koordinator"
              placeholder="Please Input Satker Koordinator"
              @update:modelValue="updateKoordinator"
              v-model="formAssigment.listSatkerKoordinator"
              :items="satkerKoordinators"
              :error-messages="e(v$.formAssigment.listSatkerKoordinator)"
            />
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
              item-title="title"
              item-value="id"
              variant="solo"
              density="comfortable"
              placeholder="Please Input Ditugaskan Kepada"
              id="ditugaskan"
              @update:modelValue="updateDitugaskan"
              v-model="formAssigment.listDitugaskanKepada"
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
                  <span style="color: #3a416f">{{ item.raw.title }}</span>
                  <br />
                  <span class="text-12 text-grey">{{ item.raw.email }}</span>
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
                <span
                  class="d-flex align-item-center ma-2 pa-1 select-empty"
                  @click="getListAdgs()"
                >
                  <!-- <v-icon class="mr-2">mdi-reload</v-icon> -->
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
                    $filters.formatTimeEngToIndNoDays(formAssigment.batasWaktu)
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
                    <td class="text-row">{{ item.namaPenugasan }}</td>
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
          :disabled="loading[0]"
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
import { required, maxLength } from "@vuelidate/validators";
import { getErrorMessages } from "@/library/ValidationHelper";
import { formatTimeYmd, dateDiff } from "@/helpers/date";
import client from "@/library/ApiClient";
// const alphaNumCustom = helpers.regex(/^[a-zA-Z0-9\-_()\s]+$/i);

export default {
  name: "createAssignment",
  emits: ["afterInsert"],
  setup: () => ({ v$: useVuelidate() }),
  validations() {
    let formData = {
      idAssignmentType: { required },
      idWorkspaceType: { required },
      tanggalPelaksanaan: {},
      idWorkspace: { required },
      idTask: { required },
    };

    if (![1, 2, 3, 4].includes(this.formData.idWorkspaceType)) {
      formData.tanggalPelaksanaan = { required };
    }

    let formAssigment = {
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

    if (this.step == 1) {
      formAssigment = {
        namaPenugasan: { required, maxLength: maxLength(1000) },
        // deskripsiPenugasan: { required },
        idTipePenugasan: { required },
        listSatkerKoordinator: { required },
        listADGBidang: { required },
        // listSatkerPendukung: { required },
        // listDitugaskanKepada: { required },
        batasWaktu: {},
        periodeReminder: {},
      };

      if (!this.isArahan) {
        formAssigment.batasWaktu = { required };
        formAssigment.periodeReminder = {
          required,
          moreThan: (val, vm) => {
            let periode = this.list.periodes.find((e) => e.id == val);
            if (periode && vm.batasWaktu) {
              let date = new Date(vm.batasWaktu);
              let now = new Date();
              return parseInt(periode.periode) < dateDiff(now, date);
            }
            return true;
          },
        };
      }
    }

    return { formData, formAssigment };
  },
  data() {
    return {
      dialog: false,
      loading: [false],
      step: 0,
      editIdx: null,
      formData: {
        idAssignmentType: null,
        idWorkspaceType: null,
        tanggalPelaksanaan: null, // belum disesuaikan dengan design si
        idWorkspace: null,
        idTask: null,
        assignments: [],
      },
      formAssigment: {
        namaPenugasan: null,
        deskripsiPenugasan: null,
        idTipePenugasan: null,
        listSatkerKoordinator: [],
        listSatkerPendukung: [],
        listDitugaskanKepada: [],
        listADGBidang: [],
        batasWaktu: null,
        periodeReminder: null,
      },
      list: {
        assignmentTypes: [],
        workspaceTypes: [],
        workspaces: [],
        tasks: [],
        typePenugasans: [],
        satkers: [],
        ditugaskanKepadas: [],
        adgBidangs: [],
        periodes: [],
      },
    };
  },
  created() {
    this.getListAdgs();
    this.getAssignmentType();
    this.getSatker();
    this.getWorkspaceType();
    this.getPeriodeReminder();
  },
  methods: {
    e: getErrorMessages,
    updateKoordinator() {
      document.getElementById("koordinator").blur();
    },
    updatePendukung() {
      document.getElementById("pendukung").blur();
    },
    updateDitugaskan() {
      document.getElementById("ditugaskan").blur();
    },
    updateAdgBidang() {
      document.getElementById("adgbidang").blur();
    },
    updatePeriode() {
      document.getElementById("periode").blur();
    },
    show() {
      this.dialog = true;
      this.resetForm("all");
    },
    hide() {
      this.dialog = false;
      localStorage.setItem(this.keyCache, null);
    },
    next() {
      this.v$.$validate().then((res) => {
        if (res) {
          if (this.step == 1) {
            this.addMore();
          }
          ++this.step;
        }
      });
    },
    resetForm(tag = "other") {
      if (tag == "all") {
        this.step = "0";
        this.formData = {
          idAssignmentType: null,
          idWorkspaceType: null,
          tanggalPelaksanaan: null, // belum disesuaikan dengan design si
          idWorkspace: null,
          idTask: null,
          assignments: [],
        };
      }
      this.formAssigment = {
        namaPenugasan: null,
        deskripsiPenugasan: null,
        idTipePenugasan: null,
        listSatkerKoordinator: [],
        listSatkerPendukung: [],
        listDitugaskanKepada: [],
        listADGBidang: [],
        batasWaktu: null,
        periodeReminder: null,
      };
      this.v$.$reset();
    },
    addMore() {
      this.v$.$validate().then((res) => {
        if (res) {
          if (this.editIdx === null) {
            this.formData.assignments.push(this.formAssigment);
          } else {
            this.formData.assignments[this.editIdx] = this.formAssigment;
          }
          this.editIdx = null;
          this.resetForm();
          localStorage.setItem(this.keyCache, JSON.stringify(this.formData));
        }
      });
    },
    editMore(idx) {
      this.editIdx = idx;
      this.formAssigment = this.formData.assignments[idx] ?? {};
      this.step = 1;
    },
    deleteMore(idx) {
      this.formData.assignments.splice(idx, 1);
    },
    process() {
      this.loading[0] = true;
      let requestData = this.formData.assignments.map((el) => {
        let form = this.formData;
        return {
          ...el,
          ...form,
        };
      });
      requestData = requestData.map((el) => {
        delete el.assignments;
        delete el.idWorkspace;
        delete el.idWorkspaceType;
        let assignmentName = el.namaPenugasan;
        let description = el.deskripsiPenugasan;

        delete el.namaPenugasan;
        delete el.deskripsiPenugasan;

        el.listDitugaskanKepada.map((elm) => {
          delete elm.id;
          delete elm.title;
          return elm;
        });

        return {
          ...el,
          // listDitugaskanKepada: penugasan,
          assignmentName: assignmentName,
          description: description,
          username: this.$store.state.username,
        };
      });

      client
        .insertAssignment({
          store: this.$store,
          data: requestData,
        })
        .then((res) => {
          if (res.plainData.responseCode == "011000") {
            this.$root.toast.show({
              message: "Successfully Create",
              color: "success",
              timeout: 3000,
            });
            this.$emit("afterInsert");
          } else {
            this.$root.toast.show({
              message: res.plainData.responseMessage,
              color: "warning",
            });
          }
        })
        .catch(() => {
          this.$root.toast.show({
            message: "internal server error",
            color: "warning",
          });
        })
        .finally(() => {
          this.loading[0] = false;
          this.dialog = false;
        });
      localStorage.setItem(this.keyCache, null);
    },
    getTypePenugasanName(id) {
      let item = this.list.typePenugasans.find((e) => e.idTipePenugasan == id);
      return item.TipePenugasan;
    },
    getListAdgs() {
      client.getMAdgList({ store: this.$store }).then((res) => {
        this.list.adgBidangs = res.plainData.responseData;
      });
    },
    getAssignmentType() {
      client.getAssignmentType({ store: this.$store }).then((res) => {
        this.list.assignmentTypes = res.plainData.responseData;
      });
    },
    getPeriodeReminder() {
      client
        .getAssignmentReminderPeriode({ store: this.$store })
        .then((res) => {
          this.list.periodes = res.plainData.responseData;
        });
    },
    getSatker() {
      client.MSatkerPembuat({ store: this.$store }).then((res) => {
        this.list.satkers = res.plainData.responseData;
      });
    },
    getWorkspaceType() {
      client.getWorkspaceTypes({ store: this.$store }).then((res) => {
        let workspaceTypes = [];
        res.data.forEach((ele) => {
          workspaceTypes = workspaceTypes.concat(
            ele.workspaceTypes.filter((e) => e.id != 7)
          );
        });
        this.list.workspaceTypes = workspaceTypes;
      });
    },
    getWorkspaceAndTask() {
      if (this.formData.idWorkspaceType != 6)
        this.formData.tanggalPelaksanaan = null;
      if (
        [1, 2, 3, 4].includes(this.formData.idWorkspaceType) ||
        (this.formData.idWorkspaceType && this.formData.tanggalPelaksanaan)
      ) {
        this.loading[1] = true;
        let requestData = {
          idWorkspaceType: this.formData.idWorkspaceType,
        };

        if (![1, 2, 3, 4].includes(this.formData.idWorkspaceType)) {
          requestData = {
            idWorkspaceType: this.formData.idWorkspaceType,
            date: formatTimeYmd(this.formData.tanggalPelaksanaan),
          };
        }

        this.formData.idWorkspace = null;
        client
          .getWorkspaceAndTaskbyWorkspaceTypeAndTaskStartDate({
            store: this.$store,
            data: requestData,
          })
          .then((res) => {
            let response = res.plainData.responseData;
            this.list.workspaces = response.listWorkspace;
            this.list.tasks = response.listTask;
          })
          .finally(() => {
            this.loading[1] = false;
          });
      }
    },
    getTypePenugasan() {
      client
        .getTipePenugasanByAssignmentType({
          store: this.$store,
          data: {
            idAssignmentType: this.formData.idAssignmentType,
          },
        })
        .then((res) => {
          this.list.typePenugasans = res.plainData.responseData;
        });
    },
    onChangeSearchFilter(val) {
      if (val) {
        client
          .SearchUserByname({
            store: this.$store,
            data: {
              name: val,
            },
          })
          .then((res) => {
            let datas = res.plainData.map((e) => {
              return {
                id: e.inputId,
                title: e.inputName,
                username: e.isGrup ? "" : e.inputId,
                groupName: e.isGrup ? e.inputId : "",
                email: e.inputEmail,
              };
            });
            this.list.ditugaskanKepadas = datas;
          });
      } else {
        this.list.ditugaskanKepadas = [];
      }
    },
  },
  computed: {
    dialogWidth() {
      if (this.formData.idAssignmentType) {
        return "800";
      } else {
        return "600";
      }
    },
    isArahan() {
      return (
        this.formAssigment.idTipePenugasan &&
        this.formAssigment.idTipePenugasan != 1
      );
    },
    keyCache() {
      return this.$store.state.username + "_form_assignment";
    },
    totalAssignment() {
      return this.formData.assignments.length;
    },
    taskWorkspace() {
      return (
        this.list.tasks.filter(
          (e) => e.idWorkspace == this.formData.idWorkspace
        ) ?? []
      );
    },
    satkerKoordinators() {
      return this.list.satkers.filter((e) => {
        return !this.formAssigment.listSatkerPendukung.includes(e.id);
      });
    },
    satkerPendukungs() {
      return this.list.satkers.filter((e) => {
        return !this.formAssigment.listSatkerKoordinator.includes(e.id);
      });
    },
  },
  watch: {
    "formData.idWorkspaceType": function () {
      if (this.formData.idWorkspaceType) {
        this.getWorkspaceAndTask();
        this.getTypePenugasan();
      }
    },
    "formData.idWorkspace": function () {
      this.formData.idTask = null;
    },
    isArahan: function (val) {
      if (val) {
        this.formAssigment.periodeReminder = null;
        this.formAssigment.batasWaktu = null;
      }
    },
  },
};
</script>

<style scoped>
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
</style>
