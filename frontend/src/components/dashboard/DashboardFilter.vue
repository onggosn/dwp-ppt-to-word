<template>
  <v-menu
    transition="slide-y-transition"
    bottom
    :close-on-content-click="false"
    :max-height="690"
    :width="filterConfig.width"
  >
    <template v-slot:activator="{ props }">
      <v-btn icon="" size="small" v-bind="props">
        <img src="/images/task/filter.svg" :width="20" :height="20" />
      </v-btn>
    </template>
    <v-card style="overflow-x: hidden" :min-width="300">
      <v-row class="mb-0">
        <v-col style="border-right: 2px solid #e4e4e4" v-if="filterSeeAll.show">
          <div class="my-3">
            <p class="text-title mt-3 ml-5">
              {{ filterSeeAll.data.title }}
            </p>
            <v-list>
              <div v-for="val in filterSeeAll.data.value" :key="val.id">
                <v-list-item
                  style="height: 5px; font-size: 11px; font-weight: 900"
                >
                  <v-checkbox
                    :label="val.name"
                    :value="
                      filterSeeAll.data.name == 'period' ? val.name : val.id
                    "
                    :disabled="isDataLoading"
                    v-model="filterForm.filter[filterSeeAll.data.name]"
                    color="#05aa59"
                    style="margin-right: 0px"
                    density="compact"
                    hide-details
                    @change="onChangeCommit()"
                  />
                </v-list-item>
              </div>
            </v-list>
          </div>
        </v-col>
        <v-col>
          <v-list>
            <p class="text-title ml-5 mt-1">Sort by</p>
            <v-list-item>
              <v-select
                item-text="title"
                item-value="name"
                variant="solo"
                density="comfortable"
                single-line
                label="Sort based"
                class="px-1 text-11 py-2"
                style="font-size: small; border-radius: 10px; min-width: 300px"
                hide-details
                :items="itemMenus"
                :loading="isLoading"
                :disabled="isDataLoading"
                v-model="filterForm.sort.sortName"
                @change="onChangeCommit()"
              >
                <template v-slot:no-data>
                  <span
                    class="d-flex align-item-center ma-2 pa-1"
                    style="cursor: pointer"
                    @click="getFilter(type)"
                  >
                    <v-icon class="mr-2">mdi-reload</v-icon>
                    Reload Data
                  </span>
                </template>
              </v-select>
              <template v-slot:append>
                <v-btn
                  class="btn-icon ml-1"
                  @click="onChangeSort()"
                  :disabled="isDataLoading"
                >
                  {{ sortAZ }}
                </v-btn>
                <v-btn
                  class="btn-icon ml-1"
                  @click="onChangeTime()"
                  v-if="isUsingButton"
                  :disabled="isDataLoading"
                >
                  <img
                    src="/images/sort-time-asc.svg"
                    height="24"
                    v-if="isTimeAsc"
                  />
                  <img src="/images/sort-time-desc.svg" height="24" v-else />
                </v-btn>
              </template>
            </v-list-item>
          </v-list>
          <div class="px-5">
            <hr />
          </div>
          <div class="my-3" v-if="itemMenus.length">
            <p class="text-title ml-5" style="margin-bottom: 0px !important">
              Filter By
            </p>
            <div v-for="(item, idx) in itemMenus" :key="idx">
              <p class="text-title mt-0 ml-5">
                {{ item.title }}
              </p>
              <v-list>
                <div v-for="(val, idx) in item.value" :key="val.id">
                  <v-list-item
                    v-if="idx < 5"
                    style="height: 5px; font-size: 11px; font-weight: 900"
                  >
                    <v-checkbox
                      :label="val.name"
                      :value="item.name == 'period' ? val.name : val.id"
                      :disabled="isDataLoading"
                      v-model="filterForm.filter[item.name]"
                      color="#05aa59"
                      style="margin-right: 0px"
                      density="compact"
                      hide-details
                      @change="onChangeCommit()"
                    />
                  </v-list-item>
                  <v-btn
                    v-if="idx == 5"
                    variant="text"
                    class="font-italic text-decoration-underline pa-0 ml-5"
                    color="blue"
                    @click="onSeeAll(item.name)"
                    style="font-size: 10px"
                  >
                    See All
                  </v-btn>
                </div>
              </v-list>
            </div>
          </div>
          <div class="mx-4 mb-5" v-if="isUsingButton">
            <v-btn
              block
              class="primary-gradient"
              style="border-radius: 10px"
              @click="applyFilter"
              >Apply</v-btn
            >
          </div>
        </v-col>
      </v-row>
    </v-card>
  </v-menu>
