<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent width="826">
      <template v-slot:activator="{ props }">
        <v-btn
          v-bind="props"
          class="rounded-lg ml-2 font-weight-bold"
          min-width="0"
          variant="outlined"
          color="#065695"
          prepend-icon="mdi-pencil"
          @click="handleShowDialog"
        >
          Edit
        </v-btn>
      </template>
      <v-card class="rounded-lg">
        <v-sheet>
          <div>
            <div class="pt-5 pb-5 text-center text-18 text-blueTheme">
              Edit Formasi ADG
            </div>
            <div
              class="pt-5 text-center text-18"
              style="position: absolute; right: 5px; top: -15px"
            >
              <v-btn
                :loading="loadingData"
                class="mx-2"
                fab
                small
                variant="text"
                @click="close()"
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
          <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
            Detail Event Banner<span style="color: red">*</span>
          </p>
          <v-card
            @dragover="dragover"
            @dragleave="dragleave"
            @drop="drop($event, 'event')"
            elevation="0"
            style="
              border-radius: 10px;
              padding-top: 60px;
              padding-bottom: 60px;
              border: 1px dashed #065695;
              text-align: -webkit-center;
            "
          >
            <v-sheet align="center" justify="center" v-if="!selectedFileEvent">
              <v-icon size="80" color="#267DC2">mdi-cloud-upload</v-icon>
              <p>
                Drag and Drop a image or
                <strong
                  style="
                    color: blue;
                    margin-bottom: 5px !important;
                    cursor: pointer;
                  "
                  class="font-weight-medium"
                  @click="handleFileImport('event')"
                  >Browse File</strong
                >
              </p>
              <span
                style="
                  font-weight: 400;
                  font-size: 14px;
                  line-height: 21px;
                  color: #a6abc7;
                "
                >Please Upload a PNG file with a ratio 1:2 aspect ratio and a
                maximum file size of 5MB</span
              >
              <template>
                <input
                  type="file"
                  accept="image/png"
                  class="d-none"
                  ref="file"
                  id="uploaderButtonEvent"
                  @change="onFileChanged($event, 'event')"
                />
              </template>
            </v-sheet>
            <v-sheet v-else>
              <v-img
                :src="selectedFileEvent"
                @error="validateBanner($event)"
                style="border-radius: 8px; width: 100px"
                aspect-ratio="1/2"
              ></v-img>
              <div class="d-flex justify-center mt-2 mb-2">
                <v-btn
                  style="
                    background: linear-gradient(
                      180deg,
                      #d6212a 0%,
                      #ff000d 100%
                    );
                    /* Drop Shadow White Element */
                    box-shadow: 0px 3px 7px rgba(133, 133, 133, 0.25);
                    border-radius: 5px;
                    color: white;
                    letter-spacing: 0px;
                  "
                  elevation="2"
                  @click="selectedFileEvent = ''"
                >
                  Clear
                </v-btn>
              </div>
            </v-sheet>
          </v-card>
          <!-- <div class="ml-2 mt-1" style="color: red; font-size: 12px">
            {{
              v$.formTempData.bannerEventDetail.$errors.length > 0
                ? "Banner Event Detail is required"
                : ""
            }}
          </div> -->

          <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold pt-4">
            Homepage Event Banner<span style="color: red">*</span>
          </p>
          <v-card
            @dragover="dragover"
            @dragleave="dragleave"
            @drop="drop($event, 'homepage')"
            elevation="0"
            style="
              border-radius: 10px;
              padding-top: 60px;
              padding-bottom: 60px;
              border: 1px dashed #065695;
              text-align: -webkit-center;
            "
          >
            <v-sheet align="center" justify="center" v-if="!selectedFileBanner">
              <v-icon size="80" color="#267DC2">mdi-cloud-upload</v-icon>
              <p>
                Drag and Drop a image or
                <strong
                  style="
                    color: blue;
                    margin-bottom: 5px !important;
                    cursor: pointer;
                  "
                  class="font-weight-medium"
                  @click="handleFileImport('homepage')"
                  >Browse File</strong
                >
              </p>
              <span
                style="
                  font-weight: 400;
                  font-size: 14px;
                  line-height: 21px;
                  color: #a6abc7;
                "
                >Please Upload a PNG file with a ratio 2:1 aspect ratio and a
                maximum file size of 5MB</span
              >
              <template>
                <input
                  type="file"
                  accept="image/png"
                  class="d-none"
                  ref="file"
                  id="uploaderButtonBanner"
                  @change="onFileChanged($event, 'homepage')"
                />
              </template>
            </v-sheet>
            <v-sheet v-else>
              <v-img
                :src="selectedFileBanner"
                @error="validateBanner($event)"
                style="border-radius: 8px; width: 100px"
                aspect-ratio="2/1"
              >
              </v-img>
              <div class="d-flex justify-center mt-2 mb-2">
                <v-btn
                  style="
                    background: linear-gradient(
                      180deg,
                      #d6212a 0%,
                      #ff000d 100%
                    );
                    box-shadow: 0px 3px 7px rgba(133, 133, 133, 0.25);
                    border-radius: 5px;
                    color: white;
                    letter-spacing: 0px;
                  "
                  elevation="2"
                  @click="selectedFileBanner = ''"
                >
                  Clear
                </v-btn>
              </div>
            </v-sheet>
          </v-card>

          <p class="ml-2 pb-1 pt-4 text-left text-darkBlue font-weight-bold">
            Effective Date<span style="color: red">*</span>
          </p>
          <VueDatePicker
            v-model="formTempData.effectiveDate"
            :year-range="[minYear, maxYear]"
            :enable-time-picker="false"
            :month-change-on-scroll="false"
            auto-apply
            model-type="dd/MM/yyyy"
            :alt-position="() => ({ top: -280, left: 0 })"
          >
            <template #trigger>
              <v-text-field
                variant="solo"
                placeholder="Choose Date"
                class="pl-2 pr-2"
                :value="formTempData.effectiveDate"
              >
                <template v-slot:append-inner>
                  <v-img
                    :width="30"
                    :src="require('@/v2/assets/icon/date.svg')"
                  />
                </template>
              </v-text-field>
            </template>

            <template #calendar-header="{ index, day }">
              <div :class="index === 5 || index === 6 ? 'red-color' : ''">
                {{ day }}
              </div>
            </template>
          </VueDatePicker>

          <v-col :cols="12" class="">
            <p class="pb-3 text-left text-darkBlue font-weight-bold">
              Status<span style="color: red">*</span>
            </p>
            <v-radio-group
              v-model="formTempData.status"
              inline
              style="margin-left: -8px"
              hide-details
            >
              <v-radio
                label="Active"
                :value="'Active'"
                color="#267DC2"
                class="me-2"
              ></v-radio>
              <v-radio
                label="In Active"
                :value="'In Active'"
                color="#267DC2"
                class="me-2"
              ></v-radio>
            </v-radio-group>
          </v-col>

          <div v-for="(item, idx) in formTempInputADG" :key="idx">
            <v-col :cols="12">
              <v-row
                class="rounded-lg px-1 py-2 mt-1 mx-0"
                style="border: 2px #babcca solid"
              >
                <p class="text-darkBlue font-weight-bold form-title">
                  ADG {{ idx + 1 }}
                </p>
                <v-col :cols="12">
                  <p class="text-darkBlue">
                    Nama ADG<span style="color: red">*</span>
                  </p>
                  <v-autocomplete
                    v-model="item.namaAdg"
                    clearable
                    variant="solo"
                    placeholder="Input Name"
                    :items="item.listNamaAdg"
                    :item-title="'value'"
                    loading-text="Loading..."
                    @click:clear="
                      (item.namaAdg = ''),
                        (item.pangkat = ''),
                        (item.jabatan = ''),
                        (item.email = ''),
                        (item.adgBidang = '')
                    "
                    return-object
                    v-model:search="item.searchNamaAdg"
                    @update:search="(value) => handleSearchNameAdg(value, idx)"
                    @update:modelValue="updateAdgSelected($event, idx)"
                    :error-messages="
                      v$.formTempInputADG.$validator.$response.$errors[idx]
                        .namaAdg.length > 0
                        ? 'namaAdg is required'
                        : ''
                    "
                  >
                    <template v-slot:item="{ props, item }">
                      <v-list-item
                        class="mt-2"
                        v-bind="props"
                        :title="item.raw.value"
                        :subtitle="item.raw?.inputEmail"
                      ></v-list-item>
                    </template>
                  </v-autocomplete>
                  <p class="text-darkBlue">
                    Pangkat<span style="color: red">*</span>
                  </p>
                  <v-text-field
                    variant="solo"
                    v-model="item.pangkat"
                    readonly
                    class="border-radius-dwp no-shadow"
                    bg-color="#DFDFDF"
                    style="border-radius: 8px"
                    :error-messages="
                      v$.formTempInputADG.$validator.$response.$errors[idx]
                        .pangkat.length > 0
                        ? 'pangkat is required'
                        : ''
                    "
                  ></v-text-field>
                  <p class="text-darkBlue">
                    Jabatan<span style="color: red">*</span>
                  </p>
                  <v-text-field
                    variant="solo"
                    v-model="item.jabatan"
                    readonly
                    class="border-radius-dwp no-shadow"
                    bg-color="#DFDFDF"
                    style="border-radius: 8px"
                    :error-messages="
                      v$.formTempInputADG.$validator.$response.$errors[idx]
                        .jabatan.length > 0
                        ? 'jabatan is required'
                        : ''
                    "
                  ></v-text-field>
                  <p class="text-darkBlue">
                    Email<span style="color: red">*</span>
                  </p>
                  <v-text-field
                    variant="solo"
                    v-model="item.email"
                    readonly
                    class="border-radius-dwp no-shadow"
                    bg-color="#DFDFDF"
                    style="border-radius: 8px"
                    :error-messages="
                      v$.formTempInputADG.$validator.$response.$errors[idx]
                        .email.length > 0
                        ? 'email is required'
                        : ''
                    "
                  ></v-text-field>
                  <p class="text-darkBlue">
                    Bidang<span style="color: red">*</span>
                  </p>
                  <v-text-field
                    variant="solo"
                    v-model="item.adgBidang"
                    class="border-radius-dwp no-shadow"
                    style="border-radius: 8px"
                    :error-messages="
                      v$.formTempInputADG.$validator.$response.$errors[idx]
                        .adgBidang.length > 0
                        ? 'Bidang is required'
                        : ''
                    "
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-col>
            <div class="d-flex px-1 py-2 mt-1 mx-0">
              <v-btn
                v-if="idx === formTempInputADG.length - 1"
                prepend-icon="mdi-plus"
                class="bg-gradient-darkblue mr-2 font-weight-bold"
                elevation="4"
                :loading="loadingData"
                style="color: white; border-radius: 10px"
                @click="handleAddInputADG"
              >
                Add ADG
              </v-btn>
              <v-btn
                v-if="formTempInputADG.length > 1"
                class="btn-red"
                elevation="2"
                :loading="loadingData"
                @click="handleDeleteInputADG(idx)"
              >
                <v-icon icon="mdi-delete" color="white"></v-icon>Delete
              </v-btn>
            </div>
          </div>

          <v-sheet class="d-flex justify-end mt-4">
            <v-sheet class="d-flex justify-space-between">
              <v-btn
                class="mr-4 text-darkBlue font-weight-bold border-radius-dwp"
                elevation="2"
                :loading="loadingData"
                @click="close()"
              >
                Cancel
              </v-btn>
              <v-btn
                class="bg-gradient-darkblue rounded-lg px-2 font-weight-bold"
                style="color: white; border-radius: 10px"
                min-width="0"
                elevation="2"
                :loading="loadingData"
                @click="handleSaveAll"
              >
                Save
              </v-btn>
            </v-sheet>
          </v-sheet>
        </v-sheet>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script setup lang="ts">
