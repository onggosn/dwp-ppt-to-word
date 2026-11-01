<template>
  <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
    {{ text }}<span v-if="important" style="color: red">*</span>
  </p>
</template>

<script setup lang="ts">
defineProps<{
  text?: string;
  important?: boolean;
}>();
</script>
