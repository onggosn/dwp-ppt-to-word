<script>
import * as pbi from "powerbi-client";
import client from "@/library/ApiClient";

export default {
  name: "BISMA",

  data: () => {
    return {
      isLoading: false,
      isFail: false,
    };
  },
  mounted() {
    this.$emit("isFooter", false);
    this.isLoading = true;
    client
      .getDataSuptechExecutiveSummary({
        store: this.$store,
      })
      .then((response) => {
        const permissions = pbi.models.Permissions.All;

        const config = {
          type: "report",
          tokenType: pbi.models.TokenType.Embed,
          accessToken: response.plainData.responseData.accessToken,
          embedUrl: response.plainData.responseData.embedUrl,
          pageView: "fitToWidth",
          permissions: permissions,
        };

        let powerbi = new pbi.service.Service(
          pbi.factories.hpmFactory,
          pbi.factories.wpmpFactory,
          pbi.factories.routerFactory
        );

        const dashboardContainer = document.getElementById("container");
        const dashboard = powerbi.embed(dashboardContainer, config);
        // dashboard.off("loaded");
        // dashboard.off("rendered");
        dashboard.on("loaded", function () {
          this.isLoading = false;
        });
      })
      .catch((err) => {
        this.isFail = true;
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
      })
      .finally(() => {
        this.isLoading = false;
      });
  },
  unmounted() {
    this.$emit("isFooter", true);
  },
};
</script>

<template>
  <div>
    <section id="container" style="height: 900px" />
  </div>
</template>

<style scoped>
::-webkit-scrollbar {
  margin-right: 2px;
  width: 1px !important;
  height: 1px !important;
}
</style>
