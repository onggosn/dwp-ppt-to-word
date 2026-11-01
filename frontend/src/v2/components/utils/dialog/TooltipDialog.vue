<template>
  <template v-if="isEllipsis">
    <v-tooltip location="bottom" origin="auto" open-delay="200">
      <template #activator="{ props }">
        <span v-bind="props" ref="label" class="multiline-ellipsis">
          {{ name }}
        </span>
      </template>

      <div class="custom-tooltip-card">
        <v-card
          class="pa-2"
          max-width="300"
          elevation="5"
          style="border-radius: 15px"
        >
          <v-card-text>
            {{ name }}
          </v-card-text>
        </v-card>
      </div>
    </v-tooltip>
  </template>

  <template v-else>
    <span ref="label" class="multiline-ellipsis">
      {{ name }}
    </span>
  </template>
</template>
<script setup lang="ts">
import { defineProps, ref, onMounted, nextTick, onBeforeUnmount } from "vue";

defineProps({
  name: {
    type: String,
    required: true,
    default: "",
  },
});

const label = ref<HTMLElement | null>(null);
const isEllipsis = ref(false);
let resizeObserver: ResizeObserver | null = null;
let mutationObserver: MutationObserver | null = null;

const checkEllipsis = () => {
  if (!label.value) return;
  const el = label.value;
  isEllipsis.value = el.scrollHeight > el.clientHeight;
};

const handleResize = () => {
  nextTick(() => {
    checkEllipsis();
  });
};

onMounted(() => {
  nextTick(() => {
    checkEllipsis();

    if (label.value) {
      resizeObserver = new ResizeObserver(() => {
        checkEllipsis();
      });
      resizeObserver.observe(label.value);

      mutationObserver = new MutationObserver(() => {
        checkEllipsis();
      });
      mutationObserver.observe(label.value, {
        childList: true,
        characterData: true,
        subtree: true,
      });
    }

    window.addEventListener("resize", handleResize);
  });
});

onBeforeUnmount(() => {
  if (resizeObserver && label.value) {
    resizeObserver.unobserve(label.value);
    resizeObserver.disconnect();
  }

  if (mutationObserver) {
    mutationObserver.disconnect();
  }

  window.removeEventListener("resize", handleResize);
});
</script>

<style scoped>
.multiline-ellipsis {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  word-break: break-word;
  line-height: 1.4;
  padding-bottom: 2px;
  margin: 0;
}

:deep(.v-overlay__content) {
  background: transparent !important;
}

.custom-tooltip-card {
  position: relative;
  display: inline-block;
}

.custom-tooltip-card::before {
  content: "";
  position: absolute;
  top: -10px;
  right: 30px;
  border-width: 0 10px 10px 10px;
  border-style: solid;
  border-color: transparent transparent #ffffff transparent;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}
</style>
