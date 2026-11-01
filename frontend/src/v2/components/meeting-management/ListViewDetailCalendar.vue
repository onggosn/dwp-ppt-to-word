<template>
  <div v-if="isLoading">
    <paragraph-shimmer :is-loading="true" :lines="5" :random-size="true" />
  </div>
  <div v-else>
    <hr style="border-top: 1px dashed ghostwhite" />
    <v-row class="me-auto pl-3 pb-4 pt-2">
      <v-col cols="12">
        <v-card class="mt-2" style="border-radius: 15px">
          <v-table style="width: 100%">
            <tr class="tabel-tr">
              <td class="tabel-header">No</td>
              <td class="tabel-header">Agenda</td>
              <td class="tabel-header">Satker Penyaji</td>
              <td class="tabel-header">Satker Diundang</td>
              <td class="tabel-header">ADG</td>
              <td class="tabel-header">Kehadiran ADG</td>
              <td class="tabel-header">Date</td>
              <td class="tabel-header">Start Time</td>
              <td class="tabel-header">Finish Time</td>
              <td class="tabel-header">Minutes</td>
              <td class="tabel-header">Status</td>
            </tr>
            <template v-if="list.length > 0">
              <tr class="tabel-tr" v-for="(item, idx) in list" :key="idx">
                <td class="tabel-row text-center">{{ ++idx }}</td>
                <td class="tabel-row">
                  {{ item.agendaName != "" ? item.agendaName : "-" }}
                </td>
                <td class="tabel-row">
                  {{ item.presentingUnit != "" ? item.presentingUnit : "-" }}
                </td>
                <td class="tabel-row">
                  {{ item.invitedUnit != "" ? item.invitedUnit : "-" }}
                </td>
                <td class="tabel-row">
                  {{ item.adgBidang != "" ? item.adgBidang : "-" }}
                </td>
                <td class="tabel-row">
                  {{
                    item.adgBidangAttendance != ""
                      ? item.adgBidangAttendance
                      : "-"
                  }}
                </td>
                <td class="tabel-row">
                  {{ item.date != "" ? item.date : "-" }}
                </td>
                <td class="tabel-row">
                  {{ item.startTime != "" ? item.startTime : "-" }}
                </td>

                <td class="tabel-row">
                  {{ item.endTime != "" ? item.endTime : "-" }}
                </td>
                <td class="tabel-row">
                  {{ item.intervalTime != "" ? item.intervalTime : "-" }}
                </td>
                <td class="tabel-row">
                  {{ item.status != "" ? item.status : "-" }}
                </td>
              </tr>
            </template>
            <template v-else>
              <tr class="tabel-tr">
                <td class="tabel-row text-center" colspan="9">Data kosong</td>
              </tr>
            </template>
          </v-table>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>
<script lang="ts" setup>
import { ref, onMounted, defineProps } from "vue";
import { IListAgenda } from "@/v2/Type";
import { useStore } from "vuex";

const prop = defineProps({
  idEvent: {
    type: String,
    default: function () {
      return {};
    },
  },
});
onMounted(() => {
  getAgenda();
});

const store = useStore();
const list = ref<IListAgenda[]>([]);
const isLoading = ref<boolean>(false);

function getAgenda() {
  isLoading.value = true;
  store
    .dispatch("meetingStore/fetchAgendaById", prop.idEvent)
    .then((response) => {
      list.value = response.responseData?.data;
    })
    .finally(() => {
      isLoading.value = false;
    });
}
</script>
<style scoped>
.tabel-header {
  background: #f7fbfe !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  color: #065695 !important;
}
.tabel-row {
  color: #3a416f !important;
  background: white !important;
  font-size: 14px;
}
.tabel-tr {
  border-bottom: solid 1px #dbd9d9;
}
:deep(.v-card--variant-elevated) {
  box-shadow: 0px 4px 18px 0px #c0c0c040 !important;
}
</style>
