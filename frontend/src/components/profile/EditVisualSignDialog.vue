<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent width="700">
      <template v-slot:activator="{ props }">
        <v-btn
          v-bind="props"
          class="ma-2 ml-4 rounded-lg"
          variant="outlined"
          color="indigo"
          style="letter-spacing: -0.2px"
        >
          <v-icon left class="pr-3"> mdi-pencil </v-icon>
          Edit Visual Sign
        </v-btn>
      </template>
      <v-card class="rounded-lg">
        <v-sheet>
          <div>
            <div class="pt-5 pb-5 text-center text-18 text-blueTheme">
              Edit Visual Sign
            </div>
            <div
              class="pt-5 text-center text-18"
              style="position: absolute; right: 5px; top: -15px"
            >
              <v-btn
                class="mx-2"
                fab
                small
                variant="text"
                @click="dialog = false"
              >
                <v-icon color="#C0C0C0"> mdi-close </v-icon>
              </v-btn>
            </div>
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
              <v-icon size="80" color="#267DC2">mdi-cloud-upload</v-icon>
              <p
                style="color: #3a416f; margin-bottom: 5px !important"
                class="font-weight-bold"
              >
                Drag and Drop Here
              </p>
              <p
                style="color: #a6abc7; margin-bottom: 5px !important"
                class="font-weight-medium"
              >
                Or
              </p>
              <p
                style="
                  color: #ff000d;
                  margin-bottom: 5px !important;
                  cursor: pointer;
                "
                class="font-weight-medium"
                @click="handleFileImport"
              >
                Browse File
              </p>
              <span
                style="
                  font-weight: 400;
                  font-size: 14px;
                  line-height: 21px;
                  color: #a6abc7;
                "
                >Please Upload the PNG file with ratio 2:1</span
              >
              <template>
                <input
                  type="file"
                  accept="image/png"
                  class="d-none"
                  ref="file"
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
              <v-btn class="mr-4 btn-white" @click="dialog = false">
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
  </v-row>
</template>
<script>
import client from "@/library/ApiClient";

export default {
  components: {},
  data() {
    return {
      loader: 0,
      dialog: false,
      isSelecting: false,
      selectedFile: null,
      file: null,
      image: "",
      base64: null,
      isLoading: false,
      isDisable: "btn-blue",
    };
  },
  methods: {
    validateFile(file) {
      if (!file) return false;

      const MAX_FILE_SIZE = 10 * 1024 * 1024;

      if (file.type !== "image/png") {
        this.$root.toast.show({
          message: "PNG File Only!",
          color: "error",
          timeout: 5000,
        });
        return false;
      }

      if (file.size > MAX_FILE_SIZE) {
        this.$root.toast.show({
          message: "File size must be 10MB or less.",
          color: "error",
          timeout: 5000,
        });
        return false;
      }

      return true;
    },
    uploadVisualSign() {
      this.isLoading = true;
      this.isDisable = "btn-grey";
      /* eslint-disable */
      return client
        .updateVisualSignByUsername({
          store: this.$store,
          data: {
            visualImage: this.file
          }
        })
        .then((response) => {
          let color = "";
          if (response.plainData.responseCode === "011000") color = "success";
          else color = "error";

          this.$root.toast.show({
            message: response.plainData.responseMessage,
            color: color,
            timeout: 9000
          });
          this.isLoading = false;
          this.isDisable = "btn-blue";
        })
        .finally(() => {
          this.selectedFile = null;
          this.close();
        });
    },
    start() {
      this.dialog = true;
    },
    close() {
      this.dialog = false;
    },
    handleFileImport() {
      this.isSelecting = true;
      // After obtaining the focus when closing the FilePicker, return the button state to normal
      window.addEventListener(
        "focus",
        () => {
          this.isSelecting = false;
        },
        { once: true }
      );
      // Trigger click on the FileInput
      document.getElementById("uploaderButton").click();
      //   this.$refs.uploader.click();
    },
    onFileChanged(e) {
      const selectedFile = e.target.files[0];

      if (!this.validateFile(selectedFile)) {
        this.file = null;
        this.selectedFile = null;
        return;
      }

      this.selectedFile = URL.createObjectURL(selectedFile);
      this.file = selectedFile;
    },
    dragover(e) {
      e.preventDefault();
      this.isDragging = true;
    },
    dragleave() {
      this.isDragging = false;
    },
    drop(e) {
      e.preventDefault();
      const selectedFile = e.dataTransfer.files[0];

      if (!this.validateFile(selectedFile)) {
        this.file = null;
        this.selectedFile = null;
        return;
      }

      this.selectedFile = URL.createObjectURL(selectedFile);
      this.file = selectedFile;
      this.isDragging = false;
    }
  }
};
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
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
  height: 1.2px;
  width: 100%;
}

img {
  width: 200px;
  height: 100px;
}
</style>
