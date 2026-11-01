<template>
  <v-menu
    transition="slide-y-transition"
    :location="'bottom end'"
    :close-on-content-click="false"
    v-model="menu"
    :offset="8"
  >
    <template v-slot:activator="{ props }">
      <v-btn
        class="btn-dropdown"
        variant="outlined"
        dark
        v-bind="props"
        style="overflow: hidden"
      >
        <v-icon icon="mdi-tune" color="#065695" />
        <span class="ml-2">Filter</span>
      </v-btn>
    </template>
    <v-card
      min-width="350"
      max-width="400"
      style="border-radius: 10px; max-height: 80vh"
    >
      <paragraph-shimmer
        v-if="isLoading"
        class="pa-5"
        :is-loading="true"
        :lines="4"
        :random-size="true"
      />
      <v-list v-else>
        <v-list-item>
          <p class="filter-header">Filter By</p>

          <div v-if="showFilters">
            <div v-for="(item, i) in list" :key="i" class="filter-section">
              <p class="filter-label">{{ item.title }}</p>
              <div
                v-for="(itemFilter, j) in getDisplayedFilterItems(item)"
                :key="j"
                class="mb-1"
              >
                <v-checkbox
                  color="#05aa59"
                  :label="itemFilter.value"
                  :value="itemFilter.id"
                  v-model="checkedOptions[item.name]"
                  :disabled="
                    itemFilter.isDisable === 1 || itemFilter.isDisable === true
                  "
                  hide-details
                />
              </div>
              <!-- See All Button -->
              <v-btn
                v-if="shouldShowSeeAllButton(item)"
                variant="text"
                class="btn-see-all font-italic text-decoration-underline pa-0"
                color="blue"
                style="font-size: 10px"
                @click="toggleSeeAll(item.name)"
              >
                See All
              </v-btn>

              <!-- See Less Button -->
              <v-btn
                v-if="shouldShowSeeLessButton(item)"
                variant="text"
                class="btn-see-all font-italic text-decoration-underline pa-0"
                color="blue"
                style="font-size: 10px"
                @click="toggleSeeAll(item.name)"
              >
                See Less
              </v-btn>
            </div>

            <!-- Date Range Filter -->
            <div v-if="useDateFilter" class="filter-section">
              <p class="filter-label">Date</p>
              <VueDatePicker
                v-model="datePicker"
                range
                :year-range="[minYear, maxYear]"
                :enable-time-picker="false"
                :month-change-on-scroll="false"
                auto-apply
                model-type="dd/MM/yyyy"
                :alt-position="() => ({ top: -280, left: 0 })"
                style="margin-left: -4px"
              >
                <template #trigger>
                  <v-text-field
                    variant="solo"
                    placeholder="dd/mm/yyyy - dd/mm/yyyy"
                    class="pl-2 pr-2"
                    :value="formattedDateRange"
                    readonly
                  >
                    <template v-slot:append-inner>
                      <v-icon
                        v-if="hasDateRange"
                        class="pr-2 pt-1"
                        @click.stop="clearDateRange"
                      >
                        mdi-close
                      </v-icon>
                      <img :src="require('@/v2/assets/icon/date.svg')" />
                    </template>
                  </v-text-field>
                </template>
                <template #calendar-header="{ index, day }">
                  <div :class="{ 'red-color': isWeekend(index) }">
                    {{ day }}
                  </div>
                </template>
              </VueDatePicker>
            </div>
          </div>

          <div v-if="routeType === 'ongoing'" class="filter-section">
            <p class="filter-label">PIC Approval</p>
            <SearchBar
              :is-admin="true"
              :place-holder-search="'Search PIC Approval here'"
              @selected="handlePICSelected"
            />
            <div v-if="selectedPIC.length > 0" class="d-flex flex-wrap">
              <v-chip
                v-for="item in selectedPIC"
                :key="item.id"
                closable
                @click:close="removePIC(item)"
                class="selected-chip"
              >
                <span class="chip-text">{{ item.value }}</span>
                <template v-slot:close>
                  <v-icon class="chip-close-icon">mdi-close</v-icon>
                </template>
              </v-chip>
            </div>
          </div>

          <div v-if="routeType === 'roleUser'" class="d-flex flex-column">
            <!-- Satker Filter -->
            <div class="filter-section">
              <p class="filter-label">Satker</p>
              <SearchBar
                :is-admin="true"
                access-type="role"
                type="satker"
                :place-holder-search="'Search satker here'"
                @selected="handleSatkerSelected"
              />
              <div v-if="selectedSatker.length > 0" class="d-flex flex-wrap">
                <v-chip
                  v-for="item in selectedSatker"
                  :key="item.id"
                  closable
                  @click:close="removeSatker(item)"
                  class="selected-chip"
                >
                  <span class="chip-text">{{ item.value }}</span>
                  <template v-slot:close>
                    <v-icon class="chip-close-icon">mdi-close</v-icon>
                  </template>
                </v-chip>
              </div>
            </div>

            <!-- Jabatan Filter -->
            <div class="filter-section">
              <p class="filter-label">Jabatan</p>
              <SearchBar
                :is-admin="true"
                access-type="role"
                type="jabatan"
                :place-holder-search="'Search jabatan here'"
                @selected="handleJabatanSelected"
              />
              <div v-if="selectedJabatan.length > 0" class="d-flex flex-wrap">
                <v-chip
                  v-for="item in selectedJabatan"
                  :key="item.id"
                  closable
                  @click:close="removeJabatan(item)"
                  class="selected-chip"
                >
                  <span class="chip-text">{{ item.value }}</span>
                  <template v-slot:close>
                    <v-icon class="chip-close-icon">mdi-close</v-icon>
                  </template>
                </v-chip>
              </div>
            </div>

            <!-- Role Filter -->
            <div class="filter-section">
              <p class="filter-label">Role</p>
              <SearchBar
                :is-admin="true"
                access-type="role"
                type="role"
                :place-holder-search="'Search role here'"
                @selected="handleRoleSelected"
              />
              <div v-if="selectedRole.length > 0" class="d-flex flex-wrap">
                <v-chip
                  v-for="item in selectedRole"
                  :key="item.id"
                  closable
                  @click:close="removeRole(item)"
                  class="selected-chip"
                >
                  <span class="chip-text">{{ item.value }}</span>
                  <template v-slot:close>
                    <v-icon class="chip-close-icon">mdi-close</v-icon>
                  </template>
                </v-chip>
              </div>
            </div>
          </div>
        </v-list-item>
      </v-list>

      <v-card-actions>
        <v-btn block class="blue-gradient" @click="applyFilter">Apply</v-btn>
      </v-card-actions>
    </v-card>
  </v-menu>
