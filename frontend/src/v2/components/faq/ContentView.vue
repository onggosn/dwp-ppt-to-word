<template>
  <v-sheet class="bg-transparent">
    <div class="ml-12">
      <v-breadcrumbs
        :items="[
          {
            title: 'Topics',
            disabled: false,
            to: {
              name: 'v2.help',
            },
          },
          {
            title: `${category} Topics`,
            disabled: true,
          },
        ]"
      >
        <template v-slot:divider>
          <v-icon icon="mdi-chevron-right"></v-icon>
        </template>
      </v-breadcrumbs>
    </div>
    <v-sheet class="ml-12 mr-10 bg-transparent">
      <p class="ml-3 mr-3 mb-5 text-28 font-weight-bold text-blueTheme">
        {{ category }} Topics
      </p>

      <!-- Shimmer skeleton while loading -->
      <template v-if="isLoading">
        <div
          v-for="n in 5"
          :key="`shimmer-faq-${n}`"
          class="shimmer-panel ma-3 mb-5"
        >
          <div class="d-flex align-center justify-space-between pa-5">
            <div
              class="shimmer-box shimmer-title"
              :style="{ width: titleWidths[n - 1] }"
            ></div>
            <div class="shimmer-box shimmer-icon-btn"></div>
          </div>
        </div>
      </template>

      <!-- Actual FAQ items -->
      <template v-else>
        <ContentFAQItem
          v-for="item in questions.filter((t) => t.isActive)"
          :key="item.idQuestion"
          :item="item"
        />
      </template>
    </v-sheet>
  </v-sheet>
</template>

<script lang="ts" setup>
import { useRoute } from "vue-router";
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";
import ContentFAQItem from "./ContentFAQItem.vue";

const store = useStore();
const route = useRoute();
const routeQuery = route.query;
const category = computed(() => routeQuery.category);

// Vary title widths so the skeleton looks natural, not robotic
const titleWidths = ["65%", "80%", "55%", "72%", "60%"];

type TQuestions = {
  idQuestion: number;
  question: string;
  order: number;
  isActive: boolean;
  idAnswerEditor: string;
};

const questions = ref<TQuestions[]>([]);
const isLoading = ref(true);

onMounted(() => {
  store
    .dispatch("userStore/getListQuestions", {
      idTopics: routeQuery.identity,
    })
    .then((res) => {
      if (res.responseCode == "011000") {
        questions.value = res.responseData;
      }
      isLoading.value = false;
    });
});
</script>
<style scoped>
:deep(.v-breadcrumbs-item--link) {
  font-weight: 900;
  color: #065695;
}

:deep(.v-expansion-panel) {
  background-color: #fff;
  border-radius: 25px !important;
  padding: 15px;
  margin-bottom: 10px;
}

:deep(.v-expansion-panels) {
  border-radius: 15px;
}

:deep(.v-expansion-panel:not(:first-child)::after) {
  border-top-style: none;
}

:deep(.v-expansion-panel-title__overlay) {
  background-color: #fff;
}

:deep(.v-expansion-panel__shadow) {
  box-shadow: none;
}

:deep(
    .v-expansion-panels:not(.v-expansion-panels--variant-accordion)
      > :first-child:not(:last-child):not(.v-expansion-panel--active):not(
        .v-expansion-panel--before-active
      )
  ) {
  border-radius: 25px !important;
  margin-bottom: 15px;
}

:deep(
    .v-expansion-panels:not(.v-expansion-panels--variant-accordion)
      > :not(:first-child):not(:last-child):not(.v-expansion-panel--active):not(
        .v-expansion-panel--after-active
      )
  ) {
  border-radius: 25px !important;
}

:deep(
    .v-expansion-panels:not(.v-expansion-panels--variant-accordion)
      > :last-child:not(:first-child):not(.v-expansion-panel--active):not(
        .v-expansion-panel--after-active
      )
  ) {
  border-radius: 25px !important;
}

/* ── Shimmer Loading ── */
@keyframes shimmer {
  0% {
    background-position: -800px 0;
  }
  100% {
    background-position: 800px 0;
  }
}

.shimmer-panel {
  background: #ffffff;
  border-radius: 25px;
  padding: 15px;
  margin-bottom: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}

.shimmer-box {
  border-radius: 6px;
  background: linear-gradient(90deg, #e8e8e8 25%, #f5f5f5 50%, #e8e8e8 75%);
  background-size: 1600px 100%;
  animation: shimmer 1.4s infinite linear;
}

.shimmer-title {
  height: 16px;
}

.shimmer-icon-btn {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  flex-shrink: 0;
}
</style>
