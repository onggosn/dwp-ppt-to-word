<template>
  <div class="text-center">
    <v-dialog v-model="dialog" activator="parent" persistent width="70vw">
      <v-sheet style="border-radius: 15px">
        <v-card style="border-radius: 15px">
          <v-card-title class="text-center mt-2">
            Add File
            <v-btn
              class="mr-5 mt-3"
              style="position: absolute; right: 0; top: 0"
              variant="text"
              fab
              small
              elevation="0"
              @click="updateStep('Close')"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>

          <v-divider></v-divider>

          <stepper
            :key="stepNumber"
            :itemNumber="stepNumber"
            :currentStep="position"
            class="mt-3"
          />

          <v-window v-model="step">
            <v-window-item :value="1">
              <v-sheet class="ml-10 mr-10 mt-10 mb-10">
                <api-loader :apiMethod="mGetDocumentSupportMethod">
                  <template v-slot:default="props">
                    <!-- {{ props.response.responseData }} -->
                    <v-autocomplete
                      v-model="methodAddDocument"
                      class="rounded-lg"
                      placeholder="Choose Method Add Document"
                      :items="props.response.responseData"
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
            </v-window-item>

            <v-window-item :value="Section.Create">
              <create-document-support
                :idTaskTemplate="idTaskTemplate"
                :methodAddDocument="methodAddDocument"
                @updateStep="updateStep"
                @updateMetadata="updateMetadata"
              />
            </v-window-item>

            <v-window-item :value="Section.CreateApprover">
              <assign-approver
                :idTaskTemplate="idTaskTemplate"
                @updateApprover="updateApprover"
                @updateStep="updateStep"
              />
            </v-window-item>

            <v-window-item :value="Section.UploadProgress">
              <upload-create-document
                @updateStep="updateStep"
                :metadata="metadata"
                :approver="approver"
                :file="file"
                :action="action"
              />
            </v-window-item>

            <v-window-item :value="Section.Approval">
              <create-document-approval-support
                :param="'Approval'"
                @updateStep="updateStep"
                @updateFile="updateFile"
              />
            </v-window-item>

            <v-window-item :value="Section.ApprovalMetadata">
              <approval-metadata
                :param="'Approval'"
                :idTaskTemplate="idTaskTemplate"
                :methodAddDocument="methodAddDocument"
                @updateStep="updateStep"
                @updateMetadataApproval="updateMetadataApproval"
              />
            </v-window-item>

            <v-window-item :value="Section.AssignApprover">
              <assign-approver-document-approval
                @updateStep="updateStep"
                @updateApproverDocumentApproval="updateApproverDocumentApproval"
              />
            </v-window-item>

            <v-window-item :value="Section.NonApproval">
              <create-document-non-approval-support
                :param="'Non Approval'"
                @updateStep="updateStep"
                @updateFile="updateFile"
              />
            </v-window-item>

            <v-window-item :value="Section.NonApprovalMetadata">
              <non-approval-metadata
                :param="'Non Approval'"
                @updateStep="updateStep"
                @updateMetadataNonApproval="updateMetadataNonApproval"
              />
            </v-window-item>

            <v-window-item :value="Section.DownloadTemplate">
              <download-template
                @updateStep="updateStep"
                @updateDownload="updateDownload"
                :idTaskTemplate="idTaskTemplate"
                :methodAddDocument="methodAddDocument"
              />
            </v-window-item>
          </v-window>

          <v-divider />
        </v-card>
      </v-sheet>
    </v-dialog>
  </div>
</template>
<script setup lang="ts">
import {
  defineProps,
  ref,
  watch,
  defineComponent,
  defineEmits,
  onMounted,
  defineExpose,
} from "vue";
import CreateDocumentSupport from "@/components/upload/support/CreateDocumentSupport.vue";
import AssignApprover from "@/components/upload/support/AssignApprover.vue";
import UploadCreateDocument from "@/components/upload/support/UploadCreateDocument.vue";
import CreateDocumentApprovalSupport from "@/components/upload/support/CreateDocumentApprovalSupport.vue";
import CreateDocumentNonApprovalSupport from "@/components/upload/support/CreateDocumentNonApprovalSupport.vue";
import ApprovalMetadata from "@/components/upload/support/ApprovalMetadata.vue";
import NonApprovalMetadata from "@/components/upload/support/NonApprovalMetadata.vue";
import AssignApproverDocumentApproval from "@/components/upload/support/AssignApproverDocumentApproval.vue";
import DownloadTemplate from "@/components/upload/support/DownloadTemplate.vue";
import { mGetDocumentSupportMethod } from "@/models/upload";
import ApiLoader from "@/components/ApiLoader.vue";
import Stepper from "@/components/stepper/CustomStepper.vue";

defineExpose({ start });

