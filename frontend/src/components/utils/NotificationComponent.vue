<template>
  <v-snackbar
    location="top right"
    :color="notificationBgColor"
    :timeout="timeout"
    v-model="showSnackbar"
  >
    <v-row class="my-0">
      <v-col cols="2" class="d-flex justify-center align-center pr-0">
        <img
          v-if="color == 'success'"
          src="/images/checkNotif2.png"
          style="width: 40px; height: 40px"
        />
        <img
          v-else-if="color == 'warning'"
          src="/images/warningNotif.png"
          style="width: 40px; height: 40px"
        />
        <img
          v-else
          src="/images/login/logoDMP.png"
          style="width: 40px; height: 40px"
        />
      </v-col>
      <v-col cols="10" style="color: #4b4b4b" class="pl-4">
        <p class="fw-600 text-18 mt-0 pt-0">{{ title }}</p>
        <p v-html="message" class="text-13 fw-400 mt-1"></p>
      </v-col>
    </v-row>
    <template v-slot:actions>
      <v-btn color="indigo" variant="text" @click="showSnackbar = false">
        <v-icon class="pointer-click mr-1" size="large">mdi-close</v-icon>
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
export default {
  data() {
    return {
      showSnackbar: false,
      message: "",
      color: "error",
      timeout: 3000,
      title: "",
    };
  },
  methods: {
    show(data) {
      this.message = data.message || 'missing "message".';
      this.color = data.color || "error";
      this.timeout = data.timeout || 3000;
      this.showSnackbar = true;
      this.title = data.title ?? "Digital Workplace";
      this.$store.dispatch("updateNotif");
    },
    toTitleCase(title) {
      return title.replace(/\w\S*/g, function (txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
      });
    },
  },
  computed: {
    notificationBgColor() {
      let bgColor = {
        success: "#EAF7EE",
        warning: "#FFEEBA",
        default: "#FFFFFFD9",
      };
      return bgColor[this.color] ?? "#FCEDE9";
    },
  },
};
</script>
<style scoped>
:deep(.v-snackbar__content) {
  width: auto !important;
}

:deep(.v-snackbar__wrapper) {
  border-radius: 10px;
}
</style>
