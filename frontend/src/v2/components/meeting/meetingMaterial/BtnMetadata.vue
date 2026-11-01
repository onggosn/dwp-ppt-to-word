<template>
  <v-btn
    v-if="!isOnContentManagement"
    class="pa-1"
    min-width="0"
    variant="text"
    @click="openModal"
  >
    <v-icon class="table-content-center btn-default" color="#267DC2" small>
      mdi-eye
    </v-icon>
    <v-tooltip activator="parent" location="top">Metadata</v-tooltip>
  </v-btn>
  <v-btn
    v-else
    density="default"
    icon="mdi-eye"
    rounded="lg"
    size="x-small"
    class="primary-gradient"
    style="color: white"
    @click="openModal"
  ></v-btn>
  <Teleport to="body">
    <v-dialog v-model="dialog" :max-width="800" persistent>
      <v-card
        class="mb-5 border-radius-dwp"
        :class="{ 'overflow-hidden': !documentItem.docType }"
      >
        <v-card-title :class="titleConfig.containerClass">
          <component :is="titleConfig.titleTag" :class="titleConfig.titleClass">
            Metadata
          </component>
          <v-btn
            density="default"
            icon="mdi-close"
            variant="text"
            :class="titleConfig.buttonClass"
            :style="titleConfig.buttonStyle"
            @click="dialog = false"
          />
          <hr v-if="titleConfig.showHr" class="line mt-5 mb-4" />
        </v-card-title>
        <div
          v-if="!isOnContentManagement"
          class="separatorHorizontalGradient"
          style="flex-shrink: 0"
        ></div>
        <div class="empty-illustration" v-if="!props.id">
          <img
            :src="require('@/v2/assets/empty/no_available_state.svg')"
            width="300px"
            height="311px"
          />
        </div>
        <v-card-text v-if="props.id">
          <v-row align="start">
            <v-col :cols="12">
              <div class="metadata-title">Title</div>
              <div class="metadata-body">
                {{ generateLabelMetadata(documentItem.title) }}
              </div>
            </v-col>
            <v-col :cols="6">
              <div v-if="documentItem.docType" class="my-3">
                <div class="metadata-title">Status</div>
                <div
                  class="metadata-body"
                  :class="getDocumentColor(documentItem.statusName)"
                >
                  {{ generateLabelMetadata(documentItem.statusName) }}
                </div>
              </div>
              <div v-if="documentItem.docType" class="my-3">
                <div class="metadata-title">List Document</div>
                <div class="metadata-body">
                  {{ generateLabelMetadata(documentItem.materialListDoc) }}
                </div>
              </div>
              <div class="my-3">
                <div class="metadata-title">Event</div>
                <div class="metadata-body">
                  {{ generateLabelMetadata(documentItem.eventName) }}
                </div>
              </div>
              <div v-if="documentItem.docType" class="my-3">
                <div class="metadata-title">Tipe Dokumen</div>
                <div class="metadata-body">
                  {{ generateLabelMetadata(documentItem.docType) }}
                </div>
              </div>
              <div v-if="documentItem.docType" class="my-3">
                <div class="metadata-title">Satker Pembuat</div>
                <div class="metadata-body">
                  {{ generateLabelMetadata(documentItem.satkerPembuat) }}
                </div>
              </div>
              <div v-if="documentItem.docType" class="my-3">
                <div class="metadata-title">Presenter</div>
                <div class="metadata-body">
                  {{ generateLabelMetadata(documentItem.presenter) }}
                </div>
              </div>
              <div v-if="documentItem.docType" class="my-3">
                <div class="metadata-title">Penyusun</div>
                <div class="metadata-body">
                  {{
                    documentItem.listPenyusun.filter((e) => e).length != 0
                      ? documentItem.listPenyusun.join(", ")
                      : "-"
                  }}
                </div>
              </div>
              <div v-if="documentItem.docType" class="my-3">
                <div class="metadata-title">Pengaju</div>
                <div class="metadata-body">
                  {{ generateLabelMetadata(documentItem.pengaju) }}
                </div>
              </div>
            </v-col>
            <v-col :cols="6">
              <div v-if="!documentItem.docType" class="my-3">
                <div class="metadata-title">Diunggah Oleh</div>
                <div class="metadata-body">
                  {{ documentItem.createdByName }}
                </div>
              </div>
              <div v-if="documentItem.docType" class="my-3">
                <div class="metadata-title">Penyetuju</div>
                <div class="metadata-body">
                  {{ generateLabelMetadata(documentItem.penyetuju) }}
                </div>
              </div>
              <div v-if="documentItem.docType" class="my-3">
                <div class="metadata-title">Version</div>
                <div class="metadata-body">
                  {{ generateLabelMetadata(documentItem.version) }}
                </div>
              </div>
              <div v-if="documentItem.docType" class="my-3">
                <div class="metadata-title">Progress</div>
                <div class="metadata-body">
                  <FlowApproval :items="documentItem.listApprovals ?? []" />
                </div>
              </div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-dialog>
  </Teleport>
