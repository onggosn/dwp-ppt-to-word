<template>
  <v-form @submit.prevent="submitForm">
    <div class="d-flex flex-wrap justify-space-between ml-5 mr-5 mt-10">
      <v-sheet class="pt-4 pb-4 pl-2 mb-4 text-14 blue-gradient" width="100%">
        <b style="color: #fff">Upload Document</b>
      </v-sheet>
      <v-sheet width="100%">
        <p class="font-weight-medium mb-2 text-blueTheme">
          Document Type <span style="color: red">*</span>
        </p>
        <api-loader :apiMethod="documentType">
          <template v-slot:default="props">
            <v-autocomplete
              class="rounded-lg"
              placeholder="Pilih Type Dokumen"
              v-model="state._typeDocument"
              :items="props.response.responseData"
              item-title="value"
              item-value="id"
              :error-messages="
                v$._typeDocument.$errors.map((e) => 'Wajib diisi')
              "
              required
              variant="solo"
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
      <v-sheet width="100%">
        <p class="font-weight-bold mb-4 mt-2 text-blueTheme">Metadata</p>
      </v-sheet>
      <v-sheet width="100%">
        <p class="font-weight-medium mb-2 text-blueTheme">Nama Dokumen</p>
        <v-textarea
          rows="3"
          max-rows="5"
          v-model="state._namaDokumen"
          placeholder="Masukan deskripsi workspace"
          :error-messages="
            v$._namaDokumen.$errors.map((e) => 'Hanya huruf dan angka')
          "
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
          Proses Bisnis <span style="color: red">*</span>
        </p>
        <api-loader :apiMethod="prosesBisnis">
          <template v-slot:default="props">
            <v-autocomplete
              v-model="state._prosesBisnis"
              @update:modelValue="updateProsesBisnis"
              :error-messages="
                v$._prosesBisnis.$errors.map((e) => 'Wajib diisi')
              "
              required
              class="rounded-lg"
              placeholder="Pilih Proses Bisnis"
              :items="props.response"
              item-title="value"
              item-value="id"
              variant="solo"
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
          Kode PN/IN/RP <span style="color: red">*</span>
        </p>
        <v-text-field
          v-model="state._kodePNIN"
          :error-messages="v$._kodePNIN.$errors.map((e) => 'Wajib diisi')"
          required
          class="rounded-lg"
          placeholder="Masukkan Kode PN/IN/RP"
          variant="solo"
        ></v-text-field>
      </v-sheet>
      <v-sheet width="52%" class="mt-5">
        <p class="font-weight-medium mb-2 text-blueTheme">
          PS <span style="color: red">*</span>
        </p>
        <api-loader :apiMethod="programStrategis">
          <template v-slot:default="props">
            <v-sheet class="d-flex align-content-start flex-wrap">
              <v-sheet
                v-for="item in props.response"
                :key="item.id"
                style="padding: 0 !important; margin: 0 !important"
              >
                <!-- <v-checkbox
                  :label="item.value"
                  :value="item.id"
                  v-model="state._programStrategis"
                  @update:modelValue="updateProgramStrategis"
                  required
                  color="success"
                /> -->
                <v-checkbox
                  :label="item.value"
                  :value="item.id"
                  v-model="state._programStrategis"
                  required
                  color="success"
                />
              </v-sheet>
            </v-sheet>
            <p
              v-if="v$._programStrategis.$error"
              style="
                color: red;
                font-size: 12px;
                line-height: 12px;
                word-break: break-word;
                word-wrap: break-word;
                -webkit-hyphens: auto;
                hyphens: auto;
                transition-duration: 150ms;
              "
            >
              Wajib diisi
            </p>
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
      <v-sheet width="100%" class="mt-5">
        <p class="font-weight-medium mb-2 text-blueTheme">
          Kode IKU/ICK <span style="color: red">*</span>
        </p>
        <v-text-field
          v-model="state._kodeIKUICK"
          :error-messages="v$._kodeIKUICK.$errors.map((e) => 'Wajib diisi')"
          required
          class="rounded-lg"
          placeholder="Masukkan Kode IKU/ICK"
          variant="solo"
        ></v-text-field>
      </v-sheet>
      <v-sheet width="49%" class="mt-5">
        <p class="font-weight-medium mb-2 text-blueTheme">
          Sifat Dokumen <span style="color: red">*</span>
        </p>
        <api-loader :apiMethod="sifatDokumen">
          <template v-slot:default="props">
            <v-autocomplete
              v-model="state._sifatDokumen"
              @update:modelValue="updateSifatDokumen"
              :error-messages="
                v$._sifatDokumen.$errors.map((e) => 'Wajib diisi')
              "
              required
              class="rounded-lg"
              placeholder="Pilih Sifat Dokumen"
              :items="props.response"
              item-title="value"
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
          Event <span style="color: red">*</span>
        </p>
        <api-loader :apiMethod="eventName">
          <template v-slot:default="props">
            <v-autocomplete
              v-model="state._eventName"
              @update:modelValue="updateEventName"
              :error-messages="v$._eventName.$errors.map((e) => 'Wajib diisi')"
              required
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

      <v-sheet width="100%" class="mt-5">
        <p class="font-weight-medium mb-2 text-blueTheme">
          Batas Waktu <span style="color: red">*</span>
        </p>
        <VueDatePicker
          auto-apply
          v-model="state._batasWaktu"
          :month-change-on-scroll="false"
          :enable-time-picker="false"
          :min-date="new Date()"
        >
          <template #trigger>
            <v-text-field
              readonly
              variant="solo"
              placeholder="DD/MM/YYYY"
              append-inner-icon="mdi-calendar-today"
              class="cursor-pointer"
              :error-messages="v$._batasWaktu.$errors.map((e) => 'Wajib diisi')"
              :value="$filters.formatTimeEngToIndNoDays(state._batasWaktu)"
            ></v-text-field>
          </template>
        </VueDatePicker>
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
        <p class="font-weight-medium mb-2 text-blueTheme">Keterangan</p>
        <v-textarea
          v-model="state._keterangan"
          rows="3"
          max-rows="5"
          placeholder="Masukkan Keterangan"
          variant="solo"
          :counter="500"
        ></v-textarea>
      </v-sheet>
      <v-sheet width="100%" class="mt-5">
        <div class="d-flex flex-row-reverse mb-6">
          <v-btn type="submit" class="btn-color-process">Next</v-btn>
          <v-btn @click="updateStep" class="mr-1 btn-color-white">Back</v-btn>
        </div>
      </v-sheet>
    </div>
  </v-form>
