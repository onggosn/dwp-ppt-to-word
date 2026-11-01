<template>
  <v-expansion-panels
    v-model="panel"
    :style="{ animationDelay: props.delay }"
    class="meeting-panel"
  >
    <v-expansion-panel :value="item.idMBPDocumentTemplate">
      <v-expansion-panel-title>
        <v-row align="center">
          <v-col cols="7">
            <p class="font-weight-bold ellipsis-1">
              {{ item.bpName || "-" }}
            </p>
          </v-col>
          <v-col cols="5">
            <v-chip
              v-if="item?.rdgType"
              :style="getColorChipTypeRdg(item.rdgType) as StyleValue"
            >
              {{ item.rdgType }}
            </v-chip>
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
            <div class="sk-block sk-inner-chip"></div>
            <div class="sk-block sk-inner-action"></div>
          </div>
        </div>
        <template v-else>
          <div v-for="meeting in item.meetings" :key="meeting.id">
            <SubsectionMeeting
              :item="meeting"
              :bpId="item.idBP"
              @on-delete-meeting="reloadListEventMeeting"
            />
          </div>
        </template>
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script setup lang="ts">
import { ref, StyleValue } from "vue";
import { getColorChipTypeRdg } from "@/v2/helpers/color";
import SubsectionMeeting from "@/v2/components/admin/meeting/SubsectionMeeting.vue";

const props = defineProps({
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
  itemLength: {
    type: Number,
    default: 0,
  },
  delay: {
    type: String,
    default: "0s",
  },
});

const loading = ref<boolean>(false);
const emit = defineEmits(["onDeleteMeeting"]);
const panel = ref<number[]>([]);

const reloadListEventMeeting = () => {
  emit("onDeleteMeeting");
};
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
:deep(.v-expansion-panel-title) {
  min-height: 60px;
}

/* Entrance animation on the panel card */
.meeting-panel {
  animation: fadeSlideUp 0.45s ease-out both;
}

/* ── Inner skeleton rows ────────────────────────────── */
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
.sk-inner-chip {
  width: 80px;
  height: 22px;
  border-radius: 999px;
}
.sk-inner-action {
  width: 28px;
  height: 28px;
  border-radius: 50%;
}

.sk-inner-chip::after {
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
