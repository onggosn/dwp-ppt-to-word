<template>
  <v-dialog v-model="dialog" width="800" persistent>
    <template v-slot:activator="{ props }">
      <v-btn
        prepend-icon="mdi-plus"
        class="bg-gradient-darkblue mr-2 font-weight-bold"
        elevation="4"
        style="color: white; border-radius: 10px"
        v-bind="props"
      >
        Add FAQ
      </v-btn>
    </template>
    <v-card class="rounded-lg pa-4">
      <v-card-title class="d-flex justify-center align-center py-4 relative">
        <h3 class="text-h6 font-weight-bold" style="color: #065695">Add FAQ</h3>
        <v-btn
          icon="mdi-close"
          variant="text"
          class="btn-close"
          @click="close"
          style="position: absolute; right: 16px; top: 16px; color: #828282"
        />
      </v-card-title>
      <div class="mb-5 separator-gradient"></div>
      <v-card-text>
        <v-form ref="form">
          <v-row no-gutters>
            <v-col cols="12" class="mb-4">
              <p class="pb-2 text-left font-weight-bold" style="color: #065695">
                Title Section FAQ<span class="text-red">*</span>
              </p>
              <v-card class="rounded-lg" elevation="1">
                <v-text-field
                  v-model="question"
                  variant="solo"
                  placeholder="Input Title"
                  class="my-input"
                  density="default"
                  single-line
                  hide-details="auto"
                  required
                  @blur="v$.question.$touch()"
                ></v-text-field>
              </v-card>
              <div
                v-if="v$.question.$error"
                class="text-red text-caption mt-1 ml-3"
              >
                {{ v$.question.$errors[0]?.$message }}
              </div>
            </v-col>

            <v-col cols="12" class="mb-4">
              <p class="pb-2 text-left font-weight-bold" style="color: #065695">
                Description (optional)
              </p>
              <v-card class="rounded-lg" elevation="1">
                <v-text-field
                  v-model="answer"
                  variant="solo"
                  placeholder="Input Description"
                  class="my-input"
                  density="default"
                  single-line
                  hide-details="auto"
                ></v-text-field>
              </v-card>
            </v-col>

            <v-col cols="12" class="mb-4">
              <!-- Hidden File Input -->
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                style="display: none"
                @change="handleFileChange"
              />

              <v-btn
                v-if="!croppedImage"
                variant="outlined"
                class="text-capitalize rounded-lg"
                style="
                  color: #065695;
                  border-color: #065695;
                  letter-spacing: 0.1px;
                "
                prepend-icon="mdi-image-plus"
                @click="triggerFileInput"
              >
                Add Icon Section
              </v-btn>
              <div
                v-if="v$.selectedFile.$error"
                class="text-red text-caption mt-2"
              >
                {{ getErrorMessages(v$.selectedFile)[0] }}
              </div>
              <!-- Display selected file preview -->
              <div
                v-if="croppedImage"
                style="position: relative; width: fit-content"
              >
                <v-img
                  :src="croppedImage"
                  width="100"
                  height="100"
                  class="rounded-lg border"
                  cover
                ></v-img>

                <v-btn
                  size="x-small"
                  color="white"
                  elevation="3"
                  class="rounded-lg"
                  style="
                    position: absolute;
                    top: -10px;
                    right: -10px;
                    z-index: 10;
                    width: 24px;
                    height: 24px;
                    min-width: 0;
                    border-radius: 6px;
                  "
                  @click="removeImage"
                >
                  <v-icon color="black" size="16">mdi-close</v-icon>
                </v-btn>

                <!-- <p
                  class="text-caption text-grey mt-1 text-truncate"
                  style="max-width: 200px"
                >
                  {{ selectedFileName }}
                </p> -->
              </div>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
      <v-card-actions class="justify-end px-6 pb-6 pt-0">
        <v-btn class="btn-prev px-6" height="45" elevation="2" @click="close">
          Cancel
        </v-btn>
        <v-btn
          :loading="isLoading"
          class="btn-next px-6"
          height="45"
          variant="flat"
          elevation="2"
          @click="save"
        >
          Create
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- Cropper Dialog -->
  <v-dialog v-model="cropperDialog" width="600" persistent>
    <v-card class="rounded-xl pa-4">
      <v-card-title class="d-flex justify-center align-center py-4 relative">
        <h3 class="text-h6 font-weight-bold" style="color: #065695">
          Crop Image
        </h3>
        <v-btn
          icon="mdi-close"
          variant="text"
          class="btn-close"
          @click="closeCropper"
          style="position: absolute; right: 16px; top: 16px; color: #828282"
        />
      </v-card-title>
      <!-- <v-divider class="mb-5"></v-divider> -->
      <div class="mb-5 separator-gradient"></div>
      <v-card-text>
        <div style="width: 100%; display: flex; justify-content: center">
          <vue-cropper
            v-if="imageUrl"
            ref="cropper"
            :src="imageUrl"
            style="width: 100%; max-height: 500px"
            alt="Source Image"
            :aspect-ratio="1"
            :view-mode="1"
            drag-mode="move"
            :background="false"
            preview=".preview"
          />
        </div>
      </v-card-text>
      <v-card-actions class="justify-end px-6 pb-6 pt-0 mt-5">
        <v-btn
          class="btn-prev px-6"
          height="45"
          elevation="2"
          @click="closeCropper"
        >
          Cancel
        </v-btn>
        <v-btn
          class="btn-next px-6"
          height="45"
          variant="flat"
          elevation="2"
          @click="cropImage"
        >
          Crop & Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import useVuelidate from "@vuelidate/core";
