<template>
  <v-btn
    size="small"
    variant="outlined"
    :style="
      routeType === 'content' ? 'border-radius: 8px' : 'border-radius: 10px'
    "
    prepend-icon="mdi-pencil"
    class="mr-2"
    :class="routeType === 'content' ? 'font-weight-bold' : ''"
    color="#065695"
    @click="onOpen()"
  >
    Edit Content
  </v-btn>
  <Teleport to="body">
    <v-dialog v-model="dialog" width="1000" persistent>
      <v-card class="border-radius-dwp">
        <v-card-title class="text-center mt-3">
          <h3 class="text-h6 font-weight-regular">Edit Content</h3>
          <v-btn
            density="default"
            icon="mdi-close"
            variant="text"
            class="btn-close"
            @click="onClose()"
          />
        </v-card-title>
        <hr class="line mt-3" />

        <v-card-text class="ma-2">
          <v-form ref="form">
            <v-row>
              <v-col :cols="12" class="">
                <p class="pb-3 text-left text-darkBlue font-weight-bold">
                  Content Type<span class="text-redTheme">*</span>
                </p>
                <v-chip class="border-radius-dwp py-7 px-4" style="width: 100%">
                  <span style="width: 100%">{{ content_type_name }}</span>
                </v-chip>
              </v-col>
              <v-col :cols="12" class="">
                <p class="pb-3 text-left text-darkBlue font-weight-bold">
                  Content Title<span class="text-redTheme">*</span>
                </p>
                <v-text-field
                  v-if="isCase1"
                  v-model="formInput.content_title"
                  autocomplete="off"
                  variant="solo"
                  placeholder="Content Name"
                  class="my-input"
                  single-line
                  :hide-details="isError(v$.content_title)"
                  :error-messages="
                    getErrorMessages(v$.content_title, {
                      required: 'Required',
                    })
                  "
                ></v-text-field>
                <v-row v-else-if="isCase3">
                  <v-col :cols="4">
                    <v-text-field
                      v-model="formInput.content_title_satker"
                      autocomplete="off"
                      variant="solo"
                      placeholder="Satker"
                      class="my-input"
                      single-line
                      :hide-details="isError(v$.content_title_satker)"
                      :error-messages="
                        getErrorMessages(v$.content_title_satker, {
                          required: 'Required',
                        })
                      "
                    ></v-text-field>
                  </v-col>
                  <v-col :cols="8">
                    <v-text-field
                      v-model="formInput.content_title_document"
                      autocomplete="off"
                      variant="solo"
                      placeholder="Document Name"
                      class="my-input"
                      single-line
                      :hide-details="isError(v$.content_title_document)"
                      :error-messages="
                        getErrorMessages(v$.content_title_document, {
                          required: 'Required',
                        })
                      "
                    ></v-text-field>
                  </v-col>
                </v-row>
                <v-row v-else>
                  <v-col :cols="4">
                    <v-text-field
                      v-model="formInput.content_title_satker"
                      autocomplete="off"
                      variant="solo"
                      placeholder="Satker"
                      class="my-input"
                      single-line
                      :disabled="isCase4"
                      :hide-details="isError(v$.content_title_satker)"
                      :error-messages="
                        getErrorMessages(v$.content_title_satker, {
                          required: 'Required',
                        })
                      "
                    ></v-text-field>
                  </v-col>
                  <v-col :cols="4">
                    <v-text-field
                      v-model="formInput.content_title_number"
                      autocomplete="off"
                      variant="solo"
                      placeholder="Document Number (Optional)"
                      class="my-input"
                      single-line
                      :disabled="isCase4"
                      :hide-details="isError(v$.content_title_number)"
                      :error-messages="
                        getErrorMessages(v$.content_title_number, {
                          required: 'Required',
                        })
                      "
                    ></v-text-field>
                  </v-col>
                  <v-col :cols="4">
                    <v-text-field
                      v-model="formInput.content_title_document"
                      autocomplete="off"
                      variant="solo"
                      placeholder="Document Name"
                      class="my-input"
                      single-line
                      :disabled="isCase4"
                      :hide-details="isError(v$.content_title_document)"
                      :error-messages="
                        getErrorMessages(v$.content_title_document, {
                          required: 'Required',
                        })
                      "
                    ></v-text-field>
                  </v-col>
                </v-row>
                <p
                  class="pa-3 mt-2 text-left"
                  style="background-color: #e9f5ff; border-radius: 15px"
                >
                  Content Title : {{ contentTitleValue }}
                </p>
              </v-col>

              <template v-if="!isContentMaterial">
                <v-col :cols="12" class="">
                  <p class="text-left text-darkBlue font-weight-bold">
                    Is this content calculated in the executive summary?<span
                      class="text-redTheme"
                      >*</span
                    >
                  </p>
                  <v-radio-group
                    inline
                    style="margin-left: -8px"
                    v-model="formInput.executive_summary"
                    hide-details
                  >
                    <v-radio
                      label="Yes"
                      :value="1"
                      color="#267DC2"
                      class="me-5"
                    ></v-radio>
                    <v-radio label="No" :value="0" color="#267DC2"></v-radio>
                  </v-radio-group>
                </v-col>

                <v-col :cols="12" class="">
                  <p class="text-left text-darkBlue font-weight-bold">
                    Can this content be submitted to STP without approval?<span
                      class="text-redTheme"
                      >*</span
                    >
                  </p>
                  <v-radio-group
                    inline
                    style="margin-left: -8px"
                    v-model="formInput.stp_with_out_approval"
                    hide-details
                  >
                    <v-radio
                      label="Yes"
                      :value="1"
                      color="#267DC2"
                      class="me-5"
                      :disabled="!enabledSubmit"
                    ></v-radio>
                    <v-radio
                      label="No"
                      :value="0"
                      color="#267DC2"
                      :disabled="!enabledSubmit"
                    ></v-radio>
                  </v-radio-group>
                </v-col>

                <v-col :cols="12" class="">
                  <p class="text-left text-darkBlue font-weight-bold">
                    Will this content be golden copy?<span class="text-redTheme"
                      >*</span
                    >
                  </p>
                  <v-radio-group
                    inline
                    style="margin-left: -8px"
                    v-model="formInput.golden_copy"
                    hide-details
                  >
                    <v-radio
                      label="Yes"
                      :value="1"
                      color="#267DC2"
                      class="me-5"
                      :disabled="!goldenCopy"
                    ></v-radio>
                    <v-radio
                      label="No"
                      :value="0"
                      color="#267DC2"
                      :disabled="!goldenCopy"
                    ></v-radio>
                  </v-radio-group>
                </v-col>

                <v-col :cols="12" class="" v-if="isCase2">
                  <p class="text-left text-darkBlue font-weight-bold">
                    Will this content be an automatic AIU?<span
                      class="text-redTheme"
                      >*</span
                    >
                  </p>
                  <v-radio-group
                    inline
                    style="margin-left: -8px"
                    v-model="formInput.automatic_aiu"
                    hide-details
                  >
                    <v-radio
                      label="Yes"
                      :value="1"
                      color="#267DC2"
                      class="me-5"
                    ></v-radio>
                    <v-radio label="No" :value="0" color="#267DC2"></v-radio>
                  </v-radio-group>
                </v-col>

                <v-col :cols="12" class="">
                  <p class="text-left text-darkBlue font-weight-bold">
                    Is the title visible?<span class="text-redTheme">*</span>
                  </p>
                  <v-radio-group
                    inline
                    hide-details
                    style="margin-left: -8px"
                    v-model="formInput.title_visible"
                  >
                    <v-radio
                      label="Yes"
                      :value="1"
                      color="#267DC2"
                      class="me-5"
                    ></v-radio>
                    <v-radio label="No" :value="0" color="#267DC2"></v-radio>
                  </v-radio-group>
                </v-col>

                <v-col
                  :cols="12"
                  class="mb-2 mt-n5"
                  v-if="formInput.title_visible == 1"
                >
                  <v-textarea
                    v-model="formInput.title_visible_text"
                    autocomplete="off"
                    variant="solo"
                    placeholder="Input title here"
                    class="my-input"
                    single-line
                    :rows="2"
                    :hide-details="isError(v$.title_visible_text)"
                    :error-messages="
                      getErrorMessages(v$.title_visible_text, {
                        required: 'Required',
                      })
                    "
                  ></v-textarea>
                </v-col>

                <v-col :cols="12" class="">
                  <p class="text-left text-darkBlue font-weight-bold">
                    Is it possible to export to Word?<span class="text-redTheme"
                      >*</span
                    >
                  </p>
                  <v-radio-group
                    inline
                    hide-details
                    style="margin-left: -8px"
                    v-model="formInput.export_word"
                  >
                    <v-radio
                      label="Yes"
                      :value="1"
                      color="#267DC2"
                      class="me-5"
                    ></v-radio>
                    <v-radio label="No" :value="0" color="#267DC2"></v-radio>
                  </v-radio-group>
                </v-col>
                <v-col :cols="12" class="">
                  <p class="text-left text-darkBlue font-weight-bold">
                    Is a revision workflow needed for this document?
                    <span class="text-redTheme">*</span>
                  </p>
                  <v-radio-group
                    inline
                    hide-details
                    style="margin-left: -8px"
                    v-model="formInput.revision_workflow"
                    :disabled="!disableRevisionWorkflow"
                  >
                    <v-radio
                      label="Yes"
                      :value="1"
                      color="#267DC2"
                      class="me-5"
                      :disabled="!disableRevisionWorkflow"
                    ></v-radio>
                    <v-radio
                      label="No"
                      :value="0"
                      color="#267DC2"
                      :disabled="!disableRevisionWorkflow"
                    ></v-radio>
                  </v-radio-group>
                </v-col>
                <v-col :cols="12" class="">
                  <p class="text-left text-darkBlue font-weight-bold">
                    Is it possible to Import PPT?<span class="text-redTheme"
                      >*</span
                    >
                  </p>
                  <v-radio-group
                    v-model="formInput.export_ppt"
                    inline
                    hide-details
                    style="margin-left: -8px"
                    :disabled="disableImportPPT"
                  >
                    <v-radio
                      label="Yes"
                      :value="1"
                      color="#267DC2"
                      class="me-5"
                      :disabled="disableImportPPT"
                    ></v-radio>
                    <v-radio
                      label="No"
                      :value="0"
                      color="#267DC2"
                      :disabled="disableImportPPT"
                    ></v-radio>
                  </v-radio-group>
                </v-col>
              </template>
            </v-row>
          </v-form>
          <div class="text-right pb-5 mt-4">
            <v-btn
              class="btn-prev mr-3"
              elevation="4"
              width="100"
              height="45"
              @click="onClose"
            >
              Cancel
            </v-btn>
            <v-btn
              class="btn-next"
              elevation="4"
              width="100"
              height="45"
              @click="onSave"
            >
              Save
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </Teleport>
</template>
<script lang="ts" setup>
import {
  getErrorMessages,
  isError,
  sharePointRegex,
} from "@v2/helpers/validation";
import { useVuelidate } from "@vuelidate/core";
import { requiredIf } from "@vuelidate/validators";
import { computed, getCurrentInstance, ref } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import { secureRandomFloat } from "@/v2/helpers/utils";
import { Stage } from "@/v2/enum/Enum";

