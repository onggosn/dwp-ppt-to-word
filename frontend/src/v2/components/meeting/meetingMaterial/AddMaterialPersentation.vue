<template>
  <v-btn variant="outlined" class="btn-create" @click="show">
    {{ title }}
  </v-btn>
  <Teleport to="body">
    <v-dialog v-model="dialog" :max-width="1000" persistent>
      <v-card class="mb-5 border-radius-dwp">
        <v-card-title class="d-flex justify-center align-center">
          <div class="text-18 text-blueTheme fw-500 mt-2 mb-2">
            Add Material Presentation
          </div>
          <v-btn
            class="mr-2"
            style="position: absolute; right: 0"
            variant="text"
            icon="mdi-close"
            @click="hide"
          ></v-btn>
        </v-card-title>
        <div class="separatorHorizontalGradient"></div>
        <v-card-text>
          <Steppy
            v-model:step="step"
            nextText="Next"
            backText="Back"
            doneText="Create"
            :class="[tabs.length == 2 ? 'kelas-1' : 'kelas-2']"
            :tabs="tabs"
          >
            <template #1>
              <v-row class="text-left">
                <v-col :cols="12">
                  <p class="pb-1 pt-2 text-left text-darkBlue font-weight-bold">
                    Method
                  </p>
                  <v-autocomplete
                    v-model="formMaterial.method"
                    variant="solo"
                    placeholder="Choose Method Add Document"
                    item-title="value"
                    item-value="id"
                    :items="store.state.meetingStore.methodList"
                    :hide-details="isError(v$.method)"
                    :error-messages="getErrorMessages(v$.method)"
                  />
                </v-col>
              </v-row>
            </template>
            <template #2>
              <v-row class="text-left">
                <v-col
                  v-if="formMaterial.method == 1"
                  :cols="12"
                  class="py-3 pl-4 mx-3 my-4 text-15 blue-gradient"
                >
                  <b style="color: #fff">Upload Document</b>
                </v-col>
                <v-col cols="12" class="py-1" v-if="formMaterial.method == 1">
                  <div class="text-15 text-blueTheme fw-500">Title</div>
                  <v-text-field
                    variant="solo"
                    v-model="formMaterial.file.name"
                    placeholder="Insert Title"
                    :hide-details="isError(v$.file.name)"
                    :error-messages="getErrorMessages(v$.file.name)"
                    readonly
                  ></v-text-field>
                </v-col>
                <v-col cols="12" class="py-1">
                  <div class="text-15 text-blueTheme fw-500">List Document</div>
                  <v-autocomplete
                    v-model="formMaterial.documentType"
                    :items="documentList"
                    variant="solo"
                    placeholder="Choose Document Type"
                    item-title="value"
                    item-value="id"
                    :hide-details="isError(v$.dokumenTipe)"
                    :error-messages="getErrorMessages(v$.dokumenTipe)"
                  />
                </v-col>
                <v-col cols="12" class="py-1">
                  <div class="text-15 text-blueTheme fw-500">Upload File</div>
                  <FileDragable
                    v-model="formMaterial.file"
                    :formatFile="['.pdf', '.ppt', '.pptx', '.doc', '.docx']"
                    :loadingPercent="loadingPercent"
                  />
                  <span
                    class="text-danger pl-3 text-12"
                    v-if="!isError(v$.file.name)"
                  >
                    {{ getErrorMessages(v$.file.name).toString() }}
                  </span>
                </v-col>
              </v-row>
            </template>
            <template #3>
              <v-row class="text-left">
                <v-col
                  :cols="12"
                  class="py-3 pl-4 mx-3 my-4 text-15 blue-gradient"
                >
                  <b style="color: #fff">Upload Document</b>
                </v-col>
                <v-col :cols="12">
                  <div class="text-15 text-blueTheme fw-700">Metadata</div>
                </v-col>
                <v-col :cols="6">
                  <div class="text-15 text-blueTheme fw-500">
                    Tipe Dokumen <span class="text-danger">*</span>
                  </div>
                  <v-autocomplete
                    v-model="formMaterial.dokumenTipe"
                    :items="store.state.meetingStore.typeDocList"
                    variant="solo"
                    placeholder="Choose Document Type"
                    item-title="value"
                    item-value="id"
                    :hide-details="isError(v$.dokumenTipe)"
                    :error-messages="getErrorMessages(v$.dokumenTipe)"
                  />
                </v-col>
                <v-col :cols="6">
                  <div class="text-15 text-blueTheme fw-500">
                    Versi <span class="text-danger">*</span>
                  </div>
                  <v-text-field
                    variant="solo"
                    v-model="formMaterial.versi"
                    placeholder="Please Fill Versi"
                    :hide-details="isError(v$.versi)"
                    :error-messages="getErrorMessages(v$.versi)"
                  ></v-text-field>
                </v-col>
                <v-col :cols="12">
                  <div class="text-15 text-blueTheme fw-500">
                    Nama Topik <span class="text-danger">*</span>
                  </div>
                  <v-textarea
                    variant="solo"
                    v-model="formMaterial.topikNama"
                    placeholder="Please Fill Nama Topik"
                    rows="3"
                    max-rows="5"
                    :counter="100"
                    :error-messages="getErrorMessages(v$.topikNama)"
                  />
                </v-col>
                <v-col :cols="6">
                  <div class="text-15 text-blueTheme fw-500">
                    Satker Pembuat<span class="text-danger">*</span>
                  </div>
                  <v-autocomplete
                    v-model="formMaterial.satkerPembuat"
                    :items="store.state.meetingStore.satkerPembuatList"
                    variant="solo"
                    placeholder="Choose Satker Pembuat"
                    item-value="id"
                    item-title="value"
                    :hide-details="isError(v$.satkerPembuat)"
                    :error-messages="getErrorMessages(v$.satkerPembuat)"
                  />
                </v-col>
                <v-col :cols="6">
                  <div class="text-15 text-blueTheme fw-500">
                    PS <span class="text-danger">*</span>
                  </div>
                  <v-autocomplete
                    v-model="formMaterial.ps"
                    :items="store.state.meetingStore.materialPSList"
                    variant="solo"
                    placeholder="Choose PS"
                    item-title="value"
                    item-value="id"
                    :hide-details="isError(v$.ps)"
                    :error-messages="getErrorMessages(v$.ps)"
                  />
                </v-col>
                <v-col :cols="6">
                  <div class="text-15 text-blueTheme fw-500">
                    Event <span class="text-danger">*</span>
                  </div>
                  <v-autocomplete
                    v-model="formMaterial.event"
                    :items="store.state.meetingStore.materialEventList"
                    variant="solo"
                    placeholder="Choose Event"
                    item-title="value"
                    item-value="id"
                    :hide-details="isError(v$.event)"
                    :error-messages="getErrorMessages(v$.event)"
                  />
                </v-col>
                <v-col :cols="6">
                  <div class="text-15 text-blueTheme fw-500">
                    Presenter <span class="text-danger">*</span>
                  </div>
                  <v-text-field
                    variant="solo"
                    v-model="formMaterial.presenter"
                    placeholder="Please Fill Presenter"
                    :hide-details="isError(v$.presenter)"
                    :error-messages="getErrorMessages(v$.presenter)"
                  ></v-text-field>
                </v-col>
                <v-col :cols="12">
                  <div class="text-15 text-blueTheme fw-500">
                    Keyword <span class="text-danger">*</span>
                  </div>
                  <v-textarea
                    v-model="formMaterial.keyword"
                    variant="solo"
                    placeholder="Please Fill Keyword"
                    rows="3"
                    max-rows="5"
                    :counter="100"
                    :error-messages="getErrorMessages(v$.keyword)"
                  />
                </v-col>
              </v-row>
            </template>
            <template #4>
              <v-row class="text-left">
                <v-col
                  :cols="12"
                  class="py-3 pl-4 mx-3 my-4 text-15 blue-gradient"
                >
                  <b style="color: #fff">Penyusun</b>
                </v-col>
                <v-col :cols="12">
                  <div class="text-15 text-blueTheme fw-500">
                    Penyusun <span class="text-danger">*</span>
                  </div>
                  <v-autocomplete
                    chips
                    multiple
                    closable-chips
                    hide-selected
                    return-object
                    variant="solo"
                    placeholder="Choose Penyusun"
                    item-title="value"
                    item-value="id"
                    v-model:search="search.penyusun"
                    v-model:model-value="formMaterial.penyusun"
                    :items="listLocal.penyusun"
                    :hide-details="isError(v$.penyusun)"
                    :error-messages="getErrorMessages(v$.penyusun)"
                    @update:modelValue="search.penyusun = ''"
                  >
                    <template v-slot:chip="{ props, item }">
                      <v-chip
                        v-bind="props"
                        :text="item.title"
                        class="custom-chip"
                      ></v-chip>
                    </template>
                    <template v-slot:item="{ props, item }">
                      <v-list-item
                        :title="item.raw.value"
                        v-bind="props"
                        class="py-3 px-6"
                      >
                        <template v-slot:prepend>
                          <v-avatar color="#eaeaea">
                            <img
                              :src="require(`@/v2/assets/icon/people.svg`)"
                            />
                          </v-avatar>
                        </template>
                        <template v-slot:append>
                          <v-icon style="color: #065695">
                            mdi-plus-circle-outline
                          </v-icon>
                        </template>
                        <v-list-item-subtitle>{{
                          item.raw?.jabatanSatker
                        }}</v-list-item-subtitle>
                      </v-list-item>
                    </template>
                  </v-autocomplete>
                </v-col>
              </v-row>
            </template>
            <template #5>
              <v-row>
                <v-col
                  :cols="12"
                  class="py-3 pl-4 mx-3 my-4 text-15 blue-gradient"
                >
                  <b style="color: #fff">Assign Approver</b>
                </v-col>
                <v-col :cols="12">
                  <div class="text-15 text-blueTheme fw-500">
                    Pengaju <span class="text-danger">*</span>
                  </div>
                  <SearchBar
                    v-model="formMaterial.pengaju"
                    v-model:search="search.pengaju"
                    :items="listLocal.pengaju"
                    :appendIcon="true"
                  />
                  <span
                    class="text-danger ml-5 text-12"
                    v-if="!isError(v$.pengaju)"
                  >
                    {{ getErrorMessages(v$.pengaju).join(", ") }}
                  </span>
                </v-col>
              </v-row>
            </template>
          </Steppy>
        </v-card-text>
        <v-card-actions class="d-flex justify-end px-6 py-4">
          <!-- logic cancel and back -->
          <v-btn
            v-if="isStartStep"
            elevation="3"
            class="btn-cancel"
            @click="hide"
          >
            Cancel
          </v-btn>
          <v-btn v-else elevation="3" class="btn-cancel" @click="backStep">
            Back
          </v-btn>
          <!-- logic next and save -->
          <v-btn
            v-if="isEndStep"
            elevation="3"
            class="btn-add"
            @click="save"
            :loading="isLoading"
          >
            Sent
          </v-btn>
          <v-btn v-else elevation="3" class="btn-add" @click="nextStep">
            Next
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </Teleport>
</template>

