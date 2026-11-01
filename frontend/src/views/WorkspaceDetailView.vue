<template>
  <div class="ml-md-10 mt-10">
    <api-loader
      :apiMethod="getWorkspace"
      @loadingEnded="handleLoadingEnded"
      ref="loader"
    >
      <template v-slot:default="props">
        <!-- <pre>{{ props.response.plainData }}</pre> -->
        <div class="d-block pa-2">
          <v-btn
            variant="outlined"
            size="large"
            icon="mdi-arrow-left"
            class="ml-5 ml-md-0"
            color="#045695"
            style="border: 0.01px solid #d3d3d3; color: white !important"
            elevation="2"
            :to="{ name: 'workspace-management' }"
            ><v-icon icon="mdi-arrow-left" color="#045695"> </v-icon
          ></v-btn>
        </div>
        <div class="d-block pa-8 pa-md-4 mt-3">
          <p style="color: dimgrey" class="text-h5 font-weight-medium">
            {{ props.response.plainData.workspaceName }}
          </p>
        </div>
        <template v-if="props.response.plainData.status == 8">
          <v-img
            class="mt-10"
            src="/images/waiting_for_approval.svg"
            style="
              display: block;
              margin: 0 auto;
              width: 20vw;
              margin-top: 20px;
            "
          ></v-img>
          <h6
            class="text-center text-17 font-weight-bold mt-6 text-gradient-grey"
          >
            Please wait for workspace approval
          </h6>
        </template>
        <template v-else-if="props.response.plainData.status == 12">
          <v-sheet
            class="text-center d-block mt-10"
            style="background: transparent"
          >
            <v-icon size="80" color="#d3d3d3"> mdi-information-outline</v-icon>
          </v-sheet>
          <h6
            class="text-center text-17 font-weight-bold mt-4 text-gradient-grey"
          >
            This workspace has been deleted
          </h6>
        </template>
        <template v-else-if="props.response.plainData.status == 13">
          <v-sheet
            class="text-center d-block mt-10"
            style="background: transparent"
          >
            <v-icon size="80" color="#d3d3d3"> mdi-information-outline</v-icon>
          </v-sheet>
          <h6
            class="text-center text-17 font-weight-bold mt-4 text-gradient-grey"
          >
            This workspace has no longer exist
          </h6>
        </template>
        <template v-else>
          <div class="d-flex pa-2 bg-white overflow-x-auto bg-transparent">
            <activity
              :items="props.response.plainData"
              @reload="refresh"
              @startTask="startTask"
            />
          </div>
        </template>
      </template>
      <template v-slot:loading>
        <Shimmer />
      </template>
    </api-loader>
    <router-view></router-view>
    <v-overlay
      :model-value="isLoading"
      class="align-center justify-center"
      persistent
    >
      <v-card
        color="#065695"
        class="pl-10 pr-10 pt-0 pb-0"
        style="border-radius: 10px"
      >
        <v-card-text>
          <p class="text-white">Please stand by</p>
          <v-progress-linear
            indeterminate
            color="white"
            class="mb-0 mt-2"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-overlay>
  </div>
</template>
<script lang="js">
/* eslint-disable */
import { defineComponent } from "vue";
import Shimmer from "@/components/loading/WorkspaceDetailViewLoading.vue"
import Activity from "@/components/workspace/WorkspaceActivityCard.vue"
import client from "@/library/ApiClient";
import ApiLoader from "@/components/ApiLoader.vue";

export default defineComponent({
  name: "WorkspaceDetailView",
  emits: ["reload","startTask","refresh"],
  components: {
    Activity,
    ApiLoader,
    Shimmer
  },
  props:{},
  data: function () {
    return {
      item: Object,
      isLoading: false
    };
  },
  methods:{
    getWorkspace() {
      return client.getListActivityAndTaskByTaskMemberandIdWorkspace({
        store: this.$store,
        data: {
          id: this.$route.params.workspaceId,
          username: this.$store.state.username,
        },
      })
      .catch((err) => {
          if (err.response) {
            if (err.response.status == 403) {
              this.$root.toast.show({
                message: "tidak memiliki akses ke halaman ini",
                color: "warning",
                timeout: 3000,
              });
              this.$router.push({ name: "home" });
            }
          }
        });
    },
    handleLoadingEnded({ success, response }) {
      if(success){
        this.item = response.plainData
      }
    },
    refresh(){
      this.$refs.loader.callApi();
    },
    startTask(idTask) {
      this.isLoading = true;
      client.startTasks({
        store: this.$store,
        data: {
          id: idTask,
        },
      }).then((response)=>{
        if (response.plainData.responseCode == "011025") {
        this.$root.toast.show({
          message: response.plainData.responseMessage,
          color: "error",
          timeout: 3000,
          icon: "mdi-check",
        });
      } else if (response.plainData.responseCode == "011000") {
        this.$root.toast.show({
          message: response.plainData.responseMessage,
          color: "success",
          timeout: 3000,
          icon: "mdi-check",
        });
        this.refresh()
      }
      }).finally(()=>{
        this.isLoading = false
      });

    },
  },
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
.text-gradient-grey {
  background: -webkit-linear-gradient(
    92.72deg,
    rgba(121, 121, 121, 0.9) 0%,
    rgba(187, 187, 187, 0.9) 152.21%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 900;
  font-size: large;
}
</style>
