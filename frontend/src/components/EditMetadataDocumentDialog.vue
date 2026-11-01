<template>
  <div class="text-center">
    <v-dialog v-model="dialog" activator="parent" persistent width="70vw">
      <v-sheet style="border-radius: 15px">
        <v-card style="border-radius: 15px">
          <v-card-title class="text-center mt-2">
            Edit Metadata
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

          <v-sheet style="text-align: -webkit-center">
            <v-timeline
              truncate-line="both"
              direction="horizontal"
              style="width: 30vw"
              line-color="#065695"
            >
              <v-timeline-item
                :icon="position > 1 ? 'mdi-check' : ''"
                icon-color="white"
                :dot-color="position > 1 ? '#065695' : 'grey'"
                size="small"
              >
                <template v-slot:opposite> Step 1 </template>
              </v-timeline-item>
              <v-timeline-item
                :icon="position > 2 ? 'mdi-check' : ''"
                icon-color="white"
                :dot-color="position > 2 ? '#065695' : 'grey'"
                size="small"
              >
                <template v-slot:opposite> </template>
                Step 2
              </v-timeline-item>
              <v-timeline-item
                :icon="position > 3 ? 'mdi-check' : ''"
                icon-color="white"
                :dot-color="position > 3 ? '#065695' : 'grey'"
                size="small"
              >
                <template v-slot:opposite> Step 3</template>
              </v-timeline-item>
            </v-timeline>
          </v-sheet>
          <free-style-shimmer
            :is-loading="isLoading"
            v-for="i in 4"
            :key="i"
            height="5.5vh"
            width="100%"
            border-radius="5px"
            color="#DCDCDC"
            class="ml-6 mt-10 mr-6 mb-10"
          />
          <v-window v-model="step" v-if="!isLoading">
            <!-- <pre>  {{ current }}</pre> -->
            <v-window-item :value="Section.Edit">
              <edit-document-support-create
                :initialState="initialState"
                :document="_document"
                @updateStep="updateStep"
                @updateMetadata="updateMetadata"
              />
            </v-window-item>

            <v-window-item :value="Section.EditApprover">
              <edit-approver-create
                :initialState="initialState"
                @updateApprover="updateApprover"
                @updateStep="updateStep"
              />
            </v-window-item>

            <v-window-item :value="Section.UploadProgress">
              <edit-create-document
                @updateStep="updateStep"
                :metadata="metadata"
                :approver="approver"
                :action="action"
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
import EditDocumentSupportCreate from "@/components/upload/support/EditDocumentSupportCreate.vue";
import EditApproverCreate from "@/components/upload/support/EditApproverCreate.vue";
import EditCreateDocument from "@/components/upload/support/EditCreateDocument.vue";
import { mGetTaskDocumentSupportEditByIdDocument } from "@/models/upload";

defineExpose({ start });

defineComponent({
  components: {
    EditDocumentSupportCreate,
    EditApproverCreate,
    EditCreateDocument,
  },
});

enum Section {
  Edit = "EDIT",
  UploadProgress = "UPLOADPROGRESS",
  EditApprover = "EDITAPPROVER",
}

const emits = defineEmits(["doneUpload"]);
const step = ref<number | string>(Section.Edit);
const position = ref<number>(2);
const dialog = ref(false);
const current = ref<object>();
const isLoading = ref(false);
let action = ref("");
let metadata = ref({});
let approver = ref({});
let _document = ref({});
let initialState = ref();

function start(params) {
  current.value = params;
  _document.value = params;
  isLoading.value = true;
  const detailtaskdialog = document.getElementById(
    "DetailTaskDialog"
  ) as HTMLElement;
  detailtaskdialog.style.visibility = "hidden";
  mGetTaskDocumentSupportEditByIdDocument(params.id)
    .then((result) => {
      initialState.value = result;
    })
    .finally(() => {
      isLoading.value = false;
    });
  dialog.value = true;
}

watch(step, (newValue) => {
  switch (newValue) {
    case Section.Edit: {
      position.value = 2;
      updateStep(Section.Edit);
      break;
    }
    case "Close": {
      const detailtaskdialog = document.getElementById(
        "DetailTaskDialog"
      ) as HTMLElement;
      detailtaskdialog.style.visibility = "visible";
      emits("doneUpload");
      dialog.value = false;
      break;
    }
  }
});

const updateStep = (_value) => (step.value = _value);

const updateMetadata = (_value) => {
  metadata.value = _value;
  updateStep(Section.EditApprover);
  position.value = 3;
};

const updateApprover = (_value) => {
  approver.value = {
    value: _value.value,
    param: _value.param,
    documentId: initialState.value.id,
  };
  action.value = "Edit Document";
  updateStep(Section.UploadProgress);
  position.value = 4;
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
