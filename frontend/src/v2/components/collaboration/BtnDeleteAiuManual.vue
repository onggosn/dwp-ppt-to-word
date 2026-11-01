<template>
  <v-btn
    size="small"
    variant="outlined"
    style="border-radius: 10px; border: 1px solid #d6212a"
    class="mr-2"
    color="#D6212A"
    @click="showDelete"
  >
    Delete
    <template v-slot:prepend>
      <v-icon class="table-content-center" color="#D6212A" small>
        mdi-delete
      </v-icon>
    </template>
  </v-btn>
  <v-dialog v-model="dialog" max-width="800" persistent>
    <v-card class="py-3 px-6 rounded-12">
      <div class="d-flex justify-space-between align-center border-bottom">
        <div></div>
        <div class="text-darkBlue font-weight-bold">Assign</div>
        <div>
          <v-btn icon="mdi-close" variant="plain" @click="onclose()"></v-btn>
        </div>
      </div>
      <div class="pt-3">
        <v-form>
          <SearchBar
            v-model="selectedItem"
            :items="itemsMemberApproval"
            :appendIcon="true"
            :rules="[validateItem]"
            :isRequired="true"
          />
          <div class="d-flex justify-end">
            <v-btn
              class="mr-4 rounded-lg font-weight-bold primary-red-gradient"
              @click="onNextStepDelete"
              >Next</v-btn
            >
          </div>
        </v-form>
      </div>
    </v-card>
  </v-dialog>

  <ModalConfirm
    ref="modal"
    :form-config="formDelete"
    @action-confirm="actionConfirm"
  />
  <ModalConfirm
    ref="modalSubmit"
    :form-config="confirmDelete"
    @action-confirm="actionConfirm"
  >
    <template v-slot:icon-img>
      <img
        src="/images/cancelNotif.png"
        style="
          width: 80px;
          margin-top: -60px;
          filter: drop-shadow(#9b9b9b 2px 2px 3px);
        "
      />
    </template>
    <template v-slot:text-area>
      <v-textarea
        variant="solo"
        placeholder="Write your description here"
        class="pl-2 pr-2 textareadescription"
      ></v-textarea>
    </template>
  </ModalConfirm>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";
import SearchBar from "@v2/components/utils/dialog/SearchBar.vue";
import { useStore } from "vuex";
import type { TModalConfirm } from "@v2/Type.d";
import { useRoute } from "vue-router";

onMounted(() => {
  getUserApproval();
});

const isLoading = ref<boolean>(false);
const modal = ref();
const dialog = ref(false);
const store = useStore();
const route = useRoute();
const itemsMemberApproval = ref<any>();
const idselectedMember = ref<any>();
const modalSubmit = ref();
const formDelete = ref<TModalConfirm>({
  title: "Delete AIU",
  message: "Are you sure delete this Document ?",
  btnSubmitLabel: "Yes",
  btnSubmitColor: "danger-gradient",
});
const confirmDelete = ref<TModalConfirm>({
  title: "Delete AIU",
  message: "",
  btnSubmitLabel: "Submit",
  btnSubmitColor: "danger-gradient",
});
const selectedItem = ref(null);
const onclose = () => {
  dialog.value = false;
};

function showDelete() {
  modal.value.show({});
}
function actionConfirm() {
  modal.value.hide();
  dialog.value = true;
}
function onNextStepDelete() {
  modalSubmit.value.show({});
  dialog.value = false;
}
function handleAdd(id: any) {
  idselectedMember.value = id;
}
const validateItem = (value) => {
  return !!value || "member selection is required";
};
function getUserApproval() {
  const reqData = {
    id: route.params.idDoc,
  };
  store.dispatch("eFormStore/GetListBpDocApproval", reqData).then((res) => {
    const data = res.responseData.map((el: any) => {
      return {
        name: el.value,
        type: "person",
        id: el.id,
        inputName: el.value,
        value: el.value,
        department: el.gradeName,
      };
    });

    itemsMemberApproval.value = data;
  });
}
</script>

<style scoped lang="scss">
:deep(.rounded-12) {
  border-radius: 12px !important;
}

.border-bottom {
  border: 1px solid;
  border-image-slice: 1;
  border-image-source: linear-gradient(to left, #fffffc, #a6abc7, #fffffc);
  border-left: 0;
  border-right: 0;
  border-top: 0;
}
.shadow {
  box-shadow: 0 3px 7px 0 #85858540;
}
</style>
