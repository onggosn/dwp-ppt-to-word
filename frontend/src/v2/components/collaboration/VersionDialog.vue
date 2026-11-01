<template>
  <Teleport to="body"> </Teleport>
  <v-dialog v-model="dialog" persistent class="dialog-visible" fullscreen>
    <v-card class="content-dialog pb-2">
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
            @click="close"
            ><v-icon icon="mdi-arrow-left" color="#045695"> </v-icon>
          </v-btn>
          <span class="view-title ml-3">{{ documentName }}</span>
        </div>
      </v-toolbar>
      <v-card-item>
        <VersionEditor
          :channelId="''"
          :sectionName="''"
          :eformId="''"
          :isEditForm="true"
          :idBPDocumentVersion="versionId"
        />
      </v-card-item>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
/* eslint-disable */
import { ref, computed } from "vue";
import { useStore } from "vuex";
import VersionEditor from "@v2/components/collaboration/editor/VersionEditor.vue";
const dialog = ref(false);

const store = useStore();
const props = defineProps({
  versionId: {
    type: String,
    required: true,
  },
});
const documentName = computed(
  () => store.getters["collaborationStore/getDocumentName"]
);
function show() {
  dialog.value = true;
}

function close() {
  dialog.value = false;
}

defineExpose({
  show,
  close,
});
</script>

<style scoped>
.view-title {
  font-family: Poppins;
  font-size: 20px;
  font-weight: 700;
  line-height: 30px;
  color: #3a416f;
  margin-left: 17px;
}
.content-dialog {
  overflow-y: hidden !important;
}
</style>
