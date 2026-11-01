<template>
  <Teleport to="body">
    <v-dialog
      v-model="isShow"
      persistent
      max-width="611px"
      class="dialog-visible"
    >
      <div class="modal-warning-container">
        <button class="modal-warning-btn-close" @click="close">
          <img :src="require('@v2/assets/icon/close.svg')" />
        </button>
        <img
          :src="require(`@v2/assets/${modalConfig.img.location}`)"
          :width="modalConfig.img.width"
          :height="modalConfig.img.height"
          style="margin: auto"
        />
        <h2 class="txt-title-modal-warning">{{ modalConfig.title }}</h2>
        <h3
          class="txt-description-modal-warning"
          :style="{
            'font-weight': modalConfig.textWeight,
            'font-style': modalConfig.textStyle,
          }"
        >
          {{ modalConfig.description }}
        </h3>
        <v-btn
          @click="close"
          variant="tonal"
          rounded="lg"
          class="btn-modal-warning"
          :style="{ background: modalConfig.btnBackgroundStyle }"
          >{{ modalConfig.textBtn }}</v-btn
        >
      </div>
    </v-dialog>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, PropType } from "vue";
import type { TModalWarning } from "@/v2/Type.d";

defineProps({
  modalConfig: {
    type: Object as PropType<TModalWarning>,
    default: () => ({}),
  },
});

const isShow = ref(false);

function show() {
  isShow.value = true;
}

function close() {
  isShow.value = false;
}

defineExpose({
  show,
  close,
});
</script>

<style scoped>
.modal-warning-container {
  background: #fff;
  border-radius: 10px;
  position: relative;
  padding: 55px 96px 50px 96px;
  display: flex;
  flex-direction: column;
}
.modal-warning-btn-close {
  position: absolute;
  top: 15px;
  right: 15px;
}
.txt-title-modal-warning {
  font-family: Poppins;
  font-size: 18px;
  font-style: italic;
  font-weight: 600;
  line-height: 27px;
  text-align: center;
  color: #4b4b4b;
}
.txt-description-modal-warning {
  font-family: Poppins;
  font-size: 15px;
  line-height: 22.5px;
  text-align: center;
  color: #4b4b4b;
  margin-top: 5px;
}
.btn-modal-warning {
  margin: 26px auto 0 auto;
  padding: 11px 0;
  color: white;
  font-family: Poppins;
  font-size: 15px;
  font-weight: 500;
  line-height: 22.5px;
  text-align: center;
}
:deep(.v-btn.v-btn--density-default) {
  height: fit-content;
}
:deep(.v-btn--size-default) {
  width: 151px;
}
</style>
