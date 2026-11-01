<template>
  <v-container>
    <loading-dialog v-if="isLoading"></loading-dialog>
    <div class="text-right" style="margin-bottom: -75px">
      <v-btn
        :class="[btnStyleWide, 'btn-primary', 'ma-2']"
        @click="onClickLevel(1)"
        >Level BI-Wide</v-btn
      >
      <v-btn
        :class="[btnStyleSatker, 'btn-primary', 'ma-2']"
        @click="onClickLevel(2)"
        >Level Satker</v-btn
      >
      <v-chip class="ma-2 separator-vertical"></v-chip>
      <filter-meeting
        :item-level="btnLevelActive"
        @onFilterMeeting="applyFilter"
      ></filter-meeting>
      <!-- Start form search meeting -->
      <v-menu
        transition="slide-y-transition"
        bottom
        :close-on-content-click="false"
      >
        <template v-slot:activator="{ props }">
          <v-btn icon="" size="small" v-bind="props" class="ml-2">
            <img
              src="/images/task/searchMagnifier.svg"
              :width="21"
              :height="21"
            />
          </v-btn>
        </template>
        <v-card min-width="300">
          <v-form ref="form" type="submit" @submit.prevent="searchMeeting">
            <v-list>
              <v-list-item>
                <v-text-field
                  v-model="searchKeyword"
                  hide-details="auto"
                  style="border-radius: 10px"
                  placeholder="search"
                  variant="outlined"
                  clearable
                  :rules="[rules.required]"
                  :autofocus="true"
                ></v-text-field>
              </v-list-item>
            </v-list>
            <v-list-item>
              <v-list-item-title class="text-right">
                <v-btn
                  class="btn-primary blue-gradient text-right mb-2"
                  @click="searchMeeting"
                  >Search</v-btn
                >
              </v-list-item-title>
            </v-list-item>
          </v-form>
        </v-card>
      </v-menu>
      <!-- End form start meeting -->
    </div>
    <v-row class="pa-8">
      <FullCalendar
        ref="fullCalendar"
        :options="calendarOptions"
        style="width: 100%"
      >
        <template v-slot:eventContent="data">
          <v-row>
            <v-col cols="12">
              <v-card style="cursor: pointer">
                <v-card-text class="pa-1 text-center">
                  <div class="text-subtitle-2 text-blueTheme-gradien">
                    {{ data.event.title }}
                  </div>
                  <div class="text-caption">
                    {{ data.event.extendedProps.platform }}
                  </div>
                  <div class="text-caption">
                    <v-icon
                      icon="mdi-clock-outline primary"
                      size="x-small"
                    ></v-icon>
                    {{ reformatTime(data.event.start) }} -
                    {{ reformatTime(data.event.end) }}
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </template>
      </FullCalendar>
    </v-row>
    <detail-meeting ref="detailDialog" @showDialogListMeeting="applyFilter">
    </detail-meeting>
  </v-container>