import { ref, getCurrentInstance, computed } from "vue";
import { useStore } from "vuex";
import { useVuelidate } from "@vuelidate/core";
import { AdgForm, DetailADGSave } from "@/v2/Type";
import { email, required, helpers } from "@vuelidate/validators";
const instance = ref<any>(getCurrentInstance()?.root.refs);
const store = useStore();
const props = defineProps({
  formData: {
    type: Object,
    default: () => ({}),
  },
  idFormasi: {
    type: String,
    default: "",
  },
});
const emit = defineEmits<{
  (e: "refreshData", value: string): void;
}>();
const dialog = ref(false);
const isSelecting = ref(false);
const imgSrcEventBase64 = ref("");
const imgSrcBannerBase64 = ref("");
const selectedFileEvent = ref("");
const selectedFileBanner = ref("");
const isDragging = ref(false);
let formTempData = ref({
  effectiveDate: "25/12/2023",
  status: "",
  bannerEventDetail: null,
  homepageEventBanner: null,
});
let formTempInputADG = ref<AdgForm[]>([]);
const loadingData = ref(false);
const fileEvent = ref<File | null>(null);
const fileBanner = ref<File | null>(null);
const minYear = computed(() => new Date().getFullYear() - 5);
const maxYear = computed(() => new Date().getFullYear() + 5);

