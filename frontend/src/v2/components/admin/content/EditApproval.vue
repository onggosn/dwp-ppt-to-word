<template>
  <v-btn
    class="rounded-lg px-2 font-weight-bold"
    min-width="0"
    color="#065695"
    variant="outlined"
    @click="openDialog"
  >
    <v-icon color="#065695" small style="cursor: pointer">mdi-pencil</v-icon>
  </v-btn>
  <Teleport to="body">
    <v-dialog v-model="dialog" :max-width="700" persistent>
      <v-card class="mb-5 border-radius-dwp">
        <v-card-title class="d-flex justify-center align-center">
          <div class="text-18 text-blueTheme fw-500 mt-2 mb-2">
            {{ labelDialog }}
          </div>
          <v-btn
            class="mr-2"
            style="position: absolute; right: 0"
            variant="text"
            icon="mdi-close"
            @click="closeDialog"
          ></v-btn>
        </v-card-title>
        <v-form @submit.prevent="handleSave()">
          <v-card-text>
            <hr class="line mb-6" />
            <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
              Name<span class="text-danger">*</span>
            </p>
            <SearchBar
              v-model="state.searchName"
              :items="listUser"
              :appendIcon="true"
              :isRequired="true"
              :rules="[validateItem]"
            />
          </v-card-text>
          <v-card-actions class="d-flex justify-end px-6 py-4">
            <v-btn
              elevation="3"
              class="rounded-lg text-light-blue-darken-4"
              @click="closeDialog"
            >
              Cancel
            </v-btn>
            <v-btn
              elevation="3"
              class="primary-gradient rounded-lg"
              type="submit"
              :loading="store.getters['documentStore/getLoading']"
            >
              Save
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>
  </Teleport>
</template>
<script lang="ts" setup>
import { ref, defineProps, getCurrentInstance } from "vue";
import { useStore } from "vuex";
import SearchBar from "@v2/components/utils/dialog/SearchBar.vue";

const emit = defineEmits(["onSuccess"]);
const dialog = ref<boolean>(false);
const store = useStore();
const { root } = getCurrentInstance() as any;
const state = ref({
  searchName: "",
});
const listUser = ref([]);
const prop = defineProps({
  labelDialog: {
    type: String,
    default: "",
  },
  item: {
    type: Object,
    default: () => ({}),
  },
  itemDialog: {
    type: Object,
    default: () => ({}),
  },
  idSector: {
    type: Number,
    default: 0,
  },
  docID: {
    type: String,
    default: "",
  },
});
const validateItem = (value) => {
  return !!value || "member selection is required";
};
const closeDialog = () => {
  dialog.value = false;
};
const openDialog = () => {
  getUserApproval();
  dialog.value = true;
};
const handleSave = () => {
  if (state.value.searchName) {
    const reqData = {
      id: prop.itemDialog.id,
      idBPDocument: prop.item.docID ?? prop.docID,
      idMUser: state.value.searchName,
    };

    store
      .dispatch("documentStore/updateUserApproval", reqData)
      .then(() => {
        root.refs.toast.show({
          message: "Successfully Saved",
          color: "success",
          timeout: 3000,
        });
        closeDialog();
      })
      .catch((e) => {
        root.refs.toast.show({
          message: e.response.data.responseMessage,
          color: "error",
          timeout: 3000,
        });
      })
      .finally(() => {
        emit("onSuccess", prop.item.docID);
      });
  }
};
const getUserApproval = () => {
  state.value.searchName = prop.itemDialog.idUser;
  let reqData = {
    id: prop.item.docID ?? prop.docID,
    idSector: prop.idSector,
  };

  store.dispatch("eFormStore/GetListBpDocApproval", reqData).then((res) => {
    if (res) {
      const { responseData } = res;

      const data = responseData.map((el: any) => {
        const { value: name, id, jabatanSatker: department } = el;

        return {
          name,
          type: "person",
          id,
          inputName: el.value,
          value: el.value,
          department,
        };
      });

      listUser.value = data;
    }
  });
};
</script>
<style scoped>
.line {
  margin-top: -10px !important;
  border: none; /* Remove the default border */
  height: 2px; /* Set the height of the hr */
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
}
</style>
