<template>
  <v-container fluid class="pl-10">
    <loading-dialog v-if="isLoading"></loading-dialog>
    <div class="d-flex justify-end mr-4" style="margin-bottom: -75px">
      <div class="d-flex flex-row" style="column-gap: 16px">
        <v-btn
          prepend-icon="mdi-plus"
          class="bg-gradient-darkblue"
          v-if="canCreate"
          elevation="4"
          size="large"
          style="color: white; border-radius: 15px"
          @click="showNewMeetingDialog"
          >New Meeting</v-btn
        >
        <v-select
          density="compact"
          variant="solo"
          :items="calendarTypeItem"
          v-model="calendarType"
          @update:modelValue="getCalendarType"
          menu-icon="mdi-unfold-more-horizontal"
        >
        </v-select>
      </div>
      <div class="ml-2">
        <v-chip class="mt-4 separator-vertical"></v-chip>
      </div>
      <div v-if="canDownload" class="ml-2">
        <v-btn icon size="small" class="mr-3">
          <v-tooltip activator="parent" location="top">Download</v-tooltip>
          <v-icon
            icon="mdi-download"
            color="#065695"
            @click="downLoadLog()"
          ></v-icon>
        </v-btn>
      </div>
      <div>
        <FilterMeeting @onFilterMeeting="applyFilter"></FilterMeeting>
      </div>
      <div>
        <SearchCalendar
          :typeSearch="`calendar`"
          :typeFilter="reqData"
        ></SearchCalendar>
      </div>
    </div>
    <v-row class="pa-8">
      <FullCalendar
        ref="fullCalendar"
        :options="calendarOptions"
        style="width: 100%"
      >
        <template v-slot:eventContent="data">
          <!-- <pre>{{ data.event.extendedProps }}</pre> -->

          <ListViewCalendar
            v-model="list"
            :itemEvent="data.event.extendedProps"
            v-if="calendarType === 'list'"
          ></ListViewCalendar>

          <v-card
            v-else-if="data.event.extendedProps.cardFlex == 'card-flex'"
            hover
            variant="flat"
            :class="[
              'border-radius-dwp mb-2',
              `card-bg-${data.event.extendedProps.colorEvent}`,
            ]"
            style="height: 100%"
          >
            <v-card-text>
              <div class="d-flex">
                <div class="mr-2">
                  <v-chip
                    variant="flat"
                    size="small"
                    :class="`chip-bg-${data.event.extendedProps.colorEvent}`"
                    >{{ data.event.extendedProps.item.eventTemplateType }}
                  </v-chip>
                </div>
                <div
                  :class="[
                    'text-body-2 font-weight-bold',
                    `text-title-${data.event.extendedProps.colorEvent}`,
                  ]"
                >
                  {{ data.event.title }}
                </div>
                <div class="mr-2 text-caption">
                  <v-icon icon="mdi-map-marker" size="x-small"></v-icon>
                  {{ data.event.extendedProps.item.meetingPlatform }}
                </div>
                <div class="mr-2 text-caption">
                  <v-icon
                    icon="mdi-clock-time-four-outline"
                    size="x-small"
                  ></v-icon>
                  {{ reformatTime(data.event.extendedProps.item.startDate) }}
                  -
                  {{ reformatTime(data.event.extendedProps.item.endDate) }}
                </div>
                <div class="mr-2">
                  <v-icon
                    size="x-small"
                    icon="mdi-paperclip"
                    v-if="data.event.extendedProps.item.isMaterial == true"
                  ></v-icon>
                </div>
              </div>
            </v-card-text>
          </v-card>
          <v-card
            v-else
            hover
            variant="flat"
            :class="[
              'border-radius-dwp mb-2',
              `card-bg-${data.event.extendedProps.colorEvent}`,
            ]"
            style="height: 100%"
            :max-width="
              data.event.extendedProps.isMoreDays === true ||
              calendarType == 'daily'
                ? 'auto'
                : '200'
            "
          >
            <v-card-text>
              <div class="d-flex justify-space-between">
                <v-chip
                  variant="flat"
                  size="small"
                  :class="`chip-bg-${data.event.extendedProps.colorEvent}`"
                  >{{ data.event.extendedProps.item.eventTemplateType }}</v-chip
                >
                <v-icon
                  size="x-small"
                  icon="mdi-paperclip"
                  v-if="data.event.extendedProps.item.isMaterial == true"
                ></v-icon>
              </div>
              <div
                :class="[
                  'text-body-2 mt-2 font-weight-bold ellipsis',
                  `text-title-${data.event.extendedProps.colorEvent}`,
                ]"
              >
                <v-tooltip activator="parent" location="top">{{
                  data.event.title
                }}</v-tooltip>
                {{ data.event.title }}
              </div>
              <div class="text-caption">
                <v-icon icon="mdi-map-marker" size="x-small"></v-icon>
                {{ data.event.extendedProps.item.meetingPlatform }}
              </div>
              <div class="text-caption">
                <v-icon
                  icon="mdi-clock-time-four-outline"
                  size="x-small"
                ></v-icon>
                {{ reformatTime(data.event.extendedProps.item.startDate) }} -
                {{ reformatTime(data.event.extendedProps.item.endDate) }}
              </div>
            </v-card-text>
          </v-card>
        </template>
      </FullCalendar>
    </v-row>
  </v-container>

  <CreateRDGDialog ref="createRDGDialog" @created="loadAfterCreate" />