const rules = {
  formTempInputADG: {
    $validator: helpers.forEach({
      namaAdg: { required },
      jabatan: { required },
      pangkat: { required },
      email: { required, email },
      adgBidang: { required },
    }),
  },
};
const v$ = useVuelidate(rules, { formTempInputADG });

async function validateBanner(temp) {
  console.log(temp);
  // try {
  //   await this.checkImageUrl(temp);
  // } catch (error) {
  //   // alert("URL Gambar tidak valid atau server tidak terjangkau!");
  //   this.$root.toast.show({
  //     message: "Gagal memuat gambar",
  //     color: "error",
  //     timeout: 3000,
  //   });
  // }
}
// function checkImageUrl(url) {
//   return new Promise((resolve, reject) => {
//     const img = new Image();

//     img.onload = () => resolve(true); // URL Oke
//     img.onerror = () => reject(false); // URL Error (termasuk ERR_NAME_NOT_RESOLVED)

//     img.src = url;
//   });
// }
function updateAdgSelected(temp, idx) {
  formTempInputADG.value[idx].email = temp?.inputEmail;
  formTempInputADG.value[idx].jabatan = temp?.jabatanName;
  formTempInputADG.value[idx].pangkat = temp?.gradeName;
}
function handleSearchNameAdg(value, idx) {
  store
    .dispatch("userStore/fetchSearchUserNew", {
      query: value,
      isEvent: false,
    })
    .then((result) => {
      if (result.length) {
        result.forEach((item) => {
          item.isDelete = true;
        });
        formTempInputADG.value[idx].listNamaAdg = result;
      }
    });
}
async function handleSaveAll() {
  const isValid = await v$.value.$validate();
  if (isValid) {
    formTempData.value.effectiveDate = formatToISO(
      formTempData.value.effectiveDate
    );
    loadingData.value = true;
    let payload = {
      username: store.state.username,
      bannerEventDetail:
        imgSrcEventBase64.value == "" ? null : imgSrcEventBase64.value,
      bannerEventDetailExtention:
        imgSrcEventBase64.value == ""
          ? props.formData.bannerEventDetailExtention
          : fileEvent?.value?.name,
      effectiveDate: formTempData.value.effectiveDate,
      detailADG: [] as DetailADGSave[],
      homepageEventBanner:
        imgSrcBannerBase64.value == "" ? null : imgSrcBannerBase64.value,
      homepageEventBannerExtention:
        imgSrcBannerBase64.value == ""
          ? props.formData.homepageEventBannerExtention
          : fileBanner?.value?.name,
      status: formTempData.value.status,
      idFormasi: props.idFormasi,
    };
    formTempInputADG.value.map((item) => {
      payload.detailADG.push({
        adgBidang: item.adgBidang,
        email: item.email,
        jabatan: item.jabatan,
        namaAdg:
          typeof item.namaAdg === "string"
            ? item.namaAdg
            : (item.namaAdg as any).value,
        pangkat: item.pangkat,
        username:
          typeof item.namaAdg === "string"
            ? String(item.username)
            : String((item.namaAdg as any).username),
      });
    });
    store
      .dispatch("adminStore/updateFormasiADG", payload)
      .then(() => {
        instance.value.toast.show({
          message: "Success Update Data",
          timeout: 1000,
          color: "success",
        });
        loadingData.value = false;
        dialog.value = false;
        emit("refreshData", props.idFormasi);
      })
      .catch((error) => {
        loadingData.value = false;
        if (error.responseMessage === "Success") {
          instance.value.toast.show({
            message: "Success Update Data",
            timeout: 1000,
            color: "success",
          });
          emit("refreshData", props.idFormasi);
          dialog.value = false;
        } else {
          instance.value.toast.show({
            message:
              error.response.data.responseMessage ?? "internal server error",
            color: "warning",
            timeout: 3000,
          });
          emit("refreshData", props.idFormasi);
          dialog.value = false;
        }
      });
    console.log("Form is valid, proceeding with save.");
  } else {
    console.log("Form is invalid.");
  }
}
function formatToISO(dateStr: string): string {
  if (!dateStr) return "";

  const [day, month, year] = dateStr.split("/");

  return `${year}-${month}-${day}T00:00:00`;
}
async function handleAddInputADG() {
  const isValid = await v$.value.$validate();
  if (!isValid) {
    return;
  }
  formTempInputADG.value.push({
    namaAdg: "",
    searchNamaAdg: "",
    jabatan: "",
    pangkat: "",
    email: "",
    adgBidang: "",
    listNamaAdg: [],
    isloadingSearchNamaAdg: false,
    username: "",
  });
}
function handleDeleteInputADG(idx) {
  formTempInputADG.value.splice(idx, 1);
}

