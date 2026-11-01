<template>
  <div>
    <template v-if="showItems.length == 0">-</template>

    <template v-else>
      <span
        class="text-15 text-subtitle-1 font-weight-medium"
        v-for="(user, idx) in showItems"
        :key="idx"
      >
        {{ user }}
        <span v-if="idx != showItems.length - 1">,</span>
      </span>

      <span
        style="cursor: pointer"
        class="text-blueTheme-gradien"
        v-if="isShowMore"
        @click="showMore = true"
        >Show More</span
      >
    </template>
  </div>
</template>

<script>
export default {
  name: "MemberShowMore",

  props: {
    items: {
      type: Array,

      default: function () {
        return [];
      },
    },
  },

  data() {
    return {
      showMore: false,
    };
  },

  computed: {
    showItems() {
      if (!this.showMore) return this.items.slice(0, 5);

      return this.items;
    },

    isShowMore() {
      return this.items.length > 5 && this.showMore == false;
    },
  },
};
</script>
