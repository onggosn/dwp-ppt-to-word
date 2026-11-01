<template>
  <div>
    <p class="mt-5 text-left text-17 text-darkBlue fw-600">Latest Content</p>

    <!-- Skeleton loading -->
    <v-card
      v-if="isLoading"
      class="border-radius-dwp card-last-content mt-1"
      elevation="4"
    >
      <div
        v-for="i in 5"
        :key="i"
        class="skeleton-item"
        :style="{ animationDelay: `${(i - 1) * 0.08}s` }"
      >
        <!-- icon placeholder -->
        <div class="sk-icon sk-block"></div>
        <!-- text column -->
        <div class="sk-text-col">
          <div class="sk-block sk-bp-name"></div>
          <div class="sk-block sk-doc-name"></div>
          <div class="sk-block sk-date"></div>
        </div>
      </div>
    </v-card>

    <!-- Real content -->
    <v-card
      v-else-if="content?.length"
      class="border-radius-dwp card-last-content mt-1"
      elevation="4"
    >
      <HighlightItem
        v-for="(item, idx) in content"
        :content="item"
        :key="item.idBPDocument"
        class="highlight-item pa-2"
        :style="{ animationDelay: `${idx * 0.07}s` }"
      />
    </v-card>

    <div v-else>
      <img
        :src="require('@/v2/assets/empty/no_available_state.svg')"
        class="img-no-available"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onBeforeMount, ref } from "vue";
import { useStore } from "vuex";
import HighlightItem from "@/v2/components/home/HighlightItem.vue";
import type { TResponseTop10DocByUser } from "@/v2/Type";

const store = useStore();
const content = ref<Array<TResponseTop10DocByUser>>([]);
const isLoading = ref<boolean>(false);

function getListTop10() {
  isLoading.value = true;
  try {
    store
      .dispatch("eventStore/fetchTop10DocByUser")
      .then((res) => {
        content.value = res.data;
      })
      .finally(() => {
        isLoading.value = false;
      });
  } catch (error) {
    isLoading.value = false;
  }
}

onBeforeMount(() => {
  getListTop10();
});
</script>

<style scoped>
.img-no-available {
  margin-top: 10vh;
  width: 100%;
  height: 20vh;
  margin-bottom: 5vh;
}
.card-last-content {
  box-shadow: 0px 4px 18px 0px #c0c0c040;
  background-color: #ffffff;
  max-height: 327px;
  overflow-y: scroll;
}
::-webkit-scrollbar {
  width: 8px;
}

/* ── Skeleton items ───────────────────────────────── */
.skeleton-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 14px 13px 18px;
  border-bottom: 1px solid #f0f0f0;
  animation: fadeSlideUp 0.4s ease-out both;
}

.sk-icon {
  width: 30px;
  height: 39px;
  border-radius: 4px;
  flex-shrink: 0;
}

.sk-text-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.sk-block {
  background: #eeeeee;
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}

.sk-block::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.75) 50%,
    transparent 100%
  );
  background-size: 200% 100%;
  animation: shimmerSweep 1.4s ease-in-out infinite;
}

/* mirrors: bp-name (11px red) | doc-name (14px bold) | date (11px grey) */
.sk-bp-name {
  height: 10px;
  width: 55%;
}
.sk-doc-name {
  height: 14px;
  width: 85%;
}
.sk-date {
  height: 10px;
  width: 40%;
}

.sk-doc-name::after {
  animation-delay: 0.1s;
}
.sk-date::after {
  animation-delay: 0.2s;
}

/* Entrance animation for real items */
.highlight-item {
  animation: fadeSlideUp 0.45s ease-out both;
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
    translate: 0 12px;
  }
  to {
    opacity: 1;
    translate: 0 0;
  }
}
</style>
