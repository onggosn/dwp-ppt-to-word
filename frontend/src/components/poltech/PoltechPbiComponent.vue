<template>
  <v-sheet
    v-if="isLoading"
    color="#dddd"
    class="mt-5 text-center justify-center"
    :height="900"
    :max-height="900"
  >
    <div
      class="custom-loader"
      style="margin-top: 240px; display: inline-block"
    ></div>
    <p class="mt-5">Please Wait ...</p>
  </v-sheet>
  <div class="col-lg-12" v-else-if="!isAvailable">
    <div class="d-flex align-items-center justify-content-center mt-10">
      <v-img
        src="/images/chartpack/emptybox.png"
        :height="300"
        :width="300"
      ></v-img>
    </div>
    <div
      class="text-center fw-600 text-18 text-italic"
      style="margin-top: -30px; color: #3279b2"
    >
      Oops! Data Not Available...
    </div>
  </div>
  <div>
    <section
      ref="container"
      :style="[
        'height: 900px; background-color: #e8e3e2; margin-top: 20px',
        !isAvailable ? 'transform:scale(0)' : '',
      ]"
    />
  </div>
</template>
<script>
import * as pbi from "powerbi-client";
import client from "@/library/ApiClient";

export default {
  name: "poltechPbiComponent",
  props: {
    items: Object,
  },
  data() {
    return {
      idSektor: null,
      idArea: null,
      isLoading: false,
      isAvailable: false,
    };
  },
  methods: {
    getMasterData() {
      this.idSektor =
        typeof this.$route.params.idSektor !== "undefined"
          ? this.$route.params.idSektor
          : 1;
      this.idArea =
        typeof this.$route.params.idArea !== "undefined"
          ? this.$route.params.idArea
          : 1;
      this.getPoltech();
    },
    getPoltech() {
      this.isLoading = true;
      var data = {
        idSektor: this.idSektor,
        idArea: this.idArea,
        reportType: "Poltech",
      };
      client
        .getDataReportPoltech({
          store: this.$store,
          data: data,
        })
        .then((response) => {
          this.isLoading = false;
          this.isAvailable = true;
          const permissions = pbi.models.Permissions.All;
          const config = {
            type: "report",
            tokenType: pbi.models.TokenType.Embed,
            accessToken: response.plainData.responseData.accessToken,
            embedUrl: response.plainData.responseData.embedUrl,
            //   id: "1d59d041-3d34-4e3c-81b0-010bf64844f8",
            pageView: "fitToWidth",
            permissions: permissions,
          };
          let powerbi = new pbi.service.Service(
            pbi.factories.hpmFactory,
            pbi.factories.wpmpFactory,
            pbi.factories.routerFactory
          );
          const dashboardContainer = this.$refs.container;
          const dashboard = powerbi.embed(dashboardContainer, config);
          dashboard.off("loaded");
          dashboard.off("rendered");
          dashboard.on("error", function () {
            this.dashboard.off("error");
          });
        })
        .catch((err) => {
          this.isLoading = false;
          this.isAvailable = false;
          if (err?.response.status === 403) {
            this.$root.toast.show({
              message: "tidak memiliki akses ke halaman ini",
              color: "warning",
              timeout: 3000,
            });
            this.$router.push({
              name: "home",
            });
          }
        });
    },
  },
  created() {
    this.getMasterData();
  },
};
</script>
<style scoped>
.custom-loader {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: radial-gradient(farthest-side, #065695 94%, #0000) top/8px 8px
      no-repeat,
    conic-gradient(#0000 30%, #065695);
  -webkit-mask: radial-gradient(farthest-side, #0000 calc(100% - 8px), #000 0);
  animation: s3 1s infinite linear;
}

@keyframes s3 {
  100% {
    transform: rotate(1turn);
  }
}
:deep(.v-img__img) {
  width: 100%;
}
</style>