</template>
<script lang="ts" setup>
import { ref, onMounted } from "vue";
import store from "@/store";
import FullCalendar from "@fullcalendar/vue3";
import DayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import listPlugin from "@fullcalendar/list";
import FilterMeeting from "@/v2/components/meeting-management/FilterMeeting.vue";
import LoadingDialog from "@/v2/components/loading/LoadingDialog.vue";
import SearchCalendar from "@/v2/components/workspace/WorkspaceSearch.vue";
import CreateRDGDialog from "@/v2/components/meeting-management/CreateRDGDialog.vue";
import Clientv2 from "@v2/library/ApiClient";
import { useStore } from "vuex";
import { TRequestEventCalendar, TCalendarTypeItem } from "@v2/Type.d";
import {
  formatDateYmd,
  reformatTime,
  getTimeRange,
  calculateDaysBetweenDates,
  getDateWithoutTime,
} from "@/v2/helpers/datetime";
import { getColorChip } from "@/v2/helpers/color";
import { useRouter } from "vue-router";
import ListViewCalendar from "@/v2/components/meeting-management/ListViewCalendar.vue";

const router = useRouter();
const list = ref<any>();
const storeMeeting = useStore();
const fullCalendar = ref<any>();
const isLoading = ref<boolean>(false);
const createRDGDialog = ref();

const calendarTypeItem: TCalendarTypeItem[] = [
  { value: "monthly", title: "Monthly View" },
  { value: "daily", title: "Daily View" },
  { value: "list", title: "List View" },
];
const calendarType = ref<string>("monthly");
const calendarOptions = ref<any>({
  plugins: [DayGridPlugin, timeGridPlugin, listPlugin],
  initialView: "dayGridMonth",
  weekends: true,
  events: [],
  height: 1500,
  dayHeaders: true,
  allDaySlot: false,
  slotMinTime: "06:00:00",
  slotMaxTime: "24:00:00",
  eventColor: "transparent",
  eventBorderColor: "transparent",
  slotEventOverlap: false,
  headerToolbar: {
    left: "title",
    center: "prev,next",
    right: "",
  },
  customButtons: {
    prev: {
      text: "Previous",
      click: () => {
        let calendarApi = fullCalendar.value.getApi();
        calendarApi.prev();
        getMeetingByMonth();
      },
    },
    next: {
      text: "Next",
      click: () => {
        let calendarApi = fullCalendar.value.getApi();
        calendarApi.next();
        getMeetingByMonth();
      },
    },
  },
  eventTimeFormat: {
    hour: "2-digit",
    minute: "2-digit",
  },
  views: {
    dayGridMonth: {
      dayMaxEventRows: 1,
      dayMaxEvents: 1,
    },
    timeGrid: {
      dayHeaders: false,
    },
  },
  eventClick: getDetailMeeting,
  moreLinkContent: function (args) {
    return args.num + " more";
  },
  noEventsContent: function () {
    return {
      html: `
        <div class="empty-state"><img src="/images/no_available_state.svg" class="img-no-available" alt="No events" /></div>
      `,
    };
  },
});
const filter = ref({
  eventTypeFilter: [] as number[],
  eventSubTypeListFilter: [] as number[],
  eventAdgFilter: [] as number[],
  eventSearching: "" as string,
  komite: [] as number[],
});

const reqData = ref<TRequestEventCalendar>({
  calendarType: calendarType.value,
  dateFilter: formatDateYmd(new Date()),
  ...filter.value,
});
onMounted(() => {
  getMeetingByMonth();
  checkUserRoleMrdg();
});