</template>
<script lang="ts" setup>
import { ref, onMounted, watch, computed } from "vue";
import {
  TResponseSearchByName,
  FilterGroup,
  FilterConfig,
  FilterItem,
} from "@v2/Type";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import SearchBar from "../collaboration/SearchBar.vue";

const store = useStore();
const route = useRoute();
const emit = defineEmits(["update"]);

const menu = ref<boolean>(false);
const list = ref<FilterGroup[]>([]);
const datePicker = ref<string[]>([]);
const startDate = ref<string>("");
const endDate = ref<string>("");
const isLoading = ref<boolean>(false);
const checkedOptions = ref<Record<string, any[]>>({});
const selectedSatker = ref<TResponseSearchByName[]>([]);
const selectedJabatan = ref<TResponseSearchByName[]>([]);
const selectedRole = ref<TResponseSearchByName[]>([]);
const selectedPIC = ref<TResponseSearchByName[]>([]);
const lastAppliedState = ref({
  checkedOptions: {} as Record<string, any[]>,
  satker: [] as TResponseSearchByName[],
  jabatan: [] as TResponseSearchByName[],
  role: [] as TResponseSearchByName[],
  pic: [] as TResponseSearchByName[],
  datePicker: [] as string[],
});
const expandedSections = ref<Record<string, boolean>>({});

const currentYear = new Date().getFullYear();
const username = ref<string>(store.state.username);