defineComponent({
  components: {
    DownloadTemplate,
    Stepper,
    ApiLoader,
    CreateDocumentSupport,
    AssignApprover,
    UploadCreateDocument,
    CreateDocumentApprovalSupport,
    CreateDocumentNonApprovalSupport,
    ApprovalMetadata,
    NonApprovalMetadata,
    AssignApproverDocumentApproval,
  },
});

enum Section {
  Create = "CREATE",
  Approval = "APPROVAL",
  NonApproval = "NONAPPROVAL",
  ApprovalMetadata = "APPROVALMETADATA",
  NonApprovalMetadata = "NONAPPROVALMETADATA",
  CreateApprover = "CREATEAPPROVER",
  UploadProgress = "UPLOADPROGRESS",
  AssignApprover = "ASSIGNAPPROVER",
  DownloadTemplate = "DOWNLOADTEMPLATE",
}

const emits = defineEmits(["doneUpload"]);
const step = ref<number | string>(1);
const position = ref<number>(1);
const dialog = ref(false);
let action = ref("");
let methodAddDocument = ref();
const metadata = ref();
const approver = ref({});
const file = ref({});
const stepNumber = ref(2);
const props = defineProps({
  idTaskTemplate: { type: Number, required: true, default: -1 },
});

onMounted(() => {
  mGetDocumentSupportMethod();
});

watch(step, (newValue) => {
  switch (newValue) {
    case 1: {
      position.value = 1;
      methodAddDocument.value = null;
      break;
    }
    case Section.Create: {
      position.value = 2;
      updateStep(Section.Create);
      break;
    }
    case Section.Approval: {
      position.value = 2;
      updateStep(Section.Approval);
      break;
    }
    case Section.ApprovalMetadata: {
      position.value = 3;
      updateStep(Section.ApprovalMetadata);
      break;
    }
    case "Close": {
      const detailTaskDialog = document.getElementById(
        "DetailTaskDialog"
      ) as HTMLElement;

      detailTaskDialog.style.visibility = "visible";
      emits("doneUpload");
      dialog.value = false;
      break;
    }
  }
});

function start() {
  const detailTaskDialog = document.getElementById(
    "DetailTaskDialog"
  ) as HTMLElement;

  detailTaskDialog.style.visibility = "hidden"; // or "hidden" to hide

  dialog.value = true;
}

watch(methodAddDocument, (newValue) => {
  switch (newValue) {
    case 1: {
      position.value = 2;
      stepNumber.value = 4;
      updateStep(Section.Create);
      break;
    }
    case 2: {
      position.value = 2;
      stepNumber.value = 4;
      updateStep(Section.Approval);
      break;
    }
    case 3: {
      position.value = 2;
      stepNumber.value = 4;
      updateStep(Section.NonApproval);
      break;
    }
    case 4: {
      position.value = 2;
      stepNumber.value = 3;
      updateStep(Section.DownloadTemplate);
      break;
    }
    default: {
      stepNumber.value = 2;
      updateStep(1);
      break;
    }
  }
});

const updateStep = (_value) => (step.value = _value);

const updateMetadata = (_value) => {
  metadata.value = _value;
  updateStep(Section.CreateApprover);
  position.value = 3;
};

const updateApprover = (_value) => {
  approver.value = _value;

  if (props.idTaskTemplate == 0) {
    action.value = "Create Document";
  } else {
    action.value = "Create Document Standarisasi";
  }
  updateStep(Section.UploadProgress);
  position.value = 4;
};

const updateFile = (_value) => {
  position.value = 3;
  file.value = _value;
  if (_value.filetype == "Approval") {
    updateStep(Section.ApprovalMetadata);
  } else {
    updateStep(Section.NonApprovalMetadata);
  }
};

const updateMetadataApproval = (_value) => {
  metadata.value = _value;
  updateStep(Section.AssignApprover);
};

const updateMetadataNonApproval = (_value) => {
  metadata.value = _value;
  action.value = "Upload Non Approval Document";
  position.value = 4;
  updateStep(Section.UploadProgress);
};

const updateApproverDocumentApproval = (_value) => {
  approver.value = _value;
  action.value = "Upload Approval Document";
  position.value = 4;
  updateStep(Section.UploadProgress);
};

const updateDownload = (_value) => {
  metadata.value = _value;
  position.value = 3;
  action.value = "Download Document Template";
  updateStep(Section.UploadProgress);
};
</script>
<style scoped>
.buttonUpload-red {
  background: linear-gradient(180deg, #d6212a, #ff000d);
  font-size: 12px;
  font-weight: 900;
  text-align: center;
}

.btn-color-process {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: #fdfdfd;
  border-radius: 10px;
  padding-left: 15px;
  padding-right: 15px;
  margin-left: 10px;
  font-weight: 800;
  color: white;
}
</style>
