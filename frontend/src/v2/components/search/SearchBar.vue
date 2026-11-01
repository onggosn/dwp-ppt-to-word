<template>
  <v-sheet class="bg-transparent px-7">
    <v-row>
      <v-col cols="9">
        <v-sheet class="d-flex flex-row align-start bg-transparent">
          <v-btn
            icon="mdi-arrow-left"
            style="
              color: rgba(38, 125, 194, 1);
              box-shadow: 10px 4px 10px rgba(255, 255, 255, 1);
            "
            elevation="0"
            @click="back"
          ></v-btn>
          <div style="margin-left: 30px; padding-top: 12px">
            <p
              style="
                color: rgba(38, 125, 194, 1);
                font-size: 28px;
                font-weight: 600;
                line-height: 23px;
              "
            >
              {{ labelSearch }}
            </p>
            <p style="color: #4b4b4b; margin-top: 16px">
              Search results displayed
              {{ totalDataPerPage }}
              (total relevant results
              {{ totalData }})
            </p>
          </div>
        </v-sheet>
      </v-col>
      <v-col cols="3">
        <v-text-field
          v-model="localKeyword"
          density="compact"
          hide-details="auto"
          clearable
          placeholder="Search"
          variant="solo"
          @keyup.enter="handleSearch"
          @click:clear="handleClear"
          :autofocus="true"
        >
          <template v-slot:prepend-inner>
            <img src="/images/task/searchMagnifier.svg" /></template
        ></v-text-field>
      </v-col>
    </v-row>
  </v-sheet>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";
import { searchLabel } from "@/v2/enum/Search";

const store = useStore();
const route = useRoute();
const emit = defineEmits(["back"]);

const localKeyword = ref("");

const totalData = computed(
  () => store.getters["globalStore/getTotalData"] || 0
);
const totalDataPerPage = computed(
  () => store.getters["globalStore/getTotalDataPerPage"] || 0
);
const labelSearch = computed(() => {
  return searchLabel[route.name as keyof typeof searchLabel] || "List";
});

function handleSearch() {
  store.commit("globalStore/setSearch", localKeyword.value);
}

function handleClear() {
  store.commit("globalStore/setSearch", "");
}

function back() {
  emit("back", route.path);
}

watch(
  () => localKeyword.value,
  (value) => {
    if (value === "" || value === null || value === undefined) {
      handleClear();
    }
  }
);

onMounted(() => {
  localKeyword.value = store.getters["globalStore/getSearch"];
});
</script>

<style scoped>
.empty-illustration {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}
:deep(.v-field) {
  border-radius: 15px;
}
:deep(.v-input--horizontal) {
  display: contents;
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
  border-radius: 10px;
  background: white;
}
:deep(.v-pagination__next) {
  color: #065695;
  border-radius: 10px;
  background: white;
}
:deep(.v-pagination__prev) {
  color: #065695;
  border-radius: 10px;
  background: white;
}
</style>
