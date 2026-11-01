<template>{{ userDetail }}</template>

<script setup lang="ts">
import { useStore } from "vuex";
import { ref } from "vue";

const store = useStore();
const userDetail = ref();

store.dispatch("userStore/fetchUserDetail").then((data) => {
  userDetail.value = data;
});
</script>