const useDateFilter = computed(() => {
  return FILTER_CONFIG[routeType.value]?.dateFields ?? false;
});
const FILTER_CONFIG: Record<string, FilterConfig> = {
  predefine: {
    keys: ["eventSubTypeListFilter", "sector", "dateSince", "dateTo"],
    defaultChecked: { rdg: [], sector: [] },
    dateFields: true,
  },
  ongoing: {
    keys: [
      "eventSubTypeListFilter",
      "tahapan",
      "status",
      "dateSince",
      "dateTo",
      "picFilter",
    ],
    defaultChecked: { rdg: [], bp: [], status: [] },
    dateFields: true,
  },
  meeting: {
    keys: ["eventSubTypeListFilter", "bp", "dateSince", "dateTo"],
    defaultChecked: { rdgType: [], bp: [] },
    dateFields: true,
  },
  presentationMaterial: {
    keys: ["eventSubTypeListFilter", "bp", "dateSince", "dateTo"],
    defaultChecked: { rdgType: [], bp: [] },
    dateFields: true,
  },
  faq: {
    keys: ["topicFilter", "dateSince", "dateTo"],
    defaultChecked: { topicFilter: [] },
    dateFields: true,
  },
  roleUser: {
    keys: ["satkerFilter", "jabatanFilter", "roleFilter"],
    defaultChecked: {},
    dateFields: false,
  },
  history: {
    keys: ["status", "workspaceType", "monthPeriod", "yearPeriod"],
    defaultChecked: {},
    dateFields: false,
  },
};

const minYear = computed(() => currentYear - 5);
const maxYear = computed(() => currentYear + 100);

const routeType = computed(() => {
  const path = route.path;
  if (path.includes("admin-management/content/predefine")) return "predefine";
  if (path.includes("admin-management/content/ongoing")) return "ongoing";
  if (path.includes("admin-management/meeting/meeting")) return "meeting";
  if (path.includes("admin-management/faq")) return "faq";
  if (path.includes("history")) return "history";
  if (path.includes("admin-management/meeting/presentation-material"))
    return "presentationMaterial";
  if (path.includes("admin-management/role/user")) return "roleUser";
  return "other";
});

const showFilters = computed(() =>
  [
    "predefine",
    "ongoing",
    "meeting",
    "presentationMaterial",
    "faq",
    "history",
  ].includes(routeType.value)
);

const formattedDateRange = computed(() => {
  if (Array.isArray(datePicker.value) && datePicker.value.length === 2) {
    const [start, end] = datePicker.value;
    return `${start} - ${end}`;
  }
  return "";
});

const hasDateRange = computed(
  () => Array.isArray(datePicker.value) && datePicker.value.length > 0
);

const filteredTahapan = computed(() => {
  const validTypes = ["meeting", "presentationMaterial"];

  if (!validTypes.includes(routeType.value)) {
    return [];
  }

  const selectedRdgTypes = checkedOptions.value.rdgType || [];
  const tahapanGroup = list.value.find((group) => group.name === "bp");

  if (!tahapanGroup || !Array.isArray(tahapanGroup.value)) return [];
  if (selectedRdgTypes.length === 0) return tahapanGroup.value;

  return tahapanGroup.value.filter((filter: FilterItem) => {
    if (!filter.idRdgType || !Array.isArray(filter.idRdgType)) return false;
    return selectedRdgTypes.some((id) => filter.idRdgType?.includes(id));
  });
});

const isWeekend = (index: number): boolean => index === 5 || index === 6;

const clearDateRange = (): void => {
  datePicker.value = [];
};

const getFilterItems = (item: FilterGroup): FilterItem[] => {
  return item.name === "bp" ? filteredTahapan.value : item.value;
};

const getDisplayedFilterItems = (item: FilterGroup): FilterItem[] => {
  const allItems = getFilterItems(item);
  const isExpanded = expandedSections.value[item.name];

  if (isExpanded || allItems.length <= 5 || item.name !== "monthPeriod") {
    return allItems;
  }

  return allItems.slice(0, 5);
};

const shouldShowSeeAllButton = (item: FilterGroup): boolean => {
  const allItems = getFilterItems(item);
  return (
    item.name === "monthPeriod" &&
    allItems.length > 5 &&
    !expandedSections.value[item.name]
  );
};

