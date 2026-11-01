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
          <v-form ref="formRef">
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
              />
            </v-col>
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-500">
                Tanggal Pelaksanaan <span class="text-redTheme">*</span>
              </div>
              <v-select
                disabled
                single-line
                :label="formatTimeEngToIndNoDays(formAssigment.workDate)"
                variant="solo"
                density="comfortable"
              />
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
              />
            </v-col>
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-500">
                Nama Penugasan <span class="text-redTheme">*</span>
              </div>
              <v-text-field
                variant="solo"
                placeholder="Please Input Nama Penugasan"
                v-model="formAssigment.assignmentName"
                :rules="[(v) => !!v || 'Wajib diisi']"
              />
            </v-col>
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-500">
                Deskripsi Penugasan
              </div>
              <v-text-field
                variant="solo"
                placeholder="Please Input Nama Penugasan"
                v-model="formAssigment.description"
              />
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
                :items="satkerKoordinators"
              >
                <template #no-data>
                  <span
                    class="d-flex align-item-center ma-2 pa-1 select-empty"
                    @click="getSatker"
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
                :items="satkerPendukungs"
              >
                <template #no-data>
                  <span
                    class="d-flex align-item-center ma-2 pa-1 select-empty"
                    @click="getAssignmentDetail"
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
                <template #item="{ props, item }">
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
                <template #no-data>
                  <span
                    class="d-flex align-item-center ma-2 pa-1 select-empty"
                    @click="getAssignmentDetail"
                  >
                    <v-icon class="mr-2">mdi-reload</v-icon>
                    Reload Data
                  </span>
                </template>
              </v-autocomplete>
            </v-col>
            <v-col
              cols="12"
              class="py-1"
              v-if="props.tag !== 'arahan_metadata'"
            >
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
                    :value="formatTimeEngToIndNoDays(formAssigment.batasWaktu)"
                  />
                </template>
              </VueDatePicker>
            </v-col>
            <v-col
              cols="12"
              class="py-1"
              v-if="props.tag !== 'arahan_metadata'"
            >
              <div class="text-15 text-blueTheme fw-500">Periode Reminder</div>
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
                :error-messages="periodeErrorMessage"
                @update:modelValue="updatePeriode"
              >
                <template #no-data>
                  <span
                    class="d-flex align-item-center ma-2 pa-1 select-empty"
                    @click="getPeriodeReminder"
                  >
                    <v-icon class="mr-2">mdi-reload</v-icon>
                    Reload Data
                  </span>
                </template>
              </v-autocomplete>
            </v-col>
          </v-form>
        </v-card-text>
        <v-card-actions class="mb-5 mr-4">
          <v-spacer />
          <v-btn class="btn-action btn-action-close" @click="dialog = false">
            Cancel
          </v-btn>
          <v-btn
            class="btn-action btn-action-create"
            @click="process"
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

<script lang="ts" setup>
import {
  ref,
  reactive,
  watch,
  getCurrentInstance,
  onMounted,
  computed,
} from "vue";
import client from "@/library/ApiClient";
import CustomLoading from "@/components/CustomLoading.vue";
import { dateDiff } from "@/helpers/date";
import { useStore } from "vuex";
import { uniqueOptions } from "@/helpers/utils";
import clientv2 from "@v2/library/ApiClient";

type Satker = {
  id: string;
  value: string;
};

type AdgBidang = {
  id: string;
  value: string;
};

type Periode = {
  id: string;
  periode: string;
};

type AssignmentMember = {
  groupName: string;
  name: string;
  username: string;
};

type DitugaskanKepada = {
  inputName: string;
  inputId: string;
  inputEmail: string;
  isGrup: boolean;
};

type AssignmentDetail = {
  id: string;
  eventSubTypeLIst: string;
  workDate: string;
  eventName: string;
  assignmentName: string;
  description: string;
  dueDate: string;
  idReminderPeriod: string;
  idTask: string;
  listSatkerKoordinatorList?: Satker[];
  listSatkerPendukungList?: Satker[];
  listAssignmentMemberList?: AssignmentMember[];
  listAdgList?: AdgBidang[];
};

const props = defineProps<{
  tag?: string;
}>();

const emit = defineEmits<{
  (e: "onSuccessEdit", value?: unknown): void;
  (e: "close", value: boolean): void;
}>();

const store = useStore();
const { proxy } = getCurrentInstance() as any;

