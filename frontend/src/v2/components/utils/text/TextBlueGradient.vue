<template>
  <div class="py-3 pl-4 ml-1 text-left my-4 text-15 blue-gradient">
    <b style="color: #fff">{{ text }}</b>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";

defineProps({
  text: {
    type: String,
    default: "",
  },
});
</script>

<style scoped>
.blue-gradient {
  background: linear-gradient(
    89.96deg,
    #065695 35.16%,
    rgba(255, 255, 255, 0) 101.03%
  );
  border-radius: 0px !important;
}
</style>
