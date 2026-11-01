<template>
  <v-menu
    transition="slide-y-transition"
    bottom
    :close-on-content-click="false"
    v-model="menu"
  >
    <template v-slot:activator="{ props }">
      <v-btn
        icon=""
        size="small"
        v-bind="props"
        class="ml-2"
        style="position: right; top: 0; margin-right: 8px"
      >
        <img
          :src="require('@/v2/assets/icon/filter.png')"
          :width="21"
          :height="21"
        />
      </v-btn>
    </template>
    <div
      :style="{
        background: 'transparent',
        width: windowWidth / divider,
        marginRight: -15 + 'px',
      }"
    >
      <div class="d-flex flex-row-reverse">
        <div class="triangle"></div>
      </div>
      <v-card
        :style="{
          zIndex: 40,
          borderRadius: 10 + 'px',
          background: 'transparent',
          display: 'flex',
          flexDirection: 'row',
        }"
      >
        <div v-if="keySeeAll" :style="leftFilterSize">
          <div>
            <h2 class="text-filter mt-1">
              {{
                seeAllData.name.charAt(0).toUpperCase() +
                seeAllData.name.slice(1)
              }}
            </h2>
            <div
              class="d-flex flex-column"
              style="margin-top: 4px; color: #4b4b4b"
            >
              <v-checkbox
                v-for="(item, idx) in seeAllData.value"
                :label="item.value"
                :key="idx"
                :color="'#02AA59'"
                hide-details
                :value="item.id"
                v-model="filterForm[seeAllData.name]"
              ></v-checkbox>
            </div>
          </div>
        </div>
        <div :style="mainSize">
          <div>
            <h1 class="text-filter" style="">Filter By</h1>
            <div v-for="(filter, id) in contentFilters" :key="id">
              <h2 class="text-filter mt-1">{{ filter.title }}</h2>
              <div
                class="d-flex flex-column"
                style="margin-top: 4px; color: #4b4b4b"
              >
                <v-checkbox
                  v-for="(item, idx) in checkBoxData(
                    filter.value,
                    checkBoxSeeAll(filter.name)
                  )"
                  :label="item.value"
                  :key="idx"
                  :color="'#02AA59'"
                  hide-details
                  :value="item.id"
                  v-model="filterForm[filter.name]"
                ></v-checkbox>
                <div
                  v-if="checkBoxSeeAll(filter.name)"
                  class="d-flex flex-row align-center"
                >
                  <span
                    class="btnSeeAll"
                    :style="{
                      color: keySeeAll == filter.name ? '#d6212a' : '#065695',
                    }"
                    @click="toggleSeeAll(filter.name)"
                  >
                    See All
                  </span>
                </div>
              </div>
            </div>
            <v-btn
              style="margin-top: 6px"
              class="w-100 blue-gradient"
              @click="commitFilter"
            >
              Apply
            </v-btn>
          </div>

          <paragraph-shimmer
            v-if="isLoading"
            class="pa-5"
            :lines="4"
            :random-size="true"
          />
        </div>
      </v-card>
    </div>
  </v-menu>
</template>

<script setup lang="ts">
import { TContentFilterItem } from "@/v2/Type";
import {
  ref,
  computed,
  onBeforeMount,
  onUnmounted,
  onMounted,
  reactive,
  watch,
} from "vue";
import { useStore } from "vuex";

const emit = defineEmits(["onUpdateFilter"]);
const store = useStore();
const menu = ref<boolean>(false);
const isLoading = ref<boolean>(false);
const keySeeAll = ref<string | null>(null);
const divider = computed(() => (keySeeAll.value ? 2 : 4));
const windowWidth = ref<number>(window.innerWidth);
const contentFilters = ref<Array<TContentFilterItem>>([]);
const filterForm = ref({});
const lastAppliedFilterForm = ref({});
const filterColumn = reactive({
  minWidth: windowWidth.value / 4 + "px",
  background: "white",
  padding: 15 + "px",
});

