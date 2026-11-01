<template>
  <div>
    <!-- <h1>This is an Document Management View</h1> -->
  </div>
</template>

<script>
export default {
  mounted() {
    const mode = process.env.VUE_APP_MODE;
    let url =
      "https://dokumen.bi.go.id/sites/Workspace_Dev/BIDIVE/Dev_Hotfix/Main.aspx";
    if (mode === "production") {
      url = "https://dokumen.bi.go.id/sites/Workspace_Dev/BIDIVE/Main.aspx";
    }
    window.open(url, "_blank").focus();
    this.$router.go(-1);
  },
};
</script>
