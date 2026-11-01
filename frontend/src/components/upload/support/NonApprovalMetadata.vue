<script setup lang="ts">
import { reactive, defineEmits } from "vue";
import ApiLoader from "@/components/ApiLoader.vue";
import { useVuelidate } from "@vuelidate/core";
import { required } from "@vuelidate/validators";
import { mProgramStrategis, mEventName, mListSatker } from "@/models/upload";

const listSatker = () => mListSatker();
const programStrategis = () => mProgramStrategis();
const eventName = () => mEventName();
const emits = defineEmits(["updateStep", "updateMetadataNonApproval"]);

const initialState = {
  _satkerName: null,
  _programStrategis: null,
  _eventName: null,
  _presenterName: null,
  _keyword: null,
};

const state = reactive({
  ...initialState,
});

const rules = {
  _satkerName: { required },
  _programStrategis: { required },
  _eventName: { required },
  _presenterName: { required },
  _keyword: { required },
};
const v$ = useVuelidate(rules, state);

const submitForm = () => {
  v$.value.$validate().then((valid) => {
    if (valid) {
      emits("updateMetadataNonApproval", state);
    }
  });
};

const back = () => {
  emits("updateStep", "NONAPPROVAL");
};
</script>
<template>
  <v-form @submit.prevent="submitForm">
    <div class="d-flex flex-wrap justify-space-between mb-6 mt-5 pa-8">
      <v-sheet class="pt-4 pb-4 pl-2 mb-4 blue-gradient" width="100%">
        <b style="color: #fff">Upload Document</b>
      </v-sheet>

      <v-sheet width="49%" class="">
        <p class="font-weight-bold mb-2 text-greyTheme">
          Satker Pembuat <span style="color: red">*</span>
        </p>
        <api-loader :apiMethod="listSatker">
          <template v-slot:default="props">
            <!-- <pre>{{ props }}</pre> -->
            <v-autocomplete
              v-model="state._satkerName"
              class="rounded-lg"
              placeholder="Pilih Satker Pembuat"
              :error-messages="v$._satkerName.$errors.map((e) => 'Wajib diisi')"
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
      <v-sheet width="49%">
        <p class="font-weight-bold mb-2 text-greyTheme">
          PS <span style="color: red">*</span>
        </p>
        <api-loader :apiMethod="programStrategis">
          <template v-slot:default="props">
            <!-- <pre>{{ props }}</pre> -->
            <v-autocomplete
              v-model="state._programStrategis"
              :error-messages="
                v$._programStrategis.$errors.map((e) => 'Wajib diisi')
              "
              class="rounded-lg"
              placeholder="Pilih Program Strategis"
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
      <v-sheet width="49%">
        <p class="font-weight-bold mb-2 text-greyTheme">
          Event <span style="color: red">*</span>
        </p>
        <api-loader :apiMethod="eventName">
          <template v-slot:default="props">
            <!-- <pre>{{ props }}</pre> -->
            <v-autocomplete
              v-model="state._eventName"
              :error-messages="v$._eventName.$errors.map((e) => 'Wajib diisi')"
              class="rounded-lg"
              placeholder="Pilih Event"
              :items="props.response"
              item-title="eventName"
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
      <v-sheet width="49%">
        <p class="font-weight-bold mb-2 text-greyTheme">
          Presenter <span style="color: red">*</span>
        </p>
        <v-text-field
          v-model="state._presenterName"
          :error-messages="v$._presenterName.$errors.map((e) => 'Wajib diisi')"
          placeholder="Presenter Name"
          variant="solo"
        ></v-text-field>
      </v-sheet>
      <v-sheet width="100%">
        <p class="font-weight-bold mb-2 text-greyTheme">
          Keyword <span style="color: red">*</span>
        </p>
        <v-textarea
          v-model="state._keyword"
          :error-messages="v$._keyword.$errors.map((e) => 'Wajib diisi')"
          placeholder="Masukan Keyword"
          variant="solo"
        ></v-textarea>
      </v-sheet>
      <v-sheet width="100%" style="text-align-last: end">
        <v-spacer></v-spacer>
        <v-btn
          elevation="3"
          style="
            background: linear-gradient(#fff -46.47%, #fff 157.9%);
            border-radius: 10px;
            padding-left: 15px;
            padding-right: 15px;
            font-weight: 800;
            color: red;
          "
          @click="back"
        >
          Back
        </v-btn>
        <v-btn
          elevation="3"
          class="btn-color-process mr-4"
          style="
            border-radius: 10px;
            padding-left: 15px;
            padding-right: 15px;
            margin-left: 10px;
            font-weight: 800;
            color: white;
          "
          type="submit"
        >
          Create
        </v-btn>
      </v-sheet>
    </div>
  </v-form>
</template>

<style scoped>
.btn-color-process {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: #fdfdfd;
}

.btn-color-process2 {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: #fdfdfd;
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
