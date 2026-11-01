<template>
  <div :class="[$route.name.includes('v2') ? 'pl-6' : '']">
    <template v-if="loading">
      <div class="ma-6">
        <free-style-shimmer
          height="5.5vh"
          width="40%"
          border-radius="5px"
          color="#DCDCDC"
          class="ml-0 mt-0 mb-2"
        />
        <paragraph-shimmer :is-loading="true" :lines="4" :random-size="true" />
      </div>
    </template>
    <template v-else-if="listMenu != null && !loading">
      <v-tabs v-model="tab" show-arrows class="ma-6">
        <v-tab
          v-for="(item, index) in listMenu"
          :key="index"
          :value="item.idSektorSuptech"
          :to="getRoute(item)"
          >{{ item.nameSektorSuptech }}</v-tab
        >
      </v-tabs>
      <router-view :key="$route.fullPath"></router-view>
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
  </div>
</template>
<script>
import { defineComponent } from "vue";
import client from "@/library/ApiClient";

export default defineComponent({
  name: "SuptechView",
  components: {},
  data: function () {
    return {
      tab: null,
      listMenu: null,
      loading: false,
      idSektor: null,
    };
  },
  created() {
    this.getMasterData();
  },
  mounted() {
    this.$emit("isFooter", false);
  },
  methods: {
    goHome() {
      this.$router.replace({
        name: "home",
      });
    },
    getMasterData() {
      //   debugger;
      this.loading = true;
      client.getDataSectorSuptech({ store: this.$store }).then((res) => {
        this.listMenu = res.plainData.responseData;
        if (res.plainData.responseData.length == 0) this.listMenu = null;
        this.loading = false;

        this.idSektor =
          typeof this.$route.params.idSektor !== "undefined"
            ? this.$route.params.idSektor
            : 1;

        if (this.$route.path.includes("v2")) {
          this.$router.push({
            name: "v2.suptechbisma.sektor",
            params: { idSektor: this.idSektor },
          });
        } else {
          this.$router.push({
            name: "suptechbisma.sektor",
            params: { idSektor: this.idSektor },
          });
        }
      });
    },
    getRoute(item) {
      if (this.$route.path.includes("v2")) {
        return {
          name: "v2.suptechbisma.sektor",
          params: { idSektor: item.idSektorSuptech },
        };
      } else {
        return {
          name: "suptechbisma.sektor",
          params: { idSektor: item.idSektorSuptech },
        };
      }
    },
  },
  unmounted() {
    this.$emit("isFooter", true);
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
