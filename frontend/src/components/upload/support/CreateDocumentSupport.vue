<template>
  <document-pnin-form
    v-if="idTaskTemplate == 0"
    :methodAddDocument="methodAddDocument"
    :idTaskTemplate="idTaskTemplate"
    @updateStep="updateStep"
    @updateMetadata="updateMetadata"
  />

  <document-standarisasi-form
    v-else
    :methodAddDocument="methodAddDocument"
    :idTaskTemplate="idTaskTemplate"
    @updateStep="updateStep"
    @updateMetadata="updateMetadata"
  />
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from "vue";
import DocumentPninForm from "@/components/upload/form/DocumentPninForm.vue";
import DocumentStandarisasiForm from "@/components/upload/form/DocumentStandarisasiForm.vue";

defineProps({
  methodAddDocument: { type: Number, required: true, default: 1 },
  idTaskTemplate: { type: Number, required: true, default: -1 },
});

const emits = defineEmits(["updateStep", "updateMetadata"]);
const updateStep = () => emits("updateStep", 1);
const updateMetadata = (state) => emits("updateMetadata", state);
</script>
