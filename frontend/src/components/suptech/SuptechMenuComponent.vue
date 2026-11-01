<template>
  <div class="row">
    <div class="col-lg-12">
      <div class="d-flex align-items-center justify-content-center">
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
  </div>
  <router-view :key="$route.fullPath"></router-view>
</template>
<script>
export default {
  name: "SuptechMenuComponent",
  components: {},
  data() {
    return {
      isLoading: false,
      idSektor: null,
    };
  },
  methods: {
    getSelectData() {
      let index = this.listArea.findIndex(
        (item) => item.id === this.selectArea
      );
      this.idSektor = this.listArea[index].idSektorPoltech;
      this.idArea = this.listArea[index].id;
    },
    getPoltech() {
      this.getSelectData();
      this.$router.push({
        name: "poltech.sektor.area",
        params: { idSektor: this.idSektor, idArea: this.idArea },
      });
    },
    isObjectEmpty(obj) {
      return Object.keys(obj).length === 0;
    },
  },
  created() {
    this.getMasterData();
  },
  watch: {
    items() {
      this.getMasterData();
    },
  },
};
</script>
<style scoped></style>
