<template>
  <div class="d-block font-weight-bold mb-2 mt-1 text-blueTheme">
    Document Detail
  </div>
  <template v-for="(item, index) in documentDetail" :key="index">
    <template v-if="item.title != '-'">
      <div class="d-block text-14 mt-3" style="color: #a6abc7">
        {{ item.title }}
      </div>
      <div class="d-block text-14 text-black" :style="getStyles(item)">
        {{ item.value }}
      </div>
    </template>
  </template>
</template>

<script setup lang="ts">
import { defineProps } from "vue";

defineProps({
  documentDetail: Object,
});

const getStyles = (_item) => {
  if (_item.title == "Status") {
    switch (_item.value) {
      case "In Progress": {
        return {
          color: "#fe7411 !important",
          "font-weight": 900,
        };
      }
      case "Approved": {
        return {
          color: "#02aa59 !important",
          "font-weight": 900,
        };
      }
      case "Rejected": {
        return {
          color: "red !important",
          "font-weight": 900,
        };
      }
      case "Need For Approval": {
        return {
          color: "#fe7411 !important",
          "font-weight": 900,
        };
      }
    }
  } else if (_item.title == "Status Penyelesaian") {
    switch (true) {
      case _item.value.includes("100%"): {
        return {
          color: "#02AA59 !important",
          "font-weight": 900,
        };
      }
      default: {
        return {
          color: "#fe7411 !important",
          "font-weight": 400,
        };
      }
    }
  }
};
</script>
