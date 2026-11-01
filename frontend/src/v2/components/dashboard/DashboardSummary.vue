<template>
  <!-- Custom skeleton matching summary card grid -->
  <v-row v-if="isLoading" align="center">
    <v-col cols="6" sm="3" v-for="x in 4" :key="x">
      <div
        class="skeleton-summary-card"
        :style="{ animationDelay: `${(x - 1) * 0.08}s` }"
      >
        <div class="sk-block sk-summary-title"></div>
        <div class="sk-block sk-summary-value"></div>
      </div>
    </v-col>
  </v-row>
  <v-row v-else align="center" align-content="center">
    <v-col
      cols="6"
      class="text-center mt-2 summary-col"
      v-for="(item, idx) in summaryDatas"
      :key="idx"
      :sm="12 / summaryDatas.length"
      :style="{ animationDelay: `${idx * 0.08}s` }"
    >
      <v-row no-gutters>
        <v-col cols="11">
          <h2 class="text-gradient-blue">{{ item.title.toUpperCase() }}</h2>
          <h1 class="my-3 py-3 text-24 text-gradient-red">
            {{ item.value }}
          </h1>
        </v-col>
        <v-col cols="1" v-if="idx < summaryDatas.length - 1">
          <div class="gradient-vertical-line"></div>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import { TSummaryData } from "@/v2/Type";

const store = useStore();
const route = useRoute();

const isLoading = ref(false);
const summaryDatas = ref<TSummaryData[]>([]);
const defaultSummaryDatas: TSummaryData[] = [];

function setDefaultSummaryDatas(path: string) {
  defaultSummaryDatas.splice(
    0,
    defaultSummaryDatas.length,
    ...(path === "/app/v2/mydashboard/assignment"
      ? [
          { title: "Need Approval", value: "0" },
          { title: "In Progress", value: "0" },
          { title: "Done", value: "0" },
          { title: "Not Started", value: "0" },
        ]
      : [
          { title: "In Progress", value: "0" },
          { title: "Approved", value: "0" },
        ])
  );
}

async function loadData(type: string | any) {
  setDefaultSummaryDatas(route.path);
  isLoading.value = true;
  summaryDatas.value = type ? await fetchData(type) : defaultSummaryDatas;
  isLoading.value = false;
}

async function fetchData(type: string) {
  switch (type) {
    case "dashboard.workspace.v2":
      return await store
        .dispatch("assignmentStore/GetListCounterWorkspace")
        .then((resp) => {
          return resp?.responseData ?? defaultSummaryDatas;
        });
    case "dashboard.assignment.v2.penugasan":
      return await store
        .dispatch("assignmentStore/getCounterAssignmentPenugasan")
        .then((resp) => {
          return resp?.responseData?.data ?? defaultSummaryDatas;
        });
    case "dashboard.assignment.v2.arahan":
      return await store
        .dispatch("assignmentStore/getCounterAssignmentArahan")
        .then((resp) => resp?.responseData?.data ?? defaultSummaryDatas);
    case "dashboard.document.v2.materi":
      return await store
        .dispatch("documentsStore/getCounterMateri")
        .then((resp) => resp?.responseData ?? defaultSummaryDatas);
    case "dashboard.document.v2.hasil":
      return await store
        .dispatch("documentsStore/getCounterHasil")
        .then((resp) => resp?.responseData ?? defaultSummaryDatas);
    default:
      return defaultSummaryDatas;
  }
}

onMounted(() => {
  loadData(route.name);
});

watch(
  () => route.name,
  (newVal) => {
    loadData(newVal);
  }
);
</script>

<style scoped>
.gradient-vertical-line {
  background: linear-gradient(
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
  width: 1px;
  height: 60px;
}

.text-gradient-blue {
  background: -webkit-linear-gradient(#065695, #267dc2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 900;
  font-size: large;
}

.text-gradient-red {
  background: -webkit-linear-gradient(90.85deg, #d6212a 15.38%, #ff000d 81.89%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 900;
  font-size: x-large;
}

/* ── Skeleton summary cards ──────────────────────── */
.skeleton-summary-card {
  background: #fff;
  border-radius: 10px;
  padding: 18px 16px;
  height: 6.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 14px;
  box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.06);
  animation: fadeSlideUp 0.4s ease-out both;
}

.sk-block {
  border-radius: 6px;
  background: #eeeeee;
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

/* mirrors text-gradient-blue title */
.sk-summary-title {
  height: 14px;
  width: 70%;
}

/* mirrors text-gradient-red big value number */
.sk-summary-value {
  height: 28px;
  width: 45%;
  border-radius: 8px;
}
.sk-summary-value::after {
  animation-delay: 0.15s;
}

/* Real summary cols entrance */
.summary-col {
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
    translate: 0 14px;
  }
  to {
    opacity: 1;
    translate: 0 0;
  }
}
</style>
