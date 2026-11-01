<template>
  <v-btn class="pa-1" min-width="0" variant="text" @click="showDelete">
    <v-icon
      class="table-content-center"
      color="#267DC2"
      small
      style="
        border: 1px solid;
        border-radius: 4px;
        padding: 13px;
        cursor: pointer;
      "
      >mdi-delete</v-icon
    >
    <v-tooltip activator="parent" location="top">Delete</v-tooltip>
  </v-btn>
  <ModalConfirm
    ref="modal"
    :form-config="formDelete"
    :isLoading="isLoading"
    @action-confirm="actionConfirm"
  />
</template>
<script lang="ts" setup>
import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";

import { ref, getCurrentInstance } from "vue";
import { useStore } from "vuex";
import { responsePromise } from "@v2/helpers/utils";
import type { TModalConfirm } from "@v2/Type.d";

const { root } = getCurrentInstance() as any;
const response = responsePromise(root);
const store = useStore();

const prop = defineProps({
  id: {
    type: [String, Number],
    required: true,
  },
  item: {
    type: Object,
  },
});
const emit = defineEmits(["onSuccess"]);

const isLoading = ref<boolean>(false);
const modal = ref();
const formDelete = ref<TModalConfirm>({
  title: "Delete Material",
  message: "Are you sure delete this Material ?",
  btnSubmitLabel: "Approve",
  usingTimeOut: true,
});

function showDelete() {
  isLoading.value = false;
  modal.value.show({}, 10);
}

function actionConfirm() {
  isLoading.value = true;
  store
    .dispatch("meetingStore/deleteMaterial", {
      id: prop.id,
    })
    .then((res) => {
      response.success(res, function () {
        modal.value.hide();
        emit("onSuccess", true);
      });
    })
    .catch(response.error)
    .finally(() => {
      isLoading.value = false;
    });
}
</script>

<style scoped>
.btn-detail-view.v-btn--size-default {
  min-width: initial;
  padding: 5px;
}
</style>
