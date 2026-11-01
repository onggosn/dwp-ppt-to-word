<template>
  <div class="homeCalendar">
    <h3 class="ml-4 mb-4 mt-4">{{ dateLabel }}</h3>
    <ZxVueCalendar
      lang="eng"
      mode="multiple"
      :hide-footer="true"
      :model-value="getDateMeetingEvent()"
    />
    <div style="margin-left: 20px">
      <h4
        class="text-17 fw-600 ls-1 text-blueTheme-gradien mb-2"
        style="margin-top: 15px"
      >
        Today's Schedule
      </h4>
      <div style="height: 180px; overflow: hidden auto">
        <template v-if="listTodayEvent.length == 0">
          <div
            class="text-14 fw-600"
            style="color: #9b9b9b; font-style: italic"
          >
            No more event s today
          </div>
        </template>
        <template v-else>
          <div v-for="(item, index) in listTodayEvent" :key="index">
            <div class="text-subtitle-2 mt-2">
              {{ item.meetingName }}
            </div>
            <v-row>
              <v-col cols="6" class="text-caption">
                {{ item.platform }}
              </v-col>
              <v-col cols="6" class="text-caption">
                <v-icon icon="mdi-alarm" size="x-small"></v-icon>
                {{ reformatTime(item.startDate) }}
              </v-col>
            </v-row>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>
<script>
import client from "@/library/ApiClient";
import { ZxVueCalendar } from "zx-calendar/vue";
import { getDatesInRange } from "@/helpers/utils";
import "zx-calendar/css";

export default {
  components: {
    ZxVueCalendar,
  },
  data() {
    return {
      username: "",
      dateLabel: this.getDateLabel(Date.now()),
      dates: [],
      listTodayEvent: [],
    };
  },
  mounted() {
    this.username = this.$store.state.username;
    this.getMeetingEvent();
  },
  methods: {
    getDateLabel(value) {
      const monthNames = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
      ];
      const dates = new Date(value);
      return monthNames[dates.getMonth()] + " " + dates.getFullYear();
    },
    checkDate(someDate) {
      const today = new Date();
      return (
        someDate.getDate() == today.getDate() &&
        someDate.getMonth() == today.getMonth() &&
        someDate.getFullYear() == today.getFullYear()
      );
    },
    reformatTime(input) {
      var date = new Date(input);
      return date.toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
      });
    },
    getMeetingEvent() {
      const d = new Date();
      let month = d.getMonth() + 1;
      let year = d.getFullYear();

      var data = {
        username: this.username,
        calendar: true,
        month: month,
        year: year,
      };
      client
        .getTaskMeetingByUsername({ data, store: this.$store })
        .then((value) => {
          let i = 0;
          for (i in value.plainData) {
            if (this.checkDate(new Date(value.plainData[i].startDate))) {
              this.listTodayEvent.push(value.plainData[i]);
            }
            const arrDate = getDatesInRange(
              value.plainData[i].startDate,
              value.plainData[i].endDate
            );

            arrDate.forEach((el) => {
              this.dates.push(el);
            });
          }
        });
    },
    getDateMeetingEvent() {
      return JSON.parse(JSON.stringify(this.dates));
    },
  },
};
</script>
<style scoped>
:deep(.zx-calendar) {
  pointer-events: none;
}
:deep(.zx-calendar .zx-calendar-header-wrapper) {
  display: none;
}

:deep(.zx-calendar .zx-calendar-header-wrapper .__title-wrapper) {
  justify-content: start;
  margin-left: 15px;
}

:deep(
    .zx-calendar .zx-calendar-body-wrapper .__item.is-current .__inner .__text
  ) {
  background-image: linear-gradient(to bottom, #267dc2, #065695);
  color: white;
}

:deep(
    .zx-calendar .zx-calendar-body-wrapper .__item.is-selected .__inner .__text,
    .zx-calendar
      .zx-calendar-body-wrapper
      .__item.is-range-temp
      .__inner
      .__text,
    .zx-calendar
      .zx-calendar-body-wrapper
      .__item.is-range-first-last
      .__inner
      .__text
  ) {
  width: 27px;
  height: 27px;
}
</style>
