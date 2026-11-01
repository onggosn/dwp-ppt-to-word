<template>
  <div>
    <p class="font-weight-bold text-darkBlue text-left">
      Title <span class="text-red font-weight-bold">*</span>
    </p>
    <v-chip style="height: 56px; border-radius: 10px; width: 100%"> </v-chip>
  </div>

  <v-card
    class="mt-5 pb-10"
    style="
      border-radius: 8px;
      padding-left: 0.5cm;
      padding-right: 0.5cm;
      padding-top: 0.5cm;
      pointer-events: none;
    "
    width="21.01cm"
  >
    <document-editor
      :channelId="'hahah'"
      :content="content"
      v-if="isContentReady"
    />
    <!-- <div v-if="idDocumentType == 1">
      <div class="d-flex justify-space-between">
        <img :src="require(`@/v2/assets/cop_logo_bi.svg`)" class="" />
        <div class="align-self-center font-weight-bold text-24">RAHASIA</div>
      </div>
      <div>
        <p class="text-24 font-weight-bold mt-6 mb-6">Risalah Rapat</p>
      </div>
    </div>

    <templage v-for="item in document" :key="item">
      <p class="text-left font-weight-bold" style="font-size: 0.9167em">
        {{ item.sectionName }}
      </p>
      <templage v-for="child in item.children" :key="child">
        <p
          class="text-left font-weight-bold ml-4 mt-2"
          v-if="child.isLabelVisible"
          style="font-size: 0.9167em"
        >
          {{ child.bPEFormLabel }}
        </p>
        <form-editor
          v-if="child.idFormEditor"
          :channelId="child.idFormEditor"
          :sectionName="child.bPEFormLabel"
          :eformId="child.idEForm"
          :isEditForm="props.isEditForm"
        />
      </templage>
    </templage> -->
  </v-card>
</template>

<script setup lang="ts">
import { defineComponent, defineProps, ref } from "vue";
import DocumentEditor from "./editor/DocumentEditor.vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";

defineComponent({
  DocumentEditor,
});

const props = defineProps({
  isEditForm: {
    type: Boolean,
    default: false,
  },
});

const isContentReady = ref(false);
const store = useStore();
const route = useRoute();
const content = ref();

store
  .dispatch("documentStore/fetchPreviewDocument", route.params.idDoc)
  .then((data) => {
    content.value = data.formEditor;
    isContentReady.value = true;
  });
</script>

<style scoped>
.documentStyle {
  border-radius: 8px;
  margin-top: 20px;
  width: 21.01cm;
  padding-top: 1cm;
  padding-left: 1cm;
  padding-right: 1cm;
  padding-bottom: 1cm;
}
</style>
