<template>
  <v-row>
    <v-col cols="12" class="pl-6">
      <h5 class="text-blackTheme fw-600 text-18 ls-1 pt-2 mobile-font-2">
        Workspace Overview
      </h5>
      <p class="text-blackTheme fw-400 text-13 ls-1">
        See your overall workspace overview
      </p>
      <!-- <pre>{{ $vuetify.display }} </pre> -->
    </v-col>
  </v-row>
  <v-row class="pb-15 mb-15">
    <v-col cols="12" lg="4" sm="12" @click="toWorkspace('inProgress')">
      <HomeWorkspaceOverviewCard
        class="cursorPointer"
        imageUrl="/images/new-asset/Icon-in-progress.png"
        :apiMethod="inProgressApi"
        label="In Progress"
      ></HomeWorkspaceOverviewCard>
    </v-col>
    <v-col cols="12" lg="4" sm="12" @click="toWorkspace('done')">
      <HomeWorkspaceOverviewCard
        class="cursorPointer"
        imageUrl="/images/new-asset/icon-done.png"
        :apiMethod="doneApi"
        label="Done"
      ></HomeWorkspaceOverviewCard>
    </v-col>
    <v-col cols="12" lg="4" sm="12 " @click="toWorkspace('notStarted')">
      <HomeWorkspaceOverviewCard
        class="cursorPointer"
        imageUrl="/images/new-asset/Icon-Not-Started.png"
        :apiMethod="notStartedApi"
        label="Not Started"
      ></HomeWorkspaceOverviewCard>
    </v-col>
  </v-row>
</template>
<script>
import client from "@/library/ApiClient";
import HomeWorkspaceOverviewCard from "@/components/home/HomeWorkspaceOverviewCard.vue";

export default {
  components: {
    HomeWorkspaceOverviewCard,
  },
  data() {
    return {};
  },
  mounted() {
    undefined;
  },
  methods: {
    toWorkspace(place) {
      this.$router.push({
        name: "workspace-management",
        params: { seeMore: place },
      });
    },
    inProgressApi() {
      return client.getWorspaceInProgressByTaskMember({
        store: this.$store,
        data: this.apiParams,
      });
    },
    doneApi() {
      return client.getWorspaceDoneByTaskMember({
        store: this.$store,
        data: this.apiParams,
      });
    },
    notStartedApi() {
      return client.getWorspaceNotStartedByTaskMember({
        store: this.$store,
        data: this.apiParams,
      });
    },
  },
};
</script>
<style scoped>
.cursorPointer {
  cursor: pointer;
}
.v-sheet.v-card:not(.v-sheet--outlined) {
  box-shadow: 0 4px 7px rgba(0, 0, 0, 0.1) !important;
}
</style>
