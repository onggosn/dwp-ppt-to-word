<template>
  <v-expansion-panels
    v-model="panel"
    :style="{ animationDelay: props.delay }"
    class="meeting-panel"
  >
    <v-expansion-panel :value="item.workspaceID">
      <v-expansion-panel-title>
        <v-row align="center">
          <v-col cols="7">
            <p class="font-weight-bold ellipsis-1">
              {{ item.workspaceName || "-" }}
            </p>
          </v-col>
          <v-col cols="5">
            <v-chip :style="getColorChipStyle(item.workspaceStatus)">
              {{ item.workspaceStatus }}
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
            <div class="sk-block sk-title"></div>
            <div class="sk-block sk-chip"></div>
            <div class="sk-block sk-action"></div>
          </div>
        </div>
        <template v-else>
          <div v-for="list in items" :key="list.bpID">
            <SubsectionOngoing :item="list" />
          </div>
        </template>
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script setup lang="ts">
import SubsectionOngoing from "@/v2/components/admin/meeting/SubsectionOngoing.vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import { computed, ref, watch } from "vue";
import { getColorChipStyle } from "@/v2/helpers/color";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
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
const route = useRoute();
const items = ref<any[]>([]);
const loading = ref<boolean>(false);
const panel = ref<number[]>([]);

const searchMode = computed(() => store.getters["globalStore/getStatusSearch"]);
const searchValue = computed(() => store.getters["globalStore/getSearch"]);
const filterValue = computed(() => store.getters["adminStore/getItemsFilter"]);

watch(panel, (newValue) => {
  if (newValue) getSectionList(newValue);
});

function getSectionList(idMBPDocumentTemplate: number | number[]) {
  loading.value = true;
  let payload = {
    idEvent: idMBPDocumentTemplate,
    eventSearching: searchMode.value ? searchValue.value : "",
    superEvent: true,
    bp: searchMode.value ? [] : filterValue.value.tahapan ?? [],
    status: searchMode.value ? [] : filterValue.value.status ?? [],
    pic: searchMode.value ? [] : filterValue.value.picFilter ?? [],
    dateStart: searchMode.value ? null : filterValue.value.dateSince || null,
    dateEnd: searchMode.value ? null : filterValue.value.dateTo || null,
    eventSort: searchMode.value ? 1 : route.query.eventSort,
  };

  store
    .dispatch("adminStore/getListSubSectionOg", payload)
    .then((res: any) => {
      items.value = res.responseData;
    })
    .finally(() => {
      loading.value = false;
    });
}
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

.sk-title {
  flex: 1;
  height: 12px;
}
.sk-chip {
  width: 90px;
  height: 24px;
  border-radius: 999px;
}
.sk-action {
  width: 28px;
  height: 28px;
  border-radius: 50%;
}

.sk-chip::after {
  animation-delay: 0.12s;
}
.sk-action::after {
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