import { required, helpers } from "@vuelidate/validators";
import { ref, computed, getCurrentInstance } from "vue";
import { useStore } from "vuex";
import VueCropper from "vue-cropperjs";
import { getErrorMessages, isError } from "@/v2/helpers/validation";
import "cropperjs/dist/cropper.css";

// eslint-disable-next-line
const emit = defineEmits(["onSuccess"]);
const store = useStore();
const dialog = ref(false);
const question = ref("");
const answer = ref("");
const fileInput = ref<HTMLInputElement | null>(null);
const selectedFileName = ref<string | null>(null);
const selectedFile = ref<File | null>(null);
const isLoading = ref(false);

// Cropper state
const cropper = ref<any>(null);
const cropperDialog = ref(false);
const imageUrl = ref<string | null>(null);
const croppedImage = ref<string | null>(null);
const originalMimeType = ref<string | null>(null);

const { root } = getCurrentInstance() as any;

const MAX_FILE_SIZE = 1 * 1024 * 1024;
const ALLOWED_TYPES = ["image/jpeg", "image/jpg", "image/png", "image/svg+xml"];

const rules = computed(() => ({
  question: {
    required: helpers.withMessage("Wajib Diisi", required),
  },
  selectedFile: {
    required: helpers.withMessage("Wajib Diisi", required),
    validType: helpers.withMessage(
      "Invalid file type. Only JPG, JPEG, PNG and SVG are allowed.",
      (file: File | null) => !file || ALLOWED_TYPES.includes(file.type)
    ),
    validSize: helpers.withMessage(
      "File size exceeds 1 MB limit.",
      (file: File | null) => !file || file.size <= MAX_FILE_SIZE
    ),
  },
}));

const v$ = useVuelidate(rules, {
  question,
  selectedFile,
  croppedImage,
});

function triggerFileInput() {
  fileInput.value?.click();
}

function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    const file = target.files[0];
    originalMimeType.value = file.type;
    selectedFile.value = file;
    v$.value.selectedFile.$touch();

    if (v$.value.selectedFile.$error) {
      target.value = "";
      return;
    }

    selectedFileName.value = file.name;

    // Create URL for the image
    const reader = new FileReader();
    reader.onload = (e) => {
      imageUrl.value = e.target?.result as string;
      cropperDialog.value = true;
    };
    reader.readAsDataURL(file);
  }
}

