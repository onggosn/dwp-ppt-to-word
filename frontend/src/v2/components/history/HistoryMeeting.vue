<template>
  <div class="activity-task-list my-5 mx-2">
    <!-- Loading Shimmer -->
    <div v-if="loading" class="mb-6">
      <div v-for="n in 3" :key="n" class="shimmer-item mb-4">
        <div class="shimmer-content">
          <v-row>
            <v-col cols="8">
              <div class="shimmer-text-long shimmer"></div>
            </v-col>
            <v-col cols="4">
              <div class="shimmer-chip shimmer"></div>
            </v-col>
          </v-row>
        </div>
      </div>
    </div>

    <!-- Actual Content -->
    <v-expansion-panels
      v-else
      class="mb-6 panel-expansion"
      v-model="panel"
      multiple
    >
      <v-expansion-panel v-for="(item, index) in items" :key="index">
        <v-expansion-panel-title>
          <v-row>
            <v-col cols="5" class="item-label align-center">
              <img
                src="/images/meeting/Detail-Calendar.png"
                style="
                  width: 40px;
                  height: 40px;
                  position: absolute;
                  margin-top: -10px;
                  margin-right: 5px;
                "
              />
              <v-tooltip :text="item.meetingName" location="top">
                <template v-slot:activator="{ props }">
                  <div
                    class="ml-10 text-ellipsis"
                    v-bind="props"
                    style="cursor: pointer"
                  >
                    {{ item.meetingName || "-" }}
                  </div>
                </template>
              </v-tooltip>
            </v-col>
            <v-col cols="2" class="item-information">
              <v-tooltip :text="item.platform" location="top">
                <template v-slot:activator="{ props }">
                  <div
                    class="d-flex align-center text-ellipsis"
                    v-bind="props"
                    style="cursor: pointer; width: 100%"
                  >
                    <v-icon
                      icon="mdi-map-marker"
                      size="16"
                      class="mr-1 flex-shrink-0"
                    ></v-icon>
                    <span class="text-ellipsis">
                      {{ item.platform || "-" }}
                    </span>
                  </div>
                </template>
              </v-tooltip>
            </v-col>

            <v-col cols="3" class="item-information">
              <v-tooltip
                :text="formatTimeEngToMonthInd(item.startDate)"
                location="top"
              >
                <template v-slot:activator="{ props }">
                  <div
                    class="d-flex align-center text-ellipsis"
                    v-bind="props"
                    style="cursor: pointer; width: 100%"
                  >
                    <v-icon
                      icon="mdi-calendar-text-outline"
                      size="16"
                      class="mr-1 flex-shrink-0"
                    ></v-icon>
                    <span class="text-ellipsis">
                      {{ formatTimeEngToMonthInd(item.startDate) || "-" }}
                    </span>
                  </div>
                </template>
              </v-tooltip>
            </v-col>

            <v-col cols="2" class="item-information">
              <v-tooltip :text="formatTimeAMPM(item.startDate)" location="top">
                <template v-slot:activator="{ props }">
                  <div
                    class="d-flex align-center text-ellipsis"
                    v-bind="props"
                    style="cursor: pointer; width: 100%"
                  >
                    <v-icon
                      icon="mdi-clock-outline"
                      size="16"
                      class="mr-1 flex-shrink-0"
                    ></v-icon>
                    <span class="text-ellipsis">
                      {{ formatTimeAMPM(item.startDate) || "-" }}
                    </span>
                  </div>
                </template>
              </v-tooltip>
            </v-col>
          </v-row>
        </v-expansion-panel-title>
        <div
          :id="`editor-container-${index}`"
          class="mx-4"
          style="display: none"
        >
          <v-divider></v-divider>
          <div class="item-content-label my-2 mx-2">Deskripsi</div>
          <div :ref="`editors${index}`" :id="`editors${index}`" />
        </div>

        <v-expansion-panel-text>
          <div>
            <!-- <v-divider></v-divider> -->

            <!-- <div class="info my-4">
              <div class="item-content-label">Deskripsi</div>
              <div v-bind="props" style="cursor: pointer">
                <p
                  v-html="item.description || '-'"
                  class="item-content-information"
                ></p>
              </div>
            </div> -->
          </div>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

    <!-- Empty State -->
    <div
      v-if="!loading && items.length === 0"
      class="empty-state text-center py-8"
    >
      <v-icon
        icon="mdi-clipboard-text-off"
        size="64"
        color="grey-lighten-1"
      ></v-icon>
      <div class="empty-text mt-4">No Meetings found</div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import { useStore } from "vuex";