const instance: any = getCurrentInstance()?.root.refs;
const store = useStore();
const route = useRoute();
const dialog = ref(false);
const stage = ref<string>("");
const goldenCopy = ref(true);
const enabledSubmit = ref<boolean>(true);
const disableRevisionWorkflow = ref<boolean>(false);
const disableImportPPT = ref<boolean>(false);
const isContentMaterial = ref<boolean>(false);

const prop = defineProps({
  id: {
    type: [Number, String],
    requried: true,
  },
});

const formInput = ref({
  template_id: 0,
  content_type: null,
  content_title: null,
  content_title_satker: null,
  content_title_number: null,
  content_title_document: null,

  executive_summary: 0,
  stp_with_out_approval: 0,
  golden_copy: 0,
  automatic_aiu: 0,
  title_visible: 0,
  title_visible_text: "",
  export_word: 0,
  export_ppt: 0,
  revision_workflow: 0,
  isDisabledEditName: false,
});
const content_type_name = ref<string | null>(null);

const contentTitleValue = computed((): string => {
  const title =
    formInput.value.content_title == null ? "" : formInput.value.content_title;
  const satker =
    formInput.value.content_title_satker == null
      ? ""
      : formInput.value.content_title_satker;
  const doc =
    formInput.value.content_title_document == null
      ? ""
      : formInput.value.content_title_document;
  // kalau dokumen publikasi, maka title tidak perlu diubah
  if (formInput.value.template_id === 74) return title;
  if (isCase1.value) return `${stage.value}_*date*_` + title;

  const no = formInput.value.content_title_number
    ? `_${formInput.value.content_title_number}`
    : "";
  if (isCase3.value)
    return `
    ${satker}_*date*${no}_${doc}
  `;
  if (isCase4.value) return formInput.value.content_title ?? "";

  return `
    ${satker} ${stage.value}_*date*${no}_${doc}
  `;
});

