<template>
  <div class="text-center mx-1">
    <v-menu>
      <template v-slot:activator="{ props }">
        <v-btn
          class="btn-dropdown w-100"
          variant="outlined"
          dark
          v-bind="props"
          style="overflow: hidden"
          >{{ title }}
          <template v-slot:append>
            <v-icon>mdi-chevron-down</v-icon>
          </template></v-btn
        >
      </template>

      <v-list>
        <v-list-item v-for="(item, index) in items" :key="index">
          <v-list-item-title
            style="cursor: pointer !important"
            @click="updateFilter(item)"
            >{{ item.value }}</v-list-item-title
          >
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>

<script lang="ts" setup>
import { PropType } from "vue";
import { TListDocument } from "@/v2/Type";

const props = defineProps({
  items: {
    type: Array as PropType<TListDocument[]>,
    default: () => [],
  },
  title: {
    type: String,
    default: "",
  },
});

const emit = defineEmits(["update", "update:title"]);
// const title = defineModel("title");

function updateFilter(item: TListDocument) {
  emit("update", item);
  emit("update:title", item.value);
}
</script>
<style scoped>
.btn-dropdown {
  color: #065695;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
}
</style>
