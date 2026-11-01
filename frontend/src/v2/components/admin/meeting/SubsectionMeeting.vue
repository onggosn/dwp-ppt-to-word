<template>
  <v-sheet class="my-3">
    <v-expansion-panels v-model="panel">
      <v-expansion-panel>
        <v-expansion-panel-title>
          <v-tooltip activator="parent" location="top left">
            {{ item.title }}
          </v-tooltip>
          <v-row align="center" style="cursor: pointer !important">
            <v-col cols="7" style="padding: 0 !important">
              <p class="ellipsis-1">
                {{ item.title }}
              </p>
            </v-col>
            <v-col
              cols="5"
              style="
                padding: 2px !important;
                display: flex;
                justify-content: start;
              "
            >
              <span class="item-information font-italic"
                >Last modified by: {{ item.modifiedBy || " - " }}
                <span style="font-style: normal">|</span> Date:
                {{ reformatDateEngWithMonthLong(item.lastModified) }}
                <span style="font-style: normal">|</span> Time:
                {{ reformatTimes(item.lastModified) }} WIB</span
              >
            </v-col>
          </v-row>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <div
            class="d-flex flex-wrap ml-auto ga-2"
            style="justify-content: flex-end"
          >
            <div class="pr-2">
              <btn-delete
                :title="'Delete Meeting'"
                :btn-title="'Delete Meeting'"
                :subtitle="'Are you sure delete this meeting ?'"
                :description="'Deleting the meeting will automatically delete the predefined agenda template '"
                :append-icon="true"
                :btn-color="'#d6212a'"
                :btn-icon-color="'#d6212a'"
                :btn-density="'comfortable'"
                @update="doDelete(item.id)"
              />
            </div>
          </div>
          <div>
            <MeetingContent :item="item" :bpId="bpId" @load="emit('load')" />
          </div>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-sheet>
</template>
<script setup lang="ts">
import MeetingContent from "@/v2/components/admin/meeting/MeetingContent.vue";
import BtnDelete from "@/v2/components/utils/dialog/DeleteEventDialog.vue";
import {
  reformatDateEngWithMonthLong,
  reformatTimes,
} from "@/v2/helpers/DateHelper";
import { useStore } from "vuex";
import { getCurrentInstance, ref } from "vue";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
defineProps({
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
  bpId: {
    type: [String, Number],
    required: true,
  },
});
const emit = defineEmits(["load", "on-delete-meeting"]);
const store = useStore();
const instance = ref<any>(getCurrentInstance()?.root.refs);
const panel = ref<number[]>([]);
const doDelete = (id) => {
  store
    .dispatch("adminStore/deletePDMeeting", {
      id: id,
    })
    .then((res) => {
      if (res.responseCode == "011000") {
        instance.value.toast.show({
          message: res.responseMessage,
          color: "success",
          timeout: 3000,
          icon: "mdi-check",
        });
      } else {
        instance.value.toast.show({
          message: res.responseMessage,
          color: "error",
          timeout: 3000,
          icon: "mdi-check",
        });
      }
    })
    .catch(() => {
      instance.value.toast.show({
        message: "Failed to delete meeting",
        color: "error",
        timeout: 3000,
        icon: "mdi-check",
      });
    })
    .finally(() => {
      emit("on-delete-meeting");
    });
};
</script>
<style scoped>
.item-information {
  color: #797979e5;
  font-size: 13px;
  line-height: 19.5px;
}
</style>
