<template>
  <v-expansion-panels
    v-model="panel"
    :style="{ animationDelay: props.delay }"
    class="meeting-panel"
  >
    <v-expansion-panel :value="item.idMBPDocumentTemplate">
      <v-expansion-panel-title>
        <v-row align="center">
          <v-col cols="4" style="z-index: 999">
            <p class="font-weight-bold ellipsis-1">
              {{ props.item?.bPDocumentName || "-" }}
            </p>
            <v-tooltip activator="parent" location="top left">
              {{ props.item?.bPDocumentName }}
            </v-tooltip>
          </v-col>
          <v-col cols="1" style="padding: 0 !important; display: flex">
            <p class="font-weight-bold text-14" style="color: #4b4b4b">
              {{ item.bPName || "-" }}
            </p>
          </v-col>
          <!-- Belum di provide BE -->
          <v-col cols="2">
            <v-chip :style="getColorChipTypeRdg(item.rDGType) as StyleValue">
              {{ item.rDGType }}
            </v-chip>
          </v-col>
          <v-col
            cols="5"
            style="
              padding: 2px !important;
              display: flex;
              justify-content: start;
            "
          >
            <span class="item-information font-italic"
              >Last modified by: {{ item.lastUpdatedBy || " - " }}
              <span style="font-style: normal">|</span> Date:
              {{ reformatDateEngWithMonthLong(item.lastUpdatedDate, true) }}
              <span style="font-style: normal">|</span> Time:
              {{ reformatTimes(item.lastUpdatedDate) }} WIB</span
            >
          </v-col>
        </v-row>
      </v-expansion-panel-title>
      <v-expansion-panel-text>
        <div v-if="loading" class="skeleton-inner">
          <div
            v-for="i in 3"
            :key="i"
            class="skeleton-inner-row"
            :style="{ animationDelay: `${(i - 1) * 0.08}s` }"
          >
            <div class="sk-block sk-inner-title"></div>
            <div class="sk-block sk-inner-meta"></div>
            <div class="sk-block sk-inner-action"></div>
          </div>
        </div>
        <template v-else>
          <ChildList
            :bp-document-name="props.item?.bPDocumentName"
            :id-mbp-document-template="props.item?.idMBPDocumentTemplate"
            :item="items"
            :perent-item="props.item"
            @on-delete-section="reloadSection"
            @on-delete-content="emit('onDeleteContent')"
          />
        </template>
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script setup lang="ts">
import ChildList from "@/v2/components/admin/children/ChildList.vue";
import { useStore } from "vuex";
import { ref, watch, provide, StyleValue } from "vue";
import {
  reformatTimes,
  reformatDateEngWithMonthLong,
} from "@/v2/helpers/DateHelper";
import { getColorChipTypeRdg } from "@/v2/helpers/color";

const props = defineProps({
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
  delay: {
    type: String,
    default: "0s",
  },
});

const store = useStore();
const items = ref<string[]>([]);
const username = ref<string>(store.state.username);
const loading = ref<boolean>(false);
const panel = ref<number[]>([]);
const emit = defineEmits(["onDeleteContent"]);

watch(panel, (newValue) => {
  if (newValue) getSectionList(newValue);
});

const reloadSection = () => {
  getSectionList(props.item.idMBPDocumentTemplate);
};

function getSectionList(idMBPDocumentTemplate: number | number[]) {
  loading.value = true;
  store
    .dispatch("adminStore/getListSection", {
      idBPDoc: idMBPDocumentTemplate,
      username: username.value,
    })
    .then((res: any) => {
      items.value = res.responseData;
    })
    .finally(() => {
      loading.value = false;
    });
}

// Provide list ke EditAccessSection components via provide/inject pattern
provide("documentList", props.item);
</script>

<style scoped>
:deep(
    .v-expansion-panel-title--active > .v-expansion-panel-title__overlay,
    .v-expansion-panel-title[aria-haspopup="menu"][aria-expanded="true"]
      > .v-expansion-panel-title__overlay
  ) {
  opacity: 0 !important;
}
:deep(.v-expansion-panel) {
  border-radius: 16px;
}
:deep(.v-expansion-panel__shadow) {
  box-shadow: 0px 2px 4px 0px #0000001f !important;
}
.item-information {
  color: #797979e5;
  font-size: 13px;
  line-height: 19.5px;
}
:deep(.v-expansion-panel-title) {
  min-height: 60px;
}

/* Entrance animation */
.meeting-panel {
  animation: fadeSlideUp 0.45s ease-out both;
}

/* ── Inner skeleton rows ──────────────────────────── */
.skeleton-inner {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 16px 20px;
}

.skeleton-inner-row {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #fafafa;
  border-radius: 10px;
  padding: 10px 14px;
  animation: fadeSlideUp 0.35s ease-out both;
}

.sk-block {
  border-radius: 6px;
  background: #e8e8e8;
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
}

.sk-block::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.7) 50%,
    transparent 100%
  );
  background-size: 200% 100%;
  animation: shimmerSweep 1.4s ease-in-out infinite;
}

.sk-inner-title {
  flex: 1;
  height: 12px;
}
.sk-inner-meta {
  flex: 1;
  height: 12px;
  max-width: 45%;
}
.sk-inner-action {
  width: 28px;
  height: 28px;
  border-radius: 50%;
}

.sk-inner-meta::after {
  animation-delay: 0.12s;
}
.sk-inner-action::after {
  animation-delay: 0.24s;
}

@keyframes shimmerSweep {
  from {
    background-position: -200% 0;
  }
  to {
    background-position: 200% 0;
  }
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
</style>