</template>
<script lang="js">
import FullCalendar from "@fullcalendar/vue3";
import DayGridPlugin from "@fullcalendar/daygrid";
import Client from "@/library/ApiClient";
import { reformatTime } from "@/library/DateHelper";
import DetailMeeting from "@/components/meeting/DetailMeetingDialog.vue";
import FilterMeeting from "@/components/meeting/FilterMeeting.vue";
import LoadingDialog from "@/components/LoadingDialog.vue"
export default {
  components: {
    FullCalendar,
    DetailMeeting,
    FilterMeeting,
    LoadingDialog,
  },
  data: function () {
    return {
      rules: {
        required: (value) => !!value || "Please input your keywords",
      },
      errMessage: "",
      btnLevelActive: 1,
      searchKeyword: "",
      btnStyleWide: "blue-gradient",
      btnStyleSatker: "none-gradient",
      calendarOptions: {
        plugins: [DayGridPlugin],
        initialView: "dayGridMonth",
        weekends: true,
        events: [],
        height: 1500,
        headerToolbar: {
          left: "title",
          center: "prev,next",
          right:""
        },
        customButtons: {
          prev: {
            text: "Previous",
            click: () => {
              let calendarApi = this.$refs.fullCalendar.getApi();
              calendarApi.prev();
              this.getMeetingByMonth();
            },
          },
          next: {
            text: "Next",
            click: () => {
              let calendarApi = this.$refs.fullCalendar.getApi();
              calendarApi.next();
              this.getMeetingByMonth();
            },
          },
        },
        eventTimeFormat : {
            hour : '2-digit',
            minute : '2-digit'
        },
        dayMaxEventRows: true,
        views : {
            dayGridMonth : {
                dayMaxEventRows : 2
            }
        },
        eventClick: this.showDetailMeeting
      },
      isLoading: false,
    };
  },
  mounted() {
    this.getMeetingByMonth()
  },
  methods: {
    checkUserCurrentView() {
      // Method ini mengecek bulan yang sedang dilihat user
      let month = 0;
      switch (
        document
          .getElementsByClassName("fc-toolbar-title")[0]
          .innerHTML.split(" ")[0]
      ) {
        case "Januari":
          month = 1;
          break;
        case "January":
          month = 1;
          break;
        case "Februari":
          month = 2;
          break;
        case "February":
          month = 2;
          break;
        case "Maret":
          month = 3;
          break;
        case "March":
          month = 3;
          break;
        case "April":
          month = 4;
          break;
        case "Mei":
          month = 5;
          break;
        case "May":
          month = 5;
          break;
        case "Juni":
          month = 6;
          break;
        case "June":
          month = 6;
          break;
        case "Juli":
          month = 7;
          break;
        case "July":
          month = 7;
          break;
        case "Agustus":
          month = 8;
          break;
        case "August":
          month = 8;
          break;
        case "September":
          month = 9;
          break;
        case "Oktober":
          month = 10;
          break;
        case "October":
          month = 10;
          break;
        case "November":
          month = 11;
          break;
        case "Desember":
          month = 12;
          break;
        case "December":
          month = 12;
          break;
      }

      let year = parseInt(
        document
          .getElementsByClassName("fc-toolbar-title")[0]
          .innerHTML.split(" ")[1]
      );

      return [month, year];
    },
    getMeetingByMonth(filter = {}) {
      let value = this.checkUserCurrentView();
      this.isLoading = true;
      let reqData = {
        username: this.$store.state.username,
        calendar: true,
        month: value[0],
        year: value[1],
        idWorkspaceLevel: this.btnLevelActive,
        ...filter,
      };
      Client
        .getTaskMeetingByUsername({
          store: this.$store,
          data: reqData,
        })
        .then((res) => {
          let value = res.plainData;
          let temp = {};
          let i = 0;

          let events = [];
          for (i in value) {
            temp = value[i];
            temp["start"] = value[i].startDate;
            temp["end"] = value[i].endDate;
            temp["title"] = value[i].meetingName;
            events.push(temp);
            temp = {};
          }
          this.calendarOptions.events = events;
          this.isLoading = false;
        })
        .catch(() => {
          this.isLoading = false;
        });
    },
    reformatTime(item) {
      return reformatTime(item);
    },
    async showDetailMeeting(value){
        await new Promise((resolve) => setTimeout(resolve, 200));
        this.dialog = true;
        this.$refs.detailDialog.start({
            id: value.event.id,
         });
    },
    onClickLevel(level) {
      // 1 = level wide ; 2 = level satker
      if (level == 2) {
        this.btnStyleSatker = "blue-gradient";
        this.btnStyleWide = "none-gradient";
        this.btnLevelActive = 2;
      } else {
        this.btnStyleSatker = "none-gradient";
        this.btnStyleWide = "blue-gradient";
        this.btnLevelActive = 1;
      }
      this.getMeetingByMonth();
    },
    applyFilter(param){
      this.getMeetingByMonth(param)
    },
    async searchMeeting(){
      const { valid } = await this.$refs.form.validate()
      if(valid){
        this.$router.push({
          name:"search-meeting",
          params:{
            searchKeyword:this.searchKeyword,
            idLevel:this.btnLevelActive
          }
        })
      }
    }
  },
};
</script>
<style scoped>
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
.primary {
  color: #267dc2;
}
.text-subtitle-2 {
  font-size: 0.75rem !important;
}
.text-caption {
  font-size: 0.7rem !important;
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
  background-color: #b5daf7 !important;
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
</style>
