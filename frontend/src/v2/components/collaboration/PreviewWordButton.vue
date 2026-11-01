<template>
  <v-btn
    size="small"
    style="border-radius: 10px"
    variant="outlined"
    class="mr-2"
    color="#d80113"
    id="preview-pdf-button"
    @click="openDialog()"
    prepend-icon="mdi-text-box-search"
  >
    Preview Word
  </v-btn>
  <PreviewWordDialog ref="modal" :currentInstance="currentInstance" />
  <ModalConfirm
    ref="modalConfirm"
    :form-config="dialogConfig"
    @action-confirm="actionConfirm"
  />
</template>

<script setup lang="ts">
import { getCurrentInstance, ref } from "vue";
import PreviewWordDialog from "@/v2/components/collaboration/PreviewWordDialog.vue";
import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";
import type { TModalConfirm } from "@v2/Type.d";
import { useStore } from "vuex";

defineProps({
  idBPDocument: {
    type: String,
    required: false,
  },
});

const store = useStore();
const modal = ref();
const modalConfirm = ref();
const currentInstance = getCurrentInstance();
const dialogConfig = ref<TModalConfirm>({
  title: "Track Changes",
  message:
    "Are you sure? You will accept all suggestion when previewing document.",
  btnSubmitLabel: "Preview",
  usingTimeOut: true,
  btnSubmitColor: "primary-gradient",
  icon: {
    code: "mdi-information-outline",
    color: "#065695",
    backgrounColor: "white",
    size: 70,
  },
});

function actionConfirm() {
  store.commit("collaborationStore/increstReloadTrackChanges");
  modal.value.show();
  modalConfirm.value.hide();
}

function openDialog() {
  modalConfirm.value.show({}, 0);
}
</script>

<style scoped></style>
