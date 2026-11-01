<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent width="800">
      <v-card class="rounded-lg">
        <v-card-title class="d-flex justify-center align-center mt-4">
          <div class="text-18 text-blueTheme fw-500">Edit Assignment</div>
          <v-btn
            class="mr-2"
            style="position: absolute; right: 0"
            variant="text"
            icon="mdi-close"
            @click="dialog = false"
          ></v-btn>
        </v-card-title>
        <v-btn
          elevation="0"
          class="d-block separatorHorizontal"
          style="cursor: none"
        />

        <v-card-text>
          <v-form ref="form">
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-500">
                Workspace Type <span class="text-redTheme">*</span>
              </div>
              <v-select
                disabled
                single-line
                :label="formAssigment.workspaceTypeName"
                variant="solo"
                density="comfortable"
              >
              </v-select>
            </v-col>
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-500">
                Tanggal Pelaksanaan <span class="text-redTheme">*</span>
              </div>
              <v-select
                disabled
                single-line
                :label="
                  $filters.formatTimeEngToIndNoDays(formAssigment.workDate)
                "
                variant="solo"
                density="comfortable"
              >
              </v-select>
            </v-col>
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-500">
                Workspace Name <span class="text-redTheme">*</span>
              </div>
              <v-select
                disabled
                single-line
                :label="formAssigment.workspaceName"
                variant="solo"
                density="comfortable"
              >
              </v-select>
            </v-col>
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-500">
                Task Name <span class="text-redTheme">*</span>
              </div>
              <v-select
                disabled
                single-line
                :label="formAssigment.taskName"
                variant="solo"
                density="comfortable"
              >
              </v-select>
            </v-col>
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-500">
                Nama Penugasan <span class="text-redTheme">*</span>
              </div>
              <v-text-field
                variant="solo"
                placeholder="Please Input Nama Penugasan"
                v-model="formAssigment.assignmentName"
                :rules="[(value) => !!value || 'Wajib diisi']"
              ></v-text-field>
            </v-col>
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-500">
                Deskripsi Penugasan <span class="text-redTheme">*</span>
              </div>
              <v-text-field
                variant="solo"
                placeholder="Please Input Nama Penugasan"
                v-model="formAssigment.description"
                :rules="[(value) => !!value || 'Wajib diisi']"
              ></v-text-field>
            </v-col>
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-500">
                Satker Koordinator <span class="text-redTheme">*</span>
              </div>
              <v-autocomplete
                :rules="[(v) => !!(v && v.length) || 'Wajib diisi']"
                chips
                closable-chips
                multiple
                hide-no-data
                hide-selected
                item-title="value"
                item-value="id"
                variant="solo"
                density="comfortable"
                id="koordinator"
                @update:modelValue="updateKoordinator"
                v-model="formAssigment.listSatkerKoordinator"
                :items="list.satkerKoordinators"
              >
                <template v-slot:no-data>
                  <span
                    class="d-flex align-item-center ma-2 pa-1 select-empty"
                    @click="getSatker()"
                  >
                    <v-icon class="mr-2">mdi-reload</v-icon>
                    Reload Data
                  </span>
                </template>
              </v-autocomplete>
            </v-col>
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-500">Satker Pendukung</div>
              <v-autocomplete
                chips
                closable-chips
                multiple
                clearable
                hide-no-data
                hide-selected
                item-title="value"
                item-value="id"
                variant="solo"
                density="comfortable"
                id="pendukung"
                @update:modelValue="updatePendukung"
                v-model="formAssigment.listSatkerPendukung"
                :items="list.satkerPendukungs"
              >
                <template v-slot:no-data>
                  <span
                    class="d-flex align-item-center ma-2 pa-1 select-empty"
                    @click="getAssignmentDetail()"
                  >
                    <v-icon class="mr-2">mdi-reload</v-icon>
                    Reload Data
                  </span>
                </template>
              </v-autocomplete>
            </v-col>
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-500">Ditugaskan Kepada</div>
              <v-autocomplete
                chips
                closable-chips
                multiple
                hide-no-data
                hide-selected
                single-line
                id="ditugaskan"
                v-model="formAssigment.listDitugaskanKepada"
                v-model:search="search"
                :loading="loading"
                :items="participant"
                :item-value="participant"
                @update:modelValue="updateDitugaskanKepada"
                return-object
                item-title="inputName"
                density="comfortable"
                variant="solo"
              >
                <template v-slot:item="{ props, item }">
                  <v-list-item v-bind="props" :title="''" class="pt-5 pb-5">
                    <v-row align="center" class="spacer" no-gutters>
                      <v-col cols="8" class="text-left ms-2">
                        <p style="color: #3a416f">
                          {{ item?.raw?.inputName }}
                        </p>
                        <p class="text-12 text-grey">
                          {{ item?.raw?.inputEmail }}
                        </p>
                      </v-col>
                    </v-row>
                  </v-list-item>
                </template>
              </v-autocomplete>
            </v-col>
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-500">
                ADG yang membawahi <span class="text-redTheme">*</span>
              </div>
              <v-autocomplete
                :rules="[(v) => !!(v && v.length) || 'Wajib diisi']"
                chips
                closable-chips
                multiple
                hide-no-data
                hide-selected
                id="adgbidang"
                item-title="value"
                item-value="id"
                variant="solo"
                density="comfortable"
                @update:modelValue="updateAdgBidang"
                v-model="formAssigment.listADGBidang"
                :items="list.adgBidangs"
              >
                <template v-slot:no-data>
                  <span
                    class="d-flex align-item-center ma-2 pa-1 select-empty"
                    @click="getAssignmentDetail()"
                  >
                    <v-icon class="mr-2">mdi-reload</v-icon>
                    Reload Data
                  </span>
                </template>
              </v-autocomplete>
            </v-col>
            <v-col cols="12" class="py-1" v-if="tag !== 'arahan_metadata'">
              <div class="text-15 text-blueTheme fw-500">Batas Waktu</div>
              <VueDatePicker
                auto-apply
                v-model="formAssigment.batasWaktu"
                :month-change-on-scroll="false"
                :enable-time-picker="false"
              >
                <template #trigger>
                  <v-text-field
                    readonly
                    variant="solo"
                    placeholder="DD/MM/YYYY"
                    append-inner-icon="mdi-calendar-today"
                    class="cursor-pointer"
                    :value="
                      $filters.formatTimeEngToIndNoDays(
                        formAssigment.batasWaktu
                      )
                    "
                  ></v-text-field>
                </template>
              </VueDatePicker>
            </v-col>
            <v-col cols="12" class="py-1" v-if="tag !== 'arahan_metadata'">
              <div class="text-15 text-blueTheme fw-500">Periode Reminder</div>
              <!-- {{ list.periodes }} -->
              <v-autocomplete
                single-line
                item-title="periode"
                item-value="id"
                variant="solo"
                density="comfortable"
                placeholder="Choose Periode"
                v-model="formAssigment.periodeReminder"
                :items="list.periodes"
                id="periode"
                @update:modelValue="updatePeriode"
              >
                <template v-slot:no-data>
                  <span
                    class="d-flex align-item-center ma-2 pa-1 select-empty"
                    @click="getPeriodeReminder()"
                  >
                    <v-icon class="mr-2">mdi-reload</v-icon>
                    Reload Data
                  </span>
                </template>
              </v-autocomplete>
            </v-col>
            <!-- <pre>{{ item }}</pre>
        ===================
        <pre>{{ listObj }}</pre> -->
          </v-form>
        </v-card-text>

        <v-card-actions class="mb-5 mr-4">
          <v-spacer></v-spacer>
          <v-btn class="btn-action btn-action-close" @click="dialog = false">
            Cancel
          </v-btn>
          <v-btn
            class="btn-action btn-action-create"
            @click="process()"
            :loading="loading"
            :disabled="loading"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <custom-loading v-if="isLoading" :title="'Updating data, please wait'" />
  </v-row>
