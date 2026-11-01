<template>
  <v-dialog width="450px" v-model="isActive">
    <template v-slot:activator="{ props }">
      <v-btn
        v-bind="props"
        class="ma-2 mt-4 rounded-lg btn-grad btn-grad:hover"
        outlined
        color="#C0C0C0"
        height="5vh"
      >
        <div class="btn-text-grad font-weight-bold pl-3 pr-3">
          + Add Another Activity
        </div>
      </v-btn>
    </template>
    <template v-slot:default="{ isActive }">
      <v-form @submit.prevent="handleSubmit" v-model="valid">
        <v-card style="border-radius: 10px">
          <v-card-title
            class="text-h6 text-center"
            style="justify-content: center; color: #3a416f"
          >
            Add Activity
          </v-card-title>
          <v-sheet class="line-gradient"> </v-sheet>

          <v-card-text>
            <v-sheet class="mt-4" style="color: #3a416f">
              Nama Activity<span class="text-redTheme text-17">*</span>
            </v-sheet>
            <v-sheet class="mt-2">
              <api-loader :apiMethod="getActivityName">
                <template v-slot:default="props">
                  <v-select
                    v-model="activityName"
                    :rules="[(v) => !!v || 'Wajib diisi']"
                    :items="props.response"
                    item-title="value"
                    item-value="id"
                    label="Pilih Nama Activity"
                    variant="solo"
                    height="7vh"
                    class="rounded-lg"
                  ></v-select>
                </template>
                <template v-slot:loading>
                  <free-style-shimmer
                    :is-loading="true"
                    height="7vh"
                    width="30vw"
                    border-radius="10px"
                    color="#DCDCDC"
                    class="ml-4 mt-2 pb-5"
                  />
                </template>
              </api-loader>
            </v-sheet>
          </v-card-text>
          <v-card-actions class="justify-end pb-5">
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
              "
              type="submit"
            >
              Save
            </v-btn>
          </v-card-actions>
        </v-card></v-form
      >
    </template>
  </v-dialog>
</template>

<script lang="js">
import { defineComponent } from "vue";
import client from "@/library/ApiClient";
import ApiLoader from "@/components/ApiLoader.vue";

export default defineComponent({
  name: "CreateActivity",
  components: {
    ApiLoader
  },
  props:{
    workspaceTypeId: {
      type: Number,
      default: 0,
    },
  },
  data: function () {
    return {
      valid: false,
      activityName: "",
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
    proceed() {
      this.loading = true
      client
        .insertActivity({
          store: this.$store,
          data: {
            username: this.$store.state.username,
            idActivityType: this.activityName,
            activityName: this.activityName,
            descriptions: "string",
            idWorkspace: this.$route.params.workspaceId,
          },
        })
        .then((response) => {
          switch(response.plainData.responseCode) {
            case "011032":
                this.$root.toast.show({
                  message: "Failed to Insert Activity",
                  color: "error",
                  timeout: 3000,
                  icon: "mdi-check",
                });
              break;
            case "011000":
                this.$emit("onSuccess");
                this.$root.toast.show({
                  message: "Successfully Added",
                  color: "success",
                  timeout: 3000,
                });
              break;
            default:
                this.$root.toast.show({
                  message:
                    response.plainData.responseMessage ??
                    "Unknown error from server",
                  color: "error",
                  timeout: 3000,
                  icon: "mdi-check",
                });
          }
        })
        .catch(() => {
          this.$root.toast.show({
            message: "Oops, Something went wrong",
            color: "error",
            timeout: 3000,
            icon: "mdi-check",
          });
        })
        .finally(() => {
          this.loading = false
          this.isActive  = false;
        });
    },
    getActivityName() {
      return client
        .getListActivityType({
          store: this.$store,
          data: {
            id: this.workspaceTypeId,
          },
        })
        .then((response) => {
          return response.plainData.responseData;
        });
    },
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
