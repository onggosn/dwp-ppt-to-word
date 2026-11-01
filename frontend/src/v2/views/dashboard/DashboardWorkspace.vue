<template>
  <!-- Custom skeleton matching expansion panel layout -->
  <template v-if="isLoading">
    <div class="skeleton-list">
      <div
        v-for="i in 6"
        :key="i"
        class="skeleton-panel"
        :style="{ animationDelay: `${(i - 1) * 0.07}s` }"
      >
        <div class="skeleton-panel-body">
          <div class="sk-block sk-name"></div>
          <div class="sk-block sk-chip"></div>
          <div class="sk-block sk-chevron"></div>
        </div>
      </div>
    </div>
  </template>
  <template v-else>
    <div v-if="workspace.list.length === 0">
      <img
        src="/images/assignment/empty-workspace.svg"
        style="display: block; margin: 0 auto; width: 450px; margin-top: 80px"
      />
      <div
        class="text-center text-18 fw-600 text-grayTheme-gradien font-italic mt-4"
      >
        No Data Available...
      </div>
    </div>
    <div v-else>
      <dhs-list-content
        v-for="(item, idx) in workspace.list"
        :is-loading="isLoading"
        :key="idx"
        class="mt-5"
        :item="item"
        :delay="`${idx * 0.07}s`"
      ></dhs-list-content>
      <div class="text-center">
        <v-pagination
          rounded="1"
          elevation="2"
          size="small"
          v-model="workspace.pagination.page"
          :length="workspace.pagination.total"
          :total-visible="workspace.pagination.visible"
          @update:modelValue="fetchWorkspace"
        />
      </div>
    </div>
  </template>
</template>

<script setup lang="ts">
import DhsListContent from "@v2/components/dashboard/DhsListContent.vue";
import dashboardWorkspace from "@/v2/composables/workspaces/useDashboard";

const { isLoading, workspace, fetchWorkspace } = dashboardWorkspace();
</script>

<style scoped>
.label-status {
  margin-right: 20px;
  border-radius: 10px;
  color: white !important;
  letter-spacing: -0.7px;
  font-weight: 900;
  height: 30px;
  font-size: 13px;
}

.btn-warning {
  background: linear-gradient(
    179.16deg,
    #e2650b 0.79%,
    #fe7411 99.34%
  ) !important;
}

.btn-status-default {
  background-color: #ffeeca;
  color: #906e2c;
}

.btn-status-style-21 {
  background-color: #e8f6eb;
  color: #1ca333;
}

.btn-status-style {
  letter-spacing: -0.1px;
  font-weight: 900;
  height: 30px !important;
  font-size: 12px;
  width: 180px;
}

:deep(.tab-header.v-slide-group-item--active) {
  background: none !important;
  color: red !important;
  border: none !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: red !important;
}

:deep(.v-btn.v-tab) {
  font-weight: 600;
  background: -webkit-linear-gradient(#065695, #267dc2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

:deep(.v-pagination__item--is-active) {
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%) !important;
  color: white !important;
  border-radius: 10px;
}

:deep(.v-pagination .v-btn) {
  border-radius: 10px;
  font-size: 15px;
  font-weight: bold;
}

:deep(.v-pagination__item) {
  color: #065695;
}

:deep(.v-pagination__next),
:deep(.v-pagination__prev) {
  color: #065695;
}

/* ── Skeleton panels ────────────────────────────── */
.skeleton-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 8px;
}

.skeleton-panel {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.12);
  padding: 0 16px;
  height: 68px;
  display: flex;
  align-items: center;
  animation: fadeSlideUp 0.4s ease-out both;
}

.skeleton-panel-body {
  display: flex;
  align-items: center;
  width: 100%;
  gap: 12px;
}

/* col-8 workspace name */
.sk-name {
  flex: 1;
  height: 13px;
  border-radius: 6px;
  background: #e8e8e8;
  max-width: 62%;
  position: relative;
  overflow: hidden;
}

/* col-4 status chip */
.sk-chip {
  width: 100px;
  height: 26px;
  border-radius: 999px;
  background: #e8e8e8;
  position: relative;
  overflow: hidden;
}

.sk-chevron {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #e8e8e8;
  position: relative;
  overflow: hidden;
  margin-left: auto;
  flex-shrink: 0;
}

/* Shimmer sweep */
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
.sk-chip::after {
  animation-delay: 0.12s;
}
.sk-chevron::after {
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
    translate: 0 16px;
  }
  to {
    opacity: 1;
    translate: 0 0;
  }
}
</style>
