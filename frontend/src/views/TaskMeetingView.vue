<template>
  <api-loader
    ref="listMeeting"
    :apiMethod="getMeeting"
    :hasOverlay="false"
    :key="loaderListMeeting"
  >
    <template v-slot:default="props">
      <div v-if="props.response.plainData.length > 0">
        <div v-for="(item, index) in props.response.plainData" :key="index">
          <v-row style="cursor: pointer" @click="openDetailMeeting(item)">
            <v-col>
              <div class="d-flex">
                <img
                  src="/images/meeting/Detail-Calendar.png"
                  style="width: 50px; margin-top: -12px"
                />
                {{ item.meetingName }}
              </div>
            </v-col>
            <v-col>
              <v-icon color="#267DC2">mdi-map-marker-outline</v-icon>
              {{ item.platform }}
            </v-col>
            <v-col
              ><div class="font-weight-bold">
                <v-icon color="#267DC2" size="20"> mdi-clock-outline</v-icon>
                {{ reformatDate(item.startDate) }}
              </div>
              <div class="ml-1">{{ reformatTime(item.startDate) }}</div>
            </v-col>
          </v-row>
        </div>
      </div>
      <div v-else>
        <div class="row">
          <div class="col-lg-12">
            <div class="d-flex align-items-center justify-content-center">
              <v-img
                src="/images/meeting/no-meeting.svg"
                :height="350"
                :width="350"
              ></v-img>
            </div>
            <div class="text-center text-blackTheme fw-600 text-18 text-italic">
              No Meeting Available....
            </div>
          </div>
        </div>
      </div>
    </template>
    <template v-slot:loading>
      <paragraph-shimmer :is-loading="true" :lines="5" :random-size="true" />
    </template>
  </api-loader>
  <div style="position: fixed; bottom: 4vh; right: 4vh">
    <free-style-shimmer
      v-if="isLoading"
      width="7.5rem"
      height="2rem"
      border-radius="10px"
      color="#DCDCDC"
    />
    <v-btn
      v-else-if="task.isAddMeeting"
      rounded="lg"
      class="btn-primary"
      @click="addMeeting()"
    >
      Add Meeting
      <v-tooltip activator="parent" location="bottom"
        >Menjadwalkan rapat baru</v-tooltip
      ></v-btn
    >
  </div>

  <DetailMeeting
    ref="detailDialog"
    @showDialogListMeeting="trigerListMeeting"
  />
  <CreateMeetingDialog
    ref="createMeeting"
    @showCreateMeetingDialog="trigerListMeeting"
  />
</template>
<script>
import { defineComponent } from "vue";
import client from "@/library/ApiClient";
import ApiLoader from "@/components/ApiLoader.vue";
import { reformatDate, reformatTime } from "@/library/DateHelper";
import DetailMeeting from "@/components/meeting/DetailMeetingDialog.vue";
import CreateMeetingDialog from "@/components/meeting/CreateMeetingDialog.vue";

export default defineComponent({
  name: "TaskMeetingView",
  components: {
    ApiLoader,
    DetailMeeting,
    CreateMeetingDialog,
  },
  props: {},
  data() {
    return {
      loaderListMeeting: 1,
      task: Object,
      isLoading: false,
    };
  },
  mounted() {
    this.getTask();
  },
  methods: {
    getTask() {
      this.isLoading = true;
      return client
        .getTasksByIdTask({
          store: this.$store,
          data: {
            id: this.$route.params.taskId,
          },
        })
        .then((response) => {
          this.task = response.plainData[0];
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getMeeting() {
      return client.getTaskMeetingByIdTasks({
        store: this.$store,
        data: {
          id: this.$route.params.taskId,
        },
      });
    },
    reformatDate(value) {
      return reformatDate(value);
    },
    reformatTime(value) {
      return reformatTime(value);
    },
    openDetailMeeting(item) {
      this.$refs.detailDialog.start(item);
    },
    addMeeting() {
      document.getElementById("DetailTaskDialog").style.visibility = "hidden";
      this.$refs.createMeeting.start();
    },
    trigerListMeeting() {
      this.loaderListMeeting++;
      document.getElementById("DetailTaskDialog").style.visibility = "visible";
    },
  },
});
</script>
<style scoped>
.btn-primary {
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%);
  color: white;
}
</style>
