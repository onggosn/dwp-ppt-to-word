<template>
  <v-btn
    color="#065695"
    class="ma-3 rounded-lg"
    variant="outlined"
    :loading="isLoading"
    @click="startEdit"
  >
    Edit Description
    <template v-slot:prepend>
      <img :src="require('@/v2/assets/icon/edit.svg')" />
    </template>
  </v-btn>
  <v-dialog v-model="dialog" persistent style="width: 60%">
    <template> </template>
    <v-card class="border-radius-dwp">
      <v-form ref="form" @submit.prevent="submitForm" class="pl-2 pr-2">
        <v-card-title class="text-center mt-3">
          <h3 class="text-h6 font-weight-regular">Edit Event</h3>
          <v-btn
            density="default"
            icon="mdi-close"
            variant="text"
            class="btn-close"
            @click="dialog = false"
          />

          <hr class="line mt-5 mb-4" />
        </v-card-title>

        <v-card-text>
          <p class="ml-2 pb-1 mt-4 text-left text-darkBlue font-weight-bold">
            Description<span style="color: red">*</span>
          </p>
          <div
            class="mx-2 my-2"
            :class="{ 'editor-error': showDescError && !!descErrorMessage }"
          >
            <div ref="myEditor" id="editingEditor" />
            <div
              v-if="showDescError"
              class="v-messages mt-1"
              style="color: rgb(var(--v-theme-error))"
            >
              <div class="v-messages__message mt-2">{{ descErrorMessage }}</div>
            </div>
          </div>
          <v-textarea
            v-model="detailDesc"
            variant="solo"
            placeholder="Write your description here"
            class="pl-2 pr-2 textareadescription hidden-validation-field"
            aria-hidden="true"
            tabindex="-1"
            readonly
          ></v-textarea>
        </v-card-text>

        <div class="text-right mt-3 pb-5 pr-5">
          <v-btn
            class="btn-prev mr-3"
            @click="dialog = false"
            elevation="4"
            width="100"
            height="45"
            :disabled="store.getters['eventStore/getLoading']"
            >Cancel</v-btn
          >
          <v-btn
            class="btn-next"
            elevation="4"
            width="100"
            height="45"
            :loading="store.getters['eventStore/getLoading']"
            @click="submitForm"
            >Save</v-btn
          >
        </div>
      </v-form>
    </v-card>
  </v-dialog>
</template>
<script setup lang="ts">
import { computed, ref, watch, getCurrentInstance } from "vue";
import { useStore } from "vuex";
import EditorOutput from "@/v2/components/side-project/ckeditor/build/ckeditor";
import { removeIrregulerSpace } from "@v2/helpers/utils";
import { useInitializeConfig } from "@/v2/composables/useInitializeConfig";

const props = defineProps({
  formData: {
    type: String,
    default: "",
  },
  idbp: {
    type: String,
    default: "",
  },
});
const emit = defineEmits(["update"]);
const { root } = getCurrentInstance() as any;
const isLoading = ref(false);
const store = useStore();
const { ckEditorLicense } = useInitializeConfig();
const dialog = ref(false);
const showDescError = ref(false);
const form = ref();
const detailDesc = ref();
const myEditor = ref<HTMLDivElement | string>(" ");
let editorInstance: any;
function getPlainTextFromHtml(value: string) {
  return (value || "")
    .replace(/<[^>]*>/g, " ")
    .replace(/&nbsp;|&#160;/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}
const rules = {
  required: (value: string) =>
    !!getPlainTextFromHtml(removeIrregulerSpace(value || "")) ||
    "Description is required",
};
const descErrorMessage = computed(() => {
  const validation = rules.required(detailDesc.value || "");
  return validation === true ? "" : validation;
});

function startEdit() {
  showDescError.value = false;
  dialog.value = true;
}
watch(
  () => myEditor.value,
  (val) => {
    if (val) {
      initEditor();
    }
  }
);
async function submitForm() {
  const dataDescripsi = removeIrregulerSpace(detailDesc.value);
  showDescError.value = true;
  const validationMessage = rules.required(detailDesc.value || "");
  if (validationMessage !== true) {
    return;
  }

  const result = await form.value?.validate();
  if (result && !result.valid) {
    return;
  }

  const req = {
    idMEventTemplate: props.idbp,
    description: dataDescripsi,
  };
  store
    .dispatch("adminStore/updateDeskripsiMeeting", req)
    .then((res) => {
      root.refs.toast.show({
        message: res.responseMessage,
        color: "success",
        timeout: 3000,
      });
      dialog.value = false;
      showDescError.value = false;
      emit("update", dataDescripsi);
    })
    .catch((err) => {
      root.refs.toast.show({
        message: err.response.data.responseData || "",
        color: "error",
        timeout: 3000,
        icon: "mdi-check",
      });
    });
}
watch(
  () => props.formData,
  (val) => {
    detailDesc.value = val;
  }
);
async function initEditor() {
  detailDesc.value = props.formData;
  // if (detailDesc.value) {
  editorInstance = await EditorOutput.CustomClassic.create(myEditor.value, {
    initialData: detailDesc.value ? detailDesc.value : "",
    updateSourceElementOnDestroy: false,
    toolbar: {
      items: [
        "undo",
        "redo",
        "|",
        "bold",
        "italic",
        "|",
        "insertTable",
        "bulletedList",
        "numberedList",
        "|",
      ],
    },
    licenseKey: ckEditorLicense.value,
  });
  editorInstance.model.document.on("change:data", () => {
    detailDesc.value = editorInstance.getData();
  });
  // }
}

watch(detailDesc, (val) => {
  if (!editorInstance) {
    return;
  }

  const currentData = editorInstance.getData();
  if (currentData !== val) {
    editorInstance.setData(val || "");
  }
});
</script>

<style scoped>
/*
:deep(.ck.ck-sticky-panel) {
  display: none !important;
}
  */

:deep(.v-textarea .v-field__input) {
  height: 1px !important;
  background: red !important;
  display: contents;
}

.hidden-validation-field {
  position: absolute;
  left: -99999px;
  width: 1px;
  height: 1px;
  opacity: 0;
  pointer-events: none;
}
:deep(.ck.ck-toolbar.ck-toolbar_grouping) {
  display: none;
}

:deep(.ck.ck-content.ck-editor__editable) {
  padding: 10px;
  border: 1px solid #dfdfdf;
  border-radius: 0 0 11px 11px;
  /* margin-bottom: 20px; */
  height: 200px;
  box-shadow: 0px 3px 1px -2px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)),
    0px 2px 2px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)),
    0px 1px 5px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.12));
}

