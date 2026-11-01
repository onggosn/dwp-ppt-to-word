<template>
  <v-container class="pa-10 h-screen">
    <template v-if="loading">
      <free-style-shimmer
        height="5.5vh"
        width="40%"
        border-radius="5px"
        color="#DCDCDC"
        class="ml-0 mt-0 mb-2"
      />
      <paragraph-shimmer :is-loading="true" :lines="4" :random-size="true" />
    </template>
    <template v-else-if="listSektor != null && !loading">
      <v-tabs v-model="tab">
        <v-tab
          v-for="(item, index) in listSektor"
          :key="index"
          :value="item.id"
          >{{ item.name }}</v-tab
        >
        <div style="margin-left: auto" class="pa-1">
          <v-form ref="form" type="submit" @submit.prevent="search">
            <v-text-field
              v-model="searchKeyword"
              v-on:keyup.enter="search"
              density="compact"
              align-self="end"
              hide-details="auto"
              variant="solo"
              clearable
              placeholder="Chartpack search"
              style="
                margin-left: auto !important;
                width: 300px;
                border-radius: 10px;
              "
              :rules="[rules.required]"
            >
              <template v-slot:prepend-inner>
                <img src="/images/task/searchMagnifier.svg" />
              </template>
            </v-text-field>
          </v-form>
        </div>
      </v-tabs>
      <v-window v-model="tab" class="pt-5 h-screen">
        <v-window-item
          v-for="(item, index) in listSektor"
          :key="index"
          :value="item.id"
        >
          <web-viewer-chartpack
            :item="item.areas"
            :rowChartPack="rowChartPack"
            :tabActive="tab"
          ></web-viewer-chartpack>
        </v-window-item>
        <v-window-item :value="3"> Two </v-window-item>
      </v-window>
    </template>
    <template v-else>
      <div class="row">
        <div class="col-lg-12">
          <div class="d-flex align-items-center justify-content-center">
            <v-img
              src="/images/chartpack/aksesError.png"
              :height="300"
              :width="300"
            ></v-img>
          </div>
          <div class="text-center text-blackTheme fw-600 text-18 text-italic">
            Access Denied
          </div>
        </div>
      </div>
      <v-row>
        <v-col></v-col>
        <v-col>
          <div class="text-center text-blackTheme fw-400 text-15">
            You do not have access to this feature. Speak to your administrator
            to unlock this feature.
          </div>
          <div class="text-center mt-2">
            <v-btn
              @click="goHome"
              elevation="4"
              class="btn-primary text-center"
            >
              Go Back Home</v-btn
            >
          </div>
        </v-col>
        <v-col></v-col>
      </v-row>
    </template>
    <!-- <loading-dialog v-if="loading"></loading-dialog> -->
  </v-container>
</template>
<script>
import { defineComponent } from "vue";
import WebViewerChartpack from "@/components/chartpack/WebViewerChartPack.vue";
import Client from "@/library/ApiClient";

export default defineComponent({
  components: {
    WebViewerChartpack,
  },
  data: function () {
    return {
      rules: {
        required: (value) => !!value || "Please input your keywords",
      },
      tab: null,
      listSektor: null,
      loading: false,
      searchKeyword: "",
      paramChartPack: "",
      rowChartPack: null,
    };
  },
  watch: {
    paramChartPack() {
      Client.GetChartpackDetailByid({
        store: this.$store,
        data: {
          id: this.paramChartPack,
        },
      }).then((response) => {
        this.tab = response.plainData.idSektor;
        this.rowChartPack = response.plainData;
      });
    },
  },
  mounted() {
    this.searchKeyword =
      typeof this.$route.params.searchKeyword !== "undefined"
        ? this.$route.params.searchKeyword
        : "";
    this.paramChartPack =
      typeof this.$route.params.idChartpack !== "undefined"
        ? this.$route.params.idChartpack
        : "";
    this.getMasterData();
  },
  methods: {
    goHome() {
      this.$router.replace({
        name: "home",
      });
    },
    getMasterData() {
      this.loading = true;
      Client.sektor({ store: this.$store }).then((res) => {
        this.listSektor = res.plainData;
        if (res.plainData.length == 0) this.listSektor = null;

        this.loading = false;
      });
    },
    async search() {
      const { valid } = await this.$refs.form.validate();
      if (valid) {
        this.$router.push({
          name: "search-chartpack",
          params: {
            searchKeyword: this.searchKeyword,
          },
        });
      }
    },
  },
});
</script>
<style scoped>
:deep(.v-tab) {
  background: #ffff;
  margin-left: 1px;
  margin-right: 1px;
  border: 1px solid #dddd;
  border-radius: 10px 10px 0px 0px !important;
}
:deep(.v-tab--selected) {
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%) !important;
  color: #ffff;
}
:deep(.v-field--variant-solo) {
  box-shadow: 0px 0px 1px 0px rgba(0, 0, 0, 0.2),
    0px 2px 3px 1px rgba(0, 0, 0, 0.14), 0px 1px 5px 0px rgba(0, 0, 0, 0.12);
}
.btn-primary {
  background-color: rgb(38, 125, 194) !important;
  color: #ffff;
  border-radius: 10px;
}
</style>
