<template>
  <v-card
    variant="flat"
    class="custom-card"
    hover
    @click="getDetailMeeting(item.id)"
  >
    <v-card-text>
      <div class="d-flex justify-space-between">
        <div class="pa-2">
          <div>
            <v-chip :class="`chip-bg-${item.color}`">{{
              item.eventTemplateType
            }}</v-chip>
          </div>
          <div
            class="text-title mt-2 ellipsis-1"
            v-html="highlightText(item.title)"
          ></div>
          <div class="text-caption color-grey">
            <v-icon icon="mdi-map-marker-outline" size="small"></v-icon>
            {{ item.meetingPlatform }}
          </div>
          <div class="text-caption color-grey">
            <v-icon icon="mdi-clock-time-four-outline" size="small"></v-icon>
            {{ item.startTime }} -
            {{ item.endTime }}
          </div>
        </div>
        <div>
          <v-img
            :src="require('@/v2/assets/icon/icon-calendar-gradient.svg')"
            width="100"
          ></v-img>
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>
<script lang="ts" setup>
import { useRouter } from "vue-router";

const router = useRouter();
const props = defineProps({
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
  query: {
    type: String,
    default: () => {
      return {};
    },
  },
});

function highlightText(query: string) {
  const escapedQuery = props.query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return query.replaceAll(
    RegExp("(" + escapedQuery + ")", "ig"),
    `<span style="background: #F1BD35;
">$1</span>`
  );
}

function getDetailMeeting(param: any) {
  router.push({
    name: "v2.meeting-detail-description",
    params: { idEvent: param },
  });
}
</script>
<style scoped>
.custom-card {
  box-shadow: 0px 4px 18px 0px #c0c0c040;
  border-radius: 23px;
  cursor: pointer;
  margin-bottom: 15px;
}
.color-grey {
  color: #4b4b4b;
}
.text-title {
  font-size: 18px;
  font-weight: 600;
  line-height: 27px;
  letter-spacing: 0em;
  text-align: left;
}
.ellipsis-1 {
  white-space: pre-wrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
}
.chip-bg-red {
  color: white;
  background-color: #de0000 !important;
}
.chip-bg-blue {
  color: white;
  background-color: #0089cd !important;
}
.chip-bg-grey {
  color: white;
  background-color: #727272 !important;
}
</style>
