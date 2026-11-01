<template>
  <v-btn
    size="small"
    variant="outlined"
    style="border-radius: 10px"
    class="mr-2"
    color="#065695"
    id="preview-pdf-button"
    :disabled="!buttonState"
    @click="openDialog()"
  >
    Preview
    <template #prepend>
      <img :src="require('@/v2/assets/icon/preview-btn.svg')" />
    </template>
  </v-btn>
  <PreviewPDFDialog ref="modal" />
  <ModalConfirm
    ref="modalConfirm"
    :form-config="dialogConfig"
    @action-confirm="actionConfirm"
  />
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import PreviewPDFDialog from "@/v2/components/collaboration/PreviewPDFDialog.vue";
import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";
import type { TModalConfirm } from "@v2/Type.d";
import { useStore } from "vuex";

defineProps({
  idBPDocument: {
    type: String,
    required: false,
  },
});

const buttonState = computed(
  (): boolean => store.getters["documentStore/getOnloadingButtonState"]
);

const store = useStore();
const modal = ref();
const modalConfirm = ref();
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
