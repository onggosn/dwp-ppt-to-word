<template>
  <v-menu
    transition="slide-y-transition"
    bottom
    :close-on-content-click="false"
    v-model="menu"
  >
    <template v-slot:activator="{ props }">
      <v-btn icon size="small" v-bind="props">
        <v-tooltip activator="parent" location="top">Filter</v-tooltip>
        <v-icon icon="mdi-tune" color="#065695"></v-icon>
      </v-btn>
    </template>
    <v-card min-width="300" style="border-radius: 10px">
      <paragraph-shimmer
        v-if="isLoading"
        class="pa-5"
        :is-loading="true"
        :lines="4"
        :random-size="true"
      />
      <v-list v-else>
        <v-list-item>
          <p
            class="pt-4"
            style="
              margin-bottom: -2px;
              font-weight: 900;
              color: #4b4b4b;
              font-size: 13px;
            "
          >
            Filter By
          </p>
          <div v-for="(item, i) in list" :key="i">
            <p
              style="
                margin-top: 10px;
                margin-bottom: 15px;
                font-weight: 900;
                color: #4b4b4b;
                font-size: 13px;
              "
            >
              {{ item.title }}
            </p>

            <div v-for="(itemFilter, j) in item.value" :key="j">
              <v-checkbox
                color="#05aa59"
                :label="itemFilter.value"
                :value="itemFilter.id"
                v-model="checkedOptions[item.name]"
                hide-details
              ></v-checkbox>
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
import { ref, onMounted, defineEmits, watch } from "vue";
import { useStore } from "vuex";

onMounted(() => {
  getFilter();
});

const store = useStore();
const list = ref<any>([]);
const isLoading = ref<boolean>(false);
const checkedOptions = ref<any>({});
const lastAppliedCheckedOptions = ref<any>({});
const menu = ref<any>(null);
const emit = defineEmits(["onFilterMeeting"]);
function getFilter() {
  isLoading.value = true;
  store
    .dispatch("meetingStore/getMeetingFilter")
    .then((resp) => {
      list.value = resp.responseData.data;
      const options = {};
      resp.responseData.data.forEach((element: any) => {
        options[element.name] = [];
      });
      checkedOptions.value = options;

      // Save as last applied state (initial state)
      lastAppliedCheckedOptions.value = JSON.parse(
        JSON.stringify(checkedOptions.value)
      );
    })
    .finally(() => {
      isLoading.value = false;
    });
}

function resetToLastAppliedState() {
  checkedOptions.value = JSON.parse(
    JSON.stringify(lastAppliedCheckedOptions.value)
  );
}
function applyFilter() {
  /* eslint-disable */
  const filter = {
    eventTypeFilter: checkedOptions.value.et,
    eventSubTypeListFilter: checkedOptions.value.rdg,
    eventAdgFilter: checkedOptions.value.adg,
    komite: checkedOptions.value.kmt,
    eventSearching: "",
  };

  // Save current state as last applied state
  lastAppliedCheckedOptions.value = JSON.parse(
    JSON.stringify(checkedOptions.value)
  );

  menu.value = false;
  emit("onFilterMeeting", filter);
}

watch(menu, (newVal, oldVal) => {
  if (oldVal === true && newVal === false) {
    // Menu was closed, reset to last applied state
    resetToLastAppliedState();
  }
});
</script>
<style scoped>
.btn-icon {
  margin-bottom: 30px;
  font-weight: 900;
  font-size: 13px;
  border-radius: 10px;
  height: 48px !important;
  border: 2px solid;
  border-color: #e4e4e4;
  color: #4b4b4b;
}
.v-list-item {
  min-height: 25px !important;
}
:deep(.v-application) {
  color: #05aa59 !important;
}
:deep(.v-list-item__title) {
  font-size: 13px;
  font-weight: 900;
  color: #4b4b4b;
}

:deep(.v-select__selection--comma) {
  font-weight: 900;
  color: #4b4b4b;
}
:deep(.v-label) {
  font-size: 13px;
  font-weight: 900;
}
:deep(
    .v-text-field.v-text-field--solo:not(.v-text-field--solo-flat)
      > .v-input__control
      > .v-input__slot
  ) {
  background: #f6f6f6;
  border: 2px solid;
  border-color: #e4e4e4;
  border-radius: 10px;
}
.label-filter {
  margin-top: 10px;
  margin-bottom: -2px;
  margin-left: 20px;
  font-weight: 900;
  color: #4b4b4b;
  font-size: 13px;
}
.btn-sorting {
  margin-bottom: 30px;
  font-weight: 900;
  border-radius: 10px;
  height: 48px;
  border: 2px solid;
  border-color: #e4e4e4;
  margin-right: 5px;
  color: #4b4b4b;
}

.v-btn--is-elevated.v-btn--fab {
  box-shadow: 0 4px 7px rgba(0, 0, 0, 0.1) !important;
}
.blue-gradient {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: white !important;
  border-radius: 10px;
}
:deep(.v-input--density-default) {
  --v-input-control-height: 0px;
}

:deep(.v-input__control) {
  margin-top: -13px;
}
</style>