<script lang="ts" setup>
import FileDragable from "@v2/components/utils/form/FileDragable.vue";
import SearchBar from "@v2/components/utils/dialog/SearchBar.vue";
import baseStore from "@/store";
import { Steppy } from "vue3-steppy";
import { encrypt } from "@/library/CryptoHelper";

import { useVuelidate } from "@vuelidate/core";
import { required, maxLength } from "@vuelidate/validators";
import { getErrorMessages, isError } from "@v2/helpers/validation";
import { ref, getCurrentInstance, computed, watch, onBeforeMount } from "vue";
import { v4 as uuidv4 } from "uuid";
import { TFormMaterial, TSelect } from "@v2/Type.d";
import { responsePromise } from "@v2/helpers/utils";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import clientv2 from "@v2/library/ApiClient";

defineProps({
  title: {
    type: String,
    required: true,
  },
});

const { root } = getCurrentInstance() as any;
const response = responsePromise(root);
const store = useStore();
const route = useRoute();
const idEvent = computed((): string => {
  return route.params.idEvent as string;
});

const documentList = computed(() => store.state.meetingStore.listDocument);

const dialog = ref<boolean>(false);
const loadingPercent = ref<number>(0);
const step = ref(1);
const tabs = computed(() => {
  const local = [
    {
      title: "Step 1",
      iconSuccess: null,
      isValid: true,
    },
    {
      title: "Step 2",
      iconSuccess: null,
      isValid: true,
    },
  ];

  if (formMaterial.value.method == 1) {
    local.push(
      {
        title: "Step 3",
        iconSuccess: null,
        isValid: true,
      },
      {
        title: "Step 4",
        iconSuccess: null,
        isValid: true,
      },
      {
        title: "Step 5",
        iconSuccess: null,
        isValid: true,
      }
    );
  }
  return local;
});
const isLoading = ref<boolean>(false);
const formMaterial = ref<TFormMaterial>({
  method: null,
  idEvent: idEvent.value,
  traceId: uuidv4(),
  file: {
    name: "",
    sizeString: "",
    sizeNumber: 0,
    file: null,
  },
  dokumenTipe: null,
  versi: null,
  topikNama: null,
  satkerPembuat: null,
  ps: null,
  event: null,
  presenter: null,
  keyword: null,
  penyusun: [],
  pengaju: null,
  documentType: null,
});
const rules = computed(() => {
  const local = {
    method: {},
    idEvent: {},
    traceId: {},
    file: {
      name: {},
    },
    dokumenTipe: {},
    versi: {},
    topikNama: {},
    satkerPembuat: {},
    ps: {},
    event: {},
    presenter: {},
    keyword: {},
    penyusun: {},
    pengaju: {},
  };

  if (step.value == 1) {
    local.method = { required };
  }

  if (step.value == 2) {
    local.file = {
      name: { required },
    };
  }

  if (step.value == 3) {
    local.dokumenTipe = { required };
    local.versi = { required };
    local.topikNama = { required, maxLength: maxLength(100) };
    local.satkerPembuat = { required };
    local.ps = { required };
    local.event = { required };
    local.presenter = { required };
    local.keyword = { required, maxLength: maxLength(100) };
  }

  if (step.value == 4) {
    local.penyusun = { required };
  }

  if (step.value == 5) {
    local.pengaju = { required };
  }

  return local;
});
const isEndStep = computed((): boolean => tabs.value.length == step.value);
const isStartStep = computed((): boolean => step.value == 1);
const search = ref<{
  penyusun: string | undefined;
  pengaju: string | undefined;
}>({
  penyusun: undefined,
  pengaju: undefined,
});
const listLocal = ref<{ penyusun: TSelect[]; pengaju: any[] }>({
  penyusun: [],
  pengaju: [],
});