import {
  formatTimeEngToMonthInd,
  formatTimeAMPM,
} from "@v2/helpers/DateHelper";
import EditorOutput from "@/v2/components/side-project/ckeditor/build/ckeditor";
import { useInitializeConfig } from "@/v2/composables/useInitializeConfig";

interface MeetingItem {
  meetingName: string;
  platform: string;
  startDate: string;
  description: string;
}

const store = useStore();
const { ckEditorLicense } = useInitializeConfig();
const panel = ref<number[]>([]);
const items = ref<MeetingItem[]>([]);
const loading = ref(false);
const props = defineProps<{ id: string }>();
const payload = { workspaceId: props.id };

// Track editor instances to prevent recreation
const editorInstances = ref<Record<number, any>>({});

const fetchList = async () => {
  loading.value = true;
  try {
    const response = await store.dispatch(
      "historyStore/getHistoryMeetingList",
      payload
    );

    if (response.responseCode === "011000") {
      items.value = response.responseData;
    }
  } finally {
    loading.value = false;
  }
};

// Watch for expansion panel changes
watch(
  panel,
  (newPanels, oldPanels) => {
    // Find newly opened panels
    const newlyOpened = newPanels.filter(
      (index) => !oldPanels?.includes(index)
    );

    // Find newly closed panels
    const newlyClosed =
      oldPanels?.filter((index) => !newPanels.includes(index)) || [];

    // Handle newly opened panels
    newlyOpened.forEach(async (panelIndex) => {
      const expandedItem = items.value[panelIndex];
      if (expandedItem) {
        // Check if editor already exists for this panel
        if (!editorInstances.value[panelIndex]) {
          const editorContainer = document.getElementById(
            `editors${panelIndex}`
          );

          if (editorContainer) {
            try {
              const editorInstance = await EditorOutput.CustomClassic.create(
                editorContainer,
                {
                  initialData: expandedItem.description || "-",
                  updateSourceElementOnDestroy: false,
                  toolbar: {
                    items: [],
                  },
                  licenseKey: ckEditorLicense.value,
                }
              );

              // Store the editor instance
              editorInstances.value[panelIndex] = editorInstance;
              editorInstance.enableReadOnlyMode("readonlyeditor");
              // Make sure the editor container is visible
              editorContainer.style.display = "block";

              // Show the editor container div when panel is opened
              const editorContainerDiv = document.getElementById(
                `editor-container-${panelIndex}`
              );
              if (editorContainerDiv) {
                editorContainerDiv.style.display = "block";
              }
            } catch (error) {
              // Failed to create editor - silent fail
            }
          }
        } else {
          // Show the editor container if it was previously hidden
          const editorContainer = document.getElementById(
            `editors${panelIndex}`
          );
          if (editorContainer) {
            editorContainer.style.display = "block";

            const editorContainerDiv = document.getElementById(
              `editor-container-${panelIndex}`
            );
            if (editorContainerDiv) {
              editorContainerDiv.style.display = "block";
            }
          }
        }
      }
    });

    // Handle newly closed panels
    newlyClosed.forEach((panelIndex) => {
      const closedItem = items.value[panelIndex];
      if (closedItem) {
        // Hide the editor container when panel is closed
        const editorContainer = document.getElementById(
          `editor-container-${panelIndex}`
        );
        if (editorContainer) {
          editorContainer.style.display = "none";
        }
      }
    });
  },
  { deep: true }
);

// Cleanup function to destroy all editors
const destroyEditors = () => {
  Object.keys(editorInstances.value).forEach((key) => {
    const editor = editorInstances.value[Number(key)];
    if (editor && typeof editor.destroy === "function") {
      editor.destroy();
    }
  });
  editorInstances.value = {};
};

onMounted(() => {
  fetchList();
});

onUnmounted(() => {
  destroyEditors();
});
</script>

