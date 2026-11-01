<template>
  <v-sheet
    class="item-card"
    :class="{ 'item-card--loaded': !props.isLoading }"
    :style="{ animationDelay: props.delay }"
  >
    <!-- Custom skeleton row -->
    <div v-if="props.isLoading" class="skeleton-row">
      <div class="skeleton-block skeleton-name"></div>
      <div class="skeleton-block skeleton-date"></div>
      <div class="skeleton-block skeleton-chip"></div>
      <div class="skeleton-block skeleton-icon"></div>
    </div>
    <v-row
      v-else
      align="center"
      style="cursor: pointer !important"
      @click="getDetailRdgb(props.item.id)"
    >
      <v-col cols="4" style="padding: 0 !important">
        <p
          class="font-weight-bold"
          style="
            color: #4b4b4b;
            max-height: 24px;
            overflow: hidden;
            padding-right: 32px;
            text-overflow: ellipsis;
            white-space: nowrap;
          "
          v-html="highlightText(props.item.eventName)"
        ></p>
      </v-col>
      <v-col
        cols="4"
        style="padding: 0 !important; display: flex; justify-content: center"
      >
        <p class="font-weight-bold text-14" style="color: #4b4b4b">
          {{ props.item && formatDate(props.item.eventDate) }}
        </p>
      </v-col>
      <v-col
        cols="3"
        style="padding: 2px !important; display: flex; justify-content: center"
      >
        <v-chip
          variant="flat"
          :color="getEventStatusColor(item.eventStatus)?.background"
          :style="[
            'font-weight: 600',
            'color:' + getEventStatusColor(item.eventStatus)?.color + ';',
          ]"
          >{{ props.item && props.item.eventStatus }}</v-chip
        >
      </v-col>
      <v-col
        cols="1"
        style="padding: 0 !important; display: flex; justify-content: end"
      >
        <v-btn icon="mdi-chevron-right" elevation="0"></v-btn>
      </v-col>
    </v-row>
  </v-sheet>
</template>

<script setup lang="ts">
import { formatDate } from "@/v2/helpers/datetime";
import { getEventStatusColor } from "@/v2/helpers/color";
import { useRouter } from "vue-router";

const props = defineProps({
  isLoading: {
    type: Boolean,
    default: false,
  },
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
  query: {
    type: String,
    default: "",
  },
  delay: {
    type: String,
    default: "0s",
  },
  type: {
    type: String,
    default: "rdgb",
  },
});

const router = useRouter();

function highlightText(query: string) {
  const escapedQuery = props.query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return query.replaceAll(
    RegExp("(" + escapedQuery + ")", "ig"),
    `<span class="highlight">$1</span>`
  );
}

function getDetailRdgb(param: any) {
  router.push({
    name: "v2.workspace-rdg-detail",
    params: { typeRDG: props.type, idEvent: param },
    // query: { name: props.item.eventName },
  });
}
</script>

<style scoped>
.item-card {
  padding: 16px 36px;
  border-radius: 12px;
  background-color: rgba(255, 255, 255, 1);
  box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.12);
  transition: transform 0.25s ease, box-shadow 0.25s ease;

  /* Entrance animation */
  animation: fadeSlideUp 0.45s ease-out both;
}

.item-card--loaded {
  cursor: pointer;
}

.item-card--loaded:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.13);
  background-color: rgba(255, 255, 255, 1);
}

/* ── Skeleton row ───────────────────────────── */
.skeleton-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.skeleton-block {
  border-radius: 8px;
  background: #e8e8e8;
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
}

/* Sweep shimmer on every block */
.skeleton-block::after {
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

/* Column widths matching real card cols */
.skeleton-name {
  flex: 1;
  height: 14px;
}
.skeleton-date {
  width: 33%;
  height: 14px;
  animation-delay: 0.1s;
}
.skeleton-chip {
  width: 80px;
  height: 24px;
  border-radius: 20px;
  animation-delay: 0.2s;
}
.skeleton-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  animation-delay: 0.3s;
}

/* Stagger the sweep per block */
.skeleton-date::after {
  animation-delay: 0.1s;
}
.skeleton-chip::after {
  animation-delay: 0.2s;
}
.skeleton-icon::after {
  animation-delay: 0.3s;
}

@keyframes shimmerSweep {
  from {
    background-position: -200% 0;
  }
  to {
    background-position: 200% 0;
  }
}

/* Entrance keyframe — uses `translate` so hover transform is never blocked */
@keyframes fadeSlideUp {
  from {
    opacity: 0;
    translate: 0 16px;
  }
  to {
    opacity: 1;
    translate: 0 0;
  }
}

:deep(.highlight) {
  background: orange;
}
</style>
@/v2/helpers/datetime