function handleFileImport(type) {
  isSelecting.value = true;
  window.addEventListener(
    "focus",
    () => {
      isSelecting.value = false;
    },
    { once: true }
  );
  if (type === "event") {
    const eventButton = document.getElementById("uploaderButtonEvent");
    eventButton?.click();
  } else {
    const bannerButton = document.getElementById("uploaderButtonBanner");
    bannerButton?.click();
  }
}
function onFileChanged(e, type) {
  const file = e.target.files[0];
  const fileType = file.type;
  const fileSize = file.size; // Ukuran dalam bytes
  const maxSize = 5 * 1024 * 1024; // 5MB
  if (fileType != "image/png") {
    alert("PNG File Only!");
    return;
  }
  if (fileSize > maxSize) {
    alert("File size exceeds the maximum limit of 5MB!");
    return;
  }
  if (type === "event") {
    fileEvent.value = file;
    selectedFileEvent.value = URL.createObjectURL(e.target.files[0]);
  } else {
    fileBanner.value = file;
    selectedFileBanner.value = URL.createObjectURL(e.target.files[0]);
  }
  const reader = new FileReader();
  reader.readAsDataURL(file);

  reader.onload = () => {
    const base64Result = reader.result;
    if (base64Result && typeof base64Result === "string") {
      const cleanBase64 = base64Result.split(",")[1];
      if (type === "event") {
        imgSrcEventBase64.value = cleanBase64;
      } else {
        imgSrcBannerBase64.value = cleanBase64;
      }
    }
  };

  reader.onerror = (error) => {
    console.error("Error converting to Base64:", error);
  };
}
function dragover(e) {
  e.preventDefault();
  isDragging.value = true;
}
function dragleave() {
  isDragging.value = false;
}
function drop(e, type) {
  e.preventDefault();
  const fileType = e.dataTransfer.files[0].type;
  const fileSize = e.dataTransfer.files[0].size; // Ukuran dalam bytes
  const maxSize = 5 * 1024 * 1024; // 5MB

  if (fileType != "image/png") {
    alert("PNG File Only!");
    return;
  }
  if (fileSize > maxSize) {
    alert("File size exceeds the maximum limit of 5MB!");
    return;
  }
  if (type === "event") {
    selectedFileEvent.value = URL.createObjectURL(e.dataTransfer.files[0]);
  } else {
    selectedFileBanner.value = URL.createObjectURL(e.dataTransfer.files[0]);
  }
  isDragging.value = false;
}
function handleShowDialog() {
  dialog.value = true;
  const date = new Date(props.formData.effectiveDate);
  const formattedDate = date.toLocaleDateString("en-GB");
  formTempData.value = {
    effectiveDate: formattedDate,
    status: props.formData.status,
    bannerEventDetail: props.formData.bannerEventDetail || null,
    homepageEventBanner: props.formData.homepageEventBanner || null,
  };
  props.formData.detailADG.map((item) => {
    formTempInputADG.value.push({
      namaAdg: item.namaAdg,
      jabatan: item.jabatan,
      pangkat: item.pangkat,
      searchNamaAdg: "",
      email: item.email,
      adgBidang: item.adgBidang,
      listNamaAdg: [],
      isloadingSearchNamaAdg: false,
      username: item.username,
    });
  });
  selectedFileEvent.value = props.formData.bannerEventDetail || null;
  selectedFileBanner.value = props.formData.homepageEventBanner || null;
}
function close() {
  emit("refreshData", props.idFormasi);
  dialog.value = false;
}
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

.form-title {
  margin-top: -21px;
  margin-left: 20px;
  background-color: white;
  width: fit-content;
}

img {
  width: 200px;
  height: 100px;
}
</style>
