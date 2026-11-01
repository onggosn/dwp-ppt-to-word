<template>
  <v-dialog persistent v-model="dialog" :max-width="450">
    <v-card style="height: 68vh">
      <v-card-title class="d-flex justify-center align-center">
        <div class="text-18 text-blueTheme fw-500">{{ title }}</div>
        <v-btn
          class="mr-2"
          style="position: absolute; right: 0"
          variant="text"
          icon="mdi-close"
          @click="hide"
        ></v-btn>
      </v-card-title>
      <v-card-text class="mt-2">
        <v-autocomplete
          multiple
          hide-selected
          variant="solo"
          item-title="value"
          item-value="id"
          :placeholder="searchPlacheHolder"
          :items="itemList"
          :hide-details="true"
        >
          <template v-slot:selection>
            <span class="d-none"></span>
          </template>
          <template v-slot:item="{ item }">
            <v-list-item class="my-2">
              <div
                class="d-flex justify-space-between align-center"
                style="cursor: pointer"
                @click="add(item.value)"
              >
                <div class="d-flex flex-row align-center">
                  <img src="/images/dummyBlue.png" style="width: 40px" />
                  <div class="mx-2">{{ item.title }}</div>
                </div>
                <div>
                  <v-icon color="#267DC2">mdi-plus-circle-outline</v-icon>
                </div>
              </div>
            </v-list-item>
          </template>
        </v-autocomplete>

        <div class="mt-4" style="max-height: 51vh; overflow: scroll">
          <div
            class="px-4 py-2 my-1"
            v-for="(item, idx) in itemSelected"
            :key="idx"
          >
            <div class="d-flex justify-space-between align-center">
              <div class="d-flex flex-row align-center">
                <img src="/images/dummyBlue.png" style="width: 40px" />
                <div class="mx-2">{{ getName(item) }}</div>
              </div>
              <div>
                <v-icon color="red" @click="hapus(idx)">mdi-close</v-icon>
              </div>
            </div>
          </div>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "addMemberComponen",
  props: {
    title: {
      type: String,
      default: "Meeting Participant",
    },
    searchPlacheHolder: {
      type: String,
      default: "Enter a name or email address",
    },
    items: {
      type: Array,
      default: function () {
        return [];
      },
    },
  },
  data() {
    return {
      dialog: false,
      search: null,
      itemSelected: [],
    };
  },
  methods: {
    getName(id) {
      let data = this.items.find((e) => e.id == id);
      if (data) return data.value;
      return "name not found";
    },
    add(data) {
      let isNew = this.itemSelected.filter((e) => e == data).length == 0;
      if (isNew) {
        this.itemSelected.push(data);
      }
    },
    clear() {
      this.itemSelected = [];
    },
    hapus(index) {
      this.itemSelected.splice(index, 1);
    },
    show(itemSelected = []) {
      this.dialog = true;
      this.itemSelected = itemSelected;
    },
    hide() {
      this.$emit("onClose", this.itemSelected);
      this.dialog = false;
    },
  },
  computed: {
    itemList() {
      return this.items.filter((e) => !this.itemSelected.includes(e.id));
    },
  },
};
</script>
