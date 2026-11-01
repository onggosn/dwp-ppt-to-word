<template>
  <Teleport to="body">
    <v-dialog v-model="isShow" persistent width="700">
      <v-card class="rounded-lg">
        <v-sheet>
          <div>
            <div class="pl-5 pt-5 text-18 font-weight-medium">
              Add Visual Sign
            </div>
            <div
              class="pt-5 text-center text-18"
              style="position: absolute; right: 5px; top: -15px"
            >
              <v-btn
                class="mx-2"
                icon
                size="small"
                variant="text"
                @click="isShow = false"
              >
                <v-icon color="#C0C0C0"> mdi-close </v-icon>
              </v-btn>
            </div>
          </div>
          <div class="pl-5 pb-2 text-12">
            Please select one of the following options to add your visual
            signature.
          </div>
        </v-sheet>
        <v-sheet>
          <div class="pt-5 pb-2 text-16 text-center font-weight-medium">
            Upload
          </div>
          <v-btn
            elevation="0"
            class="d-block separatorHorizontal"
            style="cursor: none"
          />
        </v-sheet>
        <v-sheet class="pa-4 mt-2">
          <v-card
            @dragover="dragover"
            @dragleave="dragleave"
            @drop="drop"
            elevation="0"
            style="
              border-radius: 10px;
              padding-top: 60px;
              padding-bottom: 60px;
              border: 1px dashed #065695;
              text-align: -webkit-center;
            "
          >
            <v-sheet align="center" justify="center" v-if="!selectedFile">
              <img
                :src="PaperUploadSvg"
                alt="Paper Upload"
                style="width: 80px; height: 94px"
              />
              <p>
                <span
                  style="color: #404040; margin-bottom: 5px !important"
                  class="font-weight-semi-bold"
                  >Drag and Drop a Signature image or
                </span>
                <span
                  style="
                    color: #065391;
                    margin-bottom: 5px !important;
                    cursor: pointer;
                  "
                  class="font-weight-medium"
                  @click="handleFileImport"
                  >browse files</span
                >
              </p>
              <template>
                <input
                  type="file"
                  accept="image/png"
                  class="d-none"
                  ref="fileInput"
                  id="uploaderButton"
                  @change="onFileChanged"
                />
              </template>
            </v-sheet>
            <v-sheet v-else>
              <img :src="selectedFile" style="border-radius: 5px" />
            </v-sheet>
          </v-card>

          <v-sheet class="d-flex justify-space-between mt-4">
            <v-btn class="btn-red" elevation="2" @click="selectedFile = null">
              Clear
            </v-btn>
            <v-sheet class="d-flex justify-space-between">
              <v-btn class="mr-4 btn-white" @click="isShow = false">
                Cancel
              </v-btn>
              <v-btn
                elevation="2"
                :loading="isLoading"
                :class="isDisable"
                v-if="selectedFile"
                @click="uploadVisualSign"
              >
                Apply
              </v-btn>
              <v-btn
                class="btn-grey"
                elevation="2"
                v-if="!selectedFile"
                style="pointer-events: none"
              >
                Apply
              </v-btn>
            </v-sheet>
          </v-sheet>
        </v-sheet>
      </v-card>
    </v-dialog>
  </Teleport>
</template>
<script setup lang="ts">
import { ref, getCurrentInstance } from "vue";
import client from "@/library/ApiClient";
import { useStore } from "vuex";
import PaperUploadSvg from "/public/images/icon/paper-upload.svg";

const instance: any = getCurrentInstance()?.root.refs;
const store = useStore();

const emits = defineEmits(["uploadSuccess"]);

// Reactive data with types
const isShow = ref(false);
const isSelecting = ref(false);
const selectedFile = ref<string | null>(null);
const file = ref<File | null>(null);
const isLoading = ref(false);
const isDisable = ref("btn-blue");
const isDragging = ref(false);

