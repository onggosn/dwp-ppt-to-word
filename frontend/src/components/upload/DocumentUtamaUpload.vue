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

          <!-- <v-sheet style="text-align: -webkit-center">
            <v-timeline
              truncate-line="both"
              direction="horizontal"
              style="width: 30vw"
              line-color="#065695"
            >
              <v-timeline-item
                icon="mdi-check"
                icon-color="white"
                dot-color="#065695"
                size="small"
              >
                <template v-slot:opposite> Step 1 </template>
              </v-timeline-item>
              <v-timeline-item
                :icon="position > 1 ? 'mdi-check' : ''"
                icon-color="white"
                :dot-color="position > 1 ? '#065695' : 'grey'"
                size="small"
              >
                <template v-slot:opposite> </template>
                Step 2
              </v-timeline-item>
              <v-timeline-item
                :icon="position > 2 ? 'mdi-check' : ''"
                icon-color="white"
                :dot-color="position > 2 ? '#065695' : 'grey'"
                size="small"
              >
                <template v-slot:opposite> Step 3 </template>
              </v-timeline-item>
              <v-timeline-item
                :icon="position > 3 ? 'mdi-check' : ''"
                icon-color="white"
                :dot-color="position > 3 ? '#065695' : 'grey'"
                size="small"
              >
                <template v-slot:opposite> </template>
                Step 4
              </v-timeline-item>
            </v-timeline>
          </v-sheet> -->
          <v-window v-model="step">
            <v-window-item :value="1">
              <v-sheet class="ml-10 mr-10 mt-10 mb-10">
                <v-autocomplete
                  v-model="methodAddDocument"
                  class="rounded-lg"
                  label="Choose Method Add Document"
                  :items="method"
                  variant="solo"
                ></v-autocomplete>
              </v-sheet>
            </v-window-item>

            <v-window-item :value="Section.Create">
              <create-document
                @updateStep="updateStep"
                @updateMetadata="updateMetadata"
              />
            </v-window-item>

            <v-window-item :value="Section.CreateApprover">
              <assign-approver
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

            <!-- <v-window-item :value="Section.ApprovalMetadata">
              <approval-metadata
                :param="'Approval'"
                @updateStep="updateStep"
                @updateMetadataApproval="updateMetadataApproval"
              />
            </v-window-item> -->

            <!-- <v-window-item :value="Section.AssignApprover">
              <assign-approver-document-approval
                @updateStep="updateStep"
                @updateApproverDocumentApproval="updateApproverDocumentApproval"
              />
            </v-window-item> -->

            <v-window-item :value="Section.NonApproval">
              <create-document-non-approval
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
          </v-window>

          <v-divider />
        </v-card>
      </v-sheet>
    </v-dialog>
  </div>
</template>
<script setup lang="ts">
import { ref, watch, defineComponent, defineEmits, defineExpose } from "vue";
import CreateDocument from "@/components/upload/utama/CreateDocument.vue";
import AssignApprover from "@/components/upload/utama/AssignApprover.vue";
import UploadCreateDocument from "@/components/upload/utama/UploadCreateDocument.vue";
import CreateDocumentApprovalSupport from "@/components/upload/support/CreateDocumentApprovalSupport.vue";
import CreateDocumentNonApproval from "@/components/upload/utama/CreateDocumentNonApproval.vue";
import NonApprovalMetadata from "@/components/upload/utama/NonApprovalMetadata.vue";
import Stepper from "@/components/stepper/CustomStepper.vue";

defineExpose({ start });

defineComponent({
  components: {
    Stepper,
    CreateDocument,
    AssignApprover,
    UploadCreateDocument,
    CreateDocumentNonApproval,
    NonApprovalMetadata,
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
}

const emits = defineEmits(["doneUpload"]);
const step = ref<number | string>(1);
const position = ref<number>(1);
const dialog = ref(false);
let action = ref("");
let methodAddDocument = ref("");
const metadata = ref();
const approver = ref({});
const file = ref({});
const stepNumber = ref(2);
const method = ["Create Document", "Upload Non-Approval Document"];

watch(step, (newValue) => {
  switch (newValue) {
    case 1: {
      position.value = 1;
      methodAddDocument.value = "";
      break;
    }
    case Section.Create: {
      position.value = 2;
      updateStep(Section.Create);
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
    case "Create Document": {
      position.value = 2;
      stepNumber.value = 4;
      updateStep(Section.Create);
      break;
    }
    case "Upload Non-Approval Document": {
      position.value = 2;
      stepNumber.value = 4;
      updateStep(Section.NonApproval);
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
  action.value = "Create Document";
  updateStep(Section.UploadProgress);
  position.value = 4;
};

const updateFile = (_value) => {
  position.value = 3;
  file.value = _value;
  updateStep(Section.NonApprovalMetadata);
};

// const updateMetadataApproval = (_value) => {
//   metadata.value = _value;
//   updateStep(Section.AssignApprover);
// };

const updateMetadataNonApproval = (_value) => {
  metadata.value = _value;
  action.value = "Upload Non Approval Document";
  position.value = 4;
  updateStep(Section.UploadProgress);
};

// const updateApproverDocumentApproval = (_value) => {
//   approver.value = _value;
//   action.value = "Upload Approval Document";
//   position.value = 4;
//   updateStep(Section.UploadProgress);
// };
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