const v$ = useVuelidate(rules, formMaterial);
const emit = defineEmits(["onSuccess"]);

function show(): void {
  v$.value.$reset();
  loadingPercent.value = 0;
  isLoading.value = false;
  formMaterial.value = {
    method: null,
    idEvent: idEvent.value,
    traceId: uuidv4(),
    file: {
      name: "",
      sizeString: "",
      sizeNumber: 0,
      file: null,
    },
    dokumenTipe: null,
    versi: null,
    topikNama: null,
    satkerPembuat: null,
    ps: null,
    event: null,
    presenter: null,
    keyword: null,
    penyusun: [],
    pengaju: null,
    documentType: null,
    // penyetuju: null,
  };
  dialog.value = true;
  step.value = 1;
}

function hide(): void {
  if (isLoading.value === false) {
    dialog.value = false;
  }
}

function save() {
  const maxSize = 150 * 1024 * 1024;
  if (formMaterial.value.file.sizeNumber > maxSize) {
    alert("File size is more than 150MB");
    return;
  }
  v$.value.$validate().then((res) => {
    if (res) {
      isLoading.value = true;
      if (formMaterial.value.method == 1) {
        return saveMaterialApproval();
      } else {
        return saveMaterialNonApproval();
      }
    }
  });
}

function nextStep() {
  v$.value.$validate().then((res) => {
    if (res) {
      if (isEndStep.value) return 0;
      step.value++;
      v$.value.$reset();
    }
  });
}