const dialog = ref(false);
const item = ref<Partial<AssignmentDetail>>({});
const loading = ref(false);
const isLoading = ref(false);
const periodeErrorMessage = ref("");
const formRef = ref<any>(null);
const search = ref<string | undefined>();
const participant = ref<any[]>([]);
const list = reactive<{
  satkers: Satker[];
  adgBidangs: AdgBidang[];
  ditugaskanKepadas: any[];
  periodes: Periode[];
}>({
  satkers: [],
  adgBidangs: [],
  ditugaskanKepadas: [],
  periodes: [],
});
const listObj = ref<any>({});

const formAssigment = reactive<{
  workspaceTypeName: string;
  workDate: string;
  workspaceName: string;
  assignmentName: string;
  description: string;
  listSatkerKoordinator: string[];
  listSatkerPendukung: string[];
  listDitugaskanKepada: DitugaskanKepada[];
  listADGBidang: string[];
  batasWaktu: string;
  periodeReminder: string;
}>({
  workspaceTypeName: "",
  workDate: "",
  workspaceName: "",
  assignmentName: "",
  description: "",
  listSatkerKoordinator: [],
  listSatkerPendukung: [],
  listDitugaskanKepada: [],
  listADGBidang: [],
  batasWaktu: "",
  periodeReminder: "",
});

function formatTimeEngToIndNoDays(date: string | Date): string {
  if (!date) return "";
  const d = new Date(date);
  return d.toLocaleDateString("id-ID");
}

function show(newItem: AssignmentDetail) {
  dialog.value = true;
  item.value = newItem;
  getAssignmentDetail();

  Object.assign(formAssigment, {
    workspaceTypeName: newItem.eventSubTypeLIst,
    workDate: newItem.workDate,
    workspaceName: newItem.eventName,
    assignmentName: newItem.assignmentName,
    description: newItem.description,
    listSatkerKoordinator: [],
    listSatkerPendukung: [],
    listDitugaskanKepada: [],
    listADGBidang: [],
    batasWaktu: newItem.dueDate,
    periodeReminder: newItem.idReminderPeriod,
  });
}

function getSatker() {
  client.MSatkerPembuat({ store }).then((res: any) => {
    list.satkers = res.plainData.responseData;
  });
}
function getListAdgs() {
  client.getMAdgList({ store }).then((res: any) => {
    list.adgBidangs = res.plainData.responseData;
  });
}
function getListMemberTask() {
  client
    .getListTaskMemberDataByIdTask({
      store,
      data: { id: item.value.idTask },
    })
    .then((res: any) => {
      let datas = res.plainData.map((e: any) => {
        let title = e.groupName;
        if (e.user) title = e.user.name;
        return {
          id: e.id,
          title,
          username: e.user?.username ?? "",
          groupName: e.groupName,
        };
      });
      list.ditugaskanKepadas = datas;
    });
}
function getAssignmentDetail() {
  client
    .getAssignmentDetailNew({
      store,
      data: { id: item.value.id },
    })
    .then((res: any) => {
      listObj.value = res.plainData.responseData;
      // Koordinator
      formAssigment.listSatkerKoordinator = [];
      listObj.value.listSatkerKoordinatorList?.forEach((el: Satker) => {
        formAssigment.listSatkerKoordinator.push(el.id);
      });
      // Pendukung
      formAssigment.listSatkerPendukung = [];
      listObj.value.listSatkerPendukungList?.forEach((el: Satker) => {
        formAssigment.listSatkerPendukung.push(el.id);
      });
      // Ditugaskan Kepada
      formAssigment.listDitugaskanKepada = [];
      listObj.value.listAssignmentMemberList?.forEach(
        (el: AssignmentMember) => {
          let isGrup = el.groupName !== "";
          formAssigment.listDitugaskanKepada.push({
            inputName: isGrup ? el.groupName : el.name,
            inputId: isGrup ? el.groupName : el.username,
            inputEmail: isGrup ? "" : el.username + "@bi.go.id",
            isGrup,
            ...el,
          });
        }
      );
      // Remove duplicates
      formAssigment.listDitugaskanKepada = [
        ...new Map(
          formAssigment.listDitugaskanKepada.map((m) => [m.inputId, m])
        ).values(),
      ];
      // ADG Bidang
      formAssigment.listADGBidang = [];
      listObj.value.listAdgList?.forEach((el: AdgBidang) => {
        formAssigment.listADGBidang.push(el.id);
      });
    });
}
function getPeriodeReminder() {
  client.getAssignmentReminderPeriode({ store }).then((res: any) => {
    list.periodes = res.plainData.responseData;
  });
}

