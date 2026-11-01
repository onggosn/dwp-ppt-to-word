<template>
  <v-form @submit.prevent="submitForm">
    <div class="d-flex flex-wrap justify-space-between ml-5 mr-5 mt-10">
      <v-sheet class="pt-4 pb-4 pl-2 mb-4 text-14 blue-gradient" width="100%">
        <b style="color: #fff">Edit Metadata</b>
      </v-sheet>
      <v-sheet width="100%">
        <p class="font-weight-medium mb-2 text-blueTheme">
          Document Type <span style="color: red">*</span>
        </p>
        <v-autocomplete
          class="rounded-lg"
          placeholder="Pilih Type Dokumen"
          disabled
          v-model="state._typeDocumentName"
          :items="[]"
          item-title="value"
          item-value="id"
          :error-messages="
            v$._typeDocumentName.$errors.map((e) => 'Wajib diisi')
          "
          required
          variant="solo"
        ></v-autocomplete>
      </v-sheet>
      <v-sheet width="100%">
        <p class="font-weight-bold mb-4 mt-2 text-blueTheme">Metadata</p>
      </v-sheet>
      <v-sheet width="100%">
        <p class="font-weight-medium mb-2 text-blueTheme">
          Nama Dokumen Sesuai Kodifikasi <span style="color: red">*</span>
        </p>
        <v-textarea
          rows="3"
          max-rows="5"
          disabled
          v-model="state._namaDokumen"
          placeholder="Masukan deskripsi workspace"
          variant="solo"
          :counter="190"
          @keydown.enter.prevent=""
        ></v-textarea>
      </v-sheet>
      <v-sheet width="100%">
        <p class="font-weight-medium mb-2 text-blueTheme">
          Satker Pembuat <span style="color: red">*</span>
        </p>
        <api-loader :apiMethod="listSatker">
          <template v-slot:default="props">
            <v-autocomplete
              id="inputListSatker"
              v-model="state._listSatker"
              @update:modelValue="updateListSatker"
              :error-messages="v$._listSatker.$errors.map((e) => 'Wajib diisi')"
              required
              class="rounded-lg"
              placeholder="Pilih Satker Pembuat"
              :items="props.response"
              item-title="value"
              item-value="id"
              variant="solo"
              chips
              multiple
              closable-chips
              single-line
              hide-no-data
              hide-selected
            ></v-autocomplete>
          </template>
          <template v-slot:loading>
            <free-style-shimmer
              width="100%"
              height="3rem"
              border-radius="5px"
            />
          </template>
        </api-loader>
      </v-sheet>
      <v-sheet width="49%" class="mt-5">
        <p class="font-weight-medium mb-2 text-blueTheme">
          Event <span style="color: red">*</span>
        </p>
        <api-loader :apiMethod="eventName">
          <template v-slot:default="props">
            <v-autocomplete
              v-model="state._eventName"
              @update:modelValue="updateEventName"
              :error-messages="v$._eventName.$errors.map((e) => 'Wajib diisi')"
              required
              disabled
              class="rounded-lg"
              placeholder="Pilih Event"
              :items="props.response"
              item-title="eventName"
              item-value="id"
              variant="solo"
            ></v-autocomplete
          ></template>
          <template v-slot:loading>
            <free-style-shimmer
              width="100%"
              height="3rem"
              border-radius="5px"
            /> </template
        ></api-loader>
      </v-sheet>
      <v-sheet width="49%" class="mt-5">
        <p class="font-weight-medium mb-2 text-blueTheme">
          Presenter <span style="color: red">*</span>
        </p>
        <v-text-field
          v-model="state._presenterName"
          :error-messages="v$._presenterName.$errors.map((e) => 'Wajib diisi')"
          placeholder="Presenter Name"
          variant="solo"
          required
        ></v-text-field>
      </v-sheet>
      <v-sheet width="100%" class="mt-5">
        <p class="font-weight-medium mb-2 text-blueTheme">
          Keyword <span style="color: red">*</span>
        </p>
        <v-textarea
          v-model="state._keyword"
          :error-messages="v$._keyword.$errors.map((e) => 'Wajib diisi')"
          required
          rows="3"
          max-rows="5"
          placeholder="Masukkan Keyword"
          variant="solo"
          :counter="100"
        ></v-textarea>
      </v-sheet>
      <v-sheet width="100%" class="mt-5">
        <div class="d-flex flex-row-reverse mb-6">
          <v-btn type="submit" class="btn-color-process">Next</v-btn>
          <v-btn @click="updateStep" class="mr-1 btn-color-white">Close</v-btn>
        </div>
      </v-sheet>
    </div>
  </v-form>
</template>

<script setup lang="ts">
import { reactive, defineEmits, defineProps } from "vue";
import ApiLoader from "@/components/ApiLoader.vue";
import { useVuelidate } from "@vuelidate/core";
import { required } from "@vuelidate/validators";

import { mListSatker, mEventName } from "@/models/upload";

const props = defineProps({
  document: { type: Object, required: true },
  initialState: Object,
});
const emits = defineEmits(["updateStep", "updateMetadata"]);
const updateStep = () => emits("updateStep", "Close");

const initialState = {
  _typeDocumentName: props.initialState?.documentSupportTypeName,
  _typeDocument: props.initialState?.idDocumentSupportType,
  _namaDokumen: props.initialState?.topicName,
  _listSatker: props.initialState?.listSatkerPembuat,
  _prosesBisnis: props.initialState?.idMBusinessProcess,
  _eventName: props.initialState?.idMEvent,
  _keyword: props.initialState?.keyword,
  _presenterName: props.initialState?.presenter,
};

const state = reactive({
  ...initialState,
});

const rules = {
  _typeDocumentName: { required },
  _typeDocument: { required },
  _namaDokumen: { required },
  _listSatker: { required },
  _prosesBisnis: {},
  _eventName: {},
  _keyword: { required },
  _presenterName: { required },
};
const v$ = useVuelidate(rules, state);

const listSatker = () => mListSatker();
const updateListSatker = () => {
  const html = document.getElementById("inputListSatker") as HTMLElement;
  html.blur();
};

const eventName = () => mEventName();
const updateEventName = () => {
  undefined;
};

const submitForm = () => {
  v$.value.$validate().then((valid) => {
    if (valid) {
      emits("updateMetadata", state);
    }
  });
};
</script>

<style scoped>
.text-blueTheme {
  color: #3a416f;
}

:deep(.v-chip__close) {
  color: white !important;
}
:deep(.v-chip) {
  color: white !important;
  background: #277dc2 !important;
}

.btn-color-process {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: #fdfdfd;
  border-radius: 10px;
  padding-left: 15px;
  padding-right: 15px;
  margin-left: 10px;
  font-weight: 800;
}

.btn-color-white {
  background: white;
  color: #d6212a;
  border-radius: 10px;
  padding-left: 15px;
  padding-right: 15px;
  margin-left: 10px;
  font-weight: 800;
}

.blue-gradient {
  background: linear-gradient(
    89.96deg,
    #065695 35.16%,
    rgba(255, 255, 255, 0) 101.03%
  );
  border-radius: 5px;
}
:deep(.v-field--disabled) {
  background: #dfdfdf;
}
</style>
