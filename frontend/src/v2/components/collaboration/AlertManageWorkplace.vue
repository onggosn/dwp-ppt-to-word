<template>
  <div class="alert-info d-flex justify-space-between align-center mb-4">
    <v-alert
      :title="data?.isReason.title"
      type="error"
      variant="tonal"
      class="py-3"
      style="height: 75px; border-radius: 5px; width: 100%"
      icon="mdi-information-outline"
      persistent
      ><div
        class="text-left my-1"
        style="color: black; font-weight: 600; font-size: 13px"
      >
        “{{ data?.isReason.value }}”
      </div>
      <div v-if="rejectedBy" class="d-flex" style="width: 100%">
        <p class="v-alert-title">
          {{ "Rejected by : " + rejectedBy }}
        </p>
        <p class="v-alert-title" style="margin-left: auto">
          {{ data?.isReason?.date }}
        </p>
      </div>
    </v-alert>
  </div>
</template>

<script setup lang="ts">
/* eslint-disable */
import { computed } from "vue";
const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});
const rejectedBy = computed(() => {
  return props.data?.isReason?.rejectedBy ?? false;
});

const alertTitle = computed(() => {
  if (props.data.isCancel) {
    return "Cancel Document";
  } else if (props.data.isDelete) {
    return "Delete Document";
  } else {
    return "";
  }
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
