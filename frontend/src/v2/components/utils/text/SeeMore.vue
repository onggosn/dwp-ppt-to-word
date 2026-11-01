<template>
  <div>
    <template v-if="showItems.length == 0">-</template>
    <template v-else>
      <span class="text-15 text-subtitle-1 font-weight-medium">
        {{ showItems.join(`
      </span>
      ,
      <span class="text-15 text-subtitle-1 font-weight-medium"> `) }} </span>
      <span
        class="text-15 text-subtitle-1 font-weight-medium"
        v-for="(user, idx) in showItems"
        :key="idx"
      >
        {{ user }}
        <span v-if="idx != showItems.length - 1">,</span>
      </span>

      <span
        v-if="isShowMore"
        style="cursor: pointer"
        class="text-blueTheme-gradien"
        @click="showMore = true"
      >
        Show More
      </span>
      <span
        v-else
        style="cursor: pointer"
        class="text-blueTheme-gradien"
        @click="showMore = false"
      >
        Show Less
      </span>
    </template>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref } from "vue";

const prop = defineProps({
  items: {
    type: Array<string>,
    default: function () {
      return [];
    },
  },
});

const showMore = ref<boolean>(false);

const showItems = computed(() => {
  if (showMore.value === false) return prop.items.slice(0, 5);
  return prop.items;
});

const isShowMore = computed(() => {
  return prop.items.length > 5 && showMore.value === false;
});
</script>
