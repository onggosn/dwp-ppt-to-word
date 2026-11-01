<template>
  <div class="my-2">
    <v-row>
      <v-col>
        <p class="mb-2 text-gradient-grey">Title</p>
        <p>{{ props.item.title }}</p>
        <p class="mb-2 mt-3 text-gradient-grey">Method</p>
        <p>{{ resolveEventMethod(props.item.method) }}</p>
      </v-col>
      <v-col>
        <p class="mb-2 text-gradient-grey">Media</p>
        <p>
          {{
            props.item.method == 2
              ? "-"
              : resolveMeetingPlatform(props.item.media)
          }}
        </p>
        <p class="mb-2 mt-3 text-gradient-grey">Time</p>
        <p>{{ props.item.time }}</p>
      </v-col>
    </v-row>
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue";

import { useStore } from "vuex";

const props = defineProps({
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
  updated: {
    type: Object,
    default: () => {
      return {};
    },
  },
});

const store = useStore();
const listMethod = ref([]);
const listMedia = ref([]);
store.dispatch("eventStore/fetchListMeetingMethod").then((data) => {
  listMethod.value = data;
});
store.dispatch("eventStore/fetchListMeetingPlatform").then((data) => {
  listMedia.value = data;
});
function resolveMeetingPlatform(media: any): number {
  if (media) {
    const found: any = listMedia.value.find((item: any) => item.id === media);
    return found ? found.platform : 0;
  }
  return media;
}
function resolveEventMethod(method: any): number {
  if (method) {
    const found: any = listMethod.value.find((item: any) => item.id === method);
    return found ? found.value : 0;
  }
  return method;
}
</script>
<style scoped></style>