// stage is kbku dan rdgb
const isCase1 = computed((): boolean => {
  return [
    0, 8, 9, 20, 21, 32, 33, 56, 57, 64, 70, 71, 72, 73, 83, 84, 93, 74,
  ].includes(formInput.value.template_id);
});

// stage is aiu
const isCase2 = computed((): boolean => {
  return [10, 22, 34].includes(formInput.value.template_id);
});

const isCase3 = computed((): boolean => {
  return [
    Stage.RakorRispatBulanan,
    Stage.RakorRispatMingguan,
    Stage.RakorRispatTriwulanan,
  ].includes(formInput.value.template_id);
});

const isCase4 = computed((): boolean => {
  return formInput.value.isDisabledEditName;
});

const routeType = computed(() => {
  if (route.path.includes("admin-management/content")) return "content";
  return "other";
});

const rules = computed(() => {
  return {
    content_title: {
      required: requiredIf(isCase1.value),
      ...(isCase4.value ? {} : { sharePointRegex: sharePointRegex }),
    },

    content_title_satker: {
      required: requiredIf(!isCase1.value && !isCase4.value),
      sharePointRegex: sharePointRegex,
    },
    content_title_number: {
      sharePointRegex: sharePointRegex,
    },
    content_title_document: {
      required: requiredIf(!isCase1.value && !isCase4.value),
      ...(isCase4.value ? {} : { sharePointRegex: sharePointRegex }),
    },

    title_visible_text: {
      required: requiredIf(formInput.value.title_visible == 1),
    },
  };
});
const v$ = useVuelidate(rules, formInput);

