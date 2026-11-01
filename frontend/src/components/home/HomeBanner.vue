<template>
  <v-row class="home-banner mt-2 white--text">
    <v-col cols="12" class="pa-5 ml-4 pa-md-8 ml-md-5">
      <!-- <h2 class="fw600">Welcome Back, {{ fullname }}</h2> -->
      <p class="text-sm-h6 fw600 text-md-h5 mt-md-2 mt-5">
        Welcome Back, {{ fullname }}
      </p>
      <p class="text-subtitle-sm-1 mr-4 mr-md-0">
        Here are some of the latest updates from the workplace and your latest
        schedule.
      </p>
    </v-col>
  </v-row>
</template>

<script>
export default {
  props: {},
  data: function () {
    return {
      username: "",
      fullname: "",
    };
  },
  mounted() {
    this.username = this.$store.state.username;
    this.fullname = this.$store.state.fullname;
  },
  methods: {},
};
</script>

<style>
.home-banner {
  max-width: 840px;
  background-image: url("@/assets/images/Banner.png");
  background-size: 100% 100%;
  height: 194px;
}

.white--text {
  color: white;
}
.fw600 {
  color: white;
  font-weight: 600;
  margin-top: 10px;
  letter-spacing: 1px;
}
.select-empty {
  cursor: pointer;
}
</style>
