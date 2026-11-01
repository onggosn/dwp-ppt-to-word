<template>
  <v-snackbar
    location="top right"
    max-height="75px"
    min-width="300px"
    :color="notificationBgColor"
    :timeout="timeout"
    v-model="showSnackbar"
  >
    <v-row class="my-0">
      <v-col cols="2" class="d-flex justify-center align-center pr-0">
        <img
          v-if="color == 'success'"
          src="/images/checkNotif2.png"
          style="width: 35px; height: 35px"
        />
        <img
          v-else-if="color == 'warning'"
          src="/images/warningNotif.png"
          style="width: 35px; height: 35px"
        />
        <!-- tambahan figma belum jelas variant nya -->
        <img
          v-else-if="color == 'oopss'"
          src="/images/dangerNotif.png"
          style="width: 35px; height: 35px"
        />
        <img
          v-else
          src="/images/cancelNotif.png"
          style="width: 35px; height: 35px"
        />
      </v-col>
      <v-col cols="10" style="color: #4b4b4b" class="pl-4">
        <div class="font-weight-bold text-15">{{ toTitleCase(color) }}</div>
        <div class="text-14">
          <span v-html="sanitizeHtml(message)"></span>
        </div>
      </v-col>
    </v-row>
    <template v-slot:actions>
      <v-btn color="indigo" variant="text" @click="showSnackbar = false">
        <!-- <img
         
          src="/images/closeIcon.png"
        /> -->
        <v-icon class="pointer-click mr-1" size="large">mdi-close</v-icon>
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
import sanitizeHtml from "sanitize-html";
export default {
  data() {
    return {
      showSnackbar: false,
      message: "",
      color: "error",
      timeout: 3000,
    };
  },
  methods: {
    show(data) {
      this.message = data.message || 'missing "message".';
      this.color = data.color || "error";
      this.timeout = data.timeout || 3000;
      this.showSnackbar = true;
      this.$store.dispatch("updateNotif");
    },
    toTitleCase(title) {
      return title.replace(/\w\S*/g, function (txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
      });
    },
    sanitizeHtml,
  },
  computed: {
    notificationBgColor() {
      let bgColor = {
        success: "#EAF7EE",
        warning: "#FFEEBA",
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