function getMeetingByMonth(): void {
  isLoading.value = true;
  let date: any = fullCalendar.value.getApi().getDate();
  reqData.value = {
    calendarType: calendarType.value,
    dateFilter: formatDateYmd(date),
    ...filter.value,
  };

  storeMeeting
    .dispatch("meetingStore/getListEventByCalendarType", reqData.value)
    .then((res: any) => {
      const event = res.responseData.data.map((el: any) => {
        return {
          id: el.id,
          start: el.startDate,
          end: el.endDate,
          title: el.title,
          colorEvent: getColorChip(el.eventTemplateType),
          item: el,
          cardFlex: isCardItemFlex(getTimeRange(el.startDate, el.endDate)),
          isMoreDays: isMoreDays(el.startDate, el.endDate),
        };
      });
      calendarOptions.value.events = event;
    })
    .finally(() => {
      isLoading.value = false;
    });
}

const downLoadLog = () => {
  reqData.value.calendarType =
    calendarType.value === "list" ? "daily" : calendarType.value;

  Clientv2.downloadLogFile({ data: reqData.value }).then((response) => {
    const data = response.responseData?.filebyte;
    const linkSource = `data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,${data}`;
    const downloadLink = document.createElement("a");
    downloadLink.download = response.responseData?.documentName;
    downloadLink.href = linkSource;
    downloadLink.click();
  });
};

const canDownload = ref<boolean>(false);
const canCreate = ref<boolean>(false);
const checkUserRoleMrdg = () => {
  const payload = {
    username: store.state?.username,
  };
  Clientv2.checkRoleMrdgByUsername({ data: payload }).then((response) => {
    canDownload.value = response.responseData?.isDownload;
    canCreate.value = response.responseData?.isCreateNewMeeting;
  });
};

function getCalendarType(): void {
  switch (calendarType.value) {
    case "monthly":
      getMeetingByMonth();
      fullCalendar.value.calendar.changeView("dayGridMonth");
      break;
    case "daily":
      getMeetingByMonth();
      fullCalendar.value.calendar.changeView("timeGrid");
      break;
    case "list":
      getMeetingByMonth();
      fullCalendar.value.calendar.changeView("listDay");
      break;
  }
}

function getDetailMeeting(param: any) {
  let id = param.event.id;
  if (calendarType.value !== "list") {
    router.push({
      name: "v2.meeting-detail-description",
      params: { idEvent: id },
    });
  }
}

function isCardItemFlex(param: any) {
  let result = "";
  if (param < 1 && calendarType.value === "daily") {
    result = "card-flex";
  }
  return result;
}
function isMoreDays(date1: string, date2: string): boolean {
  const firstDateOnly = getDateWithoutTime(date1);
  const secondDateOnly = getDateWithoutTime(date2);

  const days = calculateDaysBetweenDates(firstDateOnly, secondDateOnly);
  if (days > 0) {
    return true;
  } else {
    return false;
  }
}

function applyFilter(_filter: any) {
  filter.value = _filter;
  getMeetingByMonth();
}

function showNewMeetingDialog() {
  createRDGDialog.value.show();
}

function loadAfterCreate(isCreated) {
  if (isCreated) {
    getMeetingByMonth();
  }
}
</script>

<style scoped>
:deep(.fc .fc-scroller-liquid) {
  scrollbar-width: none;
}
:deep(.fc .fc-scroller) {
  overflow-x: scroll !important;
  scrollbar-width: none;
}
:deep(.fc .fc-popover) {
  border-radius: 10px;
}
:deep(.fc .fc-popover-header) {
  border-radius: 10px 10px 0 0;
}
:deep(.fc .fc-daygrid-event) {
  margin-left: 10px !important;
}
:deep(.fc .fc-more-popover .fc-popover-body) {
  overflow-y: scroll !important;
  height: 230px;
}
:deep(.v-card) {
  box-shadow: 0px 3px 7px 0px #85858540 !important;
}
:deep(.fc .fc-col-header-cell) {
  text-align: start !important;
  padding-left: 20px !important;
  padding-bottom: 30px !important;
}
:deep(.fc .fc-list-event-time) {
  display: none !important;
}
:deep(.fc .fc-list-day) {
  display: none !important;
}
:deep(.fc .fc-listDay-view) {
  border: none !important;
}
:deep(a.fc-event, a.fc-event:hover) {
  background: transparent;
}
:deep(.fc .fc-toolbar.fc-header-toolbar) {
  margin-bottom: 3.5em;
}
:deep(.fc .fc-scroller-liquid-absolute) {
  scrollbar-width: none;
}
:deep(.fc-timegrid-col.fc-day-today) {
  background-color: transparent !important;
}
:deep(.fc .fc-timegrid-slots) {
  border-top: solid 2px #d6212a;
  border-bottom: solid 2px #d6212a;
}
:deep(.fc-timegrid-event-harness > .fc-timegrid-event) {
  border-radius: 15px;
  border: none !important;
  box-shadow: none !important;
}
:deep(.fc .fc-timegrid-slot) {
  height: 3em !important;
  border-bottom: solid 2px #e3e3e3 !important;
}
:deep(.fc .fc-timegrid-slot-minor) {
  height: 3em !important;
  border-bottom: solid 2px #d6212a !important;
}
:deep(.fc .fc-timegrid-slot-label .fc-timegrid-slot-minor) {
  border: none !important;
}
:deep(.fc .fc-daygrid-more-link) {
  background-color: white;
  margin-left: 15px;
  border-radius: 10px;
  width: 90%;
  height: 27px;
  padding-left: 10px;
  padding-top: 5px;
  box-shadow: 0px 3px 7px 0px #85858540;
  font-weight: bold;
  color: #065695;
  margin-bottom: 10px;
}
:deep(.v-field--variant-solo, .v-field--variant-solo-filled) {
  border-radius: 15px;
  color: red;
  font-size: 15px;
  box-shadow: 0px 3px 7px 0px #85858540 !important;
}
:deep(
    .v-input--density-compact .v-field--variant-outlined,
    .v-input--density-compact .v-field--single-line,
    .v-input--density-compact .v-field--no-label
  ) {
  --v-field-padding-bottom: 1px;
}
.card-event {
  border-left: 5px solid;
}
.card-flex {
  display: flex;
  align-items: self-end;
}