function backStep() {
  if (isStartStep.value) return 0;
  step.value--;
}

async function saveMaterialApproval() {
  let fileName = formMaterial.value.file.name.split(".");
  fileName.pop();

  const { value } = formMaterial;

  const reqData = {
    idEvent: value.idEvent,
    traceId: value.traceId,
    title: fileName.join("."),
    // documentFile: formMaterial.value.file.file,
    idMEventDocPresentationMaterialTemplate: value.documentType,
    documentTypeId: value.dokumenTipe,
    versi: value.versi,
    documentTopic: value.topikNama,
    presenter: value.presenter,
    keyword: value.keyword,
    programStrategisId: value.ps,
    eventSubTypeListId: value.event,
    MSatkerPembuatId: value.satkerPembuat,
    listPenyusun: value.penyusun,
    idPengaju: value.pengaju,
  };

  const encryptResult = await encrypt(reqData, baseStore);
  const metadata = encryptResult.json;

  store
    .dispatch("meetingStore/uploadMaterialApproval", {
      request: {
        metadata: metadata,
        documentFile: formMaterial.value.file.file,
      },
      onUploadProgress: (progressEvent: any) => {
        var percent = Math.round(
          (progressEvent.loaded * 100) / formMaterial.value.file.sizeNumber
        );
        loadingPercent.value = percent;
      },
    })
    .then((res) => {
      response.success(res, function () {
        dialog.value = false;
        emit("onSuccess");
      });
    })
    .catch(response.error)
    .finally(() => {
      isLoading.value = false;
    });
}