const shouldShowSeeLessButton = (item: FilterGroup): boolean => {
  const allItems = getFilterItems(item);
  return (
    item.name === "monthPeriod" &&
    allItems.length > 5 &&
    expandedSections.value[item.name]
  );
};

const toggleSeeAll = (sectionName: string): void => {
  expandedSections.value[sectionName] = !expandedSections.value[sectionName];
};

const formatIsoToPickerDate = (isoDate: string): string => {
  const date = new Date(isoDate);
  const day = String(date.getDate()).padStart(2, "0");
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const year = date.getFullYear();
  return `${day}/${month}/${year}`;
};

const createFilter = (): Record<string, any> => {
  const config = FILTER_CONFIG[routeType.value];
  if (!config) return {};
  const filter: Record<string, any> = {};

  if (routeType.value === "roleUser") {
    filter["satkerFilter"] = selectedSatker.value.map((item) => item.id);
    filter["jabatanFilter"] = selectedJabatan.value.map((item) => item.id);
    filter["roleFilter"] = selectedRole.value.map((item) => item.id);
  } else {
    config.keys.forEach((key) => {
      if (key === "dateSince" || key === "dateTo") {
        filter[key] = key === "dateSince" ? startDate.value : endDate.value;
      } else if (key === "picFilter" && routeType.value === "ongoing") {
        filter[key] = selectedPIC.value.map((item) => item.value);
      } else {
        const optionKey = getOptionKey(key);
        filter[key] = checkedOptions.value[optionKey] || [];
      }
    });
  }
  return filter;
};

const getOptionKey = (key: string): string => {
  if (key === "eventSubTypeListFilter") {
    if (routeType.value === "predefine" || routeType.value === "ongoing") {
      return "rdg";
    }
    return "rdgType";
  }
  return key;
};

const saveAppliedState = (): void => {
  lastAppliedState.value = {
    checkedOptions: JSON.parse(JSON.stringify(checkedOptions.value)),
    satker: [...selectedSatker.value],
    jabatan: [...selectedJabatan.value],
    role: [...selectedRole.value],
    pic: [...selectedPIC.value],
    datePicker: [...datePicker.value],
  };
};

const resetFilter = (): void => {
  const config = FILTER_CONFIG[routeType.value];
  if (!config) return;
  checkedOptions.value = { ...config.defaultChecked };
  if (config.dateFields) {
    datePicker.value = [];
    startDate.value = "";
    endDate.value = "";
  }
  selectedSatker.value = [];
  selectedJabatan.value = [];
  selectedRole.value = [];
  selectedPIC.value = [];

  lastAppliedState.value = {
    checkedOptions: { ...config.defaultChecked },
    satker: [],
    jabatan: [],
    role: [],
    pic: [],
    datePicker: [],
  };

  menu.value = false;
  emit("update", createFilter());
};

const getFilter = async (): Promise<void> => {
  isLoading.value = true;
  const config = FILTER_CONFIG[routeType.value];

  if (!config) {
    resetFilterData();
    emit("update", {});
    return;
  }

  await loadFilterData();
  initializeCheckedOptions();
  emit("update", createFilter());
  isLoading.value = false;
};

const resetFilterData = (): void => {
  list.value = [];
  checkedOptions.value = {};
  startDate.value = "";
  endDate.value = "";
  datePicker.value = [];
  isLoading.value = false;
};

const loadFilterData = async (): Promise<void> => {
  const actions = {
    predefine: () =>
      store.dispatch("adminStore/getAdminFilter", { username: username.value }),
    ongoing: () =>
      store.dispatch("adminStore/getOnGoingFilter", {
        username: username.value,
      }),
    meeting: () =>
      store.dispatch("adminStore/GetMeetingFilter", {
        username: username.value,
      }),
    faq: () =>
      store.dispatch("adminStore/GetFilterFAQ", {
        username: username.value,
      }),
    presentationMaterial: () =>
      store.dispatch("adminStore/GetPresentationMaterialFilter", {
        username: username.value,
      }),
    role: () => Promise.resolve({ responseData: [] }),
    history: () => store.dispatch("historyStore/GetFilterWorkspaceHistory"),
  };

  const action = actions[routeType.value];

  if (!action) return;

  const response = await action();

  if (["meeting", "presentationMaterial"].includes(routeType.value)) {
    list.value = transformMeetingFilter(response.responseData);
  } else if (routeType.value === "faq") {
    list.value = transformFaqFilter(response.responseData);

    if (response.responseData?.startDate && response.responseData?.endDate) {
      datePicker.value = [
        formatIsoToPickerDate(response.responseData.startDate),
        formatIsoToPickerDate(response.responseData.endDate),
      ];
    }
  } else if (routeType.value !== "roleUser") {
    list.value = response.responseData;
  }
};

