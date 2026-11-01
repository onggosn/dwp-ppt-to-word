<template>
  <div class="container">
    <h2 class="bs-title">{{ title }}</h2>
    <div class="d-flex flex-column pa-3" style="row-gap: 16px">
      <slot></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";

defineProps({
  title: {
    type: String,
    default: "",
  },
  typeFilter: {
    type: Object,
    default: () => ({}),
  },
});
</script>

<style scoped>
.container {
  padding: 16px;
  border-radius: 10px;
  border: 1px solid #c2c2c2;
}
.bs-title {
  font-family: Poppins;
  font-size: 14px;
  font-weight: 600;
  line-height: 18px;
  text-align: left;
  color: #000;
  opacity: 50%;
  margin-bottom: 12px;
}
</style>
