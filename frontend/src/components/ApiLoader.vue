<template>
  <div>
    <v-overlay v-if="hasOverlay" absolute :value="loading" :opacity="0.2">
      <slot name="loadingOverlay">
        <v-progress-circular
          indeterminate
          color="primary"
        ></v-progress-circular>
      </slot>
    </v-overlay>
    <div v-if="loading" key="v1">
      <slot name="loading"></slot>
    </div>
    <div v-else key="v2">
      <slot v-if="isError" name="error" :retry="retry">
        <!-- <div>{{ currentErrorMessage }}</div> -->
        <p style="font-size: 14px">
          Oops, Something went wrong. Please try again
        </p>
        <!-- <v-btn @click="retry" color="white"
          >Coba Lagi <v-icon right>mdi-refresh</v-icon></v-btn
        > -->
        <v-btn @click="retry" color="white"
          >Refresh<v-icon right>mdi-refresh</v-icon></v-btn
        >
      </slot>
      <template v-else-if="!!response">
        <slot name="default" :response="response"></slot>
      </template>
    </div>
  </div>
</template>

<script lang="js">
export default {
  props: {
    apiMethod: Function,
    initialData: Object,
    customErrorMessage: String,
    loadingMessage: {
      type: String,
      default: "Memuat Data...",
    },
    showDefaultErrorMessage: {
      type: Boolean,
      default: true,
    },
    autoload: {
      type: Boolean,
      default: true,
    },
    hasOverlay: {
      type: Boolean,
      default: true,
    },
  },
  computed: {
    currentErrorMessage() {
      if (this.showDefaultErrorMessage) {
        return this.errorMessage;
      }
      if (this.customErrorMessage) {
        return this.customErrorMessage;
      }
      return null;
    },
  },
  data() {
    return {
      loading: false,
      isError: false,
      response: null,
      errorMessage: "",
    };
  },
  mounted() {
    if (this.autoload) {
      this.callApi();
    }
  },
  methods: {
    retry() {
      return this.callApi();
    },
    callApi() {
      // eslint-disable-next-line
      const instance = this;
      if (instance.initialData) {
        instance.$emit("loadingStarted");

        instance.loading = false;
        instance.isError = false;

        instance.$emit("loadingEnded", {
          success: true,
          response: instance.initialData,
          message: "Data Found. Prevent unnecessary API call",
        });
      } else {
        instance.loading = true;
        instance.$emit("loadingStarted");

        instance
          .apiMethod()
          .then((response) => {
            instance.loading = false;
            instance.isError = false;
            let errorMessage = "";

            if (!response.errors) {
              this.response = response;
              instance.$emit("loadingEnded", {
                success: true,
                response: response,
                message: "API success",
              });
            } else {
              instance.isError = true;
              errorMessage = "Error Fetching via API: status not success";

              instance.$emit("loadingEnded", {
                success: false,
                message: errorMessage,
                error: response,
              });
            }
            instance.errorMessage = errorMessage;
          })
          .catch((error) => {
            instance.loading = false;
            instance.isError = true;
            instance.errorMessage = "Error API response";
            if (error.response?.status === 406) {
              instance.isError = false;
              this.$store
                .dispatch("logout")
                .then(() => {
                  return this.$router.push({ name: "sso" });
                })
                .then(() => {
                  window.location.reload();
                });
            }else if (error.response?.status === 401) {
              instance.isError = false;
            }

            instance.$emit("loadingEnded", {
              success: false,
              message: instance.errorMessage,
              error,
            });
          });
      }
    },
  },
};
</script>

<style></style>
