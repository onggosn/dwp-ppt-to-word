<template>
  <v-sheet
    class="ml-10 mr-10 mt-7 pb-10 mb-15 bg-transparent"
    style="background: #f5f5f5"
  >
    <v-row no-gutters>
      <v-col>
        <banner-welcome />
        <workspace-list />
      </v-col>
      <v-col cols="3">
        <banner-event />
        <latest-content />
      </v-col>
    </v-row>
  </v-sheet>
</template>

<script setup lang="ts">
import BannerWelcome from "@/v2/components/home/BannerWelcome.vue";
import WorkspaceList from "@/v2/components/home/WorkspaceList.vue";
import BannerEvent from "@/v2/components/home/BannerEvent.vue";
import LatestContent from "@/v2/components/home/LatestContent.vue";
</script>
