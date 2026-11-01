<template>
  <template v-if="items.activityViewList.length">
    <!-- <pre> {{ items.activityViewList }}</pre> -->
    <v-sheet class="d-md-flex bg-transparent">
      <v-sheet
        v-for="item in items.activityViewList"
        :key="item.id"
        class="mr-7 bg-transparent"
      >
        <template v-if="true">
          <v-card elevation="3" class="rounded-lg" style="min-width: 320px">
            <p
              class="text-center pa-3 bg-white font-weight-bold text-uppercase text-14"
              style="color: #4b4b4b !important"
            >
              {{ item.activityName }}
            </p>

            <v-menu v-if="items.isAvailableCreateActivity">
              <template v-slot:activator="{ props }">
                <v-btn
                  density="compact"
                  icon="mdi-dots-vertical"
                  variant="text"
                  style="position: absolute; right: 0; top: 0; margin: 10px"
                  v-bind="props"
                ></v-btn>
              </template>

              <v-list>
                <v-list-item>
                  <delete-activity-dialog
                    :isAvailableDelete="item.tasksWithMemberViews.length == 0"
                    :idActivity="item.id"
                    @onSuccess="refreshWorkspace"
                  />
                </v-list-item>
              </v-list>
            </v-menu>
            <v-card-text
              :class="
                item.status === 1
                  ? 'bg-activity-nonActive'
                  : 'bg-activity-active'
              "
              class="pb-5"
              :style="{
                display: 'grid',
                'grid-template-columns': `repeat(${
                  item.tasksWithMemberViews.length > 3 ? 3 : 1
                }, 1fr)`,
                gap: '12px',
              }"
            >
              <template v-if="item.tasksWithMemberViews.length">
                <v-card
                  class="mt-4 bg-white rounded-lg"
                  elevation="3"
                  v-for="task in item.tasksWithMemberViews"
                  :key="task.id"
                  :width="getTaskCardWidth($vuetify.display.smAndDown)"
                  :height="getTaskCardHeight($vuetify.display.smAndDown)"
                >
                  <v-card-item>
                    <div>
                      <v-row no-gutters>
                        <v-col>
                          <p
                            class="text-11 pa-1 mb-1 pl-2 text-white font-weight-bold"
                            style="border-radius: 6px 1px 1px 6px"
                            :class="[
                              task.status == 1 || task.status == 15
                                ? 'gradient-Red'
                                : task.status == 2 ||
                                  task.status == 14 ||
                                  task.status == 16
                                ? 'gradient-Orange'
                                : task.status == 3 || task.status == 17
                                ? 'gradient-Green'
                                : 'undefined',
                            ]"
                          >
                            {{ labelStatus[task.status].label }}
                          </p>
                        </v-col>
                        <v-col
                          cols="2"
                          style="align-self: center; text-align: end"
                        >
                          <v-menu
                            v-if="
                              task.status != 3 &&
                              task.status != 17 &&
                              task.status != 14
                            "
                          >
                            <template v-slot:activator="{ props }">
                              <v-btn
                                size="sm"
                                class="pb-0"
                                icon="mdi-dots-horizontal"
                                variant="text"
                                v-bind="props"
                              >
                              </v-btn>
                            </template>

                            <v-list>
                              <v-list-item
                                v-if="task.status == 1 || task.status == 15"
                              >
                                <v-btn
                                  size="sm"
                                  variant="text"
                                  prepend-icon="mdi-play"
                                  color="#065695"
                                  style="font-size: 13px; font-weight: 800"
                                  @click="startTask(task.id)"
                                >
                                  <template v-slot:prepend>
                                    <v-icon color="#065695" size="25"></v-icon>
                                  </template>

                                  Start Task
                                </v-btn>
                              </v-list-item>
                              <v-list-item
                                v-if="task.status == 2 || task.status == 16"
                              >
                                <close-task-dialog
                                  :idTask="task.id"
                                  @onSuccess="refreshWorkspace"
                                />
                              </v-list-item>
                              <v-list-item>
                                <v-btn
                                  size="sm"
                                  variant="text"
                                  prepend-icon="mdi-account-multiple-plus"
                                  color="#065695"
                                  style="font-size: 13px; font-weight: 800"
                                  @click="
                                    addParticipantDialog(task.id, task.isOwner)
                                  "
                                >
                                  <template v-slot:prepend>
                                    <v-icon
                                      color="#065695"
                                      size="25"
                                      class="pr-1"
                                    ></v-icon>
                                  </template>
                                  Participant List
                                </v-btn>
                              </v-list-item>
                            </v-list>
                          </v-menu>
                        </v-col>
                      </v-row>

                      <div
                        class="mb-1 textBlue mt-2 font-weight-bold"
                        style="
                          line-height: 3vh;
                          font-size: 15px;
                          overflow: hidden;
                          text-overflow: ellipsis;
                          display: -webkit-box;
                          -webkit-line-clamp: 2;
                          -webkit-box-orient: vertical;
                        "
                      >
                        {{ task.taskName }}
                      </div>
                      <div
                        class="text-caption textBlue"
                        style="
                          overflow: hidden;
                          text-overflow: ellipsis;
                          display: -webkit-box;
                          -webkit-line-clamp: 3;
                          -webkit-box-orient: vertical;
                        "
                      >
                        {{ task.descriptions }}
                      </div>
                    </div>
                  </v-card-item>
                  <v-card-actions
                    class="d-none d-sm-flex"
                    style="position: absolute; bottom: 0; right: 0"
                  >
                    <v-btn
                      v-if="
                        task.status != 1 &&
                        task.status != 14 &&
                        task.status != 15
                      "
                      variant="text"
                      class="text-red font-weight-bold"
                      style="letter-spacing: 0.1px; font-size: 11px"
                      :to="{
                        name: 'task-detail',
                        params: {
                          taskId: task.id,
                          workspaceId: item.idWorkspace,
                        },
                      }"
                    >
                      see detail
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </template>
              <template v-else>
                <v-sheet
                  height="4vh"
                  class="bg-transparent"
                  v-if="!items.isAvailableCreateActivity"
              /></template>
            </v-card-text>
            <v-card-actions
              v-if="items.isAvailableCreateActivity"
              :class="
                item.status === 1
                  ? 'bg-activity-nonActive'
                  : 'bg-activity-active'
              "
            >
              <v-btn
                color="white"
                variant="text"
                class="font-weight-bold mt-n4 ml-2"
                @click="addTask(item)"
              >
                + Add Task
              </v-btn>
            </v-card-actions>
          </v-card>
        </template>
      </v-sheet>
      <create-activity-dialog
        v-if="items.isAvailableCreateActivity"
        ref="create_activity"
        :workspaceTypeId="items.idWorkspaceType"
        @onSuccess="refreshWorkspace"
      />
      <add-participant-dialog ref="add_participant" />
    </v-sheet>
    <add-task-dialog
      ref="add_task"
      :satkerId="items.idSatker"
      @submit="refreshWorkspace"
    />
  </template>
  <template v-else>
    <template v-if="items.isAvailableCreateActivity">
      <create-activity-dialog
        ref="create_activity"
        :workspaceTypeId="items.idWorkspaceType"
        @onSuccess="refreshWorkspace"
      />
      <v-img
        src="/images/add_activity_bg.svg"
        style="
          display: block;
          margin: 0 auto;
          height: 50vh;
          margin-top: 10vh;
          margin-left: -20vw;
        "
      ></v-img>
    </template>
  </template>