const mainSize = computed((): any => {
  if (windowWidth.value >= 1706) return filterColumn;
  return {
    ...filterColumn,
    height: "400px",
    overflowY: "scroll",
  };
});

const leftFilterSize = computed((): any => {
  if (windowWidth.value >= 1706) {
    return {
      ...filterColumn,
      borderRight: "2px solid #E4E4E4",
      maxHeight: "750px",
      overflowY: "scroll",
    };
  }
  return {
    ...filterColumn,
    borderRight: "2px solid #E4E4E4",
    height: "400px",
    overflowY: "scroll",
  };
});

const seeAllData = computed((): TContentFilterItem => {
  return (
    contentFilters.value.find((item) => item.name === keySeeAll.value) ||
    ({} as TContentFilterItem)
  );
});

function getContentFilter() {
  isLoading.value = true;
  store
    .dispatch("workspaceStore/fetchContentFilter")
    .then((res: any) => {
      contentFilters.value = res.data;
      res.data.map((item: any) => {
        filterForm.value[item.name] = [];
      });

      // apply old filter
      const filter = store.getters["workspaceStore/getContentFilterCommit"];
      if (Object.keys(filter).length !== 0) {
        filterForm.value = filter;
      }

      // Save as last applied state (initial state)
      lastAppliedFilterForm.value = JSON.parse(
        JSON.stringify(filterForm.value)
      );
    })
    .finally(() => {
      isLoading.value = false;
    });
}

function commitFilter() {
  menu.value = false;

  // Save current state as last applied state
  lastAppliedFilterForm.value = JSON.parse(JSON.stringify(filterForm.value));

  emit("onUpdateFilter", filterForm.value);
}

function checkBoxData(datas: Array<any>, showAll: boolean): Array<any> {
  if (showAll) return datas.slice(0, 6);
  return datas;
}

function checkBoxSeeAll(name: string): boolean {
  return ["month", "year"].includes(name);
}

function toggleSeeAll(key: string): void {
  if (keySeeAll.value === key) keySeeAll.value = null;
  else keySeeAll.value = key;
}

function resetToLastAppliedState(): void {
  filterForm.value = JSON.parse(JSON.stringify(lastAppliedFilterForm.value));
  keySeeAll.value = null;
}

function handleResize() {
  windowWidth.value = window.innerWidth;
}

onBeforeMount(() => {
  window.addEventListener("resize", handleResize);
});

onUnmounted(() => {
  window.removeEventListener("resize", handleResize);
});

onMounted(() => {
  getContentFilter();
});

watch(menu, (newVal, oldVal) => {
  if (oldVal === true && newVal === false) {
    // Menu was closed, reset to last applied state
    resetToLastAppliedState();
  }
});
</script>

<style scoped>
.btnSeeAll {
  font-size: 11px;
  font-style: italic;
  font-weight: 400;
  line-height: 16.5px;
  text-align: left;
  color: #d6212a;
  cursor: pointer;
  text-decoration: underline;
}

.text-filter {
  color: #4b4b4b;
  font-size: 13px;
  font-weight: 900;
  line-height: 22.5px;
  font-weight: 700;
}

.blue-gradient {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: white !important;
  border-radius: 10px;
}
.triangle {
  width: 0;
  height: 0;
  border: 20px solid transparent;
  border-top: 0;
  border-bottom: 32px solid #fff;
  z-index: 50;
  margin-right: 15px;
}
.btnSeeAll {
  font-size: 11px;
  font-style: italic;
  font-weight: 400;
  line-height: 16.5px;
  text-align: left;
  cursor: pointer;
  text-decoration: underline;
}
.blue-gradient {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: white !important;
  border-radius: 10px;
}

:deep(.v-selection-control--density-default) {
  --v-selection-control-size: 25px;
}
:deep(.v-checkbox .v-selection-control) {
  min-height: 0;
}
:deep(.v-label) {
  font-size: 13px;
  font-weight: 900;
}
</style>