async function process() {
  const valid = await formRef.value?.validate();
  if (!valid.valid || periodeErrorMessage.value) return;
  let tempList: { username: string; groupName: string }[] = [];
  formAssigment.listDitugaskanKepada.forEach((element) => {
    tempList.push({
      username: element.isGrup ? "" : element.inputId,
      groupName: element.isGrup ? element.inputId : "",
    });
  });
  isLoading.value = true;
  client
    .editAssignmentByIdAssignmentNew({
      store,
      data: {
        id: item.value.id,
        assignmentName: formAssigment.assignmentName,
        description: formAssigment.description ?? "",
        listSatkerKoordinator: formAssigment.listSatkerKoordinator,
        listSatkerPendukung: formAssigment.listSatkerPendukung,
        listAssignmentMember: tempList,
        listAdg: formAssigment.listADGBidang,
        batasWaktu: formAssigment.batasWaktu,
        idPeriodeReminder: formAssigment.periodeReminder,
      },
    })
    .then(() => {
      proxy.$root.toast.show({
        message: "Successfully Changes",
        color: "success",
        timeout: 3000,
      });
    })
    .catch((error: any) => {
      const errorMessage =
        error.response?.data?.responseMessage || "Oops, Something went wrong";
      proxy.$root.toast.show({
        message: errorMessage,
        color: "error",
        timeout: 3000,
        icon: "mdi-check",
      });
    })
    .finally(() => {
      emit("onSuccessEdit");
      dialog.value = false;
      isLoading.value = false;
    });
}

function updateKoordinator(value: string[]) {
  let ada = false;
  formAssigment.listSatkerPendukung.forEach((element) => {
    if (value.includes(element)) {
      alert("Satker telah menjadi pendukung");
      ada = true;
    }
  });
  if (ada) formAssigment.listSatkerKoordinator.pop();
  (document.getElementById("koordinator") as HTMLElement)?.blur();
}
function updatePendukung(value: string[]) {
  let ada = false;
  formAssigment.listSatkerKoordinator.forEach((element) => {
    if (value.includes(element)) {
      alert("Satker telah menjadi koordinator");
      ada = true;
    }
  });
  if (ada) formAssigment.listSatkerPendukung.pop();
  (document.getElementById("pendukung") as HTMLElement)?.blur();
}
function updateAdgBidang() {
  (document.getElementById("adgbidang") as HTMLElement)?.blur();
}
function updateDitugaskanKepada() {
  (document.getElementById("ditugaskan") as HTMLElement)?.blur();
}
function updatePeriode(value: string) {
  let selected = 0;
  list.periodes.forEach((element) => {
    if ([value].includes(element.id)) {
      selected = parseInt(element.periode);
    }
  });
  let date = new Date(formAssigment.batasWaktu);
  let now = new Date();
  let val = parseInt(String(selected)) < dateDiff(now, date);
  if (!val) {
    periodeErrorMessage.value =
      "Opps!, periode tidak boleh melebihi batas waktu";
    // formAssigment.periodeReminder = item.value.idReminderPeriod || "";
  } else {
    periodeErrorMessage.value = "";
  }
  (document.getElementById("periode") as HTMLElement)?.blur();
}
function querySelections(query: string) {
  if (query.length >= 3) {
    const trimmedSearch = query
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

    loading.value = true;
    clientv2
      .SearchUserAndGroupNew({ data: reqData })
      .then((res: any) => {
        if (Array.isArray(res) && res.length > 0) {
          const taskMember = [
            ...(res
              .map((item: any) => {
                item.inputName = item.value;
                item.groupName = item.isGroup ? item.value : null;
                item.inputId = item.isGroup ? item.value : item.username;
                item.isGrup = item.isGroup;
                if (
                  formAssigment.listDitugaskanKepada.some(
                    (el: any) => el.inputId === item.inputId
                  )
                ) {
                  return null;
                }
                return item;
              })
              .filter((v: any) => v !== null) as any[]),
          ];
          participant.value = taskMember;
          query.includes(";") &&
            (formAssigment.listDitugaskanKepada = [
              ...formAssigment.listDitugaskanKepada,
              ...taskMember,
            ]);
          query.includes(";") && (search.value = ""); // Clear the search input after getting results
        }
        loading.value = false;
      })
      .catch(() => {
        loading.value = false;
      });
  } else {
    participant.value = [];
  }
}

const satkerKoordinators = computed(() =>
  uniqueOptions(list.satkers, formAssigment.listSatkerPendukung)
);

const satkerPendukungs = computed(() =>
  uniqueOptions(list.satkers, formAssigment.listSatkerKoordinator)
);

watch(search, (val) => {
  if (val) querySelections(val);
});

onMounted(() => {
  getSatker();
  getListMemberTask();
  getListAdgs();
  getPeriodeReminder();
});

defineExpose({ show });
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