.editor-error :deep(.ck.ck-content) {
  border-color: rgb(var(--v-theme-error)) !important;
  box-shadow: 0 0 0 1px rgb(var(--v-theme-error)) !important;
}

.editor-error :deep(.ck .ck-sticky-panel__content) {
  border-top-left-radius: 10px !important;
  border-top-right-radius: 10px !important;
  box-shadow: 0 0 0 1px rgb(var(--v-theme-error)) !important;
}
:deep(.v-chip.v-chip--density-default.chip-shadow) {
  box-shadow: 0px 3px 1px -2px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)),
    0px 2px 2px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)),
    0px 1px 5px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.12));
  height: 56px;
  width: 98%;
  color: grey !important;
  border: none;
  background: #dfdfdf;
  font-size: 16px;
  margin: 10px;
}

:deep(.v-chip.v-chip--density-default) {
  height: calc(var(--v-chip-height) + 0px);
  border-radius: 5px;
  background: #e9f5ff;
  border: 1px solid #6eb3ea;
  color: #065391;
  padding: 10px;
  margin-right: 5px;
  margin-bottom: 5px;
}

:deep(.dp__overlay) {
  border-radius: 10px;
}
:deep(.dp__instance_calendar) {
  box-shadow: 1px 1px 7px 3px #7393b3;
  border-radius: 5px;
  padding: 10px;
}

:deep(.dp__arrow_top) {
  display: none;
}

:deep(.v-textarea .v-field) {
  --v-textarea-control-height: var(--v-input-control-height);
  background: white;
  border-radius: 12px;
}
:deep(.v-field.v-field--appended) {
  border-radius: 12px !important;
}

:deep(.v-text-field .v-field) {
  border-radius: 12px;
}

:deep(.ck .ck-sticky-panel__content) {
  border-top-left-radius: 10px !important;
  border-top-right-radius: 10px !important;
  box-shadow: 0px 3px 1px -2px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)),
    0px 2px 2px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)),
    0px 1px 5px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.12));
}

:deep(.ck .ck-toolbar) {
  border-radius: 10px;
}

.btn-close {
  position: absolute;
  right: 0;
  top: 0;
  margin-top: 10px;
  margin-right: 10px;
}

.line {
  border: none; /* Remove the default border */
  height: 2px; /* Set the height of the hr */
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
}

.btn-next {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  border-radius: 10px !important;
  border-color: #267dc2 !important;
  padding-left: 16px !important;
  padding-right: 16px !important;
  font-size: 14px !important;
  color: white;
  font-weight: 900;
}

.btn-prev {
  background: white;
  border-radius: 10px !important;
  /* border-color: #267dc2 !important; */
  padding-left: 16px !important;
  padding-right: 16px !important;
  font-size: 14px !important;

  color: #267dc2;
  font-weight: 900;
}
</style>