</template>
<script>
import client from "@/library/ApiClient";
import CustomLoading from "@/components/CustomLoading.vue";
import { dateDiff } from "@/helpers/date";

export default {
  components: { CustomLoading },
  emits: ["onSuccessEdit"],
  props: {
    tag: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      dialog: false,
      item: {},
      loading: false,
      formAssigment: {},
      list: [],
      listObj: [],
      search: null,
      participant: [],
      isLoading: false,
    };
  },
  created() {
    this.getSatker();
    this.getListMemberTask();
    this.getListAdgs();
    this.getPeriodeReminder();
  },
  methods: {
    show(item) {
      this.dialog = true;
      this.item = item;
      this.getAssignmentDetail();

      this.formAssigment = {
        workspaceTypeName: item.workspaceTypeName,
        workDate: item.workDate,
        workspaceName: item.workspaceName,
        taskName: item.taskName,
        assignmentName: item.assignmentName,
        description: item.description,
        listSatkerKoordinator: [],
        listSatkerPendukung: [],
        listDitugaskanKepada: [],
        listADGBidang: [],
        batasWaktu: item.dueDate,
        periodeReminder: item.idReminderPeriod,
      };
    },
    async process() {
      const { valid } = await this.$refs.form.validate();
      if (!valid) return;

      // alert(this.formAssigment.listSatkerKoordinator.length);

      let tempList = [];
      this.formAssigment.listDitugaskanKepada.forEach((element) => {
        tempList.push({
          username: element.isGrup ? "" : element.inputId,
          groupName: element.isGrup ? element.inputId : "",
        });
      });
      this.isLoading = true;
      client
        .editAssignmentByIdAssignment({
          store: this.$store,
          data: {
            username: this.$store.state.username,
            id: this.item.id,
            assignmentName: this.formAssigment.assignmentName,
            description: this.formAssigment.description,
            listSatkerKoordinator: this.formAssigment.listSatkerKoordinator,
            listSatkerPendukung: this.formAssigment.listSatkerPendukung,
            listAssignmentMember: tempList,
            listAdg: this.formAssigment.listADGBidang,
            batasWaktu: this.formAssigment.batasWaktu,
            idPeriodeReminder: this.formAssigment.periodeReminder,
          },
        })
        .then(() => {
          this.$root.toast.show({
            message: "Successfully Changes",
            color: "success",
            timeout: 3000,
          });
        })
        .catch(() => {
          this.$root.toast.show({
            message: "Oops, Something went wrong",
            color: "error",
            timeout: 3000,
            icon: "mdi-check",
          });
        })
        .finally(() => {
          this.$emit("onSuccessEdit");
          this.dialog = false;
          this.isLoading = false;
        });
    },

    getSatker() {
      client.MSatkerPembuat({ store: this.$store }).then((res) => {
        this.list.satkerKoordinators = res.plainData.responseData;
        this.list.satkerPendukungs = res.plainData.responseData;
      });
    },
    getListAdgs() {
      client.getMAdgList({ store: this.$store }).then((res) => {
        this.list.adgBidangs = res.plainData.responseData;
      });
    },
    async updateKoordinator(value) {
      let ada = false;
      await this.formAssigment.listSatkerPendukung.forEach(function (element) {
        if (value.includes(element)) {
          alert("Satker telah menjadi pendukung");
          ada = true;
        }
      });
      if (ada) this.formAssigment.listSatkerKoordinator.pop();
      document.getElementById("koordinator").blur();
    },
    async updatePendukung(value) {
      let ada = false;
      await this.formAssigment.listSatkerKoordinator.forEach(function (
        element
      ) {
        if (value.includes(element)) {
          alert("Satker telah menjadi koordinator");
          ada = true;
        }
      });
      if (ada) this.formAssigment.listSatkerPendukung.pop();
      document.getElementById("pendukung").blur();
    },
    async updateAdgBidang() {
      document.getElementById("adgbidang").blur();
    },
    async updateDitugaskanKepada() {
      document.getElementById("ditugaskan").blur();
    },
    async updatePeriode(value) {
      let selected = 0;
      await this.list.periodes.forEach(function (element) {
        if ([value].includes(element.id)) {
          selected = parseInt(element.periode);
        }
      });
      let date = new Date(this.formAssigment.batasWaktu);
      let now = new Date();
      let val = parseInt(selected) < dateDiff(now, date);
      if (!val) {
        alert("Periode reminder melebihi batas waktu");
        this.formAssigment.periodeReminder = this.item.idReminderPeriod;
      }
      document.getElementById("periode").blur();
    },
    getListMemberTask() {
      client
        .getListTaskMemberDataByIdTask({
          store: this.$store,
          data: {
            id: this.item.idTask,
          },
        })
        .then((res) => {
          // debugger;
          let datas = res.plainData.map((e) => {
            let title = e.groupName;
            if (e.user) {
              title = e.user.name;
            }
            return {
              id: e.id,
              title: title,
              username: e.user?.username ?? "",
              groupName: e.groupName,
            };
          });
          this.list.ditugaskanKepadas = datas;
        });
    },
    getAssignmentDetail() {
      client
        .getAssignmentDetail({
          store: this.$store,
          data: {
            id: this.item.id,
          },
        })
        .then((res) => {
          this.listObj = res.plainData.responseData;
          // debugger;
          this.listObj.listSatkerKoordinatorList.forEach((element) => {
            this.formAssigment.listSatkerKoordinator.push(element.id);
          });

          this.listObj.listSatkerPendukungList.forEach((element) => {
            this.formAssigment.listSatkerPendukung.push(element.id);
          });

          this.listObj.listAssignmentMemberList.forEach((element) => {
            let isGrup = element.groupName == "" ? false : true;
            this.formAssigment.listDitugaskanKepada.push({
              inputName: isGrup ? element.groupName : element.name,
              inputId: isGrup ? element.groupName : element.username,
              inputEmail: isGrup ? "" : element.username + "@bi.go.id",
              isGrup: isGrup,
            });
          });
          this.formAssigment.listDitugaskanKepada = [
            ...new Map(
              this.formAssigment.listDitugaskanKepada.map((m) => [m.inputId, m])
            ).values(),
          ];

          this.listObj.listAdgList.forEach((element) => {
            this.formAssigment.listADGBidang.push(element.id);
          });
        });
    },
    getPeriodeReminder() {
      client
        .getAssignmentReminderPeriode({ store: this.$store })
        .then((res) => {
          this.list.periodes = res.plainData.responseData;
        });
    },
    querySelections(query) {
      if (query) {
        this.loading = true;
        client
          .SearchUserByname({
            store: this.$store,
            data: {
              name: query,
            },
          })
          .then((response) => {
            this.participant = response.plainData;

            this.loading = false;
          })
          .catch(() => {
            this.loading = false;
          });
      } else {
        this.participant = [];
      }
    },
  },
  watch: {
    search(val) {
      val && val !== this.select && this.querySelections(val);
    },
    // "formAssigment.listSatkerKoordinator": {
    //   handler(val) {
    //     if (!val.length) this.validate = false;
    //   },
    // },
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
.btn-action-create-grey {
  background: linear-gradient(92.09deg, grey -46.47%, darkgrey 157.9%);
  color: white !important;
}

.btn-action-close {
  background: linear-gradient(92.09deg, #fff -46.47%, #fff 157.9%);
  color: red !important;
}
:deep(.v-chip__close) {
  color: white !important;
}
:deep(.v-chip) {
  color: white !important;
  background: #277dc2 !important;
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
</style>
