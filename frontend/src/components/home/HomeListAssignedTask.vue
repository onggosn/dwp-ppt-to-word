<template>
  <div
    class="border-box-activity mb-2 border-radius-lg shadow-10 mt-5"
    style="max-width: 820px; height: 64px; padding-top: 2px; background: white"
  >
    <v-row class="pa-4">
      <v-col
        cols="6"
        class="cut-text"
        @click="toWorkspace"
        :style="{
          cursor: $vuetify.display.mobile == true ? 'pointer' : 'default',
          pointerEvents: $vuetify.display.mobile == true ? 'auto' : 'none',
        }"
        ><h6
          class="fw-600 text-15 text-blackTheme"
          style="text-overflow: ellipsis; overflow: hidden; white-space: nowrap"
        >
          {{ item.taskName }}
        </h6></v-col
      >
      <v-col md="3" sm="6">
        <span
          v-if="item.statusName == 'Not Started'"
          class="text-13 fw-700"
          style="color: red; padding-top: 1px"
          ><b>{{ item.statusName }}</b></span
        >
        <span
          v-if="item.statusName == 'In Progress'"
          class="text-13 fw-700"
          style="color: #fe7411; padding-top: 1px"
          ><b>{{ item.statusName }}</b></span
        >
        <span
          v-if="item.statusName == 'Done'"
          class="text-13 fw-700"
          style="color: #02aa59; padding-top: 1px"
          ><b>{{ item.statusName }}</b></span
        ></v-col
      >
      <v-col md="3" sm="0" class="d-none d-md-flex">
        <v-row align="center" justify="center" no-gutters>
          <v-btn
            rounded="lg"
            size="small"
            class="button-red"
            @click="toWorkspace"
            >See Detail
          </v-btn>
        </v-row></v-col
      >
    </v-row>
  </div>
</template>
<script>
export default {
  props: {
    item: Object,
  },
  data() {
    return {};
  },
  methods: {
    toWorkspace() {
      this.$router.push({
        name: "task-description",
        params: { taskId: this.item.id, workspaceId: this.item.idWorkspace },
      });
    },
  },
};
</script>
<style scoped>
.button-red {
  color: #fff;
  background: linear-gradient(180deg, #d6212a 0%, #ff000d 100%);
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.25);
  border-radius: 10px;
  padding: 5px 15px;
}

.shadow-10 {
  box-shadow: 0 4px 7px rgba(0, 0, 0, 0.1) !important;
  margin-bottom: -4px !important;
}
</style>
