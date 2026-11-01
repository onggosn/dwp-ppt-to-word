<template>
  <v-menu
    transition="slide-y-transition"
    bottom
    :close-on-content-click="false"
  >
    <template v-slot:activator="{ props }">
      <v-btn
        icon=""
        size="small"
        v-bind="props"
        class="ml-2"
        style="position: right; top: 0; margin-right: 8px"
      >
        <img src="/images/task/searchMagnifier.svg" :width="21" :height="21" />
      </v-btn>
    </template>
    <v-card min-width="300">
      <v-form ref="form" type="submit" @submit.prevent="applySearch">
        <v-list>
          <v-list-item>
            <v-text-field
              v-model="searchKeyword"
              hide-details="auto"
              style="border-radius: 10px"
              placeholder="search"
              variant="outlined"
              clearable
              :autofocus="true"
            ></v-text-field>
            <!-- <div class="text-10 fw-600 text-grey-theme">
              Search berupa nama, tanggal pelaksanaan RDG (dd/mm/yyyy)
            </div> -->
          </v-list-item>
        </v-list>
        <v-list-item>
          <v-list-item-title class="text-right">
            <v-btn
              class="btn-primary blue-gradient text-right mb-2"
              @click="applySearch"
              >Search</v-btn
            >
          </v-list-item-title>
        </v-list-item>
      </v-form>
    </v-card>
  </v-menu>
</template>

<script>
export default {
  name: "dashboardSearch",
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
      searchKeyword: null,
    };
  },
  methods: {
    applySearch() {
      this.$emit("submitFilter", this.searchKeyword);
    },
  },
  watch: {
    typeFilter() {
      this.searchKeyword = "";
    },
    subFilter() {
      this.searchKeyword = "";
    },
    dataLoading(val) {
      this.isDataLoading = val;
    },
  },
};
</script>
<style scoped>
.blue-gradient {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: white !important;
  border-radius: 10px;
}
.text-grey-theme {
  color: rgba(121, 121, 121, 0.9);
}
</style>
