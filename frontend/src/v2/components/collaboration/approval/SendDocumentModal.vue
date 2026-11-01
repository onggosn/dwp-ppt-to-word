<template>
  <Teleport to="body">
    <v-dialog v-model="dialog" max-width="800" persistent>
      <v-card class="border-radius-dwp h-100">
        <v-card-title class="d-flex justify-center align-center">
          <div class="pb-1 text-left text-darkBlue font-weight-bold">
            Send Document
          </div>
          <v-btn
            density="default"
            icon="mdi-close"
            variant="text"
            class="btn-close"
            @click="onclose"
          />
        </v-card-title>
        <hr class="line my-3 d-block pb-1" />
        <v-card-text>
          <Steppy v-model:step="step" :tabs="tabs">
            <template #1>
              <v-row>
                <v-col :cols="12"
                  ><TextBlueGradient text="Nomor Siaran Pers"
                /></v-col>
                <v-col :cols="12">
                  <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
                    Nomor<span class="text-danger">*</span>
                  </p>
                  <v-text-field
                    v-model="state.nomorSiaranPers"
                    variant="solo"
                    placeholder="ex. No.27/194/Dkom"
                    class="px-2 mt-1 border-radius-dwp"
                    :error-messages="
                      v$.nomorSiaranPers.$errors.map((e) => e.$message)
                    "
                    @input="v$.nomorSiaranPers.$touch()"
                  ></v-text-field>
                </v-col>
              </v-row>
            </template>
            <template #2>
              <v-row>
                <v-col :cols="12"><TextBlueGradient text="Assign" /></v-col>
                <v-col :cols="12">
                  <p
                    class="ml-2 pb-1 mb-1 text-left text-darkBlue font-weight-bold"
                  >
                    Penyetuju<span class="text-danger">*</span>
                  </p>
                  <SearchBar
                    v-model="state.penyetuju"
                    class="px-2"
                    :items="props.searchItem"
                    :appendIcon="true"
                    :isRequired="true"
                    :error-messages="
                      v$.penyetuju.$errors.map((e) => e.$message)
                    "
                    @input="v$.penyetuju.$touch()"
                  />
                </v-col>
              </v-row>
            </template>
          </Steppy>
        </v-card-text>
        <v-card-actions class="mt-n4">
          <div class="d-flex w-100 justify-end mb-4 mr-4">
            <v-btn
              v-if="step === 1"
              elevation="3"
              class="btn-cancel"
              @click="onclose"
              :loading="onLoading"
            >
              Cancel
            </v-btn>
            <v-btn
              v-else
              elevation="3"
              class="btn-cancel"
              @click="backStep"
              :loading="onLoading"
            >
              Back
            </v-btn>
            <v-btn
              v-if="step !== tabs.length"
              @click="nextStep"
              type="submit"
              class="ml-2 rounded-lg font-weight-bold primary-gradient p-2 mr-2"
              :loading="onLoading"
            >
              Next
            </v-btn>
            <v-btn
              v-else
              @click="submitDocument"
              type="submit"
              class="ml-2 rounded-lg font-weight-bold primary-gradient mr-2"
              :loading="onLoading"
            >
              Send
            </v-btn>
          </div>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useStore } from "vuex";
import SearchBar from "@v2/components/utils/dialog/SearchBar.vue";
import TextBlueGradient from "../../utils/text/TextBlueGradient.vue";
import { Steppy } from "vue3-steppy";
import useVuelidate from "@vuelidate/core";
import { required, helpers } from "@vuelidate/validators";

type SearchItem = {
  value: string;
  id: string;
  type: string;
  department: string;
};

const props = defineProps<{
  searchItem: SearchItem[] | undefined;
}>();

const emit = defineEmits<{
  (e: "submit", value: unknown): void;
}>();

const store = useStore();
const dialog = ref<boolean>(false);
const step = ref<number>(1);
const isLoading = ref<boolean>(false);

const state = ref({
  nomorSiaranPers: "",
  penyetuju: null as any,
});

const disableAllApprovalButton = computed(() => {
  return store.getters["collaborationStore/getDisableAllApprovalButton"];
});

const onLoading = computed(() => {
  return isLoading.value || disableAllApprovalButton.value;
});

const rules = {
  nomorSiaranPers: {
    required: helpers.withMessage("Nomor Siaran Pers is required", required),
    ascii: helpers.withMessage(
      "Nomor Siaran Pers must contain only ASCII characters",
      // eslint-disable-next-line no-control-regex
      (value: string) => /^[\u0000-\x7F]*$/.test(value)
    ),
  },
  penyetuju: {
    required: helpers.withMessage("Penyetuju is required", required),
  },
};

const v$ = useVuelidate(rules, state);
const tabs = computed(() => {
  return [
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
});

async function nextStep() {
  await v$.value.nomorSiaranPers.$touch();
  if (v$.value.nomorSiaranPers.$invalid) return;
  if (step.value === tabs.value.length) return;
  step.value++;
}

const backStep = () => {
  if (step.value === 1) return;

  step.value--;
};

function showDialog() {
  dialog.value = true;
}

function onclose() {
  dialog.value = false;
  v$.value.$reset();
  state.value = {
    nomorSiaranPers: "",
    penyetuju: null,
  };
}

async function submitDocument() {
  const isValid = await v$.value.$validate();
  if (!isValid) return;

  try {
    isLoading.value = true;
    emit("submit", {
      nomorSiaranPers: state.value.nomorSiaranPers,
      penyetuju: state.value.penyetuju,
    });
  } finally {
    isLoading.value = false;
  }
}

defineExpose({ showDialog, onclose });
</script>

<style lang="scss" scoped>
:deep(.steppy) {
  margin-left: 35%;
  margin-right: 35%;
}

:deep(.number) {
  display: none !important;
}

:deep(.wrapper-steppy) {
  padding: 25px 10px 0px 10px !important;
}

:deep(.steppy-pane) {
  box-shadow: none !important;
  margin: 30px 0 0 0 !important;
  padding: 25px 0 !important;
}
:deep(.steppy-item.success .steppy-item-counter) {
  border: 8px solid #267dc2 !important;
}

:deep(.steppy-item-counter) {
  height: 20px !important;
  width: 20px !important;
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

:deep(.wrapper-steppy > .controls) {
  display: none;
}

.btn-cancel {
  background: linear-gradient(#fff -46.47%, #fff 157.9%);
  border-radius: 10px;
  font-weight: 800;
  color: #065695 !important;
}

.line {
  border: none;
  height: 3px;
  margin: 16px 0;
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
}

.btn-close {
  position: absolute;
  right: 0;
  top: 0;
  margin-top: 10px;
  margin-right: 10px;
}
</style>