const uploadVisualSign = (): Promise<void> => {
  isLoading.value = true;
  isDisable.value = "btn-grey";
  return client
    .updateVisualSignByUsername({
      store: store,
      data: {
        visualImage: file.value,
      },
    })
    .then((response: any) => {
      let color = "";
      if (response.plainData.responseCode === "011000") color = "success";
      else color = "error";

      instance.toast.show({
        message: response.plainData.responseMessage,
        color: color,
        timeout: 9000,
      });
      isLoading.value = false;
      isDisable.value = "btn-blue";
    })
    .finally(() => {
      selectedFile.value = null;
      hide();
      emits("uploadSuccess");
    });
};

const show = () => {
  isShow.value = true;
};

const hide = () => {
  isShow.value = false;
};

const handleFileImport = () => {
  isSelecting.value = true;
  window.addEventListener(
    "focus",
    () => {
      isSelecting.value = false;
    },
    { once: true }
  );
  const uploaderButton = document.getElementById(
    "uploaderButton"
  ) as HTMLInputElement;
  uploaderButton?.click();
};

const onFileChanged = (e: Event) => {
  const target = e.target as HTMLInputElement;
  const files = target.files;

  if (!files || files.length === 0) {
    return;
  }

  const fileType: string = files[0].type;
  if (fileType !== "image/png") {
    alert("PNG File Only!");
    return;
  }

  selectedFile.value = URL.createObjectURL(files[0]);
  file.value = files[0];
};

const dragover = (e: DragEvent) => {
  e.preventDefault();
  isDragging.value = true;
};

const dragleave = () => {
  isDragging.value = false;
};

const drop = (e: DragEvent) => {
  e.preventDefault();

  if (!e.dataTransfer?.files || e.dataTransfer.files.length === 0) {
    return;
  }

  const fileType: string = e.dataTransfer.files[0].type;
  if (fileType !== "image/png") {
    alert("PNG File Only!");
    return;
  }

  selectedFile.value = URL.createObjectURL(e.dataTransfer.files[0]);
  file.value = e.dataTransfer.files[0];
  isDragging.value = false;
};

defineExpose({
  show,
  hide,
});
</script>
<style scoped>
.btn-red {
  background: linear-gradient(180deg, #d6212a 0%, #ff000d 100%);
  /* Drop Shadow White Element */
  box-shadow: 0px 3px 7px rgba(133, 133, 133, 0.25);
  border-radius: 10px;
  color: white;
  letter-spacing: 0px;
  font-weight: 500;
}
.btn-blue {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  /* Drop Shadow White Element */

  box-shadow: 0px 3px 7px rgba(133, 133, 133, 0.25);
  border-radius: 10px;
  /* Drop Shadow White Element */
  box-shadow: 0px 3px 7px rgba(133, 133, 133, 0.25);
  border-radius: 10px;
  color: white;
  letter-spacing: 0px;
  font-weight: 500;
}
.btn-grey {
  background: linear-gradient(
    92.72deg,
    rgba(121, 121, 121, 0.9) 0%,
    rgba(187, 187, 187, 0.9) 152.21%
  );
  /* Drop Shadow White Element */

  box-shadow: 0px 3px 7px rgba(133, 133, 133, 0.25);
  border-radius: 10px;
  /* Drop Shadow White Element */
  box-shadow: 0px 3px 7px rgba(133, 133, 133, 0.25);
  border-radius: 10px;
  color: white;
  letter-spacing: 0px;
  font-weight: 500;
}

.btn-white {
  background: white;
  /* Drop Shadow White Element */

  border-radius: 10px;
  /* Drop Shadow White Element */
  border-radius: 10px;
  color: red;
  letter-spacing: 0px;
  font-weight: 600;
}
.separator {
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
}
.separatorHorizontal {
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #1668a9 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
  height: 2px;
  width: 100%;
}

img {
  width: 200px;
  height: 100px;
}
</style>
