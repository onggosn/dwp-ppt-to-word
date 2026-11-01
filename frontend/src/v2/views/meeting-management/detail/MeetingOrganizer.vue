<template>
  <div>
    <v-card class="mt-5 mr-5 card-organizer" outlined>
      <v-row
        no-gutters
        v-for="(item, index) in itemOrganizer"
        :key="index"
        class="mt-5 ml-2 mr-5 mb-5 align-center"
      >
        <v-col cols="1">
          <div style="margin-top: 10px">
            <v-card-actions class="icon-organizer">
              <v-img
                :src="require('@/v2/assets/icon/add-user.svg')"
                alt="Icon"
                class="icon-people"
              ></v-img>
            </v-card-actions>
          </div>
        </v-col>
        <v-col cols="11" class="mt-2">
          <div class="name-organizer">{{ item.name || "-" }}</div>
          <div class="name-grade">{{ item.grade || "-" }}</div>
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { TListOrganizer } from "@/v2/Type";
const itemOrganizer = ref<TListOrganizer[]>();
import { useStore } from "vuex";
import { useRoute } from "vue-router";
const route = useRoute();
const store = useStore();
const idEvent = route.params.idEvent as string;

function getMeetingOrganizer() {
  store
    .dispatch("meetingStore/getOrganizerByMeetingId", idEvent)
    .then((response: any) => {
      itemOrganizer.value = response.responseData?.data;
    });
}
onMounted(() => {
  getMeetingOrganizer();
});
</script>

<style scoped>
.icon-organizer {
  display: flex;
  width: 50px;
  height: 52px;
  padding: 3px 4px;
  justify-content: center;
  align-items: center;
  gap: 8px;
  border-radius: 200px;
  background: var(--Neutral-30, #ededed);
  margin-left: 28px;
}
.icon-people {
  width: 21.315px;
  height: 27px;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  margin-left: 10px;
}
.card-organizer {
  border-radius: 12px;
  background: var(--White-Colot, #fff);
  box-shadow: 0px 4px 18px 0px rgba(192, 192, 192, 0.25);
}
.name-organizer {
  color: var(--Neutral-100, #25282b);
  font-family: Poppins;
  font-size: 20px;
  font-style: normal;
  font-weight: 700;
  line-height: 32px;
}
.name-grade {
  color: var(--Neutral-90, #404040);
  font-family: Poppins;
  font-size: 16px;
  font-style: normal;
  font-weight: 400;
  line-height: 24px;
}
</style>