function cropImage() {
  if (cropper.value) {
    const canvas = cropper.value.getCroppedCanvas();

    if (
      originalMimeType.value === "image/jpeg" ||
      originalMimeType.value === "image/jpg"
    ) {
      croppedImage.value = canvas.toDataURL("image/jpeg", 0.85);
    } else if (originalMimeType.value === "image/png") {
      croppedImage.value = canvas.toDataURL("image/png");
    } else {
      croppedImage.value = canvas.toDataURL("image/png");
    }

    closeCropper();
  }
}

function closeCropper() {
  cropperDialog.value = false;
  // If cancelled and no cropped image, maybe reset file input?
  // But user might just want to cancel cropping but keep file (behavior depends on req)
  // Assuming if cancel crop, we cancel the file selection too
  if (!croppedImage.value) {
    selectedFileName.value = null;
    selectedFile.value = null;
    imageUrl.value = null;
    if (fileInput.value) {
      fileInput.value.value = "";
    }
  }
}

function validateAndExtractBase64(base64: string): string {
  const [header, data] = base64.split(",");

  if (!header || !data) {
    throw new Error("Invalid image format.");
  }

  const mimeType = header.match(/data:(.*?);base64/)?.[1];

  if (!mimeType || !ALLOWED_TYPES.includes(mimeType)) {
    throw new Error(
      "Invalid file type. Only JPG, JPEG, PNG and SVG are allowed."
    );
  }

  const fileSize = Math.ceil((data.length * 3) / 4);

  if (fileSize > MAX_FILE_SIZE) {
    throw new Error("File size exceeds 1 MB limit.");
  }

  return data;
}

const save = async () => {
  isLoading.value = true;

  try {
    const valid = await v$.value.$validate();

    if (!valid) return;

    const pureBase64 = croppedImage.value
      ? validateAndExtractBase64(croppedImage.value)
      : null;

    const payload = {
      topicName: question.value.trim(),
      description: answer.value?.trim() || "",
      iconName: selectedFileName.value,
      topicIcon: pureBase64,
    };

    const response = await store.dispatch("adminStore/addFAQTopic", payload);

    root.refs.toast.show({
      message: response.responseMessage || "Successfully Created",
      color: "success",
      timeout: 3000,
    });

    emit("onSuccess", payload);
    close();
  } catch (error: any) {
    root.refs.toast.show({
      message:
        error?.responseMessage ||
        error?.message ||
        "Failed to create FAQ topic.",
      color: "error",
      timeout: 3000,
    });
  } finally {
    isLoading.value = false;
  }
};

function close() {
  dialog.value = false;
  // Reset form
  question.value = "";
  answer.value = "";
  selectedFileName.value = null;
  selectedFile.value = null;
  imageUrl.value = null;
  croppedImage.value = null;
  if (fileInput.value) {
    fileInput.value.value = "";
  }
  v$.value.$reset();
}
function removeImage() {
  selectedFileName.value = null;
  selectedFile.value = null;
  imageUrl.value = null;
  croppedImage.value = null;
  if (fileInput.value) {
    fileInput.value.value = "";
  }
}
</script>

<style scoped>
.bg-gradient-darkblue {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
}
.btn-next {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  border-radius: 10px !important;
  color: white !important;
  font-weight: 700;
  letter-spacing: 0;
  text-transform: none;
}

.btn-prev {
  background: white;
  border-radius: 10px !important;
  color: #267dc2 !important;
  font-weight: 700;
  letter-spacing: 0;
  text-transform: none;
}

:deep(.v-field--variant-solo) {
  box-shadow: none !important;
  border-radius: 10px;
}

:deep(.v-field__input) {
  min-height: 48px;
}

.text-red {
  color: #f44336;
}
/* Ensure cropper container has height */
:deep(.cropper-container) {
  width: 100%;
}
</style>
