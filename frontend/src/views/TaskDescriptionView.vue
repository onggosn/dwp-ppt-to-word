<template>
  <div class="ml-4">
    <api-loader :apiMethod="getTask" @loadingEnded="handleLoadingEnded">
      <template v-slot:default="props">
        <!-- <pre> {{ props.response.plainData }} </pre> -->
        <div class="d-block pa-2 font-weight-bold textGreyTitle">Task Name</div>
        <div class="d-block pl-2 pr-2 pb-2 text-gradient-blue grand-title">
          {{ props.response.plainData[0].taskName }}
        </div>
        <div class="d-block pa-2 mt-2 font-weight-bold textGreyTitle">
          Description
        </div>
        <div class="d-block pl-2 pr-2 mt-n1 text-subtitle-1 font-weight-bold">
          {{ props.response.plainData[0].descriptions }}
        </div>
        <div class="d-block pa-2 font-weight-bold textGreyTitle">Status</div>
        <div
          class="d-block pl-2 font-weight-bold"
          :style="{
            color:
              labelStatus[props.response.plainData[0].status].label ==
              'In Progress'
                ? '#fe7411'
                : labelStatus[props.response.plainData[0].status].label ==
                  'Done'
                ? '#02aa59'
                : 'red',
          }"
        >
          {{ labelStatus[props.response.plainData[0].status].label }}
        </div>
        <div v-if="props.response.plainData[0].ps">
          <div class="d-block pa-2 mt-2 font-weight-bold textGreyTitle">PS</div>
          <div
            class="d-block pl-2 pr-2 mt-n1 text-subtitle-1 font-weight-medium"
          >
            {{ props.response.plainData[0].ps }}
          </div>
        </div>
        <div class="d-flex justify-space-between mb-6 flex-wrap">
          <v-sheet width="50%" v-if="props.response.plainData[0].taskTypeName">
            <div class="d-block pa-2 mt-2 font-weight-bold textGreyTitle">
              Task Type
            </div>
            <div
              class="d-block pl-2 pr-2 mt-n1 text-subtitle-1 font-weight-medium"
            >
              {{ props.response.plainData[0].taskTypeName }}
            </div>
          </v-sheet>
          <v-sheet width="50%">
            <div class="d-block pa-2 mt-2 font-weight-bold textGreyTitle">
              PIC
            </div>
            <div
              class="d-block pl-2 pr-2 mt-n1 text-subtitle-1 font-weight-medium"
            >
              <MemberShowMore
                :items="props.response.plainData[0].listPIC.split(',')"
              >
              </MemberShowMore>
            </div>
          </v-sheet>
          <v-sheet width="50%" v-if="props.response.plainData[0].satker">
            <div class="d-block pa-2 mt-2 font-weight-bold textGreyTitle">
              Satker
            </div>
            <div
              class="d-block pl-2 pr-2 mt-n1 text-subtitle-1 font-weight-medium"
            >
              {{ props.response.plainData[0].satker }}
            </div>
          </v-sheet>
          <v-sheet width="50%">
            <div class="d-block pa-2 mt-2 font-weight-bold textGreyTitle">
              Contributor
            </div>
            <div
              class="d-block pl-2 pr-2 mt-n1 text-subtitle-1 font-weight-medium"
            >
              <MemberShowMore
                :items="props.response.plainData[0].listContributor.split(',')"
              >
              </MemberShowMore>
            </div>
          </v-sheet>
          <v-sheet width="50%">
            <div class="d-block pa-2 mt-2 font-weight-bold textGreyTitle">
              Due Date
            </div>
            <div
              class="d-block pl-2 pr-2 mt-n1 text-subtitle-1 font-weight-medium"
            >
              {{ dueDate() }}
            </div>
          </v-sheet>
          <v-sheet width="50%">
            <div class="d-block pa-2 mt-2 font-weight-bold textGreyTitle">
              Participant
            </div>
            <div
              class="d-block pl-2 pr-2 mt-n1 text-subtitle-1 font-weight-medium"
              v-if="props.response.plainData[0].listParticipant"
            >
              <MemberShowMore
                :items="props.response.plainData[0].listParticipant.split(',')"
              >
              </MemberShowMore>
            </div>
            <div
              class="d-block pl-2 pr-2 mt-n1 text-subtitle-1 font-weight-medium"
              v-else
            >
              -
            </div>
          </v-sheet>
        </div>
      </template>
      <template v-slot:loading>
        <paragraph-shimmer :lines="8" :random-size="true" />
      </template>
    </api-loader>
  </div>
</template>
<script>
import { defineComponent } from "vue";
import ApiLoader from "@/components/ApiLoader.vue";
import client from "@/library/ApiClient";
import { reformatFormDate } from "@/library/DateHelper";
import MemberShowMore from "@/components/task/MemberShowMore.vue";

export default defineComponent({
  name: "ListDocumentView",
  components: {
    ApiLoader,
    MemberShowMore,
  },
  props: {
    taskId: String,
  },
  data() {
    return {
      seeMore: false,
      partOfMember: "",
      allMembers: "",
      labelStatus: {
        1: { label: "Not Started" },
        2: { label: "In Progress" },
        3: { label: "Done" },
        14: { label: "Need for Approval" },
        15: { label: "Not Started" },
        16: { label: "In Progress" },
        17: { label: "Done" },
      },
      task: Object,
    };
  },
  methods: {
    getTask() {
      return client
        .getTasksByIdTask({
          store: this.$store,
          data: {
            id: this.$route.params.taskId,
            username: this.$store.state.username,
          },
        })
        .catch((err) => {
          if (err.response?.status === 403) {
            this.$root.toast.show({
              message: "tidak memiliki akses ke halaman ini",
              color: "warning",
              timeout: 3000,
            });
            this.$router.push({
              name: "workspace-management",
            });
          }
        });
    },
    handleLoadingEnded({ success, response }) {
      if (success) {
        (this.task = response.plainData[0]),
          this.setMember(response.plainData[0].taskMembers);
      }
    },
    dueDate() {
      if (this.task.startDate == null || this.task.endDate == null) return "-";
      return (
        reformatFormDate(this.task.startDate.substring(0, 10)) +
        " - " +
        reformatFormDate(this.task.endDate.substring(0, 10))
      );
    },
    setMember(member) {
      if (member.length > 10) {
        for (let index = 0; index < 10; ++index) {
          this.partOfMember += member[index].name + ", ";
          this.allMembers += member[index].name + ", ";
        }
        for (let index = 10; index < member.length; ++index) {
          this.allMembers += member[index].name + ", ";
        }
      } else {
        for (const item of member) {
          this.allMembers += item.name + ", ";
        }
      }
    },
    showAllMembers() {
      document.getElementById("allMember").style.display = "block";
      document.getElementById("partMember").style.display = "none";
    },
    showLessMembers() {
      document.getElementById("allMember").style.display = "none";
      document.getElementById("partMember").style.display = "block";
    },
  },
  mounted() {
    undefined;
  },
});
</script>

<style scoped>
.textGreyTitle {
  color: #a6abc7;
}

.text-gradient-blue {
  background: linear-gradient(90.76deg, #267dc2 15.32%, #ff000d 61.36%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.text-orangeTheme {
  color: #fe7411;
}

.grand-title {
  font-family: "Poppins";
  font-style: normal;
  font-weight: 600;
  font-size: 20px;
}
</style>
