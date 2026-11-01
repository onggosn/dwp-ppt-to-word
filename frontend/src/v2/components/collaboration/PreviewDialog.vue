<template>
  <Teleport to="body">
    <v-dialog v-model="isShow" persistent class="dialog-visible" fullscreen>
      <v-card class="content-dialog pb-2">
        <v-toolbar
          class="pa-4 bg-white"
          style="border-bottom: solid 2px #e4e4e4"
        >
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
          <PreviewEditor />
        </v-card-item>
      </v-card>
    </v-dialog>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useStore } from "vuex";
import PreviewEditor from "@v2/components/collaboration/editor/PreviewEditorDecouple.vue";

const isShow = ref(false);
const store = useStore();

const documentName = computed(
  () => store.getters["collaborationStore/getDocumentName"]
);

function show() {
  isShow.value = true;
}

function close() {
  isShow.value = false;
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
.modal-container {
  margin: auto;
  background: #fff;
  border-radius: 10px;
  position: relative;
  padding-top: 1cm;
  padding-left: 1cm;
  padding-right: 1cm;
  padding-bottom: 1cm;
  width: 21.01cm;
  display: flex;
  flex-direction: column;
  overflow-y: scroll;
  width: 21.01cm;
}
.modal-warning-btn-close {
  position: absolute;
  top: 15px;
  right: 15px;
}

.preview-container {
  overflow-x: scroll;
}
</style>
