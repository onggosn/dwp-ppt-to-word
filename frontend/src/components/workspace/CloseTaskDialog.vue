<template>
  <v-dialog width="450px" v-model="isActive" class="dialog-visible" persistent>
    <template v-slot:activator="{ props }">
      <v-btn
        v-bind="props"
        size="sm"
        variant="text"
        prepend-icon="mdi-stop"
        color="#065695"
        style="font-size: 13px; font-weight: 800"
      >
        <template v-slot:prepend>
          <v-icon color="#065695" size="25"></v-icon>
        </template>

        Close Task
      </v-btn>
    </template>
    <template v-slot:default="{ isActive }">
      <v-card
        style="
          border-radius: 10px;
          background: transparent;
          box-shadow: 0px 0px;
        "
      >
        <v-card-title class="text-center pa-0">
          <v-sheet style="background: transparent; height: 10vh"> </v-sheet>
        </v-card-title>
        <v-card-text
          style="
            padding-top: 0px;
            background: white;
            border-radius: 10px 10px 0px 0px;
            box-shadow: 10px 10px;
          "
        >
          <v-sheet style="background: transparent" class="text-center">
            <v-icon
              class="mt-n8"
              icon="mdi-close-circle-outline"
              size="100"
              color="red"
              style="
                background: white;
                border-radius: 100px;
                border: 3px solid white;
              "
            ></v-icon>
          </v-sheet>
          <p
            class="text-h6 pt-2 text-center"
            style="justify-content: center; color: #3a416f"
          >
            Close Task
          </p>
          <p class="text-center" style="color: rgb(121, 121, 121)">
            Are you sure to close this task ?
          </p>
          <p class="text-center" style="color: rgb(121, 121, 121)">
            This action cannot be reversed
          </p>
        </v-card-text>
        <v-card-actions
          class="justify-end pb-5"
          style="
            padding-top: 0px;
            background: white;
            border-radius: 0px 0px 10px 10px;
            box-shadow: 10px 10px;
          "
        >
          <v-spacer></v-spacer>
          <v-btn
            :disabled="loading"
            elevation="3"
            style="
              background: linear-gradient(#fff -46.47%, #fff 157.9%);
              border-radius: 10px;
              padding-left: 15px;
              padding-right: 15px;
              font-weight: 800;
              color: red;
              width: 5.5vw;
            "
            @click="isActive.value = false"
          >
            Cancel
          </v-btn>
          <v-btn
            v-if="!showCounter"
            :loading="loading"
            elevation="3"
            class="btn-color-process mr-4"
            style="
              border-radius: 10px;
              padding-left: 15px;
              padding-right: 15px;
              margin-left: 10px;
              font-weight: 800;
              color: white;
              font-weight: 600;
              background: linear-gradient(#d6212a, #ff000d);
              width: 5.5vw;
            "
            @click="proceed"
          >
            Close
          </v-btn>
          <v-btn
            v-if="showCounter"
            elevation="3"
            class="btn-color-process mr-4"
            style="
              border-radius: 10px;
              padding-left: 15px;
              padding-right: 15px;
              margin-left: 10px;
              font-weight: 800;
              color: white;
              font-weight: 600;
              background: linear-gradient(grey, darkgrey);
              pointer-events: none;
              width: 5.5vw;
            "
          >
            <v-progress-circular
              indeterminate
              color="white"
            ></v-progress-circular>
            <p style="position: absolute">{{ countDown }}</p>
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<script>
import { defineComponent } from "vue";
import client from "@/library/ApiClient";

export default defineComponent({
  name: "CloseTask",
  components: {},
  props: {
    idTask: String,
  },
  data: function () {
    return {
      isActive: false,
      loading: false,
      countDown: 10,
      showCounter: true,
    };
  },
  mounted() {
    this.countDownTimer();
  },
  methods: {
    countDownTimer() {
      if (this.countDown > 0) {
        setTimeout(() => {
          this.countDown -= 1;
          this.countDownTimer();
        }, 1000);
      } else {
        this.showCounter = false;
      }
    },
    proceed() {
      this.loading = true;
      client
        .closingTasks({
          store: this.$store,
          data: {
            id: this.idTask,
          },
        })
        .then((response) => {
          // debugger
          switch (response.plainData.responseCode) {
            case "011000":
              this.$root.toast.show({
                message: response.plainData.responseData.description,
                color: "success",
                timeout: 3000,
                icon: "mdi-check",
              });
              break;
            default:
              this.$root.toast.show({
                message: response.plainData.responseMessage,
                color: "error",
                timeout: 10000,
                icon: "mdi-check",
              });
              break;
          }
          this.$emit("onSuccess");
        })
        .catch(() => {
          this.$root.toast.show({
            message: "Something went wrong",
            color: "error",
            timeout: 10000,
            icon: "mdi-check",
          });
        })
        .finally(() => {
          this.loading = false;
          this.dialog = false;
        });
    },
  },
});
</script>
<style scoped>
.btn-grad {
  border: solid 2.5px transparent;
  background-image: linear-gradient(
      rgba(255, 255, 255, 0),
      rgba(255, 255, 255, 0)
    ),
    linear-gradient(90.76deg, #267dc2 15.32%, #ff000d 61.36%);
  border-radius: 15px;
  background-origin: border-box;
  background-clip: content-box, border-box;
  box-shadow: 2px 1000px 1px #fff inset;
}
.btn-text-grad {
  font-size: 14px;
  background: linear-gradient(90.76deg, #267dc2 15.32%, #ff000d 61.36%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.line-gradient {
  height: 1px;
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
}
.btn-color-process {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: #fdfdfd;
}
</style>