</template>
<script lang="ts" setup>
import FlowApproval from "@v2/components/meeting/MetadataFlowApproval.vue";
import { generateLabelMetadata } from "@/v2/helpers/utils";
import { getDocumentColor } from "@/v2/helpers/color";
import { ref, computed } from "vue";
import { useStore } from "vuex";
import { TMaterialMetadata } from "@/v2/Type";
import { useRoute } from "vue-router";

const store = useStore();
const route = useRoute();
const props = defineProps({
  id: String,
  isOnContentManagement: Boolean,
});
const idEvent = computed((): string => {
  return route.params.idEvent as string;
});
const dialog = ref<boolean>(false);
const documentItem = computed((): TMaterialMetadata => {
  return store.state.meetingStore.materialMetadata as TMaterialMetadata;
});

const titleConfig = computed(() => {
  if (props.isOnContentManagement) {
    return {
      titleTag: "h3",
      titleClass: "text-h6 text-darkBlue font-weight-bold",
      containerClass: "text-center mt-3",
      buttonClass: "btn-close",
      buttonStyle: undefined,
      showHr: true,
    };
  }
  return {
    titleTag: "div",
    titleClass: "text-20 text-blackTheme fw-600 mt-2 mb-2",
    containerClass: "d-flex justify-center align-center",
    buttonClass: "mr-2",
    buttonStyle: "position: absolute; right: 0",
    showHr: false,
  };
});

function openModal() {
  if (!props.id) {
    dialog.value = true;
  } else {
    store
      .dispatch("meetingStore/getMaterialMetadata", {
        idEvent: props.isOnContentManagement ? "" : idEvent.value,
        idEventPresentationMaterial: props.id,
      })
      .then(() => {
        dialog.value = true;
      });
  }
}
</script>
<style scoped>
.empty-illustration {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding-bottom: 40px;
}

.btn-default {
  border: 1px solid;
  border-radius: 4px;
  padding: 13px;
  transform: scaleX(-1);
}

.metadata-header {
  font-weight: 700;
  font-size: 20px;
  line-height: 27px;
  color: #3a416f;
  margin-top: 6px;
  margin-bottom: 6px;
}

.metadata-title {
  font-weight: 400;
  font-size: 18px;
  line-height: 24px;
  color: #9e9e9e;
}

.metadata-body {
  font-weight: 600;
  font-size: 16px;
  line-height: 28px;
  color: #4b4b4b;
  margin-top: 4px;
}

.meta-data-status-approve {
  color: #02aa59;
}

.line {
  border: none; /* Remove the default border */
  height: 2px; /* Set the height of the hr */
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
}

.btn-close {
  position: absolute;
  right: 0;
  top: 0;
  margin-top: 10px;
  margin-right: 10px;
}
</style>