function saveMaterialNonApproval() {
  let fileName = formMaterial.value.file.name.split(".");

  fileName.pop();

  const { value } = formMaterial;

  const reqData = {
    idEvent: value.idEvent,
    traceId: value.traceId,
    title: fileName.join("."),
    documentFile: value.file.file,
    idMEventDocPresentationMaterialTemplate: value.documentType,
  };

  store
    .dispatch("meetingStore/uploadMaterial", {
      request: reqData,
      onUploadProgress: (progressEvent: any) => {
        var percent = Math.round(
          (progressEvent.loaded * 100) / formMaterial.value.file.sizeNumber
        );
        loadingPercent.value = percent;
      },
    })
    .then((res) => {
      response.success(res, function () {
        dialog.value = false;
        emit("onSuccess");
      });
    })
    .catch(response.error)
    .finally(() => {
      isLoading.value = false;
    });
}

function fetchPenyusunList(name: string) {
  if (name.length > 2) {
    const trimmedName = name
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

    const payload = {
      name: trimmedName,
      idEvent: route.params.idEvent,
    };
    clientv2.SearchUserAndGroupMaterial({ data: payload }).then((res) => {
      listLocal.value.penyusun = [...(res as Array<any>)];
      name.includes(";") &&
        res.length &&
        (formMaterial.value.penyusun = [
          ...formMaterial.value.penyusun,
          ...(res as Array<any>).filter(
            (item) => !formMaterial.value.penyusun.some((p) => p.id === item.id)
          ),
        ]);
      name.includes(";") && res.length && (search.value.penyusun = ""); // Clear the search input after getting results
    });
  }
}

function fetchPengajuList(name: string) {
  const payload = {
    name: name,
    idEvent: route.params.idEvent,
    idMEventDocPresentationMaterialTemplate: formMaterial.value.documentType,
  };
  store
    .dispatch(
      "materialStore/searchEventPresentationMaterialByUsername",
      payload
    )
    .then((resp: TSelect[]) => {
      listLocal.value.pengaju = resp;
    });
}

