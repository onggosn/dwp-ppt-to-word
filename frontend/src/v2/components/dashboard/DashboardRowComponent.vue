<template>
  <v-expansion-panels v-model="panel" class="panel-custom">
    <v-expansion-panel
      :value="item.id"
      class="panel-expansion mb-5"
      :key="item.id"
      :style="panelBorderStyle"
    >
      <v-expansion-panel-title
        class="panel-header"
        :class="{ 'primary-gradient': type === 'type-1' }"
      >
        <template v-slot:actions="{ expanded }">
          <v-icon
            size="large"
            :class="iconClass"
            :icon="expanded ? 'mdi-chevron-up' : 'mdi-chevron-down'"
          />
        </template>
        <v-row class="pr-3" align="center" justify="space-between">
          <v-col cols="6">
            <h6 class="fw-600 text-14 my-2 pl-3 ellipsis-3" :style="titleStyle">
              {{ item.assignmentTitle }}
            </h6>
          </v-col>
          <slot name="datetime" />
          <slot name="label">
            <v-btn
              rounded
              class="ml-5 label-status"
              :class="`btn-${statusColor}`"
            >
              {{ item.statusName }}
            </v-btn>
          </slot>
        </v-row>
      </v-expansion-panel-title>
      <v-expansion-panel-text class="panel-content" :style="contentBorderStyle">
        <slot />
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script setup lang="ts">
import { ref, computed, defineProps } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const panel = ref<any[]>([]);

const props = defineProps({
  item: {
    type: Object,
    default: () => ({}),
  },
  type: {
    type: String,
    default: "default",
  },
});

// Computed properties
const statusColor = computed(() => {
  const colorMap = {
    1: "danger",
    2: "warning",
    3: "success",
    8: "warning",
    9: "danger",
    10: "warning",
    11: "success",
    12: "danger",
    13: "danger",
    16: "warning",
    17: "success",
  };
  return colorMap[props.item.status] ?? "danger";
});

const panelBorderStyle = computed(() =>
  props.type === "default"
    ? {
        "border-left": "5px solid rgb(6, 86, 149)",
        "border-bottom-left-radius": "15px",
      }
    : {}
);

const contentBorderStyle = computed(() =>
  props.type !== "default" ? { "border-left": "5px solid rgb(6, 86, 149)" } : {}
);

const titleStyle = computed(() =>
  props.type === "default" ? { color: "#3a416f" } : {}
);

const iconClass = computed(() =>
  props.type === "default"
    ? "border-icon-expansion-default"
    : "border-icon-expansion-n-default"
);

// Initialize panel
panel.value = [route.params.id === "undefined" ? "" : route.params.id];
</script>

<style scoped>
:deep(.v-expansion-panel__shadow) {
  box-shadow: 0px 4px 18px 0px rgba(192, 192, 192, 0.25) !important;
}

.panel-expansion {
  margin-bottom: 20px;
  border-radius: 15px !important;
}

.panel-expansion .panel-header {
  border-radius: 15px;
  background-color: #fff;
}

.panel-expansion .panel-content {
  padding-bottom: 15px;
  border-bottom-left-radius: 15px;
}

.border-icon-expansion-n-default {
  display: inline-block;
  border-radius: 100px;
  background: #fff;
  color: #065695;
  box-shadow: 0 0 0 1px #065695;
}

.label-status {
  margin-right: 20px;
  border-radius: 10px;
  color: white !important;
  letter-spacing: -0.7px;
  font-weight: 900;
  height: 30px !important;
  font-size: 13px;
  width: 130px;
}

.btn-danger {
  background: linear-gradient(180deg, #d6212a 0%, #ff000d 100%) !important;
}

.btn-success {
  background: linear-gradient(180deg, #00783e 0%, #02aa59 100%) !important;
}

.btn-warning {
  background: linear-gradient(
    179.16deg,
    #e2650b 0.79%,
    #fe7411 99.34%
  ) !important;
}

:deep(.v-expansion-panel-title__overlay) {
  background-color: #fff;
  border-bottom: 1px solid !important;
}

:deep(.v-expansion-panel-title__icon) {
  margin-left: 2vh;
  color: #757575;
}

:deep(.v-expansion-panel--active > .v-expansion-panel-title) {
  border-bottom-left-radius: 0px !important;
  border-bottom-right-radius: 0px !important;
}
</style>