.card-bg-red {
  background-color: #fbd6d6;
  border-left: 4px solid var(--Gradient-Red, #d6212a);
}
.card-bg-blue {
  background-color: #daf2fe;
  border-left: 4px solid var(--Gradient-Blue, #065695);
}
.card-bg-grey {
  background-color: white;
  border-left: 4px solid var(--Gradient-Grey, #727272);
}
.chip-bg-red {
  background-color: #de0000 !important;
}
.chip-bg-blue {
  background-color: #0089cd !important;
}
.chip-bg-grey {
  background-color: #727272 !important;
}
.text-title-red {
  background: var(
    --Gradient-Red,
    linear-gradient(180deg, #d6212a 0%, #ff000d 100%)
  );
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.text-title-blue {
  background: var(
    --Gradient-Blue,
    linear-gradient(180deg, #065695 0%, #267dc2 100%)
  );
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.text-title-grey {
  background: var(
    --Gradient-Grey,
    linear-gradient(180deg, #4b4b4b 0%, #605f5f 100%)
  );
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.btn-primary {
  box-shadow: 0px 3px 7px rgba(133, 133, 133, 0.25);
  border-radius: 10px;
  height: 34px;
}

.blue-gradient {
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%);
  color: white !important;
}
.none-gradient {
  color: red !important;
  background: white !important;
}
.text-subtitle-2 {
  font-size: 0.75rem !important;
}
.text-caption {
  font-size: 0.7rem !important;
  color: #4b4b4b;
  white-space: pre-wrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
}
:deep(.fc-scrollgrid-sync-table tr) {
  height: 22% !important;
}
:deep(.fc-button-primary) {
  color: #d6212a !important;
  background: none !important;
  border: none !important;
}
:deep(.fc-toolbar) {
  justify-content: normal !important;
}
:deep(.fc .fc-button .fc-icon) {
  vertical-align: baseline !important;
}
:deep(.fc-toolbar-title) {
  padding-right: 10px;
}
:deep(.fc-daygrid-day-number) {
  border-top: solid !important;
  border-top-color: #d6212a !important;
  text-decoration: none;
  width: 90%;
  color: #4b4b4b;
}
:deep(.fc-scrollgrid) {
  border: none !important;
}
:deep(.fc th) {
  border-style: none !important;
}
:deep(.fc td) {
  border-style: none !important;
}
:deep(.fc-daygrid-day-top) {
  font-size: 29px;
  text-align: left;
}
:deep(.fc-daygrid-day-frame) {
  padding-right: 10px;
  height: 220px !important;
}
:deep(.fc .fc-daygrid-day.fc-day-today) {
  background-color: #d4e7f6 !important;
  border-radius: 10px;
}
:deep(.fc .fc-list-empty) {
  background-color: transparent;
  display: flex;
  height: 100%;
  justify-content: center;
  align-items: baseline;
}
.separator-vertical {
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  ) !important;
  transform: rotate(90deg);
  height: 1px !important;
}

:root {
  --Gradient-Blue: linear-gradient(180deg, #065695 0%, #267dc2 100%);
  --Gradient-Red: linear-gradient(180deg, #d6212a 0%, #ff000d 100%);
  --Gradient-Grey: linear-gradient(
    92.72deg,
    rgba(121, 121, 121, 0.9) 0%,
    rgba(187, 187, 187, 0.9) 152.21%
  );
}
/* remove space  between New Meeting and filter button */
:deep(.v-text-field .v-input__details) {
  padding-inline-start: 0;
  padding-inline-end: 0;
}
</style>
