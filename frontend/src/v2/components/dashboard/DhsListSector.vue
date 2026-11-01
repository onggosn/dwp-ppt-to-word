<template>
  <v-sheet class="my-3">
    <v-expansion-panels v-model="panel">
      <v-expansion-panel :value="item.sectorId">
        <v-expansion-panel-title>
          <v-tooltip activator="parent" location="top left">
            {{ item.sectorName }}
          </v-tooltip>
          <v-row align="center" style="cursor: pointer !important">
            <v-col cols="5" style="padding: 0 !important">
              <p
                style="
                  color: #4b4b4b;
                  max-height: 24px;
                  overflow: hidden;
                  padding-right: 32px;
                  text-overflow: ellipsis;
                  white-space: nowrap;
                  font-weight: bold;
                "
              >
                {{ item.sectorName }}
              </p>
            </v-col>
            <v-col
              cols="2"
              style="
                padding: 2px !important;
                display: flex;
                justify-content: start;
              "
            >
              <v-chip :style="chipStyles[item?.status?.toLocaleLowerCase()]">
                {{ item.status }}
              </v-chip>
            </v-col>
            <v-col
              cols="5"
              style="
                padding: 2px !important;
                display: flex;
                justify-content: start;
              "
            >
              <span class="item-information font-italic ellipsis"
                >Last modified by: {{ item.modifiedBy || " - " }}
                <span style="font-style: normal">|</span> Date:
                {{
                  item.modifiedDate
                    ? formatTimeEngToMonthInd(item.modifiedDate)
                    : " - "
                }}
                <span style="font-style: normal">|</span> Time:
                {{
                  item.modifiedDate ? reformatTimes(item.modifiedDate) : " - "
                }}
                WIB</span
              >
            </v-col>
          </v-row>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-row class="mx-2">
            <v-col cols="6" class="mt-2">
              <v-row>
                <v-col cols="12" class="px-0">
                  <div class="text-grey-theme fw-600 text-13">Pengaju</div>
                  <div class="text-black-theme text-13">
                    <text-ellipsis :text="pengaju" />
                  </div>
                </v-col>
              </v-row>
            </v-col>
            <v-col cols="4" class="mt-2">
              <v-row>
                <v-col cols="12" class="px-0">
                  <div class="text-grey-theme fw-600 text-13">Penyetuju</div>
                  <div class="text-black-theme text-13">
                    <text-ellipsis :text="penyetuju" />
                  </div>
                </v-col>
              </v-row>
            </v-col>
            <v-col cols="2" class="mt-2 text-right"></v-col>
          </v-row>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-sheet>
</template>
<script setup lang="ts">
import TextEllipsis from "@/v2/components/admin/TextEllipsis.vue";
import { chipStyles } from "@/v2/helpers/color";
import {
  reformatTimes,
  formatTimeEngToMonthInd,
} from "@/v2/helpers/DateHelper";
import { ref, computed } from "vue";

const props = defineProps({
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
});

const panel = ref<number[]>([]);

const pengaju = computed(() => {
  return props.item?.pengaju?.name || "-";
});

const penyetuju = computed(() => {
  return props.item?.penyetuju?.name || "-";
});
</script>
<style scoped>
.item-information {
  color: #797979e5;
  font-size: 13px;
  line-height: 19.5px;
}
.text-grey-theme {
  color: #a6abc7;
}
.text-black-theme {
  color: #4b4b4b;
}
.btn-outline-rounded {
  border-radius: 10px;
  letter-spacing: -0.5px;
}
</style>
