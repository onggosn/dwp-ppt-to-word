<template>
  <v-btn
    v-if="isNewData"
    style="border-radius: 10px"
    color="#065695"
    variant="outlined"
    @click="onOpen()"
  >
    <v-icon>mdi-plus</v-icon>
    Add Member
  </v-btn>
  <v-btn
    v-else
    class="rounded-lg px-2 py-2"
    min-width="0"
    color="#065695"
    variant="outlined"
    style="border-radius: 8px"
    @click="onOpen()"
  >
    <img :src="require('@/v2/assets/icon/edit.svg')" />
  </v-btn>
  <Teleport to="body">
    <v-dialog v-model="dialog" width="600" persistent>
      <v-card class="border-radius-dwp">
        <v-card-title class="text-center mt-3">
          <h3 class="text-h6 font-weight-regular">
            {{ isNewData ? "Add Member" : "Edit Member" }}
          </h3>
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
            <v-row class="tight-rows">
              <v-col :cols="12" class="">
                <p class="pb-3 text-left text-darkBlue font-weight-bold">
                  Name
                </p>
                <SearchBar
                  v-if="isNewData"
                  v-model="formNameSelected"
                  v-model:search="search_item"
                  :items="listUser"
                  :appendIcon="true"
                  :isRequired="true"
                />
                <v-text-field
                  v-else
                  variant="solo"
                  :value="props.item?.name || ''"
                  class="border-radius-dwp no-shadow"
                  bg-color="#DFDFDF"
                  readonly
                  style="border-radius: 8px"
                >
                  <template v-slot:append-inner>
                    <img :src="require('@/v2/assets/icon/search.svg')" />
                  </template>
                </v-text-field>
              </v-col>
              <v-col :cols="12" class="">
                <p class="pb-3 text-left text-darkBlue font-weight-bold">
                  Satker
                </p>
                <v-text-field
                  v-if="isNewData"
                  variant="solo"
                  :value="tempSatker"
                  readonly
                  class="border-radius-dwp no-shadow"
                  bg-color="#DFDFDF"
                  style="border-radius: 8px"
                ></v-text-field>
                <v-text-field
                  v-else
                  variant="solo"
                  :value="props.item?.organizationName || ''"
                  readonly
                  class="border-radius-dwp no-shadow"
                  bg-color="#DFDFDF"
                  style="border-radius: 8px"
                ></v-text-field>
              </v-col>
              <v-col :cols="12" class="">
                <p class="pb-3 text-left text-darkBlue font-weight-bold">
                  Job Title
                </p>
                <v-text-field
                  v-if="isNewData"
                  variant="solo"
                  :value="tempJobTitle"
                  readonly
                  class="border-radius-dwp"
                  bg-color="#DFDFDF"
                  style="border-radius: 8px"
                ></v-text-field>
                <v-text-field
                  v-else
                  variant="solo"
                  :value="props.item?.gradeName || ''"
                  readonly
                  class="border-radius-dwp"
                  bg-color="#DFDFDF"
                  style="border-radius: 8px"
                ></v-text-field>
              </v-col>
              <v-col :cols="12" class="">
                <p class="pb-3 text-left text-darkBlue font-weight-bold">
                  Access Type
                </p>
                <v-radio-group
                  inline
                  style="margin-left: -8px"
                  hide-details
                  v-model="selectedAccessType"
                >
                  <v-radio
                    label="Participant"
                    :value="'participant'"
                    color="#267DC2"
                    class="me-2"
                  ></v-radio>
                  <v-radio
                    label="Organizer"
                    :value="'organizer'"
                    color="#267DC2"
                    class="me-2"
                  ></v-radio>
                  <v-radio
                    label="Pemrakarsa"
                    :value="'pemrakarsa'"
                    color="#267DC2"
                  ></v-radio>
                  <v-radio label="ADG" :value="'adg'" color="#267DC2"></v-radio>
                </v-radio-group>
                <div v-if="errorMessage" style="color: red; font-size: 13px">
                  {{ errorMessage }}
                </div>
              </v-col>
            </v-row>
          </v-form>
          <div class="text-right pb-5 mt-10">
            <v-btn
              class="btn-prev mr-3"
              elevation="4"
              :loading="isLoading"
              width="100"
              height="45"
              @click="onClose"
            >
              Cancel
            </v-btn>
            <v-btn
              class="btn-next"
              :loading="isLoading"
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
import { ref, watch, getCurrentInstance } from "vue";
import clientv2 from "@v2/library/ApiClient";
import SearchBar from "@v2/components/utils/dialog/SearchBar.vue";