watch(
  () => formMaterial.value.method,
  () => {
    formMaterial.value.file = {
      name: "",
      sizeString: "",
      sizeNumber: 0,
      file: null,
    };
    formMaterial.value.dokumenTipe = null;
    formMaterial.value.versi = null;
    formMaterial.value.topikNama = null;
    formMaterial.value.satkerPembuat = null;
    formMaterial.value.ps = null;
    formMaterial.value.event = null;
    formMaterial.value.presenter = null;
    formMaterial.value.keyword = null;
    formMaterial.value.penyusun = [];
    formMaterial.value.pengaju = null;
    // formMaterial.value.penyetuju = null;
  }
);

watch(
  () => search.value.penyusun,
  (val) => {
    if (val) {
      fetchPenyusunList(val);
    }
  }
);

watch(
  () => search.value.pengaju,
  (val) => {
    if (val) {
      fetchPengajuList(val);
    }
  }
);

watch(
  () => step.value,
  (val) => {
    if (val === 4) {
      fetchPenyusunList("a");
    }

    if (val === 5) {
      fetchPengajuList("a");
    }
  }
);

onBeforeMount(() => {
  store.dispatch("meetingStore/getDocumentList", idEvent.value);
  store.dispatch("meetingStore/getMaterialMethod");
  store.dispatch("meetingStore/getTypeDocument");
  store.dispatch("meetingStore/getSatkerPembuat");
  store.dispatch("meetingStore/getMaterialPS");
  store.dispatch("meetingStore/getMaterialEvent");
  store.dispatch("meetingStore/getEventMember", idEvent.value);
});
</script>

<style scoped>
.btn-create {
  color: #065695;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
}

.btn-cancel {
  background: linear-gradient(#fff -46.47%, #fff 157.9%);
  border-radius: 10px;
  padding-left: 15px;
  padding-right: 15px;
  font-weight: 800;
  color: #065695 !important;
}

.btn-add {
  background: linear-gradient(#065695 -46.47%, #267dc2 157.9%);
  border-radius: 10px;
  padding-left: 15px;
  padding-right: 15px;
  font-weight: 800;
  width: 120px;
  color: white !important;
}

.blue-gradient {
  background: linear-gradient(
    89.96deg,
    #065695 35.16%,
    rgba(255, 255, 255, 0) 101.03%
  );
  border-radius: 5px;
}

.custom-chip {
  color: white !important;
  background-color: #267dc2 !important;
  font-size: 15px !important;
  padding: 15px !important;
}

:deep(.v-field.v-field--appended) {
  border-radius: 12px !important;
}
</style>

<style lang="scss" scoped>
:deep(.kelas-1 .steppy) {
  margin-left: 15vw;
  margin-right: 15vw;
}

:deep(.kelas-2 .steppy) {
  margin-left: 5vw;
  margin-right: 5vw;
}

:deep(.number) {
  display: none !important;
}

:deep(.wrapper-steppy) {
  padding: 25px 0px 0px 0px !important;
}

:deep(.steppy-pane) {
  box-shadow: none !important;
  text-align: left !important;
  padding: 0px;
  margin-bottom: 5px;
}

:deep(.steppy-item.success .steppy-item-counter) {
  border: 8px solid #267dc2 !important;
}

:deep(.steppy-item-counter) {
  height: 25px !important;
  width: 25px !important;
  border: 5px solid grey !important;
  background-color: white !important;
}

:deep(.current .steppy-item-counter) {
  border: 5px solid #065695 !important;
}

:deep(.steppy-item.success .steppy-item-counter .icon-success) {
  width: 15px !important;
  height: 15px !important;
  fill: white !important;
  background-color: #267dc2 !important;
  border-radius: 50% !important;
}

:deep(.steppy-item-title) {
  font-size: 14px !important;
  font-weight: 900 !important;
  color: #3a416f !important;
  white-space: nowrap !important;
}

:deep(.steppy-progress) {
  background: #d9d9d9 !important;
  height: 3px !important;
}

:deep(.steppy-progress-bar) {
  background: #267dc2 !important;
  height: 3px !important;
}
:deep(.controls) {
  display: none !important;
}
.hide {
  display: none;
}

.show {
  display: show;
}
</style>