const transformFaqFilter = (responseData: any): FilterGroup[] => {
  if (!responseData || !Array.isArray(responseData.value)) return [];

  return [
    {
      title: responseData.title || "Category FAQ",
      name: "topicFilter",
      value: responseData.value.map((topic: any) => ({
        id: topic.topicId,
        value: topic.name,
        isDisable: 0,
        isChecked: topic.isChecked ?? false,
      })),
    },
  ];
};

const transformMeetingFilter = (responseData: any): FilterGroup[] => {
  return Object.entries(responseData).map(([key, group]: [string, any]) => ({
    title: group.name,
    name: key,
    value: group.filters.map((filter: any) => ({
      id: filter.id,
      value: filter.name,
      isDisable: filter.isDisable ?? 0,
      isChecked: filter.isChecked ?? 0,
      idRdgType: filter.idRdgType || [],
    })),
  }));
};

const initializeCheckedOptions = (): void => {
  const options: Record<string, (number | string)[]> = {};

  list.value.forEach((element) => {
    options[element.name] = element.value
      .filter(
        (opt: FilterItem) => opt.isChecked === 1 || opt.isChecked === true
      )
      .map((opt: FilterItem) => opt.id);
  });

  checkedOptions.value = { ...checkedOptions.value, ...options };

  saveAppliedState();
};

const applyFilter = (): void => {
  const filter = createFilter();

  saveAppliedState();

  menu.value = false;
  emit("update", filter);
};

const resetToLastAppliedState = (): void => {
  const s = lastAppliedState.value;
  checkedOptions.value = JSON.parse(JSON.stringify(s.checkedOptions));
  selectedSatker.value = [...s.satker];
  selectedJabatan.value = [...s.jabatan];
  selectedRole.value = [...s.role];
  selectedPIC.value = [...s.pic];
  datePicker.value = [...s.datePicker];
};

const handleSatkerSelected = (item: TResponseSearchByName): void => {
  if (!selectedSatker.value.some((existing) => existing.id === item.id)) {
    selectedSatker.value.push(item);
  }
};

const handleJabatanSelected = (item: TResponseSearchByName): void => {
  if (!selectedJabatan.value.some((existing) => existing.id === item.id)) {
    selectedJabatan.value.push(item);
  }
};

const handleRoleSelected = (item: TResponseSearchByName): void => {
  if (!selectedRole.value.some((existing) => existing.id === item.id)) {
    selectedRole.value.push(item);
  }
};

const handlePICSelected = (item: TResponseSearchByName): void => {
  if (!selectedPIC.value.some((existing) => existing.id === item.id)) {
    selectedPIC.value.push(item);
  }
};

const removeSatker = (item: TResponseSearchByName): void => {
  selectedSatker.value = selectedSatker.value.filter((s) => s.id !== item.id);
};

const removeJabatan = (item: TResponseSearchByName): void => {
  selectedJabatan.value = selectedJabatan.value.filter((s) => s.id !== item.id);
};

const removeRole = (item: TResponseSearchByName): void => {
  selectedRole.value = selectedRole.value.filter((s) => s.id !== item.id);
};

const removePIC = (item: TResponseSearchByName): void => {
  selectedPIC.value = selectedPIC.value.filter((s) => s.id !== item.id);
};

