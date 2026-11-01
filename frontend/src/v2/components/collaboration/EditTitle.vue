<template>
  <v-btn
    size="small"
    variant="outlined"
    style="border-radius: 10px"
    color="#065695"
    class="mr-2"
    :loading="isLoading"
    @click="handleShowDialog"
  >
    Edit Title
    <template v-slot:prepend>
      <img :src="require('@/v2/assets/icon/edit.svg')" />
    </template>
  </v-btn>
  <Teleport to="body">
    <v-dialog v-model="dialog" width="700" persistent>
      <v-card class="border-radius-dwp">
        <v-card-title class="text-center mt-3">
          <h3 class="text-17 fw-700 text-darkBlue">Edit Title</h3>
          <v-btn
            density="default"
            icon="mdi-close"
            variant="text"
            class="btn-close"
            @click="onClose()"
          />
        </v-card-title>
        <hr class="line mt-3" />
        <v-card-text class="px-6 py-4">
          <v-form ref="form" @submit.prevent="saveTitle">
            <p class="pb-3 text-left text-darkBlue font-weight-bold">
              Title<span class="text-redTheme">*</span>
            </p>
            <v-text-field
              v-model="formData.title"
              autocomplete="off"
              variant="solo"
              placeholder="Document Title"
              class="my-input ellipsis-input"
              single-line
              clearable
              maxLength="100"
              :error-messages="v$.title.$errors.map((e) => e.$message)"
              :error="v$.title.$error"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions class="justify-end px-6 pb-4 pt-0">
          <v-btn
            class="btn-cancel mr-3"
            elevation="4"
            width="100"
            height="45"
            @click="onClose"
            >Cancel</v-btn
          >
          <v-btn
            class="btn-save"
            elevation="4"
            width="100"
            height="45"
            :loading="isLoading"
            :disabled="v$.title.$invalid || !hasChanges"
            @click="saveTitle"
            >Save</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </Teleport>
</template>

<script setup lang="ts">
import {
  ref,
  computed,
  watch,
  nextTick,
  reactive,
  getCurrentInstance,
} from "vue";
import { useVuelidate } from "@vuelidate/core";
import { required, minLength, maxLength } from "@vuelidate/validators";
import { useStore } from "vuex";

const dialog = ref<boolean>(false);
const isLoading = ref<boolean>(false);
const form = ref();
const store = useStore();
const instance: any = getCurrentInstance()?.root.refs;

interface Props {
  currentTitle?: string;
  documentId?: string;
}

const props = withDefaults(defineProps<Props>(), {
  currentTitle: "",
  documentId: "",
});

const emit = defineEmits<{
  titleUpdated: [title: string];
}>();

const formData = reactive({
  title: "",
});

const rules = {
  title: {
    required: required,
    minLength: minLength(3),
    maxLength: maxLength(100),
  },
};

const v$ = useVuelidate(rules, formData);

const hasChanges = computed(() => {
  return formData.title.trim() !== (props.currentTitle || "").trim();
});

watch(
  () => props.currentTitle,
  (newTitle) => {
    formData.title = newTitle || "";
  },
  { immediate: true }
);

async function saveTitle() {
  const isFormCorrect = await v$.value.$validate();

  if (!isFormCorrect) {
    return;
  }

  if (!hasChanges.value) {
    return;
  }

  isLoading.value = true;

  try {
    await store
      .dispatch("eFormStore/updateTitleEForm", {
        id: props.documentId,
        bPDocumentName: formData.title.trim(),
      })
      .then((response: any) => {
        const responseMessage =
          response?.responseMessage || "Successfully Change";

        store.commit(
          "collaborationStore/setDocumentName",
          formData.title.trim()
        );
        instance.toast.show({
          message: responseMessage,
          color: "success",
          timeout: 3000,
        });
      });
  } catch (error: any) {
    instance.toast.show({
      message: error?.response?.data?.message || "Failed to update title",
      color: "error",
      timeout: 3000,
    });
  } finally {
    isLoading.value = false;
    dialog.value = false;
  }
}

function handleShowDialog() {
  nextTick(() => {
    formData.title = props.currentTitle || "";
    v$.value.$reset();
    dialog.value = true;
  });
}

function onClose() {
  dialog.value = false;
  v$.value.$reset();
}
</script>

<style scoped>
.btn-close {
  position: absolute;
  right: 0;
  top: 0;
  margin-top: 10px;
  margin-right: 10px;
}
.line {
  border: none;
  min-height: 2px;
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
}
.position-absolute {
  position: absolute !important;
}

.text-grey-600 {
  color: rgba(0, 0, 0, 0.6) !important;
}

:deep(.v-field--variant-outlined .v-field__outline) {
  --v-field-border-width: 1px;
}

:deep(.v-field--focused .v-field__outline) {
  --v-field-border-width: 2px;
}

.btn-save {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  border-radius: 10px !important;
  border-color: #267dc2 !important;
  padding-left: 16px !important;
  padding-right: 16px !important;
  font-size: 14px !important;
  color: white;
  font-weight: 900;
}

.btn-cancel {
  background: white;
  border-radius: 10px !important;
  padding-left: 16px !important;
  padding-right: 16px !important;
  font-size: 14px !important;
  color: #267dc2 !important;
  font-weight: 900;
}

:deep(.v-field.v-field--appended) {
  border-radius: 10px !important;
}

.ellipsis-input :deep(.v-field__input) {
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}

.ellipsis-input :deep(input) {
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}

.ellipsis-input :deep(input:focus) {
  text-overflow: clip;
  overflow: visible;
  white-space: normal;
}

.ellipsis-input :deep(.v-field__input input::placeholder) {
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}
</style>