import { useStore } from "vuex";

const selectedAccessType = ref<string | null>("participant");
const errorMessage = ref<string | null>(null);
const instance = ref<any>(getCurrentInstance()?.root.refs);
const dialog = ref(false);
const formNameSelected = ref<number | null>(null);
const formNameSelectedDetail = ref<any>({});
const search_item = ref<string | null>(null);
const listUser = ref([]);
const tempSatker = ref("");
const tempJobTitle = ref("");
const isLoading = ref<boolean>(false);

const store = useStore();

const props = defineProps({
  item: { type: Object, default: null },
  isNewData: { type: Boolean, default: false },
  idbp: { type: String, default: "" },
});

watch(selectedAccessType, () => {
  errorMessage.value = null;
});

const emit = defineEmits(["load"]);

function onOpen() {
  if (props.item) selectedAccessType.value = props.item.accessType;
  if (props.isNewData) selectedAccessType.value = "participant";
  dialog.value = true;
}

function onClose() {
  errorMessage.value = null;
  dialog.value = false;
  formNameSelected.value = null;
  formNameSelectedDetail.value = {};
  search_item.value = null;
  listUser.value = [];
  tempSatker.value = "";
  tempJobTitle.value = "";
}

function onSave() {
  isLoading.value = true;
  if (props.isNewData) {
    let payload = {
      idMEventTemplate: props.idbp,
      eventMemberType: selectedAccessType.value,
      nameUserOrNameGroup: formNameSelectedDetail.value.value,
      idMUserOridMGroup: formNameSelectedDetail.value.id,
    };
    clientv2
      .createBPMember({ data: payload })
      .then((res) => {
        isLoading.value = false;
        instance.value.toast.show({
          message: res.responseMessage,
          color: "success",
          timeout: 3000,
          icon: "mdi-check",
        });
        onClose();
        emit("load", {});
      })
      .catch((err) => {
        isLoading.value = false;
        errorMessage.value = err.response?.data?.responseData || "";
      });
  } else {
    let payload = {
      idMeventMemberTemplate: props.item.id,
      eventMemberType: selectedAccessType.value,
      idMEventTemplate: props.idbp,
      idMuser: props.item.idMUserOrGroup,
    };
    clientv2
      .updateBPMember({ data: payload })
      .then((res) => {
        isLoading.value = false;
        instance.value.toast.show({
          message: res.responseMessage,
          color: "success",
          timeout: 3000,
          icon: "mdi-check",
        });
        onClose();
        emit("load", {});
      })
      .catch((err) => {
        isLoading.value = false;
        errorMessage.value = err.response?.data?.responseData || "";
      });
  }
}
watch(
  () => search_item.value,
  (val) => {
    if (val) {
      store.dispatch("adminStore/getSearchNameMember", val).then((res) => {
        if (res) {
          const data = res.map((el) => {
            const { value: name, id, jabatanSatker: department } = el;
            return {
              name,
              type: el.isGroup ? "group" : "person",
              id,
              inputName: el.value,
              value: el.value,
              department,
              detail: { el },
            };
          });
          listUser.value = data;
        }
      });
    }
  }
);

watch(
  () => formNameSelected.value,
  (val) => {
    if (val) {
      listUser.value.map((item: any) => {
        if (item.id == val) {
          formNameSelectedDetail.value = item;
          tempSatker.value = formNameSelectedDetail.value.detail?.el?.satker;
          tempJobTitle.value =
            formNameSelectedDetail.value.detail?.el?.jobTitle;
        }
      });
    }
  }
);
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
  height: 2px; /* Set the height of the hr */
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
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

.tight-rows .v-col {
  margin-bottom: -25px;
}
</style>
