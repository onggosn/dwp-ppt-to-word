<template>
  <div class="d-flex flex-wrap justify-space-between mb-6 mt-5 pa-5">
    <v-sheet class="pt-4 pb-4 pl-2 mb-4 blue-gradient" width="100%">
      <b style="color: #fff">Upload Document</b>
    </v-sheet>

    <v-sheet width="100%">
      <p class="font-weight-bold mb-2 text-greyTheme">
        Document Title <span style="color: red">*</span>
      </p>
      <v-text-field
        :label="fileToUploadName"
        variant="solo"
        disabled
      ></v-text-field>
    </v-sheet>
    <v-sheet width="100%" class="">
      <p class="font-weight-bold mb-2 text-greyTheme">
        Attach Document
        <span style="color: red">*</span>
      </p>
      <v-sheet v-if="!selectedFile">
        <v-sheet
          @dragover="dragover"
          @dragleave="dragleave"
          @drop="dropApproval"
          style="
            border-style: dotted;
            text-align-last: center;
            border: 2.3px dotted #065695;
            padding: 70px;
            border-radius: 10px;
          "
        >
          <v-icon icon="mdi-cloud-upload-outline" size="120" color="#065695">
          </v-icon>
          <br />

          <input
            type="file"
            multiple
            name="file"
            id="fileInputApproval"
            class="hidden-input d-none"
            @change="onFileChangedApproval"
            ref="file"
            accept=".pptx, .docx"
          />
          <p>Drag and Drop Here</p>
          <p>Or</p>
          <v-btn
            @click="handleFileImportApproval"
            density="compact"
            variant="text"
            color="red"
            style="text-decoration: underline"
            >Browse File</v-btn
          >
        </v-sheet>
      </v-sheet>
      <v-sheet
        v-else
        style="
          border-style: dotted;
          text-align-last: center;
          border: 2.3px dotted #065695;
          padding: 5px;
          border-radius: 10px;
        "
      >
        <v-btn
          size="small"
          elevation="3"
          style="
            right: 0;
            display: block;
            margin-right: 3vw;
            position: absolute;
            margin-top: 0.5vw;
          "
          @click="clearUpload()"
        >
          <v-icon color="#e5252a" icon="mdi-delete"></v-icon
        ></v-btn>
        <img
          v-if="fileToUploadName.includes('pptx')"
          class="mb-3"
          src="/images/docImage/iconPpt.png"
          style="width: 2.4vw; height: 6vh; margin-top: 10vh"
        />

        <img
          v-else
          class="mb-3"
          src="/images/docImage/iconDoc.png"
          style="width: 2.4vw; height: 6vh; margin-top: 10vh"
        />
        <p style="margin-bottom: 10vh">{{ fileToUploadName }}</p>
      </v-sheet>
    </v-sheet>
    <v-sheet width="100%" style="text-align-last: end" class="mt-5">
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
        @click="back()"
      >
        Back
      </v-btn>
      <v-btn
        elevation="3"
        :class="
          selectedFile ? 'btn-color-process' : 'btn-color-process-disabled'
        "
        class="btn-color-process mr-4"
        btn-color-process
        style="
          border-radius: 10px;
          padding-left: 15px;
          padding-right: 15px;
          margin-left: 10px;
          font-weight: 800;
          color: white;
        "
        @click="updateFile()"
      >
        Next
      </v-btn>
    </v-sheet>
  </div>
</template>
<script setup lang="ts">
import { ref, defineEmits } from "vue";

const emits = defineEmits(["updateStep", "updateFile"]);

let fileToUploadName = ref("Please input a file");
let fileToUploadSize = "";
let selectedFile = ref("");
let isDragging = ref(false);
let fileToUpload = null;

const dragover = (e) => {
  e.preventDefault();
  isDragging.value = true;
};

const dragleave = () => {
  isDragging.value = false;
};

const dropApproval = (e) => {
  e.preventDefault();
  const fileType = e.dataTransfer.files[0].type;
  // if (
  //   fileType !=
  //   "application/vnd.openxmlformats-officedocument.presentationml.presentation"
  // ) {
  //   alert("Please upload Pptx File or Docx");
  //   return;
  // }

  switch (fileType) {
    case "application/vnd.openxmlformats-officedocument.presentationml.presentation":
    case "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {
      break;
    }
    default: {
      alert("Please upload Pptx File or Docx");
      return;
    }
  }

  const maxSize = 150 * 1024 * 1024;
  if (e.dataTransfer.files[0].size > maxSize) {
    alert("File size is more than 150MB");
    return;
  }

  fileToUpload = e.dataTransfer.files[0];
  fileToUploadName.value = e.dataTransfer.files[0].name;
  fileToUploadSize = e.dataTransfer.files[0].size;
  selectedFile.value = URL.createObjectURL(e.dataTransfer.files[0]);
  isDragging.value = false;
};

const onFileChangedApproval = (e) => {
  switch (e.target.files[0].type) {
    case "application/vnd.openxmlformats-officedocument.presentationml.presentation":
    case "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {
      break;
    }
    default: {
      alert("Please upload Pptx File or Docx");
      return;
    }
  }

  const maxSize = 150 * 1024 * 1024;
  if (e.target.files[0].size > maxSize) {
    alert("File size is more than 150MB");
    const upl = document?.getElementById("fileInputApproval") as HTMLElement;
    upl.value = null;
    return;
  }

  fileToUpload = e.target.files[0];
  fileToUploadName.value = e.target.files[0].name;
  fileToUploadSize = e.target.files[0].size;
  selectedFile.value = URL.createObjectURL(e.target.files[0]);
};

const handleFileImportApproval = () => {
  window.addEventListener(
    "focus",
    () => {
      undefined;
    },
    { once: true }
  );
  document?.getElementById("fileInputApproval")?.click();
};

const clearUpload = () => {
  fileToUploadName.value = "Please input file name";
  selectedFile.value = "";
};

const back = () => emits("updateStep", 1);
const updateFile = () =>
  emits("updateFile", {
    file: fileToUpload,
    filename: fileToUploadName.value,
    filesize: fileToUploadSize,
    filetype: "Approval",
  });
</script>

<style scoped>
.btn-color-process {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: #fdfdfd;
}

.btn-color-process-disabled {
  background: linear-gradient(92.09deg, darkgrey -46.47%, grey 157.9%);
  color: #fdfdfd;
  pointer-events: none;
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
