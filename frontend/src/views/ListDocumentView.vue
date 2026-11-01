<template>
  <div>
    <div v-if="$route.name == 'main'">
      <div class="d-block bg-white mt-0">
        <v-row no-gutters class="text-center mb-5">
          <v-col cols="5" style="align-self: center">
            <v-sheet class="pa-0 ma-0 bg-white font-weight-bold">
              <p style="color: #3a416f">Document</p>
            </v-sheet>
          </v-col>
          <v-col cols="4">
            <v-sheet class="pa-0 ma-0 font-weight-bold">
              <v-sheet class="pa-0 ma-0 bg-white font-weight-bold">
                <p style="color: #3a416f">Type</p>
              </v-sheet>
            </v-sheet>
          </v-col>
          <v-col cols="3" style="align-self: center">
            <v-sheet class="pa-0 ma-0 bg-white font-weight-bold">
              <p style="color: #3a416f">Action</p>
            </v-sheet>
          </v-col>
        </v-row>

        <api-loader :key="loader" :apiMethod="getListDocument">
          <template v-slot:default="props">
            <template v-if="props.response.length">
              <v-sheet
                class="d-block"
                v-for="document in props.response"
                :key="document.id"
              >
                <v-row no-gutters class="text-center pa-1 mt-4">
                  <v-col cols="5" style="align-self: center">
                    <v-sheet
                      class="pa-0 pl-5 ma-0 bg-white font-weight-medium text-left"
                    >
                      {{ document.name }}
                      <v-tooltip activator="parent" location="top">{{
                        document.name
                      }}</v-tooltip>
                    </v-sheet>
                  </v-col>
                  <v-col cols="4" style="align-self: center">
                    <img
                      v-if="document.isSendDocument"
                      :src="document.icon"
                      style="width: 40px; height: 40px; margin-left: -10px"
                    />
                    <img
                      v-else
                      :src="document.icon"
                      style="width: 22px; height: 30px"
                    />
                    <v-tooltip activator="parent" location="top">
                      .{{ document.extension }} file
                    </v-tooltip>
                  </v-col>
                  <v-col
                    cols="3"
                    style="align-self: left; text-align-last: left"
                  >
                    <v-sheet
                      class="pa-0 ma-0 bg-white font-weight-bold"
                      style="text-align: center"
                    >
                      <document-access-management
                        :document="document"
                        :isOwner="isOwner"
                        @action="handleAction"
                      />
                    </v-sheet>
                  </v-col>
                </v-row>
                <v-expand-transition>
                  <div
                    v-show="expandMap.get(document.id)"
                    class="ml-5 mr-5 mb-2 mt-2"
                    :id="document.id"
                    style="display: none"
                  >
                    <document-detail
                      :document="document"
                      :isOpen="expandMap.get(document.id)"
                      :key="expandMap.get(document.id)"
                    />
                  </div>
                </v-expand-transition>
                <hr color="#d3d3d3" size="1" class="ml-5 mr- mt-5" />
              </v-sheet>
            </template>
            <template v-else>
              <v-sheet class="text-grey text-center text-16 font-weight-medium">
                <v-img
                  src="/images/no_workspace_available.png"
                  width="100%"
                  style="height: 20vh"
                  class="d-block mt-10"
                >
                </v-img>

                <p class="mt-5 font-italic">There is no data...</p>
              </v-sheet>
            </template>
            <div class="text-center" v-if="props.response.length">
              <v-container>
                <v-row justify="center">
                  <v-col cols="8">
                    <v-container class="max-width">
                      <v-pagination
                        v-model="page"
                        class="my-4"
                        rounded="1"
                        elevation="2"
                        size="small"
                        :length="pageInfo.totalPage"
                        @update:modelValue="onPageUpdated"
                      ></v-pagination>
                    </v-container>
                  </v-col>
                </v-row>
              </v-container>
            </div>
          </template>
          <template v-slot:loading>
            <paragraph-shimmer :lines="10" :random-size="true" />
          </template>
        </api-loader>
      </div>
      <Toast ref="toast" />
    </div>
    <div v-else>
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { getDocumentUtama } from "@/models/document";
import { ref, defineComponent } from "vue";
import { useRoute, useRouter } from "vue-router";
import DocumentAccessManagement from "@/components/document/DocumentAccessManagement.vue";
import DocumentDetail from "@/components/document/DocumentListDetail.vue";
import ApiLoader from "@/components/ApiLoader.vue";
// import { useToast } from "vue-toastification";
import Toast from "@/components/utils/ToastComponent.vue";

defineComponent({
  components: {
    ApiLoader,
    DocumentAccessManagement,
    DocumentDetail,
  },
});

const isOwner = ref(false);
const expandMap = ref(new Map([]));
const toast = ref();
const router = useRouter();
const route = useRoute();
const loader = ref(0);
let pageInfo = ref(0);
const page = ref(parseInt(route.params.pageId));
const onPageUpdated = () => {
  router.push({ params: { pageId: page.value } });
  loader.value++;
};

const getListDocument = () => {
  return getDocumentUtama(route.params.taskId, page.value, 10).then(
    (result) => {
      isOwner.value = result.isOwner;
      pageInfo.value = result.info;

      result.list.filter((element) => {
        expandMap.value.set(element.id, false);
      });
      return result.list;
    }
  );
};

const handleAction = (action) => {
  switch (action.name) {
    case "see detail": {
      const listIndex = action.value;
      if (!expandMap.value.get(listIndex)) {
        expandMap.value.set(listIndex, true);
      } else {
        expandMap.value.set(listIndex, false);
      }
      break;
    }
    case "reload page": {
      loader.value++;
      break;
    }
    case "delete": {
      if (action.value) {
        toast.value.show({
          message: "Document has been deleted",
          color: "success",
          timeout: 3000,
          icon: "mdi-check",
        });
        loader.value++;
      } else {
        toast.value.show({
          message:
            "Unable to delete document. Please check your connection and try again",
          color: "error",
          timeout: 3000,
          icon: "mdi-check",
        });
      }
      break;
    }
  }
};
</script>

<style scoped>
:deep(.v-icon) {
  color: #065695;
}
:deep(.v-pagination__item--is-active) {
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%) !important;
  color: white !important;
  border-radius: 10px;
}
:deep(.v-pagination .v-btn) {
  border-radius: 10px;
  font-size: 15px;
  font-weight: bold;
}
:deep(.v-pagination__item) {
  color: #065695;
}
:deep(.v-pagination__next) {
  color: #065695;
}
:deep(.v-pagination__prev) {
  color: #065695;
}
.textGrey {
  color: rgb(166, 171, 199);
}
.buttonUpload {
  background: linear-gradient(180deg, #d6212a, #ff000d);
  font-size: 12px;
  font-weight: 900;
  text-align: center;
}
.sectionRed {
  background: linear-gradient(
    89.97deg,
    #d6212a 33.34%,
    rgba(255, 255, 255, 0) 109.62%
  );
  border-radius: 0px;
}

.sectionBlue {
  background: linear-gradient(
    89.96deg,
    #065695 35.16%,
    rgba(255, 255, 255, 0) 101.03%
  );
  border-radius: 0px;
}

:deep(.v-overlay__content) {
  border-radius: 10px;
}

:deep(.v-expansion-panel-title__overlay) {
  background: white;
}
</style>
