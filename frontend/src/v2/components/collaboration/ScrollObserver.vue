<template>
  <div>
    <document-template-local
      v-for="(flag, key) in tocList"
      :observer="observer"
      :id="key"
      :key="key"
      :isLoaded="flag"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import DocumentTemplateLocal from "./DocumentTemplateLocal.vue";

const store = useStore();
const router = useRouter();

const tocList = ref<Record<string, boolean>>(
  store.getters["contentStore/getTOCDoc"].reduce((obj, tocItem) => {
    obj[tocItem.idBpDocument] = false;
    return obj;
  }, {})
);

const observer = ref(
  new IntersectionObserver(callback, {
    root: document,
    threshold: 1.0,
  })
);

function callback(entries) {
  entries.forEach(({ target, isIntersecting }) => {
    if (!isIntersecting) {
      return;
    } else {
      tocList.value[target.id] = true;
      router.replace({ hash: `/#${target.id}` });
    }
  });
}

onUnmounted(() => {
  observer.value.disconnect();
});
</script>
