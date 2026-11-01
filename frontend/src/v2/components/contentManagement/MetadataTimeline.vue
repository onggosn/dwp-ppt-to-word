<template>
  <div class="mt-2">
    <v-timeline :truncate-line="truncateLine" align="start" side="end">
      <v-timeline-item
        v-for="(item, index) in showItems"
        :dot-color="getDotColor(item)"
        :key="item.title"
        :class="{ 'progress-here': index === progressIndex }"
        size="x-small"
        fill-dot
      >
        <template v-slot:icon>
          <v-icon color="white" size="18" :icon="getIcon(item)"></v-icon>
        </template>
        <div class="d-flex flex-column" style="width: 326px">
          <div>
            <span :class="[getTextColor(item)]">
              {{ item.title }}
            </span>
            <div class="text-caption">
              <v-icon color="grey">mdi-account</v-icon>
              {{ item.name === "" ? "-" : `by ${item.name}` }}
            </div>
          </div>
          <div>
            <div class="text-caption">
              <v-icon color="grey">mdi-clock-outline</v-icon>
              {{
                item.approvedDate === "" || item.approvedDate === null
                  ? "-"
                  : item.approvedDate
              }}
            </div>
          </div>
        </div>
      </v-timeline-item>
    </v-timeline>
    <div
      class="ml-8 mt-3 text-progress-done"
      style="cursor: pointer"
      @click="showMore = true"
      v-if="!showMore && needShowMore"
    >
      see all progress
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
const props = defineProps(["items", "status"]);

const progressIndex = computed(() => {
  return props.items.reduce((count, item) => {
    if (item.approvedDate === "") return count;
    else return count + 1;
  }, -1);
});

const showMore = ref<boolean>(false);
const needShowMore = computed((): boolean => props.items.length > 4);
const showItems = computed(() => {
  if (showMore.value === false) return props.items.slice(0, 4);
  return props.items;
});
const truncateLine = computed((): string => {
  if (needShowMore.value && showMore.value === false) return "start";
  return "both";
});

function getIcon(item: any): string {
  if (item.approvedDate != "" && item.isReject) return "mdi-close";
  else if (item.approvedDate != "") return "mdi-check";
  return "mdi-circle";
}

function getDotColor(item: any): string {
  if (item.approvedDate != "" && item.isReject) return "#ea111c";
  else if (item.approvedDate != "") return "#065695";
  return "#797979";
}

function getTextColor(item: any): string {
  if (item.approvedDate != "" && item.isReject) return "text-progress-rejected";
  else if (item.approvedDate != "") return "text-progress-done";
  return "text-progress-none";
}
</script>

<style scoped lang="scss">
:deep(.v-timeline-item:has(~ .progress-here)) {
  & .v-timeline-divider__after,
  & .v-timeline-divider__before {
    background: #065695;
  }
}

:deep(.progress-here .v-timeline-divider__before) {
  background: #065695;
}

.text-progress-done {
  color: #3a416f;
}

.text-progress-none {
  color: #797979e5;
}

.text-progress-rejected {
  color: #ea111c;
}
</style>
