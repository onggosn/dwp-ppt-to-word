<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-expansion-panels v-model="panel">
          <v-expansion-panel>
            <v-expansion-panel-title>
              <div class="d-flex">
                <div class="mr-5 py-3">
                  <v-img
                    :src="require('@/v2/assets/icon/icon-calendar.svg')"
                    width="45"
                  ></v-img>
                </div>
                <div class="me-auto pt-3 pb-3">
                  <div>
                    <v-chip :class="`chip-bg-${itemEvent.colorEvent}`">
                      {{ itemEvent.item.eventTemplateType }}
                    </v-chip>
                  </div>
                  <v-btn
                    variant="text"
                    color="transparent"
                    class="text-h5 pt-2 text-20 font-weight-medium color-grey ellipsis px-0"
                    @click.stop="getDetailMeeting($event, itemEvent.item.id)"
                  >
                    <span style="color: #065695">
                      {{ itemEvent.item.title }}
                    </span>
                  </v-btn>

                  <div class="text-caption color-grey">
                    <v-icon
                      icon="mdi-map-marker-outline"
                      color="#797979E5"
                      size="small"
                    ></v-icon>
                    {{ itemEvent.item.meetingPlatform }}
                  </div>
                  <div class="text-caption color-grey">
                    <v-icon
                      icon="mdi-clock-time-four-outline"
                      size="small"
                      color="#797979E5"
                    ></v-icon>
                    {{ itemEvent.item.startTime }} -
                    {{ itemEvent.item.endTime }}
                  </div>
                </div>
              </div>
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <ListViewDetailCalendar
                :idEvent="itemEvent.item.id"
              ></ListViewDetailCalendar>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
  </div>
</template>
<script lang="ts" setup>
import { defineProps, ref } from "vue";
import { useRouter } from "vue-router";
import ListViewDetailCalendar from "@/v2/components/meeting-management/ListViewDetailCalendar.vue";

const router = useRouter();
defineProps({
  itemEvent: {
    type: Object,
    default: function () {
      return {};
    },
  },
});

const panel = ref<number[]>([]);

function getDetailMeeting(event, id: string) {
  event.stopPropagation();
  router.push({
    name: "v2.meeting-detail-description",
    params: { idEvent: id },
  });
}
</script>
<style scoped>
:deep(
    .v-expansion-panel-title--active > .v-expansion-panel-title__overlay,
    .v-expansion-panel-title[aria-haspopup="menu"][aria-expanded="true"]
      > .v-expansion-panel-title__overlay
  ) {
  opacity: 0 !important;
}
:deep(.v-expansion-panel) {
  border-radius: 16px;
}
:deep(.v-expansion-panel__shadow) {
  box-shadow: 0px 2px 4px 0px #0000001f !important;
}
:deep(.v-table) {
  border-radius: 12px;
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
.color-grey {
  color: #4b4b4b;
}
:deep(.v-img__img) {
  width: 100%;
}
</style>
<script lang="ts" setup></script>
