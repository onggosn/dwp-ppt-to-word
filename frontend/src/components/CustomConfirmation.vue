<template>
  <v-dialog v-model="dialog" :scrim="true" persistent width="auto">
    <v-card
      style="border-radius: 10px; background: transparent; box-shadow: 0px 0px"
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
          {{ title }}
        </p>
        <p class="text-center" style="color: rgb(121, 121, 121)">
          {{ message }}
        </p>
      </v-card-text>
      <v-card-actions
        class="justify-end pb-5 pr-8 pt-5"
        style="
          padding-top: 0px;
          background: white;
          border-radius: 0px 0px 10px 10px;
          box-shadow: 10px 10px;
        "
      >
        <v-spacer></v-spacer>

        <v-btn
          variant="flat"
          elevation="3"
          width="6vw"
          class="rounded-lg font-weight-bold"
          @click="dialog = false"
          style="
            background: linear-gradient(#fff -46.47%, #fff 157.9%);
            border-radius: 10px;
            padding-left: 15px;
            padding-right: 15px;
            font-weight: 800;
            color: red;
          "
        >
          Cancel
        </v-btn>
        <v-btn
          variant="flat"
          color="red"
          width="6vw"
          elevation="3"
          class="ml-5 rounded-lg font-weight-bold"
          @click="deleteDoc"
        >
          Delete
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {},
  data() {
    return {
      dialog: false,
      title: "",
      message: "",
      id: "",
      hasExtraParams: Object,
    };
  },
  methods: {
    start(documentName, params = null) {
      this.id = documentName;
      this.title = "Delete Document";
      this.message = "Are you sure delete this document from your task ?";
      this.dialog = true;
      this.hasExtraParams = params;
    },
    close() {
      this.dialog = false;
    },
    deleteDoc() {
      this.dialog = false;
      if (this.hasExtraParams) {
        if (this.hasExtraParams.isDocumentPendukung) {
          this.$emit("deleteDoc", this.hasExtraParams);
        }
      } else {
        this.$emit("deleteDoc", this.id);
      }
    },
  },
};
</script>
