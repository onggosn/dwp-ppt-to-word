<template>
  <v-sheet class="pl-3 mr-0">
    <v-row no-gutters class="pl-3 pr-3 pb-6">
      <v-col>
        <v-btn
          :class="
            $route.name == 'support'
              ? 'tab-title-active-red'
              : 'tab-title-active-white'
          "
          class="text-white text-none ml-0"
          rounded="lg"
          :to="{
            name: 'support',
            params: {
              pageId: 1,
              workspaceId: $route.params.workspaceId,
              taskId: $route.params.taskId,
            },
          }"
        >
          Materi Pembahasan
        </v-btn>
        <v-btn
          :class="
            $route.name == 'main'
              ? 'tab-title-active-blue'
              : 'tab-title-active-white'
          "
          class="text-white text-none ml-0"
          rounded="lg"
          :to="{
            name: 'main',
            params: {
              pageId: 1,
              workspaceId: $route.params.workspaceId,
              taskId: $route.params.taskId,
            },
          }"
        >
          Hasil Pembahasan
        </v-btn>
      </v-col>
      <v-col cols="2" style="align-self: center" class="mr-4">
        <api-loader :apiMethod="getTask" @loadingEnded="handleLoadingEnded">
          <template v-slot:default="props">
            <document-utama-upload
              ref="DocumentUtamaUpload"
              :taskMembers="props.response.plainData[0].taskMembers"
              :idTask="props.response.plainData[0].id"
              :idTaskTemplate="props.response.plainData[0].idTaskTemplate"
              @doneUpload="refresh"
            />
            <document-support-upload
              ref="DocumentSupportUpload"
              :taskMembers="props.response.plainData[0].taskMembers"
              :idTask="props.response.plainData[0].id"
              :idTaskTemplate="props.response.plainData[0].idTaskTemplate"
              @doneUpload="refreshSupport"
            />

            <v-btn
              v-if="$route.name == 'main' && isAddDocument"
              @click="UtamaUpload()"
              rounded="pill"
              color="white"
              class="bg-blue ml-4 pa-2 pr-4 buttonUpload-blue"
              elevation="2"
              >+ Add New File</v-btn
            >

            <v-btn
              v-if="$route.name == 'support' && isAddDocument"
              @click="SupportUpload()"
              rounded="pill"
              color="white"
              class="bg-blue ml-4 pa-2 pr-4 buttonUpload-red"
              elevation="2"
              >+ Add New File</v-btn
            >
          </template>
          <template v-slot:loading>
            <free-style-shimmer
              height="4.5vh"
              width="80%"
              border-radius="20px"
              color="#DCDCDC"
              class="ml-10 mt-1 mb-4"
            />
          </template>
        </api-loader>
      </v-col>
    </v-row>

    <router-view :key="docloader" :isOwner="isOwner" />
  </v-sheet>
</template>
<script>
import ApiLoader from "@/components/ApiLoader.vue";
import client from "@/library/ApiClient";
import DocumentUtamaUpload from "@/components/upload/DocumentUtamaUpload.vue";
import DocumentSupportUpload from "@/components/upload/DocumentSupportUpload.vue";

export default {
  components: {
    ApiLoader,
    DocumentUtamaUpload,
    DocumentSupportUpload,
  },
  data: () => ({
    tab: null,
    showDialog1: false,
    docloader: 0,
    docsupportloader: 0,
    isAddDocument: false,
    isOwner: false,
    isLoading: true,
  }),
  methods: {
    UtamaUpload() {
      this.$refs.DocumentUtamaUpload.start();
    },
    SupportUpload() {
      this.$refs.DocumentSupportUpload.start();
    },
    getTask() {
      return client.getTasksByIdTask({
        store: this.$store,
        data: {
          id: this.$route.params.taskId,
          username: this.$store.state.username,
        },
      });
    },
    handleLoadingEnded({ success, response }) {
      if (success) {
        this.isAddDocument = response.plainData[0].isAddDocument;
        this.isOwner = response.plainData[0].isOwner;
      }
    },
    openUploadDialog1() {
      this.$refs.dialogDocUtama.start();
    },
    refresh() {
      this.docloader++;
    },
    refreshSupport() {
      this.docloader++;
    },
  },
  mounted() {
    if (this.$route.name == "task-document") {
      this.$router.push({
        name: "support",
        params: {
          pageId: 1,
          workspaceId: this.$route.params.workspaceId,
          taskId: this.$route.params.taskId,
        },
      });
    }
  },
};
</script>

<style scoped>
.buttonUpload-red {
  background: linear-gradient(180deg, #d6212a, #ff000d);
  font-size: 12px;
  font-weight: 900;
  text-align: center;
}

.buttonUpload-blue {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  font-size: 12px;
  font-weight: 900;
  text-align: center;
}
:deep(.materi.v-tab--selected) {
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%);
  color: white !important;
  font-weight: 600 !important;
  border-radius: 10px 10px 0px 0px !important;
  border: 0px solid #a6abc7;
  height: 5vh;
  place-self: center;
}
:deep(.hasil.v-tab--selected) {
  background: linear-gradient(180deg, #d6212a 0%, #ff000d 100%);
  color: white !important;
  font-weight: 600 !important;
  border-radius: 10px 10px 0px 0px !important;
  border: 0px solid #a6abc7;
  height: 5vh;
  place-self: center;
}
:deep(.v-tab) {
  letter-spacing: 0.1px;
  font-weight: 200;
  color: #797979 !important;
  border: 1.5px solid #a6abc7;
  border-radius: 10px 10px 0px 0px !important;
  height: 5vh;
  place-self: center;
}
.tab-title-active-blue {
  border-radius: 10px 10px 0px 0px !important;
  border: 1.5px solid #bfc3d7;
  letter-spacing: -0.3px;
  font-weight: 900;
  background: linear-gradient(180deg, #065695, #267dc2);
  color: white !important;
  min-height: 5vh;
  max-height: 7vh;
}
.tab-title-active-red {
  border-radius: 10px 10px 0px 0px !important;
  border: 1.5px solid #bfc3d7;
  letter-spacing: -0.3px;
  font-weight: 900;
  background: linear-gradient(180deg, #d6212a 0%, #ff000d 100%);
  color: white !important;
  min-height: 5vh;
  max-height: 7vh;
}
.tab-title-active-white {
  border-radius: 10px 10px 0px 0px !important;
  border: 1.5px solid #bfc3d7;
  letter-spacing: -0.3px;
  font-weight: 900;
  background: white;
  color: grey !important;
  min-height: 5vh;
  max-height: 7vh;
}
</style>
