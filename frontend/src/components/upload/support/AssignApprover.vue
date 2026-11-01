<template>
  <assign-approver-pnin-form
    v-if="idTaskTemplate == 0"
    :idTaskTemplate="idTaskTemplate"
    @updateStep="updateStep"
    @updateApprover="updateApprover"
  />

  <assign-approver-standarisasi-form
    v-else
    :idTaskTemplate="idTaskTemplate"
    @updateStep="updateStep"
    @updateApprover="updateApprover"
  />
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from "vue";
import AssignApproverPninForm from "@/components/upload/form/AssignApproverPninForm.vue";
import AssignApproverStandarisasiForm from "@/components/upload/form/AssignApproverStandarisasiForm.vue";

defineProps({
  idTaskTemplate: { type: Number, required: true, default: -1 },
});

const emits = defineEmits(["updateStep", "updateApprover"]);
const updateStep = () => emits("updateStep", "CREATE");
const updateApprover = (value) => emits("updateApprover", value);
</script>
