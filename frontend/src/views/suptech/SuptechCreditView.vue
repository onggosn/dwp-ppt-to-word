<script>
import * as pbi from "powerbi-client";
import client from "@/library/ApiClient";

export default {
  name: "BISMA",

  mounted() {
    this.$emit("isFooter", false);
    client
      .getDataCredit({
        store: this.$store,
      })
      .then((response) => {
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

        const dashboardContainer = document.getElementById("container");
        const dashboard = powerbi.embed(dashboardContainer, config);
        dashboard.off("loaded");
        dashboard.off("rendered");
        dashboard.on("error", function () {
          this.dashboard.off("error");
        });
      })
      .catch((err) => {
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

<style scoped></style>
