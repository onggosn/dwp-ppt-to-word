<template>
  <v-form @submit.prevent="submitForm" class="pa-6">
    <div class="d-flex flex-wrap justify-space-between mb-6">
      <v-sheet class="pt-4 pb-4 pl-2 mb-4 blue-gradient" width="100%">
        <b style="color: #fff">Assign Approver </b>
      </v-sheet>
      <v-sheet width="100%">
        <p class="font-weight-bold mb-2 text-greyTheme">
          Penyusun <span style="color: red">*</span>
        </p>

        <api-loader :apiMethod="mListPenyusun">
          <template v-slot:default="props">
            <!-- <pre>{{ props.response }}</pre> -->
            <v-autocomplete
              id="inputListPenyusun"
              v-model="state._penyusun"
              :items="props.response"
              item-title="name"
              return-object
              @update:modelValue="updateListPenyusun"
              :error-messages="v$._penyusun.$errors.map((e) => 'Wajib diisi')"
              chips
              hide-details
              hide-no-data
              hide-selected
              closable-chips
              color="pink"
              label="Pilih Penyusun"
              multiple
              single-line
              variant="solo"
              class="mb-5"
            >
              <template v-slot:item="{ props, item }">
                <v-list-item
                  v-bind="props"
                  :title="item?.raw?.name"
                  :subtitle="item?.raw?.email"
                ></v-list-item>
              </template>
            </v-autocomplete>
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
          Pengaju <span style="color: red">*</span>
        </p>
        <api-loader :apiMethod="mListTaskMemberExcludeGroupMember">
          <template v-slot:default="props">
            <!-- <pre>{{ props.response }}</pre> -->
            <v-autocomplete
              v-model="state._pengaju"
              :items="props.response"
              item-title="name"
              item-value="username"
              :error-messages="v$._pengaju.$errors.map((e) => 'Wajib diisi')"
              hide-details
              hide-no-data
              hide-selected
              color="pink"
              label="Pilih Pengaju"
              single-line
              variant="solo"
              class="mb-5"
            >
              <template v-slot:item="{ props, item }">
                <v-list-item
                  v-bind="props"
                  :title="item?.raw?.name"
                  :subtitle="item?.raw?.email"
                ></v-list-item>
              </template>
            </v-autocomplete>
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
          Penyetuju <span style="color: red">*</span>
        </p>
        <api-loader :apiMethod="mListTaskMemberExcludeGroupMember">
          <template v-slot:default="props">
            <!-- <pre>{{ props.response }}</pre> -->
            <v-autocomplete
              v-model="state._penyetuju"
              :items="props.response"
              item-title="name"
              item-value="username"
              @update:modelValue="updatePenyetuju"
              :error-messages="v$._penyetuju.$errors.map((e) => 'Wajib diisi')"
              hide-details
              hide-no-data
              hide-selected
              color="pink"
              label="Pilih Penyetuju"
              single-line
              variant="solo"
              class="mb-5"
            >
              <template v-slot:item="{ props, item }">
                <v-list-item
                  v-bind="props"
                  :title="item?.raw?.name"
                  :subtitle="item?.raw?.email"
                ></v-list-item>
              </template>
            </v-autocomplete>
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
      <v-sheet width="100%" style="text-align-last: end">
        <v-spacer></v-spacer>
        <v-btn class="btn-color-white" elevation="3" @click="updateStep">
          Back
        </v-btn>
        <v-btn elevation="3" class="btn-color-process mr-4" type="submit">
          Create
        </v-btn>
      </v-sheet>
    </div>
  </v-form>
</template>

<script setup lang="ts">
import { required } from "@vuelidate/validators";
import {
  mListPenyusun,
  mListTaskMemberExcludeGroupMember,
} from "@/models/upload";
import { reactive, defineEmits } from "vue";
import { useVuelidate } from "@vuelidate/core";
import ApiLoader from "@/components/ApiLoader.vue";

const emits = defineEmits(["updateStep", "updateApproverDocumentApproval"]);
const updateStep = () => emits("updateStep", "APPROVALMETADATA");

const initialState = {
  _penyusun: null,
  _pengaju: null,
  _penyetuju: null,
};

const state = reactive({
  ...initialState,
});

const rules = {
  _penyusun: { required },
  _pengaju: { required },
  _penyetuju: { required },
};
const v$ = useVuelidate(rules, state);

const updateListPenyusun = () => {
  document.getElementById("inputListPenyusun")?.blur();
};

const updatePenyetuju = () => {
  undefined;
};

const submitForm = () => {
  v$.value.$validate().then((valid) => {
    if (valid) {
      emits("updateApproverDocumentApproval", state);
    }
  });
};
</script>

<style scoped>
.btn-color-process {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: #fdfdfd;
  border-radius: 10px;
  padding-left: 15px;
  padding-right: 15px;
  margin-left: 10px;
  font-weight: 800;
  color: ;
}

.btn-color-white {
  background: white;
  color: #d6212a;
  border-radius: 10px;
  padding-left: 15px;
  padding-right: 15px;
  margin-left: 10px;
  font-weight: 800;
  color: ;
}
.blue-gradient {
  background: linear-gradient(
    89.96deg,
    #065695 35.16%,
    rgba(255, 255, 255, 0) 101.03%
  );
  border-radius: 5px;
}
:deep(.v-chip__close) {
  color: white !important;
}
:deep(.v-chip) {
  color: white !important;
  background: #277dc2 !important;
}
</style>
