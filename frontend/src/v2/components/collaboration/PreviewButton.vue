<template>
  <v-btn
    size="small"
    variant="outlined"
    style="border-radius: 10px"
    class="mr-2"
    color="#065695"
    :disabled="!buttonState"
    @click="openDialog()"
  >
    Preview
    <template #prepend>
      <img :src="require('@/v2/assets/icon/preview-btn.svg')" />
    </template>
  </v-btn>
  <ModalConfirm
    ref="modalConfirm"
    :form-config="dialogConfig"
    @action-confirm="actionConfirm"
  />
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";
import type { TModalConfirm } from "@v2/Type.d";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

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
const router = useRouter();
const modalConfirm = ref();
const dialogConfig = ref<TModalConfirm>({
  title: "Track Changes",
  message:
    "Are you sure? All suggestions will be accepted <br>when previewing the document in the <b>active collaboration section.</b>",
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

async function actionConfirm() {
  store.commit("collaborationStore/increstReloadTrackChanges");
  modalConfirm.value.hide();
  await new Promise((resolve) => setTimeout(resolve, 500));
  router.push({
    name: "preview.doc",
    params: {
      typeRDG: router.currentRoute.value.params?.typeRDG ?? "rdgm",
      idEvent: router.currentRoute.value.params?.idEvent,
      idDoc: router.currentRoute.value.params?.idDoc,
    },
  });
}

function openDialog() {
  modalConfirm.value.show({}, 0);
}
</script>

<style scoped></style>
