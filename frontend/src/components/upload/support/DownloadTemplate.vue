<script setup lang="ts">
import { reactive, defineEmits, defineProps, ref } from "vue";
import ApiLoader from "@/components/ApiLoader.vue";
import { useVuelidate } from "@vuelidate/core";
import { required } from "@vuelidate/validators";
import { mGetDocumentSupportTypeByIdMethod } from "@/models/upload";

const props = defineProps({
  methodAddDocument: { type: Number, required: true, default: 2 },
  idTaskTemplate: { type: Number, required: true, default: -1 },
});

const emits = defineEmits(["updateStep", "updateDownload"]);
const docType = ref(-1);
const sizeDocument = ref(0);
const documentName = ref<string>("");

const documentType = () =>
  mGetDocumentSupportTypeByIdMethod(
    props.methodAddDocument,
    props.idTaskTemplate
  );

const updateDocumentType = (newValue) => {
  sizeDocument.value = newValue.fileSize;
  documentName.value = newValue.value + ".pptx";
  docType.value = newValue.id;
};

const initialState = {
  _documentType: null,
};

const state = reactive({
  ...initialState,
});

const rules = {
  _documentType: { required },
};

const v$ = useVuelidate(rules, state);

const submitForm = () => {
  v$.value.$validate().then((valid) => {
    if (valid) {
      emits("updateDownload", state._documentType);
    }
  });
};

const back = () => {
  emits("updateStep", 1);
};
</script>
<template>
  <v-form @submit.prevent="submitForm">
    <div class="d-flex flex-wrap justify-space-between mb-6 mt-5 pa-8">
      <v-sheet class="pt-4 pb-4 pl-2 mb-4 blue-gradient" width="100%">
        <b style="color: #fff">Download Document</b>
      </v-sheet>
      <v-sheet width="100%">
        <p class="font-weight-bold mb-2 text-greyTheme">
          Document Type <span style="color: red">*</span>
        </p>
        <api-loader :apiMethod="documentType">
          <template v-slot:default="props">
            <!-- <pre>{{ props }}</pre> -->
            <v-autocomplete
              v-model="state._documentType"
              class="rounded-lg"
              placeholder="Pilih Tipe Dokumen"
              @update:modelValue="updateDocumentType"
              :items="props.response.responseData"
              :error-messages="
                v$._documentType.$errors.map((e) => 'Wajib diisi')
              "
              item-title="value"
              item-value="id"
              return-object
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

      <v-sheet width="100%" style="text-align-last: end">
        <v-spacer></v-spacer>
        <v-btn
          elevation="3"
          style="
            background: linear-gradient(#fff -46.47%, #fff 157.9%);
            border-radius: 10px;
            padding-left: 30px;
            padding-right: 30px;
            font-weight: 800;
            color: red;
          "
          @click="back()"
        >
          Back
        </v-btn>
        <v-btn
          elevation="3"
          class="btn-color-process mr-0"
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
          Download
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

:deep(.v-chip__close) {
  color: white !important;
}
:deep(.v-chip) {
  color: white !important;
  background: #277dc2 !important;
}
</style>