</template>

<script>
import client from "@/library/ApiClient";

export default {
  name: "dashboardFilter",
  emits: ["submitFilter"],
  props: {
    typeFilter: {
      type: String,
      default: null,
    },
    subFilter: {
      type: String,
      default: null,
    },
    dataLoading: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      itemMenus: [],
      isLoading: false,
      isDataLoading: false,
      filterConfig: {
        width: 500,
      },
      filterForm: {
        sort: {
          sortName: null,
          sortType: "ascending",
          sortTime: "descending",
        },
        filter: {},
      },
      filterSeeAll: {
        show: false,
        data: {},
      },
    };
  },
  methods: {
    onChangeSort() {
      if (this.filterForm.sort.sortType == "ascending") {
        this.filterForm.sort.sortType = "descending";
      } else {
        this.filterForm.sort.sortType = "ascending";
      }
      this.onChangeCommit();
    },
    onChangeTime() {
      if (this.filterForm.sort.sortTime == "ascending") {
        this.filterForm.sort.sortTime = "descending";
      } else {
        this.filterForm.sort.sortTime = "ascending";
      }
    },
    onSeeAll(param) {
      if (this.filterSeeAll.data.name == param) {
        this.filterSeeAll.show = false;
        this.filterSeeAll.data = {};
        this.filterConfig.width = 500;
      } else {
        let filterSeeAll = this.itemMenus.find((e) => e.name == param);
        this.filterSeeAll.show = true;
        this.filterSeeAll.data = filterSeeAll;
        this.filterConfig.width = 1000;
      }
    },
    getFilter(type) {
      this.itemMenus = [];
      this.filterSeeAll.show = false;
      this.filterSeeAll.data = {};
      this.filterConfig.width = 500;

      if (type == "dashboard.workspace") {
        this.getFilterWorkspace();
      } else if (type == "dashboard.task") {
        this.getFilterTask();
      } else if (
        ["dashboard.persetujuan", "dashboard.pengajuan"].includes(type)
      ) {
        if (this.subFilter == "task") {
          this.getFilterPersetujuanPengajuan("task");
        } else {
          this.getFilterPersetujuanPengajuan("workspace");
        }
      } else if (type == "dashboard.document") {
        if (this.subFilter == "materi") {
          this.getFilterDocument("materi");
        } else {
          this.getFilterDocument("hasil");
        }
      } else if (type == "dashboard.assignment") {
        this.getFilterAssignment();
      }
    },
    getFilterWorkspace() {
      this.isLoading = true;
      client
        .getFilterDashboard({
          store: this.$store,
          data: {
            username: this.$store.state.username,
          },
        })
        .then((response) => {
          let data = response.plainData.responseData.data;
          this.itemMenus = data;

          let filter = {};
          data.forEach((element) => {
            filter[element.name] = [];
          });
          this.filterForm.filter = filter;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getFilterTask() {
      this.isLoading = true;
      client
        .getFilterDashboard({
          store: this.$store,
          data: {
            username: this.$store.state.username,
          },
        })
        .then((response) => {
          let data = response.plainData.responseData.data.filter(
            (item) => item.title == "Category"
          );
          this.itemMenus = data;

          let filter = {};
          data.forEach((element) => {
            filter[element.name] = [];
          });
          this.filterForm.filter = filter;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getFilterPersetujuanPengajuan(type = "workspace") {
      this.isLoading = true;
      client
        .getFilterDashboard({
          store: this.$store,
          data: {
            filterType: type,
          },
        })
        .then((response) => {
          let data = response.plainData.responseData.data;
          this.itemMenus = data;

          let filter = {};
          data.forEach((element) => {
            filter[element.name] = [];
          });
          this.filterForm.filter = filter;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getFilterDocument(type = "materi") {
      // debugger;
      this.isLoading = true;
      client
        .getFilterDocument({
          store: this.$store,
          data: {
            filterType: type,
          },
        })
        .then((response) => {
          let datas = response.plainData.responseData.data ?? [];
          this.itemMenus = datas;

          let filter = {};
          datas.forEach((element) => {
            filter[element.name] = [];
          });
          this.filterForm.filter = filter;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getFilterAssignment(type = "assignment") {
      this.isLoading = true;
      client
        .getFilterDashboard({
          store: this.$store,
          data: {
            filterType: type,
          },
        })
        .then((response) => {
          let data = response.plainData.responseData.data;
          this.itemMenus = data;

          let filter = {};
          data.forEach((element) => {
            filter[element.name] = [];
          });
          this.filterForm.filter = filter;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    onChangeCommit() {
      let commit = {
        sort: {
          sortName: this.filterForm.sort.sortName,
          sortType: this.filterForm.sort.sortType,
          sortTime: this.filterForm.sort.sortTime,
        },
        filter: this.filterForm.filter,
        search: this.searchDashboard,
      };

      //bypass onchange ketika menggunakan tombol
      if (this.isUsingButton) return 0;
      this.$emit("submitFilter", commit);
    },
    applyFilter() {
      // debugger;
      let commit = {
        sort: {
          sortName: this.filterForm.sort.sortName,
          sortType: this.filterForm.sort.sortType,
          sortTime: this.filterForm.sort.sortTime,
        },
        filter: this.filterForm.filter,
      };

      if (!this.isUsingButton) return 0;
      this.$emit("submitFilter", commit);
    },
  },
  watch: {
    typeFilter(value) {
      this.getFilter(value);
    },
    subFilter() {
      this.getFilter(this.typeFilter);
    },
    dataLoading(val) {
      this.isDataLoading = val;
    },
  },
  created() {
    this.getFilter(this.typeFilter);
  },
  computed: {
    sortAZ() {
      if (this.filterForm.sort.sortType == "ascending") return "A-Z";
      return "Z-A";
    },
    isTimeAsc() {
      return this.filterForm.sort.sortTime == "ascending";
    },
    isUsingButton() {
      return [
        "dashboard.persetujuan",
        "dashboard.pengajuan",
        "dashboard.document",
      ].includes(this.typeFilter);
    },
  },
};
</script>

<style scoped>
hr {
  display: block;
  height: 1px;
  border: 0;
  border-top: 1px solid #e4e4e4;
  padding: 0;
}
.btn-icon {
  font-weight: 900;
  font-size: 13px;
  border-radius: 10px;
  height: 48px !important;
  border: 2px solid;
  border-color: #e4e4e4;
  color: #4b4b4b;
}
.text-title {
  font-weight: 900;
  color: #4b4b4b;
  font-size: 12px;
}
.cheeckbox-custom {
  margin-top: 10px;
  font-size: 1.5vh;
  font-weight: bold;
  opacity: 0.7;
  display: grid;
  grid-template-columns: 1em auto;
  gap: 1em;
}
.cheeckbox-custom input[type="checkbox"] {
  width: 2vh;
  height: 2vh;
  accent-color: #05aa59;
}
.checkbox-spacing {
  margin: -15px -10px 0px -10px;
  height: 40px;
}

.v-list-item {
  min-height: 25px !important;
}
:deep(.v-application) {
  color: #05aa59 !important;
}
:deep(.v-list-item__title) {
  font-size: 11px;
  font-weight: 900;
  color: #4b4b4b;
}

:deep(.v-select__selection--comma) {
  font-weight: 900;
  color: #4b4b4b;
}
:deep .v-label {
  font-size: 11px;
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
</style>
