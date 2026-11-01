<template>
  <v-dialog width="450px" v-model="isActive">
    <template v-slot:activator="{ props }">
      <v-btn
        v-bind="props"
        color="#fff"
        elevation="1"
        style="border-radius: 5px; border: 0.5px solid #d3d3d3"
      >
        <v-icon icon="mdi-delete" color="#065695"></v-icon>
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
              v-if="this.item.user?.username == this.$store.state.username"
              class="mt-n8"
              icon="mdi-alert-circle"
              size="100"
              color="orange"
              style="
                background: white;
                border-radius: 100px;
                border: 3px solid white;
              "
            ></v-icon>
            <v-icon
              v-else
              class="mt-n8"
              icon="mdi-delete-circle"
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
            class="text-h6 text-center pt-2"
            style="justify-content: center; color: #3a416f"
          >
            Delete Participant
          </p>
          <p
            class="text-center"
            style="color: rgb(121, 121, 121)"
            v-if="this.item.user?.username != this.$store.state.username"
          >
            Are you sure delete this participant?
          </p>
          <p class="text-center" style="color: rgb(121, 121, 121)" v-else>
            You will no longer a participant of this task! <br />
            Are you sure?
          </p>
        </v-card-text>
        <v-card-actions
          class="justify-end pb-5 pt-4"
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
            :loading="loading"
            elevation="3"
            class="mr-4 btn-color-process"
            @click="proceed"
          >
            Delete
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
   item: Object
  },
  data: function () {
    return {
      isActive: false,
      loading: false,
      warning: false,
    };
  },
  methods:{
    proceed(){
    this.loading = true
    client
        .deleteTaskMember({
          store: this.$store,
          data: {
            username: this.$store.state.username,
            id_not_guid: this.item.id,
          },
        })
        .then((res) => {
          if (res.plainData.Response == "OK") {
            this.$root.toast.show({
              message: "User successfully deleted",
              color: "success",
              timeout: 3000,
              icon: "mdi-check",
            });
            this.$emit("onSuccess");
          }
        }).finally(()=>{
          this.loading = false;
        })
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
  border-radius: 10px;
  padding-left: 15px;
  padding-right: 15px;
  margin-left: 10px;
  font-weight: 800;
  color: white;
  font-weight: 600;
  background: linear-gradient(#ff000d, #ff000d);
}
.btn-color-process-warning {
  border-radius: 10px;
  padding-left: 15px;
  padding-right: 15px;
  margin-left: 10px;
  font-weight: 800;
  color: white;
  font-weight: 600;
  background: linear-gradient(#ff9800, #ff9800);
}
</style>
