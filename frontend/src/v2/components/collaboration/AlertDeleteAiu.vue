<template>
  <div class="alert-info d-flex justify-space-between align-center mb-4">
    <v-alert
      title="Delete Document"
      type="error"
      variant="tonal"
      style="height: 64px; border-radius: 5px; width: 100%"
      icon="mdi-information-outline"
      persistent
      ><div
        class="text-left"
        style="color: black; font-weight: 600; font-size: 13px"
      >
        {{ reasons }}
      </div></v-alert
    >
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
const props = defineProps({
  reasons: {
    type: String,
    required: true,
  },
});
</script>

<style scoped>
:deep(.v-alert-title) {
  align-items: center;
  align-self: center;
  display: flex;
  font-family: Poppins;
  font-size: 13px;
  font-weight: 500;
  line-height: 19.5px;
  text-align: left;
  letter-spacing: 0.0125em;
  line-height: 1.75rem;
  overflow-wrap: normal;
  text-transform: none;
  word-break: normal;
  word-wrap: break-word;
  color: #a6abc7;
  margin-bottom: -3px;
}
.alert-info {
  border: 1px solid #b13737 !important;
  border-radius: 5px;
  color: white;
}
</style>
