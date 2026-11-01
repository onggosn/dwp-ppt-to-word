<template>
  <mobile-layout-v2 v-if="mobileLayout" />
  <desktop-layout-v2 v-else />
</template>

<script setup lang="ts">
import { useDisplay } from "vuetify";
import DesktopLayoutV2 from "./DesktopLayoutV2.vue";
import MobileLayoutV2 from "./MobileLayoutV2.vue";
import { ref, onMounted, computed } from "vue";

const isMobile = ref(false);
const { width } = useDisplay();

onMounted(() => {
  if (typeof window !== "undefined" && window.navigator) {
    const agentString = window.navigator.userAgent;
    isMobile.value = detectMobile(agentString);
  }
});

const detectMobile = (agent) => {
  if (!agent) return false;
  const lowercasedAgent = agent.toLowerCase();
  const ANY_NON_DESKTOP_REGEX =
    /android.*mobile|iphone|ipod|windows phone|ipad|android(?!.*mobile)|webos/i;
  return ANY_NON_DESKTOP_REGEX.test(lowercasedAgent);
};

const mobileLayout = computed(() => {
  return isMobile.value || width.value <= 1024;
});
</script>