<style scoped>
.line-dashed {
  width: 100%;
  height: 1px;
  border-top: 1.5px dashed #065695;
  background-color: transparent;
}

/* .line {
  width: 100%;
  height: 1px;
  border-top: 1px dashed ;
  background-color: transparent;
} */

.item-content-information {
  color: #4b4b4b;
  font-size: 13px;
  line-height: 19.5px;
}

.item-content-label {
  color: #a6abc7;
  font-size: 13px;
  line-height: 19.5px;
  font-weight: 500;
}

.item-information {
  color: #3a416f;
  font-size: 14px;
  line-height: 19.5px;
}

.text-ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.item-label {
  color: #4b4b4b;
  font-size: 15px;
  line-height: 19.5px;
  font-weight: 800;
}

.comment-item {
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #065695;
}

.comment-header {
  margin-bottom: 8px;
}

.comment-author {
  font-weight: 600;
  color: #4b4b4b;
  font-size: 13px;
}

.comment-date {
  color: #a6abc7;
  font-size: 12px;
}

.comment-text {
  color: #4b4b4b;
  font-size: 13px;
  line-height: 18px;
}

.empty-state {
  color: #a6abc7;
}

.empty-text {
  font-size: 16px;
  color: #797979e5;
}

/* Shimmer Loading Styles */
.shimmer-item {
  background: white;
  border-radius: 10px;
  box-shadow: 0px 2px 4px 0px #0000001f;
  padding: 16px;
  min-height: 60px;
}

.shimmer-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.shimmer {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 4px;
}

.shimmer-text-long {
  height: 20px;
  flex: 1;
  max-width: 300px;
}

.shimmer-chip {
  height: 24px;
  width: 60px;
  border-radius: 12px;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* Expansion Panel Styles */
:deep(
    .v-expansion-panel-title--active > .v-expansion-panel-title__overlay,
    .v-expansion-panel-title[aria-haspopup="menu"][aria-expanded="true"]
      > .v-expansion-panel-title__overlay
  ) {
  opacity: 0 !important;
}

:deep(.v-expansion-panel) {
  border-radius: 10px !important;
  margin-bottom: 10px;
  transition: all 0.3s ease;
}

:deep(.v-expansion-panel:hover) {
  transform: translateY(-2px);
  box-shadow: 0px 4px 12px 0px rgba(0, 0, 0, 0.15) !important;
}

:deep(.v-expansion-panel__shadow) {
  box-shadow: 0px 2px 4px 0px #0000001f !important;
}

:deep(.v-expansion-panel-title) {
  min-height: 60px;
}

:deep(.v-expansion-panel-title__icon) {
  border: 1px solid #065695 !important;
  border-radius: 10px !important;
  padding: 4px !important;
  background-color: white !important;
  color: #065695 !important;
}

:deep(.v-expansion-panel .v-expansion-panel--after-active) {
  border-radius: 10px !important;
}

:deep(
    .v-expansion-panels:not(.v-expansion-panels--variant-accordion)
      > :not(:first-child):not(:last-child):not(.v-expansion-panel--active):not(
        .v-expansion-panel--after-active
      )
  ) {
  border-radius: 10px !important;
}

:deep(.v-expansion-panel:not(:first-child)::after) {
  display: none;
}

:deep(
    .v-expansion-panels:not(.v-expansion-panels--variant-accordion)
      > :last-child:not(:first-child):not(.v-expansion-panel--active):not(
        .v-expansion-panel--after-active
      )
  ) {
  border-radius: 10px !important;
}

:deep(
    .v-expansion-panels:not(.v-expansion-panels--variant-accordion)
      > :first-child:not(:last-child):not(.v-expansion-panel--active):not(
        .v-expansion-panel--before-active
      )
  ) {
  border-radius: 10px !important;
}

/* Remove CKEditor borders */
:deep(.ck.ck-editor__main > .ck-editor__editable:not(.ck-focused)) {
  border-color: transparent !important;
  border: none !important;
}

:deep(.ck.ck-editor__main > .ck-editor__editable) {
  border: none !important;
}

/* Hide CKEditor top panel */
:deep(.ck.ck-editor__top .ck-sticky-panel .ck-sticky-panel__content) {
  display: none !important;
}
</style>
