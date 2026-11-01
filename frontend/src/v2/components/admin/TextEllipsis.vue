<template>
  <div>
    <p>
      <span>{{ isExpanded ? text : truncatedText }}</span>
      <span v-if="!isExpanded && hasMoreText">...</span>
      <a v-if="hasMoreText" href="#" @click.prevent="toggleText">
        {{ isExpanded ? " see less" : " see more" }}
      </a>
    </p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from "vue";

export default defineComponent({
  props: {
    text: {
      type: String,
      required: true,
    },
    maxLength: {
      type: Number,
      default: 130, // Default truncation length
    },
  },
  setup(props) {
    const isExpanded = ref(false);

    const hasMoreText = computed(() => props.text.length > props.maxLength);

    const truncatedText = computed(() =>
      hasMoreText.value ? props.text.slice(0, props.maxLength) : props.text
    );

    const toggleText = () => {
      isExpanded.value = !isExpanded.value;
    };

    return {
      isExpanded,
      truncatedText,
      toggleText,
      hasMoreText,
    };
  },
});
</script>

<style scoped>
a {
  color: #267dc2;
  cursor: pointer;
  text-decoration: none;
}
p {
  word-break: break-word;
}
</style>
