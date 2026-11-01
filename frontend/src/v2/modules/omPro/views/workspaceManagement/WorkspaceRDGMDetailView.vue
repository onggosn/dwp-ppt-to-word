<script setup lang="ts">
import { ref, onBeforeMount } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter, onBeforeRouteLeave } from "vue-router";

import RdgmAnalysisPersentase from "../../components/workspace/RDGMAnalysisPersentase.vue";
import BusinessStage from "@omPro/components/workspace/BusinessStage.vue";
import SectionNote from "@omPro/components/workspace/SectionNote.vue";
import LoadingSpinner from "@/components/loading/LoadingSpinner.vue";
import BusinessStageSection from "@omPro/components/workspace/BusinessStageSection.vue";
import BusinessStageItem from "@omPro/components/workspace/BusinessStageItem.vue";

import { TDetailRDGItem, TSectionSummary } from "@/v2/modules/omPro/Type";

const route = useRoute();
const router = useRouter();
const store = useStore();

/* Loading states for each function */
const isLoadingAnalysis = ref<boolean>(false);
const isLoadingAssesment = ref<boolean>(false);
const isLoadingRekomendasi = ref<boolean>(false);
const isLoadingPersetujuan = ref<boolean>(false);
const isLoadingOthers = ref<boolean>(false);

const idEvent = route.params.idEvent as string;

const summaryDataSection = ref<TSectionSummary>({
  chartpack: 0,
  aiu: null,
  policyNote: null,
  issueNote: null,
  publikasi: null,
  assignment: null,
  isvisible: true,
});

/* Business Process Stages */
const asesmenRekomendasi = ref<number>(0);
const persetujuan = ref<number>(0);
const total = ref<number>(0);
const asesmenRekomendasiList = ref<Array<TDetailRDGItem>>([]);
const persetujuanList = ref<Array<TDetailRDGItem>>([]);
const title = ref<string>("");
const dummyItem = {
  stages: "",
  bp: "",
  idBp: "",
  idBpDocument: "",
  bpStatus: "",
  bpValue: 0,
  bpLink: "",
  isAllowNext: false,
};

async function fetchAnalysisData() {
  isLoadingAnalysis.value = true;
  try {
    const analysis = await store.dispatch(
      "omContentStore/getDataByEventIdAnalysisRDGM",
      idEvent
    );
    title.value = analysis.eventName;
    store.commit("collaborationStore/setEventName", analysis.eventName);
    return analysis;
  } finally {
    isLoadingAnalysis.value = false;
  }
}

async function fetchAssesmentRecomendationData() {
  isLoadingAssesment.value = true;
  try {
    const asesmenRekomedasiData = await store.dispatch(
      "omContentStore/getDataByEventIdBPAssesmentRekomendasi",
      idEvent
    );
    asesmenRekomendasiList.value = asesmenRekomedasiData;
    return asesmenRekomedasiData;
  } finally {
    isLoadingAssesment.value = false;
  }
}

async function fetchPersetujuanData() {
  isLoadingPersetujuan.value = true;
  try {
    const persetujuanData = await store.dispatch(
      "omContentStore/getDataByEventIdBPPersetujuan",
      idEvent
    );
    persetujuanList.value = persetujuanData;
    return persetujuanData;
  } finally {
    isLoadingPersetujuan.value = false;
  }
}

async function fetchOthersData() {
  isLoadingOthers.value = true;
  try {
    const others = await store.dispatch(
      "omContentStore/getDataByEventIdBPOthers",
      idEvent
    );
    summaryDataSection.value = {
      chartpack: others.chartpack ?? {},
      aiu: others.aiu ?? {},
      policyNote: others.policyNote ?? {},
      issueNote: others.issueNote ?? {},
      publikasi: others.publikasi ?? {},
      assignment: others.assignment ?? {},
    };
    return others;
  } finally {
    isLoadingOthers.value = false;
  }
}

function mapSummaryData(analysis) {
  analysis.summary.forEach((item) => {
    if (item.title === "Asesmen & Rekomendasi") {
      asesmenRekomendasi.value = item.value;
    } else if (item.title === "Persetujuan") {
      persetujuan.value = item.value;
    } else if (item.title === "Total") {
      total.value = item.value;
    }
  });
}

async function fetchDataSummary() {
  try {
    const [analysis] = await Promise.all([
      fetchAnalysisData(),
      fetchAssesmentRecomendationData(),
      fetchPersetujuanData(),
      fetchOthersData(),
    ]);

    mapSummaryData(analysis);
  } catch (error) {
    undefined;
  }
}

function handleLoading() {
  if (
    isLoadingAnalysis.value ||
    isLoadingPersetujuan.value ||
    isLoadingRekomendasi.value ||
    isLoadingAssesment.value
  ) {
    return true;
  } else {
    return false;
  }
}

function back() {
  router.push({ name: "om.workspace-management-rdgm" });
}

// set overlay
const loader = ref(false);
onBeforeRouteLeave(() => {
  loader.value = true;
});

onBeforeMount(() => {
  fetchDataSummary();
  handleLoading();
});
</script>

<template>
  <v-sheet class="ml-5 px-10 mt-6 pb-10 bg-transparent">
    <div class="d-flex flex-row align-content-center">
      <v-btn icon size="small" @click="back">
        <img
          :src="require('@/v2/assets/icon/back-arrow.svg')"
          :width="24"
          :height="25"
        />
      </v-btn>
      <span class="text-detail">{{ title }}</span>
    </div>
    <hr
      style="
        opacity: 0.1;
        color: #000;
        margin-top: 17px;
        height: 2px;
        width: 100%;
      "
    />

    <v-sheet class="d-flex flex-row mt-8 bg-transparent justify-space-between">
      <v-sheet class="bg-transparent child">
        <rdgm-analysis-persentase
          :is-loading="handleLoading()"
          :asesmenRekomendasi="asesmenRekomendasi"
          :persetujuan="persetujuan"
          :total="total"
        />
        <section-note
          :is-loading="isLoadingOthers"
          :item-section="summaryDataSection"
          :title="title"
        />
      </v-sheet>

      <v-sheet class="bg-transparent child">
        <business-stage>
          <template
            #asesmenRekomendasi
            v-if="asesmenRekomendasiList.length > 0 || isLoadingAssesment"
          >
            <business-stage-section title="Asesmen & Rekomendasi">
              <business-stage-item
                v-for="(item, idx) in isLoadingAssesment
                  ? Array(3).fill(dummyItem)
                  : asesmenRekomendasiList"
                :key="idx"
                :item="item"
                :is-loading="isLoadingAssesment"
                :stage="'Asesmen & Rekomendasi'"
              />
            </business-stage-section>
          </template>

          <template #persetujuan>
            <business-stage-section title="Persetujuan">
              <business-stage-item
                v-for="(item, idx) in isLoadingPersetujuan
                  ? Array(3).fill(dummyItem)
                  : persetujuanList"
                :key="idx"
                :item="item"
                :is-loading="isLoadingPersetujuan"
                :stage="'Persetujuan'"
              />
            </business-stage-section>
          </template>
        </business-stage>
      </v-sheet>
    </v-sheet>
  </v-sheet>

  <loading-spinner v-if="loader" />
</template>

<style lang="scss" scoped>
.child {
  flex: 1;
  max-width: calc(50% - 12px);
}
.text-detail {
  font-family: Poppins;
  font-style: normal;
  line-height: 40px;
  letter-spacing: 0.5px;
  background: #100f0f;
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-left: 24px;
  font-size: 26px;
  font-weight: 600;
  text-align: left;
}
</style>
