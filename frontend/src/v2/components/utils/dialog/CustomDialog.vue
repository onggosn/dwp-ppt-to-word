<template>
  <!-- <div class="text-center pa-4"> -->
  <!-- <v-btn @click="handleShowDialog">Open Dialog</v-btn> -->
  <v-btn
    @click="handleShowDialog"
    style="border-radius: 15px"
    :variant="variant"
    color="#065695"
    :class="buttonClass"
    :width="buttonWidth"
    :loading="loading ?? false"
    :prepend-icon="prependIcon"
  >
    {{ buttonLabel }}
  </v-btn>
  <v-dialog
    v-model="dialog"
    :max-width="maxWidth"
    :class="dialogClass"
    persistent
  >
    <v-card class="py-3 px-6 rounded-lg">
      <div
        class="d-flex justify-space-between align-center border-bottom header dialog-header mt-4"
      >
        <div class="w-100 font-weight-bold text-center dialog-title">
          {{ props.title }}
        </div>
        <v-btn
          class="close-button"
          icon="mdi-close"
          variant="plain"
          @click="handleShowDialog"
        ></v-btn>
      </div>
      <div class="pt-3">
        <slot />
      </div>
    </v-card>
  </v-dialog>
  <!-- </div> -->
</template>

<script setup>
import { ref, defineProps, defineEmits, watch } from "vue";

const props = defineProps({
  showDialogProps: {
    type: Boolean,
    default: false,
  },
  buttonLabel: {
    type: String,
    default: "",
  },
  buttonClass: {
    type: Object,
    default: () => ({}),
  },
  buttonWidth: {
    type: String,
    default: "",
  },
  loading: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: "",
  },
  prependIcon: {
    type: String,
    default: "",
  },
  variant: {
    type: String,
    default: "elevated",
  },
  dialogClass: {
    type: String,
    default: "",
  },
  maxWidth: {
    type: String,
    default: "800",
  },
});

const dialog = ref(false);

watch(
  () => props.showDialogProps,
  (val) => {
    dialog.value = val;
  }
);

const emits = defineEmits(["handleShowDialog"]);
const handleShowDialog = () => {
  emits("handleShowDialog");
};
</script>
<style scoped>
.close-button {
  position: absolute;
  right: 0;
  margin-right: 1.5rem;
}
</style>
