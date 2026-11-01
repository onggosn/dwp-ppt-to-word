<template>
  <v-select
    readonly
    multiple
    variant="solo"
    item-title="value"
    item-value="id"
    :model-value="selectedCustom"
    :items="itemCostums"
    :error-messages="errorMsg"
    :hide-details="!isError"
  >
    <template v-slot:chip="{ item }">
      <v-chip
        color="#d6212a"
        class="mx-1 my-1"
        v-if="item.value == 'clear'"
        @click="clear"
      >
        <span>Clear All</span>
      </v-chip>
      <v-chip
        color="#065695"
        class="mx-1 my-1"
        v-else-if="item.value == 'add'"
        @click="add"
      >
        <span>+ Add More</span>
      </v-chip>
      <v-chip color="#3a416f" class="mx-1 my-1" v-else>
        {{ item.title }}
        <v-icon end icon="mdi-close" @click="remove(item.value)"></v-icon>
      </v-chip>
    </template>
  </v-select>

  <add-member-component
    ref="dialog_member"
    :title="title"
    :searchPlacheHolder="searchPlacheHolder"
    :items="items"
    @onClose="assignMember"
  />
</template>

<script>
import AddMemberComponent from "./AddMemberComponent.vue";

export default {
  /* eslint-disable */
  name: "selectMemberComponent",
  components: {
    AddMemberComponent
  },
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
    selected: {
      type: Array,
      default: function () {
        return [];
      },
    },
    errorMsg: {
      type: Array,
      default: function () {
        return [];
      },
    },
  },
  data() {
    return {
      itemSelected: this.selected,
    };
  },
  computed: {
    isError() {
      return this.errorMsg.length > 0;
    },
    itemCostums() {
      let data = [];
      this.items.forEach((el) => {
        data.push(el);
      });

      if (this.items.length > 0) {
        data.push({ id: "clear", value: "clear" });
      }
      data.push({ id: "add", value: "add" });
      return data;
    },
    selectedCustom() {
      let data = [];
      this.itemSelected.forEach((el) => {
        data.push(el);
      });

      if (this.itemSelected.length > 0) {
        data.push("clear");
      }
      data.push("add");
      return data;
    },
  },
  methods: {
    clear() {
      this.itemSelected.length = 0;
    },
    add() {
      this.$refs.dialog_member.show(this.itemSelected);
    },
    remove(id) {
      let idx = this.itemSelected.indexOf(id);
      if (idx !== -1) {
        this.itemSelected.splice(idx, 1);
      }
    },
    assignMember(items) {
      this.itemSelected = items;
    },
  },
  watch: {
    selected(val) {
      this.itemSelected = val;
    },
  },
};
</script>

<style>
:deep(.chip.clearButton) {
  background: linear-gradient(180deg, #d6212a 0%, #ff000d 100%) !important;
}

:deep(.chip.addButton) {
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%) !important;
}

:deep(.chip) {
  background-color: #3a416f !important;
  color: white;
  cursor: pointer;
}
</style>
