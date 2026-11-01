<template>
  <v-btn
    size="small"
    variant="outlined"
    style="border-radius: 10px"
    class="mr-2"
    color="#065695"
    @click="dialog = true"
    :loading="isLoading"
  >
    Update
    <template v-slot:prepend>
      <img :src="require('@/v2/assets/icon/cached.svg')" />
    </template>
  </v-btn>
  <v-dialog v-model="dialog" width="720" persistent>
    <v-card class="border-radius-dwp h-100">
      <v-card-title class="text-center my-1">
        <h3 class="text-h6 font-weight-regular">Update Section</h3>
        <v-btn
          density="default"
          icon="mdi-close"
          variant="text"
          class="btn-close"
          @click="dialog = false"
        />
      </v-card-title>
      <hr class="line my-3 d-block mb-5 pb-1" />
      <div class="mx-3" style="padding: 20px">
        <p class="mt-2 font-weight-regular my-3">Select Section to Update</p>
        <v-row v-if="listForm.length">
          <v-col cols="1">
            <v-checkbox
              v-model="selectAll"
              :value="true"
              color="#065391"
              style="height: 50px"
              class="mt-n2"
              @click="onSelectAllClicked($event)"
            />
          </v-col>
          <v-col cols="5">
            <p class="mt-2 font-weight-regular">Select All</p>
          </v-col>
        </v-row>
        <div v-if="!listForm.length">
          <v-img
            src="/images/chartpack/emptybox.png"
            style="
              display: block;
              margin: 0 auto;
              width: 450px;
              margin-top: 80px;
            "
          />
          <div
            class="text-center text-18 fw-600 text-grayTheme-gradien font-italic mb-4"
          >
            No Data Available
          </div>
        </div>
        <v-form v-else>
          <v-row v-for="item in listForm" :key="item.idEformSource">
            <v-col cols="1">
              <v-checkbox
                v-model="listIdEform"
                color="#065391"
                :value="item.children[0].idEForm"
                class="mt-n2"
                @click="onItemClicked"
              />
            </v-col>
            <v-col cols="12" sm="11">
              <v-chip class="border-radius-dwp py-7 px-4" style="width: 100%">
                <span style="width: 100%">{{ item.sectionName }}</span>
              </v-chip>
            </v-col>
          </v-row>
        </v-form>
        <div v-if="listForm.length">
          <p class="font-weight-regular">
            Should the updated data be appended or replaced?<span
              class="text-red"
              >*</span
            >
          </p>
          <v-radio-group v-model="isAppend" class="w-50">
            <div class="d-flex">
              <v-radio label="Append" :value="true" color="#065391" />
              <v-radio label="Replaced" :value="false" color="#065391" />
            </div>
          </v-radio-group>
        </div>
      </div>
      <v-card-actions
        v-if="listForm.length"
        class="justify-end pb-5 pr-8 pt-5"
        style="
          padding-top: 0px;
          background: white;
          border-radius: 0px 0px 10px 10px;
          box-shadow: 10px 10px;
        "
      >
        <v-spacer />
        <v-btn
          variant="flat"
          elevation="3"
          width="6vw"
          class="rounded-lg font-weight-bold"
          style="
            background: linear-gradient(#fff -46.47%, #fff 157.9%);
            border-radius: 10px;
            padding-left: 15px;
            padding-right: 15px;
            font-weight: 800;
            color: #065695;
          "
          :loading="isLoading"
          @click="dialog = false"
        >
          Cancel
        </v-btn>
        <v-btn
          variant="flat"
          :color="!listIdEform.length ? '#dfdfdf' : '#065695'"
          width="6vw"
          elevation="3"
          class="ml-5 rounded-lg font-weight-bold"
          style="color: #fdfdfd"
          :disabled="!listIdEform.length"
          :loading="isLoading"
          @click="submit"
        >
          Update
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import {
  defineComponent,
  ref,
  watch,
  computed,
  defineEmits,
  getCurrentInstance,
} from "vue";
import SearchBar from "./SearchBar.vue";
import EditAccessDialog from "./EditAccessDialog.vue";
import { useStore } from "vuex";

defineComponent({
  SearchBar,
  EditAccessDialog,
});
const { root } = getCurrentInstance() as any;
const emits = defineEmits(["refresh"]);
const dialog = ref<boolean>(false);
const listIdEform = ref<string[]>([]);
const isAppend = ref<boolean>(false);
const selectAll = ref<boolean>(false);
const store = useStore();
const isLoading = ref(false);
const listForm = computed(
  () => store.getters["collaborationStore/getListForm"]
);

const onItemClicked = () => {
  setTimeout(() => {
    selectAll.value = listIdEform.value.length === listForm.value.length;
  }, 100);
};

const onSelectAllClicked = (ev: any) => {
  if (ev.target?.checked) {
    // Select all
    listIdEform.value = listForm.value.map(
      (item: any) => item.children[0].idEForm
    );
  } else {
    // Deselect all
    listIdEform.value = [];
  }
};
watch(dialog, () => {
  listIdEform.value = [];
  selectAll.value = false;
  isAppend.value = false;
});
async function submit() {
  isLoading.value = true;
  const reqData = {
    idEForm: listIdEform.value,
    isAppend: isAppend.value,
  };
  store
    .dispatch("eFormStore/updateAiuOtomatis", reqData)
    .then((res) => {
      if (res.responseMessage === "Success") {
        root.refs.toast.show({
          message: "Successfully Saved",
          color: "success",
          timeout: 3000,
        });
        dialog.value = false;
        emits("refresh", true);
      }
    })
    .finally(() => {
      isLoading.value = false;
    });
}
</script>

<style scoped>
.line {
  border: none;
  height: 3px;
  margin: 16px 0;
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
}

.btn-close {
  position: absolute;
  right: 0;
  top: 0;
  margin-top: 10px;
  margin-right: 10px;
}

.chip-shadow {
  box-shadow: 0px 3px 1px -2px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)),
    0px 2px 2px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)),
    0px 1px 5px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.12));
  height: 56px;
  width: 94%;
  color: grey;
  font-size: 16px;
}

:deep(.v-btn--disabled) {
  color: #000 !important;
}

:deep(.v-btn__overlay) {
  background-color: #dfdfdf !important;
}
</style>
