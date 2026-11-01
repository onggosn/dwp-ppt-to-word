<template>
  <div class="list my-5">
    <!-- Loading Shimmer -->
    <div v-if="loading" class="mb-6">
      <div
        v-for="n in 3"
        :key="n"
        class="shimmer-item mb-4"
        :style="{ animationDelay: `${(n - 1) * 0.08}s` }"
      >
        <div class="shimmer-content">
          <v-row>
            <v-col cols="6">
              <div class="shimmer-text-long shimmer"></div>
            </v-col>
            <v-col cols="3">
              <div class="shimmer-chip shimmer"></div>
            </v-col>
            <v-col cols="3">
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
      <v-expansion-panel
        v-for="(item, idx) in list"
        :key="item.id"
        class="panel-item"
        :style="{ animationDelay: `${idx * 0.07}s` }"
      >
        <v-expansion-panel-title>
          <v-row>
            <v-col cols="6" class="item-label d-flex align-center">
              {{ item.workspaceName }}
            </v-col>
            <v-col cols="3" class="item-information chip-container">
              <v-chip
                :style="
                  getColorChipTypeRdgHistory(
                    getWorkspaceGroupAbbreviation(item.workspaceGroupName)
                  )
                "
              >
                {{ getWorkspaceGroupAbbreviation(item.workspaceGroupName) }}
              </v-chip>
            </v-col>
            <v-col cols="3" class="item-information chip-container">
              <v-chip
                class="uniform-chip"
                :style="getColorChipStyle(item.status.toString())"
              >
                {{ item.status }}
              </v-chip>
            </v-col>
          </v-row>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <div>
            <div class="line" />

            <div class="info my-4">
              <div class="item-content-label">Workspace type</div>
              <div class="item-content-information mt-2">
                {{ item.workspaceType }}
              </div>

              <div class="item-content-label mt-2">Description</div>
              <div class="item-content-information mt-2">
                {{ item.description || "No description available" }}
              </div>

              <div class="item-content-label mt-2">Due Date</div>
              <div class="item-content-information mt-2">
                {{ formatDateRange(item.startDate, item.endDate) }}
              </div>
            </div>

            <div class="line-dashed" />

            <HistoryTabs :id="item.id" />
          </div>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import {
  getColorChipStyle,
  getColorChipTypeRdgHistory,
} from "@/v2/helpers/color";

import HistoryTabs from "@/v2/components/history/HistoryTabsComponent.vue";

interface WorkspaceItem {
  id: string;
  workspaceName: string;
  workspaceGroupName: string;
  status: number;
  workspaceType: string;
  description: string;
  startDate: string;
  endDate: string;
}

interface Props {
  list: WorkspaceItem[];
  loading?: boolean;
}

defineProps<Props>();
const panel = ref<number[]>([]);

const getWorkspaceGroupAbbreviation = (workspaceGroupName: string): string => {
  // Extract text between parentheses
  const match = workspaceGroupName.match(/\(([^)]+)\)/);
  if (match) {
    return match[1]; // Returns RDGB or RDGM
  }

  // Fallback: if no parentheses found, try to extract from the full name
  if (workspaceGroupName.includes("RDG Bulanan")) {
    return "RDGB";
  } else if (workspaceGroupName.includes("RDG Mingguan")) {
    return "RDGM";
  } else {
    return "RDGM";
  }

  // Return original if no pattern matches
  // return workspaceGroupName;
};

const formatDateRange = (startDate: string, endDate: string): string => {
  try {
    const start = new Date(startDate);
    const end = new Date(endDate);

    const formatDate = (date: Date): string => {
      const weekday = date.toLocaleDateString("en-US", { weekday: "short" });
      const day = date.getDate().toString().padStart(2, "0");
      const month = (date.getMonth() + 1).toString().padStart(2, "0");
      const year = date.getFullYear();

      return `${weekday} ${day}/${month}/${year}`;
    };

    const startFormatted = formatDate(start);
    const endFormatted = formatDate(end);

    return `${startFormatted} - ${endFormatted}`;
  } catch (error) {
    return "Invalid date range";
  }
};
</script>

<style scoped>
.line-dashed {
  width: 100%;
  height: 1px;
  border-top: 1.5px dashed #267dc2;
  background-color: transparent;
}

.line {
  width: 100%;
  height: 1px;
  background-color: #eeeeee;
}

.item-content-information {
  color: #4b4b4b;
  font-size: 13px;
  line-height: 19.5px;
}

.item-content-label {
  color: #a6abc7;
  font-size: 13px;
  line-height: 19.5px;
}

.workspace-type-chip {
  font-size: 12px !important;
  font-weight: 500 !important;
  height: 24px !important;
}

/* Chip container for centering */
.chip-container {
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
}

/* Uniform chip styling */
.uniform-chip {
  min-width: 100px !important;
  width: 80px !important;
  min-height: 28px !important;
  justify-content: center !important;
  font-size: 0.875rem !important;
  font-weight: 400 !important;
  text-align: center !important;
  padding: 0 11px !important;
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

/* Entrance animations */
.shimmer-item {
  animation: fadeSlideUp 0.4s ease-out both;
}

.panel-item {
  animation: fadeSlideUp 0.45s ease-out both;
}

@keyframes fadeSlideUp {
  from {
    opacity: 0;
    translate: 0 14px;
  }
  to {
    opacity: 1;
    translate: 0 0;
  }
}

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
}
:deep(.v-expansion-panel__shadow) {
  box-shadow: 0px 2px 4px 0px #0000001f !important;
}
.item-information {
  color: #797979e5;
  font-size: 14px;
  line-height: 19.5px;
}

.item-label {
  color: #4b4b4b;
  font-size: 15px;
  line-height: 19.5px;
  font-weight: 800;
}

:deep(.v-expansion-panel-title) {
  min-height: 60px;
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
</style>
