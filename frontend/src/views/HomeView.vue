<template>
  <v-container>
    <v-row no-gutters>
      <v-col sm="12" md="9">
        <HomeBanner />
        <HomeAssignedTask />
        <HomeDocument />
        <HomeWorkspaceOverview />
      </v-col>
      <v-col md="3" class="d-none d-md-flex">
        <HomeCalendar />
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import HomeBanner from "@/components/home/HomeBanner.vue";
import HomeCalendar from "@/components/home/HomeCalendar.vue";
import HomeAssignedTask from "@/components/home/HomeAssignedTask.vue";
import HomeDocument from "@/components/home/HomeDocument.vue";
import HomeWorkspaceOverview from "@/components/home/HomeWorkspaceOverview.vue";
export default {
  name: "HomeView",
  components: {
    HomeBanner,
    HomeCalendar,
    HomeAssignedTask,
    HomeDocument,
    HomeWorkspaceOverview,
  },
  props: {},
  data: function () {
    return {};
  },
  mounted() {
    //test from development @intr
    undefined;
  },
  methods: {},
};
</script>

<style scoped></style>
