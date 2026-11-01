<template>
  <Teleport to="body">
    <v-dialog v-model="isShow" :max-width="props.maxWidth" persistent>
      <v-card class="py-3 px-6 rounded-12">
        <div class="d-flex justify-space-between align-center border-bottom">
          <div></div>
          <div class="text-darkBlue font-weight-bold">{{ props.title }}</div>
          <div>
            <v-btn icon="mdi-close" variant="plain" @click="hide()"></v-btn>
          </div>
        </div>
        <div class="pt-3">
          <slot v-if="isShow" />
        </div>
      </v-card>
    </v-dialog>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from "vue";

const props = defineProps({
  title: {
    type: String,
    default: "",
  },
  maxWidth: {
    type: String,
    default: "800",
  },
});

const emit = defineEmits(["onClose"]);
const isShow = ref<boolean>(false);

function show() {
  isShow.value = true;
}

function hide() {
  isShow.value = false;
  emit("onClose");
}

defineExpose({
  show,
  hide,
});
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
