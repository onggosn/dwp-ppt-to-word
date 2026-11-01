<template>
  <MeetingCalendar
    v-if="router.currentRoute.value.name === 'v2.meeting-management'"
  ></MeetingCalendar>
  <RouterView v-else></RouterView>
</template>
<script lang="ts" setup>
import { useRouter } from "vue-router";
import MeetingCalendar from "./MeetingManagementCalendar.vue";

const router = useRouter();
</script>
