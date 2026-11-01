<template>
  <div class="mt-3">
    <v-timeline truncate-line="both" align="start" side="end">
      <v-timeline-item
        v-for="(item, index) in items"
        :dot-color="item.approvedDate == null ? '#797979' : '#065695'"
        :key="index"
        :class="{ 'progress-here': item.approvedDate != null }"
        size="x-small"
        fill-dot
      >
        <template v-slot:icon>
          <v-icon
            color="white"
            size="18"
            :icon="item.approvedDate == null ? 'mdi-circle' : 'mdi-check'"
          ></v-icon>
        </template>
        <div class="d-flex flex-column">
          <div>
            <span
              :class="[
                item.approvedDate == null
                  ? 'text-progress-none'
                  : 'text-progress-done',
              ]"
              >{{ item.title }}</span
            >
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
  </div>
</template>

<script lang="ts" setup>
defineProps({
  items: {
    type: Array<any>,
    default: function () {
      return [];
    },
    required: true,
  },
});
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

:deep(.v-timeline) {
  justify-content: start;
}

:deep(.v-timeline-item__opposite) {
  display: none;
}
:deep(.v-timeline-divider.v-timeline-divider--fill-dot) {
  margin-left: 5px;
}
.text-progress-done {
  color: #3a416f;
  font-weight: 600;
}
.text-progress-none {
  color: #797979e5;
}
</style>
