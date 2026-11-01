<template>
  <v-dialog v-model="dialog" width="40%" persistent>
    <v-card>
      <v-card-title
        class="text-center mt-4 mb-2 font-weight-medium"
        style="color: #4b4b4b"
      >
        <v-btn
          class="mr-5 mt-3"
          style="position: absolute; right: 0; top: 0"
          text
          fab
          small
          elevation="0"
          @click="close()"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text style="color: rgba(0, 0, 0, 0.6)">
        <div class="d-flex justify-center">
          <v-avatar size="68" color="white" class="mb-4 box-shadow"
            ><v-icon color="red" size="40" icon="mdi-trash-can-outline"></v-icon
          ></v-avatar>
        </div>
        <div class="text-center font-weight-bold text-h4">Delete Meeting</div>
        <div class="text-center subtitle-1">
          Are you sure delete this meeting from your Task ?
        </div>
        <div>
          <v-col class="d-flex justify-end">
            <v-btn rounded="lg" class="mr-2" @click="close()">Close</v-btn>
            <v-btn
              rounded="lg"
              elevation="2"
              class="btn-danger"
              @click="doDelete()"
              >Delete</v-btn
            >
          </v-col>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
  <loading-dialog v-if="isLoading"></loading-dialog>
</template>
<script>
import { defineComponent } from "vue";
import client from "@/library/ApiClient";
import LoadingDialog from "@/components/LoadingDialog.vue";

export default defineComponent({
  components: { LoadingDialog },
  data() {
    return {
      dialog: false,
      idMeeting: "",
      isLoading: false,
    };
  },
  emits: ["dialog", "refrehAfterDelete"],
  methods: {
    start(idMeeting) {
      this.idMeeting = idMeeting;
      this.dialog = true;
    },
    close() {
      this.dialog = false;
      this.$emit("dialog", true);
    },
    doDelete() {
      this.dialog = false;
      this.isLoading = true;
      client
        .deleteTaskMeeting({
          store: this.$store,
          data: {
            username: this.$store.state.username,
            id: this.idMeeting,
          },
        })
        .then((response) => {
          this.isLoading = false;
          if (response.status === 200) {
            this.$emit("refrehAfterDelete", true);
            this.$root.toast.show({
              message: "Meeting successfully deleted",
              color: "success",
              timeout: 5000,
              icon: "mdi-check",
            });
          } else {
            this.$root.toast.show({
              message: "[500] Meeting failed deleted",
              color: "error",
              timeout: 5000,
              icon: "mdi-check",
            });
          }
        })
        .catch(() => {
          this.isLoading = false;
          this.$root.toast.show({
            message: "[500] Meeting failed deleted",
            color: "error",
            timeout: 5000,
            icon: "mdi-check",
          });
          this.$emit("refrehAfterDelete", true);
          this.loading = false;
        });
    },
  },
});
</script>
<style scoped>
.separator-horizontal {
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
  height: 1.2px;
  width: 100%;
}

.btn-danger {
  background-color: #ff5252;
  color: white;
}

.box-shadow {
  box-shadow: 0px 3px 5px -1px rgb(0 0 0 / 20%),
    0px 6px 10px 0px rgb(0 0 0 / 14%), 0px 1px 18px 0px rgb(0 0 0 / 12%);
}
</style>
