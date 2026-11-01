<template>
  <v-sheet class="ml-5 mr-3 pb-5 mb-15 bg-transparent">
    <div class="ml-md-10 mt-10">
      <div class="d-block pa-2">
        <v-btn
          variant="outlined"
          size="large"
          icon="mdi-arrow-left"
          class="ml-5 ml-md-0"
          color="#045695"
          style="border: 0.01px solid #d3d3d3; color: white !important"
          elevation="2"
          @click="router.push({ name: 'v2.meeting-management' })"
          ><v-icon icon="mdi-arrow-left" color="#045695"> </v-icon>
        </v-btn>
        <span class="text-detail">Detail Event</span>
      </div>
    </div>
    <v-sheet class="d-flex mt-4 bg-transparent" min-height="500">
      <v-sheet class="flex-xl-fill bg-transparent">
        <banner-meeting :itemBanner="meetingIdData" />
      </v-sheet>
      <v-sheet class="flex-fill bg-transparent w-100">
        <info-detail
          :item="meetingIdData"
          :isLoading="isLoading"
          @refresh="refreshData"
        />
      </v-sheet>
    </v-sheet>

    <v-row class="ml-11 mr-5 pb-5 mb-15 mt-10 pl-3">
      <v-tabs v-model="tab" bg-color="transparent ">
        <v-tab
          class="tab-header"
          :to="{
            name: 'v2.meeting-detail-description',
            params: {
              idEvent: idEvent,
            },
          }"
        >
          DESCRIPTION
        </v-tab>
        <v-tab
          class="tab-header"
          :to="{
            name: 'v2.meeting-detail-agenda',
            params: {
              idEvent: idEvent,
            },
          }"
        >
          AGENDA
        </v-tab>
        <v-tab
          class="tab-header"
          :to="{
            name: 'v2.meeting-detail-material',
            params: {
              idEvent: idEvent,
            },
          }"
        >
          MATERIAL
        </v-tab>
        <v-tab
          class="tab-header"
          :to="{
            name: 'v2.meeting-detail-result',
            params: {
              idEvent: idEvent,
            },
          }"
        >
          HASIL PEMBAHASAN
        </v-tab>
        <v-tab
          class="tab-header"
          :to="{
            name: 'v2.meeting-detail-organizer',
            params: {
              idEvent: idEvent,
            },
          }"
        >
          ORGANIZER
        </v-tab>
      </v-tabs>
      <v-col cols="12">
        <router-view @refresh="refreshData()" :ref="tab" :key="loader" />
      </v-col>
    </v-row>
  </v-sheet>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import InfoDetail from "@/v2/components/detailMeeting/InfoDetail.vue";
import BannerMeeting from "@/v2/components/detailMeeting/BannerMeeting.vue";
import { useStore } from "vuex";
import { useRoute, useRouter, RouterView } from "vue-router";

const tab = ref("description");
const route = useRoute();
const router = useRouter();
const store = useStore();
const idEvent = route.params.idEvent as string;
const meetingIdData = ref({});
const isLoading = ref<boolean>(false);
const loader = ref<number>(0);

function getMeetingId() {
  isLoading.value = true;
  const idEvent = route.params.idEvent as string;
  store
    .dispatch("meetingStore/getTaskMeetingByIdMeetingByUsername", idEvent)
    .then((response: any) => {
      meetingIdData.value = {
        bannerEvent: response.responseData.bannerEvent,
        title: response.responseData.title,
        description: response.responseData.description,
        eventend: response.responseData.eventend,
        eventlink: response.responseData.eventlink,
        eventplace: response.responseData.eventplace,
        eventTemplateType: response.responseData.eventTemplateType,
        eventstart: response.responseData.eventstart,
        eventSubtype: response.responseData.eventSubtype,
        idEventSubtype: response.responseData.idEventSubtype,
        isEdit: response.responseData.isEdit,
        liveStatus: response.responseData.liveStatus,
        isCancel: response.responseData.isCancel,
        method: response.responseData.method,
        participants: response.responseData.participants.replace(/,/g, ", "),
        participantsadg: response.responseData.participantsadg.replace(
          /,/g,
          ", "
        ),
        platform: response.responseData.platform,
        isDelete: response.responseData.isDelete,
        isPublish: response.responseData.isPublish,
      };
      store.commit("meetingStore/setListAdg", response.responseData.listADG);
    })
    .catch(() => {
      meetingIdData.value = {};
    })
    .finally(() => {
      isLoading.value = false;
    });
}

onMounted(() => {
  getMeetingId();
});

const refreshData = () => {
  loader.value++;
  getMeetingId();
};
</script>

<style lang="scss" scoped>
.text-detail {
  font-family: Poppins;
  font-size: 16px;
  font-style: normal;
  font-weight: 600;
  line-height: 15px;
  letter-spacing: 0.5px;
  background: var(
    --Gradient-CTA,
    linear-gradient(92deg, #065695 -46.47%, #267dc2 157.9%)
  );
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-left: 17px;
}
:deep(.tab-header.v-slide-group-item--active) {
  background: none !important;
  color: #ff000d !important;
  border: none !important;
  background-clip: text;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: #ff000d !important;
}
.tab-header {
  color: #065695;
  font-weight: 600;
}

:deep(.v-tab--selected .v-tab__slider) {
  height: 2px;
  border-radius: 10px;
  color: #ff000d;
}

:deep(.v-tab.v-tab) {
  height: 35px;
  font-weight: 900;
  color: #267dc2 !important;
}
</style>