function onOpen() {
  store
    .dispatch("adminStore/getEditContentPreDefine", prop.id)
    .then(({ responseData }) => {
      const data = responseData;
      goldenCopy.value = responseData.enableGoldenCopy;
      content_type_name.value = data.contentTypeName;
      enabledSubmit.value = data.enabledSubmit;
      disableRevisionWorkflow.value = data.isEditRevision || false;
      disableImportPPT.value = data.isDisableChangeImportPPTStatus ?? false;
      isContentMaterial.value = data.isContentMaterial ?? false;
      formInput.value = {
        template_id: data.idMBPTemplate,
        content_type: data.contentType,
        content_title: data.mBPDocumentTemplate,
        content_title_satker: null,
        content_title_number: null,
        content_title_document: null,

        executive_summary: data.isExecutiveSummary ? 1 : 0,
        stp_with_out_approval: data.isSubmit ? 1 : 0,
        golden_copy: data.isGoldenCopy ? 1 : 0,
        automatic_aiu: data.isAutoAIU ? 1 : 0,
        title_visible: data.isVisibleTitle ? 1 : 0,
        title_visible_text: data.title?.replace(/<\s*br\s*\/?>/gi, "\n") ?? "", // Covers <br />, <br>, < br />, etc.
        export_word: data.isWordConvert ? 1 : 0,
        export_ppt: data.isImportPPT ? 1 : 0,
        revision_workflow: data.isRevision ? 1 : 0,
        isDisabledEditName: data.isDisabledEditName ?? false,
      };

      // logic name
      try {
        const tmps = data.mBPDocumentTemplate?.trim()?.split("_") ?? [];

        if (isCase1.value) {
          formInput.value.content_title = tmps.at(-1);
          stage.value = tmps[0];
        } else if (isCase4.value) {
          formInput.value.content_title = data.mBPDocumentTemplate;
        } else {
          const satkers = tmps[0]?.split(" ") ?? [];
          formInput.value.content_title = null;
          formInput.value.content_title_satker = null;
          if (satkers.length == 1) {
            stage.value = satkers[0];
            if (isCase3.value)
              formInput.value.content_title_satker = satkers[0];
          } else {
            stage.value = satkers[1];
            formInput.value.content_title_satker = satkers[0];
          }
          if (tmps.length == 3) {
            formInput.value.content_title_document = tmps[2];
          } else if (tmps.length >= 4) {
            if (!isNaN(parseInt(tmps[2]))) {
              formInput.value.content_title_number = tmps[2];
            }
            formInput.value.content_title_document = tmps
              .filter((d, i) => ![0, 1, 2].includes(i))
              .join("_");
          }
        }
      } catch (error) {
        undefined;
      }

      dialog.value = true;
    });
}

