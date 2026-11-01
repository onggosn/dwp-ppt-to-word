<template>
  <div>
    <v-card class="mt-5 ml-n3 mb-10 description-detail">
      <v-sheet
        class="mt-10 ml-10 mb-10 pa-2 ma-2 text-left font-weight-bold text-newBlack"
      >
        <div class="editor-desc__container">
          <div ref="editors" id="readonlyeditor" />
        </div>
      </v-sheet>
    </v-card>
    <v-card
      v-if="meetingData.method != 'Offline'"
      class="mt-2 ml-n3 mb-15 description-detail"
    >
      <v-sheet
        class="mt-10 ml-10 mb-10 pa-2 ma-2 text-left font-weight-bold text-newBlack"
      >
        <div>
          <p class="font-weight-bold text-darkBlue mb-5">Meeting Link</p>
          <p class="mb-3">
            1. Main Link :
            <a
              class="link-media font-weight-bold text-newBlack"
              :href="sanitizedMainLink"
              v-html="sanitizedMainLinkText"
            ></a>
          </p>
          <p v-if="meetingData.idMeetingBackupPlatform != null" class="mb-3">
            2. Backup Link :
            <a
              class="link-media font-weight-bold text-newBlack"
              :href="sanitizedBackupLink"
              v-html="sanitizedBackupLinkText"
            ></a>
          </p>
        </div>
      </v-sheet>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { computed, watch, ref, onMounted } from "vue";
import { useStore } from "vuex";
import EditorOutput from "@/v2/components/side-project/ckeditor/build/ckeditor";
import { sanitizeUrl, sanitizeLinkText } from "@/v2/helpers/utils";
import { useInitializeConfig } from "@/v2/composables/useInitializeConfig";

const store = useStore();
const { ckEditorLicense } = useInitializeConfig();
const editors = ref<HTMLDivElement>();
let editorInstance: any;

const meetingData = computed((): any => {
  return store.state.meetingStore.meetingItem ?? {};
});

const sanitizedMainLink = computed(() => {
  return sanitizeUrl(meetingData.value.eventlink);
});

const sanitizedMainLinkText = computed(() => {
  return sanitizeLinkText(meetingData.value.eventlink);
});

const sanitizedBackupLink = computed(() => {
  return sanitizeUrl(meetingData.value.eventLinkBackup);
});

const sanitizedBackupLinkText = computed(() => {
  return sanitizeLinkText(meetingData.value.eventLinkBackup);
});

async function initEditor() {
  if (editors.value) {
    editorInstance = await EditorOutput.CustomClassic.create(editors.value, {
      initialData: meetingData.value.description,
      updateSourceElementOnDestroy: false,
      toolbar: {
        items: [],
      },
      licenseKey: ckEditorLicense.value,
    });
    editorInstance.enableReadOnlyMode("readonlyeditor");
  }
}
watch(
  () => meetingData.value.description,
  (val) => {
    if (val) {
      editorInstance.setData(val);
    }
  }
);

onMounted(() => {
  if (editors.value) initEditor();
});
</script>

<style>
.editor-desc__container > .ck .ck-sticky-panel__content {
  display: none;
}
</style>

<style scoped>
.description-detail {
  border-radius: 12px;
  background: var(--White-Colot, #fff);
  box-shadow: 0px 4px 18px 0px rgba(192, 192, 192, 0.25);
  flex-shrink: 0;
}

:deep(.ck.ck-editor__main > .ck-editor__editable:not(.ck-focused)) {
  border: 0 !important;
}

.link-media {
  text-decoration: none;
}

.link-media:visited {
  color: inherit;
}

.link-media:hover {
  text-decoration: underline;
}
</style>
