<template>
  <v-btn variant="outlined" class="btn-create" @click="show">
    {{ title }}
  </v-btn>
  <Teleport to="body">
    <v-dialog v-model="dialog" :max-width="800" persistent>
      <v-card class="mb-5 border-radius-dwp">
        <v-card-title class="d-flex justify-center align-center">
          <div class="text-18 text-blueTheme fw-500 mt-2 mb-2">
            Add Document
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
          <v-row>
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-500">Title</div>
              <v-text-field
                variant="solo"
                v-model="file.name"
                placeholder="Insert Title"
                :error-messages="getErrorMessages(v$.file)"
                readonly
              ></v-text-field>
            </v-col>
            <v-col cols="12" class="py-1">
              <div class="text-15 text-blueTheme fw-500">Upload File</div>
              <FileDragable
                v-model="file"
                :formatFile="['.pdf', '.ppt', '.pptx', '.doc', '.docx']"
                :loadingPercent="loadingPercent"
              />
              <span class="text-danger pl-3 text-12">
                {{ getErrorMessages(v$.file).toString() }}
              </span>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions class="d-flex justify-end px-6 py-4">
          <v-btn elevation="3" class="btn-cancel" @click="hide"> Cancel </v-btn>
          <v-btn
            elevation="3"
            class="btn-add"
            @click="save"
            :loading="isLoading"
          >
            Add
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </Teleport>
</template>

<script lang="ts" setup>
import FileDragable from "@v2/components/utils/form/FileDragable.vue";

import { useVuelidate } from "@vuelidate/core";
import { required } from "@vuelidate/validators";
import { getErrorMessages } from "@v2/helpers/validation";
import { ref, getCurrentInstance } from "vue";
import { v4 as uuidv4 } from "uuid";
import { TFileDragable, THasilPembahasan } from "@v2/Type.d";
import { responsePromise } from "@v2/helpers/utils";
import { useStore } from "vuex";
import { computed } from "vue";
import { useRoute } from "vue-router";

const { root } = getCurrentInstance() as any;
const response = responsePromise(root);
const store = useStore();
const route = useRoute();
const dialog = ref<boolean>(false);
const loadingPercent = ref<number>(0);
defineProps({
  title: {
    type: String,
    required: true,
  },
});

const file = ref<TFileDragable>({
  name: "",
  sizeString: "",
  sizeNumber: 0,
  file: null,
});
const isLoading = ref<boolean>(false);

const idEvent = computed((): string => {
  return route.params.idEvent as string;
});

const rules = {
  file: { required },
};

const v$ = useVuelidate(rules, file);
const emit = defineEmits(["onSuccess"]);

function show(): void {
  v$.value.$reset();
  loadingPercent.value = 0;
  isLoading.value = false;
  file.value = {
    name: "",
    sizeString: "",
    sizeNumber: 0,
    file: null,
  };
  dialog.value = true;
}

function hide(): void {
  if (isLoading.value === false) {
    dialog.value = false;
  }
}

function save() {
  const maxSize = 150 * 1024 * 1024;
  if (file.value.sizeNumber > maxSize) {
    alert("File size is more than 150MB");
    return;
  }
  v$.value.$validate().then((res) => {
    if (res) {
      isLoading.value = true;
      let fileName = file.value.name.split(".");
      fileName.pop();
      const reqData: THasilPembahasan = {
        idEvent: idEvent.value,
        traceId: uuidv4(),
        title: fileName.join("."),
        documentFile: file.value.file,
      };

      uploadResult(reqData);
    }
  });
}

function uploadResult(payload: THasilPembahasan) {
  store
    .dispatch("meetingStore/uploadMeetingResult", {
      request: payload,
      onUploadProgress: (progressEvent: any) => {
        var percent = Math.round(
          (progressEvent.loaded * 100) / file.value.sizeNumber
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
</script>

<style>
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

:deep(.v-field.v-field--appended) {
  border-radius: 12px !important;
}
</style>