watch(
  () => checkedOptions.value.rdgType,
  () => {
    if (routeType.value === "meeting") {
      const visibleTahapanIds = filteredTahapan.value.map((item) => item.id);
      checkedOptions.value.bp = checkedOptions.value.bp.filter((id) =>
        visibleTahapanIds.includes(id)
      );
    }

    if (routeType.value === "presentationMaterial") {
      const visibleTahapanIds = filteredTahapan.value.map((item) => item.id);
      checkedOptions.value.bp = checkedOptions.value.bp.filter((id) =>
        visibleTahapanIds.includes(id)
      );
    }
  },
  { deep: true }
);

watch(
  () => route.path,
  () => {
    resetFilter();
    getFilter();
    menu.value = false;
    selectedSatker.value = [];
    selectedJabatan.value = [];
    selectedRole.value = [];
    selectedPIC.value = [];
  }
);

watch(menu, (newVal, oldVal) => {
  if (oldVal === true && newVal === false) {
    // Menu was closed, check if it was closed without applying
    // Reset to last applied state
    resetToLastAppliedState();
  }
});

watch(datePicker, () => {
  if (Array.isArray(datePicker.value) && datePicker.value.length === 2) {
    const [start, end] = datePicker.value;
    const startParts = start.split("/");
    const endParts = end.split("/");

    startDate.value = `${startParts[2]}-${startParts[1]}-${startParts[0]}`;
    endDate.value = `${endParts[2]}-${endParts[1]}-${endParts[0]}`;
    return;
  }

  startDate.value = "";
  endDate.value = "";
});

onMounted(() => {
  getFilter();
});
</script>
<style scoped lang="scss">
.btn-dropdown {
  color: #065695;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
}

.filter-card {
  border-radius: 10px;
}

.filter-section {
  margin-bottom: 0px;
}

.filter-header {
  padding-top: 16px;
  margin-bottom: -2px;
  font-weight: 900;
  color: #4b4b4b;
  font-size: 13px;
}

.filter-label {
  margin-top: 10px;
  margin-bottom: 15px;
  font-weight: 900;
  color: #4b4b4b;
  font-size: 13px;
}

.selected-chip {
  margin-right: 8px;
  margin-bottom: 8px;
  color: #6eb3ea;
  border: 1px solid #007bff;
  border-radius: 6px;
  margin-top: 10px;
}

.chip-text {
  color: #065391;
}

.chip-close-icon {
  color: #065391;
}

.blue-gradient {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: white !important;
  border-radius: 10px;
}

.red-color {
  color: red;
}

.v-list-item {
  min-height: 25px !important;
}

:deep(.v-list-item__title) {
  font-size: 13px;
  font-weight: 900;
  color: #4b4b4b;
}

:deep(.v-application) {
  color: #05aa59 !important;
}

:deep(.v-select__selection--comma) {
  font-weight: 900;
  color: #4b4b4b;
}

:deep(.v-label) {
  font-size: 13px;
  font-weight: 900;
  margin-left: 5px;
}

:deep(
    .v-text-field.v-text-field--solo:not(.v-text-field--solo-flat)
      > .v-input__control
      > .v-input__slot
  ) {
  background: #f6f6f6;
  border: 2px solid #e4e4e4;
  border-radius: 10px;
}

:deep(.v-input--density-default) {
  --v-input-control-height: 0px;
}

:deep(.v-input__control) {
  height: fit-content !important;
  min-height: auto !important;
  max-height: none !important;
}

:deep(.v-selection-control--density-default) {
  --v-selection-control-size: auto !important;
  align-items: flex-start !important;
}

.btn-sorting {
  margin-bottom: 30px;
  font-weight: 900;
  border-radius: 10px;
  height: 48px;
  border: 2px solid #e4e4e4;
  margin-right: 5px;
  color: #4b4b4b;
}

.v-btn--is-elevated.v-btn--fab {
  box-shadow: 0 4px 7px rgba(0, 0, 0, 0.1) !important;
}

.label-filter {
  margin-top: 10px;
  margin-bottom: -2px;
  margin-left: 20px;
  font-weight: 900;
  color: #4b4b4b;
  font-size: 13px;
}

.btn-see-all {
  :deep(.v-btn__content) {
    margin-left: -14px !important;
  }
}
</style>
