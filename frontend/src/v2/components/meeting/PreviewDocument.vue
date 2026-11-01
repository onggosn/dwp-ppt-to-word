<template>
  <v-dialog
    v-model="isOpen"
    transition="dialog-bottom-transition"
    fullscreen
    persistent
  >
    <v-card>
      <v-toolbar class="pa-4 bg-white" style="border-bottom: solid 2px #e4e4e4">
        <div class="d-block">
          <v-btn
            variant="outlined"
            size="large"
            icon="mdi-arrow-left"
            class="ml-5 ml-md-0"
            color="#045695"
            style="border: 0.01px solid #d3d3d3; color: white !important"
            elevation="2"
            @click="router.push({ name: 'v2.meeting-detail-material' })"
            ><v-icon icon="mdi-arrow-left" color="#045695"> </v-icon>
          </v-btn>
          <span class="view-title ml-3">{{ documentPriviewItem.title }}</span>
        </div>
      </v-toolbar>
      <div class="my-2 d-flex justify-center">
        <PreviewFlowApproval
          :idDoc="materialId"
          @update="getMetaData(materialId)"
          v-if="isUseMetadata"
        />
      </div>
      <v-row align="start" no-gutters>
        <v-col :cols="isUseMetadata ? 9 : 12" style="height: 100%">
          <view-document
            v-if="materialId"
            :document="documentPriviewItem"
            type="material"
          />
        </v-col>
        <v-col :cols="3" v-if="isUseMetadata" class="px-3">
          <MetadataPreview />
        </v-col>
      </v-row>
    </v-card>
  </v-dialog>
</template>

<script lang="ts" setup>
import ViewDocument from "@v2/components/meeting/meetingMaterial/ViewDocument.vue";
import MetadataPreview from "@v2/components/meeting/PreviewDocumentMetadata.vue";
import PreviewFlowApproval from "@v2/components/meeting/PreviewFlowApproval.vue";

import { ref, computed, onBeforeMount, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { TMaterialPreview } from "@/v2/Type";
import { useStore } from "vuex";

const store = useStore();
const route = useRoute();
const router = useRouter();
const isOpen = ref<boolean>(route.name == "v2.meeting-detail-material-preview");
const materialId = computed((): string => route.params.idMaterial as string);
const eventId = computed((): string => route.params.idEvent as string);
const isUseMetadata = ref<boolean>(false);

const documentPriviewItem = ref<TMaterialPreview>({
  id: null,
  docExt: "",
  title: "",
});

function getMetaData(materialId: string) {
  store
    .dispatch("meetingStore/getMaterialMetadata", {
      idEvent: eventId.value,
      idEventPresentationMaterial: materialId,
    })
    .then((res: any) => {
      documentPriviewItem.value.docExt = res.responseData.title
        .split(".")
        .at(-1);
      documentPriviewItem.value.title = res.responseData.title;
      isUseMetadata.value = res.responseData.docType != null;
    });
}

onBeforeMount(() => {
  if (isOpen.value) {
    documentPriviewItem.value.id = materialId.value;
    getMetaData(materialId.value);
  }
});

watch(
  () => materialId.value,
  (val: string) => {
    getMetaData(val);
  }
);
</script>
<style>
.metadata-header {
  font-weight: 700;
  font-size: 20px;
  line-height: 27px;
  color: #3a416f;
  margin-top: 6px;
  margin-bottom: 6px;
}

.metadata-title {
  font-weight: 700;
  font-size: 17px;
  line-height: 25px;
  color: #a6abc7;
}

.metadata-body {
  font-weight: 700;
  font-size: 17px;
  line-height: 25px;
  color: #3a416f;
  margin-top: 8px;
}

.meta-data-status-approve {
  color: #02aa59;
}
.view-title {
  font-family: Poppins;
  font-size: 20px;
  font-weight: 700;
  line-height: 30px;
  color: #3a416f;
  margin-left: 17px;
}
</style>
