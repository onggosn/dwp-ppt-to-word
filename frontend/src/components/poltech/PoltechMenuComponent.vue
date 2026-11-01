<template>
  <div class="row" v-if="isObjectEmpty(items)">
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
  <v-row v-else>
    <v-col cols="5">
      <v-select
        v-model="selectArea"
        :loading="isLoading"
        :items="listArea"
        :disabled="isLoading"
        item-title="nameAreaPoltech"
        item-value="id"
        variant="solo"
        placeholder="Choose area"
        @update:modelValue="getPoltech"
      ></v-select>
    </v-col>
  </v-row>
  <router-view :key="$route.fullPath"></router-view>
</template>
<script>
export default {
  name: "poltechMenuComponent",
  components: {},
  props: {
    items: Object,
  },
  data() {
    return {
      listArea: [],
      selectArea: null,
      isLoading: false,
      idSektor: null,
      idArea: null,
    };
  },
  methods: {
    getMasterData() {
      if (!this.isObjectEmpty(this.items)) {
        this.listArea = this.items.areasPoltech;
        this.selectArea = this.listArea[0].id;
        this.getPoltech();
      }
    },
    getSelectData() {
      let index = this.listArea.findIndex(
        (item) => item.id === this.selectArea
      );
      this.idSektor = this.listArea[index].idSektorPoltech;
      this.idArea = this.listArea[index].id;
    },
    getPoltech() {
      this.getSelectData();
      if (this.$route.path.includes("v2")) {
        this.$router.push({
          name: "v2.poltech.sektor.area",
          params: { idSektor: this.idSektor, idArea: this.idArea },
        });
      } else {
        this.$router.push({
          name: "poltech.sektor.area",
          params: { idSektor: this.idSektor, idArea: this.idArea },
        });
      }
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