</template>

<script setup lang="ts">
import { reactive, defineEmits, defineProps } from "vue";
import ApiLoader from "@/components/ApiLoader.vue";
import { useVuelidate } from "@vuelidate/core";
import { required, helpers } from "@vuelidate/validators";
import { mGetDocumentSupportTypeByIdMethod } from "@/models/upload";

import {
  mListSatker,
  mProsesBisnis,
  mProgramStrategis,
  mSifatDokumen,
  mEventName,
} from "@/models/upload";

const props = defineProps({
  methodAddDocument: { type: Number, required: true, default: 1 },
  idTaskTemplate: { type: Number, required: true, default: -1 },
});

const emits = defineEmits(["updateStep", "updateMetadata"]);
const updateStep = () => emits("updateStep", 1);

const initialState = {
  _typeDocument: null,
  _namaDokumen: "",
  _listSatker: null,
  _prosesBisnis: null,
  _programStrategis: [],
  _kodePNIN: null,
  _kodeIKUICK: null,
  _sifatDokumen: null,
  _eventName: null,
  _keyword: null,
  _keterangan: "",
  _batasWaktu: null,
};

const state = reactive({
  ...initialState,
});

const alphaNumCustom = helpers.regex(/^[a-zA-Z0-9\-_()\s]+$/i);

const rules = {
  _typeDocument: { required },
  _namaDokumen: { alphaNumCustom },
  _listSatker: { required },
  _prosesBisnis: { required },
  _programStrategis: { required },
  _kodePNIN: { required },
  _sifatDokumen: { required },
  _eventName: { required },
  _keyword: { required },
  _keterangan: {},
  _batasWaktu: { required },
  _kodeIKUICK: { required },
};
const v$ = useVuelidate(rules, state);

const documentType = () =>
  mGetDocumentSupportTypeByIdMethod(
    props.methodAddDocument,
    props.idTaskTemplate
  );

const listSatker = () => mListSatker();
const updateListSatker = () => {
  const html = document.getElementById("inputListSatker") as HTMLElement;
  html.blur();
};

const prosesBisnis = () => mProsesBisnis();
const updateProsesBisnis = () => {
  undefined;
};

const programStrategis = () => mProgramStrategis();

const sifatDokumen = () => mSifatDokumen();
const updateSifatDokumen = () => {
  undefined;
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

// const filter = (evt) => {
//   evt = evt ? evt : window.event;
//   let expect = evt.target.value.toString() + evt.key.toString();

//   if (!/^[+]?[0-9]*?[0-9]*$/.test(expect)) {
//     evt.preventDefault();
//   } else {
//     return true;
//   }
// };
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
</style>
