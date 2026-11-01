<template>
  <v-dialog
    v-model="dialog"
    activator="parent"
    width="80vw"
    height="85vh"
    persistent
    id="DetailTaskDialog"
  >
    <v-card style="border-radius: 15px">
      <v-card-title
        class="text-center mt-4 mb-2 font-weight-medium"
        style="color: #4b4b4b"
      >
        Detail Task
        <v-btn
          class="mr-5 mt-3"
          style="position: absolute; right: 0; top: 0"
          text
          fab
          small
          elevation="0"
          @click="close()"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-btn
        elevation="0"
        class="d-block separatorHorizontal"
        style="cursor: none"
      />
      <v-card-text>
        <v-tabs v-model="tab" bg-color="white" align-tabs="center">
          <v-tab
            class="text-grey font-weight-medium"
            slider-color="transparent"
            value="1"
            :to="{
              name: 'task-description',
              params: {
                workspaceId: $route.params.workspaceId,
                taskId: $route.params.taskId,
              },
            }"
            >Description</v-tab
          >
          <!-- <v-sheet class="separatorVertical"></v-sheet> -->
          <v-btn elevation="0" class="d-block separatorVertical" />
          <v-tab
            class="text-grey font-weight-medium"
            slider-color="transparent"
            value="2"
            :to="{
              name: 'task-document',
              params: {
                workspaceId: $route.params.workspaceId,
                taskId: $route.params.taskId,
              },
            }"
            >Document</v-tab
          >
          <v-btn elevation="0" class="d-block separatorVertical" />

          <v-tab
            class="text-grey font-weight-medium"
            slider-color="transparent"
            value="3"
            :to="{
              name: 'task-meeting',
              params: {
                workspaceId: $route.params.workspaceId,
                taskId: $route.params.taskId,
              },
            }"
            >Meeting</v-tab
          >
          <v-btn elevation="0" class="d-block separatorVertical" />
          <v-tab
            class="text-grey font-weight-medium"
            slider-color="transparent"
            value="4"
            :to="{
              name: 'task-discussion',
              params: {
                workspaceId: $route.params.workspaceId,
                taskId: $route.params.taskId,
              },
            }"
            >Discussion</v-tab
          >
        </v-tabs>
      </v-card-text>
      <v-btn
        elevation="0"
        class="d-block separatorHorizontal mt-1"
        style="cursor: none"
      />
      <v-card-actions>
        <v-card-text style="min-height: 70vh">
          <v-window v-model="tab">
            <v-window-item value="1">
              <task-description-view />
            </v-window-item>
            <v-window-item value="2">
              <!-- <task-document-view /> -->
              <router-view />
            </v-window-item>

            <v-window-item value="3">
              <task-meeting-view />
            </v-window-item>
            <v-window-item value="4">
              <task-discussion-view />
            </v-window-item>
          </v-window>
        </v-card-text>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script lang="js">
/* eslint-disable */
import { defineComponent } from "vue";
import TaskDescriptionView from "@/views/TaskDescriptionView.vue"
import ListDocumentView from "@/views/ListDocumentView.vue"
import ListDocumentSupportView from "@/views/ListDocumentSupportView.vue"
import TaskMeetingView from "@/views/TaskMeetingView.vue"
import TaskDiscussionView from "@/views/TaskDiscussionView.vue"
import TaskDocumentView from "@/views/TaskDocumentView.vue"

export default defineComponent({
  name: "DetailTask",
  components:{
    TaskDescriptionView,
    ListDocumentView,
    ListDocumentSupportView,
    TaskMeetingView,
    TaskDiscussionView,
    TaskDocumentView
  },
  props:{
    taskId: String
  },
  data() {
    return {
        dialog: false,
        tab: null
    };
  },
  methods:{
    close(){
        this.$router.replace({
          name: "workspace-detail",
          params: { workspaceId: this.$route.params.workspaceId },
        });
        this.dialog = false
    },
  },
  mounted(){
    this.dialog = true
  }
});
</script>

<style scoped>
:deep(.v-tab--selected) {
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%);
  color: white !important;
  font-weight: 900 !important;
  border-radius: 10px !important;
  height: 5vh;
  place-self: center;
}
:deep(.v-tab) {
  letter-spacing: 0.1px;
}

.separatorVertical {
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
  margin-left: -10px;
  margin-right: -10px;
  align-self: center;
  flex-direction: row;
  cursor: none;
  height: 1px;
  transform: rotate(90deg);
}
.separatorHorizontal {
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
  height: 1.2px;
  width: 100%;
}
::-webkit-scrollbar {
  width: 10px;
}
</style>