function onClose() {
  dialog.value = false;
}

function onSave() {
  v$.value.$validate().then((res) => {
    if (res) {
      const req = {
        idMBPDocumentTemplate: prop.id,
        MBPDocumentName: contentTitleValue.value.trim(),
        isExecutiveSummary: formInput.value.executive_summary == 1,
        isSubmit: formInput.value.stp_with_out_approval == 1,
        isGoldenCopy: formInput.value.golden_copy == 1,
        isAIUotomatis: formInput.value.automatic_aiu == 1,
        isVisibleTitle: formInput.value.title_visible == 1,
        title: formInput.value.title_visible
          ? formInput.value.title_visible_text.replaceAll(/\n/g, "<br />")
          : null,
        isExportToWord: formInput.value.export_word == 1,
        isImportPPT: formInput.value.export_ppt == 1,
        isRevision: formInput.value.revision_workflow == 1,
      };

      store
        .dispatch("adminStore/updateContentPreDefine", req)
        .then(({ responseMessage }) => {
          instance.toast.show({
            message: responseMessage,
            color: "success",
            timeout: 3000,
          });
          store.commit("adminStore/setRefreshList", secureRandomFloat());
        })
        .catch((error) => {
          instance.toast.show({
            message:
              error.response.data.responseMessage ?? "internal server error",
            color: "warning",
            timeout: 3000,
          });
        });
    }
  });
}
</script>
<style lang="scss" scoped>
.btn-close {
  position: absolute;
  right: 0;
  top: 0;
  margin-top: 10px;
  margin-right: 10px;
}

.line {
  border: none; /* Remove the default border */
  min-height: 2px; /* Set the height of the hr */
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
}

:deep(.v-field--error) {
  border: 1px solid #b13737 !important;
}
:deep(.v-messages__message) {
  line-height: 12px;
  word-break: break-word;
  overflow-wrap: break-word;
  word-wrap: break-word;
  -webkit-hyphens: auto;
  hyphens: auto;
  transition-duration: 154ms;
  font-size: 13px;
  font-style: normal;
  font-weight: 600;
  font-family: Poppins;
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

:deep(.v-field--disabled) {
  color: #000000;
  background-color: rgb(196, 186, 186) !important;
}
</style>
