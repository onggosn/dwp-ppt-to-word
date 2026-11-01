<template>
  <v-dialog width="450px" v-model="isActive">
    <template v-slot:activator="{ props }">
      <v-btn
        v-bind="props"
        size="sm"
        variant="text"
        prepend-icon="mdi-delete-forever"
        color="#065695"
        style="font-size: 13px; font-weight: 800; letter-spacing: -0.1px"
      >
        <template v-slot:prepend>
          <v-icon color="#065695" size="25"></v-icon>
        </template>

        Delete Activity
      </v-btn>
    </template>
    <template v-slot:default="{ isActive }">
      <v-card
        style="
          border-radius: 10px;
          background: transparent;
          box-shadow: 0px 0px;
        "
        v-if="isAvailableDelete"
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
              class="mt-n13"
              icon="mdi-delete-circle"
              size="100"
              color="red"
              style="
                background: white;
                border-radius: 100px;
                border: 3px solid white;
                box-shadow: 0px 1px 6px 1px darkgry;
              "
            ></v-icon>
          </v-sheet>
          <p
            class="text-h6 pt-2 text-center"
            style="justify-content: center; color: #3a416f"
          >
            Delete Activity
          </p>
          <p
            class="text-center"
            style="color: rgb(121, 121, 121); letter-spacing: -0.1px"
          >
            Deleting activity will permanently remove all activity
          </p>
          <p
            class="text-center"
            style="color: rgb(121, 121, 121); letter-spacing: -0.1px"
          >
            Are you sure?
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
            elevation="3"
            style="
              background: linear-gradient(#fff -46.47%, #fff 157.9%);
              border-radius: 10px;
              padding-left: 15px;
              padding-right: 15px;
              font-weight: 800;
              color: red;
            "
            @click="isActive.value = false"
          >
            Cancel
          </v-btn>
          <v-btn
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
            "
            @click="proceed"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
      <v-card
        v-else
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
              class="mt-n13"
              icon="mdi-alert-circle-outline"
              size="100"
              color="#fc8b24"
              style="
                background: white;
                border-radius: 100px;
                border: 3px solid white;
                box-shadow: 0px 1px 6px 1px darkgry;
              "
            ></v-icon>
          </v-sheet>
          <p
            class="text-h6 pt-2 text-center"
            style="justify-content: center; color: #3a416f"
          >
            Oops
          </p>
          <p class="text-center" style="color: rgb(121, 121, 121)">
            You must delete your task first before deleting this activity
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
            elevation="3"
            style="
              background: linear-gradient(#fff -46.47%, #fff 157.9%);
              border-radius: 10px;
              padding-left: 15px;
              padding-right: 15px;
              font-weight: 800;
              color: #fc8b24;
            "
            class="mr-5"
            @click="isActive.value = false"
          >
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<script lang="js">
import { defineComponent } from "vue";
import client from "@/library/ApiClient";

export default defineComponent({
  name: "CreateActivity",
  components: {
  },
  props:{
    isAvailableDelete: {
      type: Boolean,
      default: false,
    },
    idActivity: String
  },
  data: function () {
    return {
      isActive: false,
      loading: false
    };
  },
  methods:{
    handleSubmit() {
      if (!this.valid) {
        return;
      }
      this.proceed();
    },
    proceed(){
    this.loading = true
    client
        .deleteActivity({
          store: this.$store,
          data: {
            username: this.$store.state.username,
            id: this.idActivity,
          },
        })
        .then((response) => {
          if (response.plainData.Response == "OK") {
            this.$root.toast.show({
              message: "Successfully Deleted",
              color: "success",
              timeout: 3000,
            });
          } else {
            this.$root.toast.show({
              message: "Oops, Delete Failed. Please try again",
              color: "error",
              timeout: 3000,
              icon: "mdi-check",
            });
          }
          this.$emit("onSuccess");
        })
        .catch(() => {
          this.$root.toast.show({
            message: "Something went wrong",
            color: "error",
            timeout: 3000,
            icon: "mdi-check",
          });
        })
        .finally(() => {
          this.loading = false
          this.dialog = false;
        });
    }
  }
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
