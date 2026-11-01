<template>
  <v-dialog width="450px" v-model="isActive">
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
              class="mt-n13"
              :icon="mainIcon"
              size="100"
              :color="mainIconColor"
              style="
                background: white;
                border-radius: 100px;
                border: 3px solid white;
                box-shadow: 0px 1px 6px 1px darkgry;
              "
            ></v-icon>
          </v-sheet>
          <p
            class="text-h6 pt-3 text-center"
            style="justify-content: center; color: #3a416f"
          >
            {{ title }}
          </p>
          <p
            class="text-center"
            style="color: rgb(121, 121, 121); letter-spacing: -0.1px"
          >
            {{ descriptions }}
          </p>
        </v-card-text>
        <v-card-actions
          class="justify-end pb-5 pt-7 pr-5"
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
              border-radius: 10px;
              padding-left: 15px;
              padding-right: 15px;
              font-weight: 800;
            "
            :style="{
              background: negativeButtonColor,
              color: negativeButtonTextColor,
            }"
            @click="isActive.value = false"
          >
            {{ negativeButtonTitle }}
          </v-btn>
          <v-btn
            :loading="loading"
            elevation="3"
            style="
              border-radius: 10px;
              padding-left: 15px;
              padding-right: 15px;
              margin-left: 10px;
              font-weight: 800;
              font-weight: 600;
            "
            :style="{
              background: positiveButtonColor,
              color: positiveButtonTextColor,
            }"
            @click="positiveButtonClick()"
          >
            {{ positiveButtonTitle }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<script lang="js">
import { defineComponent } from "vue";

export default defineComponent({
  name: "CustomDialog",
  components: {
  },
  props:{
    title: {
      type: String,
      default: "",
    },
    descriptions: {
      type: String,
      default: "",
    },
    positiveButtonTitle: {
      type: String,
      default: "Ok",
    },
    negativeButtonTitle: {
      type: String,
      default: "Cancel",
    },
    positiveButtonTextColor: {
      type: String,
      default: "white",
    },
    negativeButtonTextColor: {
      type: String,
      default: "white",
    },
    positiveButtonColor: {
      type: String,
      default: "white",
    },
    negativeButtonColor: {
      type: String,
      default: "white",
    },
    mainIcon: {
      type: String,
      default: "",
    },
    mainIconColor: {
      type: String,
      default: "red",
    },
  },
  data: function () {
    return {
      isActive: false,
      loading: false,
      uniqueID: ""
    };
  },
  methods:{
    start(uniqueID = null){
        this.isActive = true
        this.uniqueID = uniqueID
    },
    close(){
        this.isActive = false
    },
    positiveButtonClick(){
        this.$emit("positiveButtonClicked", this.uniqueID)
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