</template>
<script lang="js">
import { defineComponent } from "vue";
import CreateActivityDialog from "@/components/workspace/CreateActivityDialog.vue";
import DeleteActivityDialog from "@/components/workspace/DeleteActivityDialog.vue";
import CloseTaskDialog from "@/components/workspace/CloseTaskDialog.vue";
import AddParticipantDialog from "@/components/AddParticipantDialog.vue";
import AddTaskDialog from "@/components/task/AddTaskDialog.vue"

export default defineComponent({
  name: "WorkspaceActivityCard",
  emits: ["startTask","reload"],
  components: {
    CreateActivityDialog,
    DeleteActivityDialog,
    AddParticipantDialog,
    CloseTaskDialog,
    AddTaskDialog
  },
  props:{
    items: {},
  },
  data: function () {
    return {
      labelStatus: {
        1: { label: "Not Started" },
        2: { label: "In Progress" },
        3: { label: "Done" },
        14: { label: "Need for Approval" },
        15: { label: "Not Started" },
        16: { label: "In Progress" },
        17: { label: "Done" },
      },
      isLoading: false
    };
  },
  methods:{
    refreshWorkspace() {
      this.$emit("reload");
    },
    addParticipantDialog(idTask, isOwner){
      this.$refs.add_participant.start(idTask,isOwner)
    },
    startTask(idTask) {
      this.$emit("startTask", idTask);
    },
    addTask(item){
      this.$refs.add_task.show(item)
    },
    getCardWidth(length, isMobile) {

      if(isMobile){
        return '100%'
      }else{
        // debugger;
        switch(true){
        case length < 5:
          return '20vw'
        case length < 9:
          return '40vw'
        case length < 13:
          return '60vw'
        case length < 17:
          return '80vw'
        case length < 21:
          return '100vw'
        case length < 25:
          return '120vw'
        case length < 29:
          return '140vw'
        case length < 33:
          return '160vw'
        case length < 37:
          return '180vw'
        case length < 41:
          return '200vw'
        case length < 45:
          return '220vw'
        case length < 49:
          return '240vw'
        case length < 53:
          return '260vw'
        default:
          return '280vw'
      }
      }
    },
    getTaskCardWidth(isMobile){
      if(isMobile){
        return '60vw'
      }else{
        return '18vw'
      }
    },
    getTaskCardHeight(isMobile){
      if(isMobile){
        return '15vh'
      }else{
        return '31vh'
      }
    },
  }
});
</script>

<style scoped>
.bg-activity-active {
  background-image: url("@/assets/img/bg-activity-active.png");
  padding-left: 15px;
  padding-top: 5px;
  padding-right: 15px;
  padding-bottom: 2px;
  background-attachment: scroll;
  background-size: cover;
  background-repeat: no-repeat !important;
}
.bg-activity-nonActive {
  background-image: url("@/assets/img/bg-activity-nonActive.png");
  /* background-image: url("../assets/img/bg-activity-nonActive.png"); */
  padding-left: 15px;
  padding-top: 5px;
  padding-right: 15px;
  background-repeat: round;
  padding-bottom: 2px;
  background-attachment: scroll;
  background-size: cover;
  background-repeat: no-repeat !important;
}

.textBlue {
  color: #3a416f;
}

.gradient-Red {
  background: linear-gradient(90deg, #d6212a 0%, #ea111c 33.33%, #ffffff 100%);
}

.gradient-Orange {
  background: linear-gradient(90deg, #c45b10 0%, #e46911 39.06%, #ffffff 100%);
}

.gradient-Green {
  background: linear-gradient(90deg, #00783e 0%, #02aa59 32.81%, #ffffff 100%);
}

.btn-grad {
  border: solid 2.5px transparent;
  background-image: linear-gradient(
      rgba(255, 255, 255, 0),
      rgba(255, 255, 255, 0)
    ),
    linear-gradient(90.76deg, #267dc2 15.32%, #ff000d 61.36%);
  border-radius: 15px;
  background-origin: border-box;
  background-clip: content-box, border-box;
  box-shadow: 2px 1000px 1px #fff inset;
}
.btn-text-grad {
  font-size: 14px;
  background: linear-gradient(90.76deg, #267dc2 15.32%, #ff000d 61.36%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
