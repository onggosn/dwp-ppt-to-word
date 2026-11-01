<template>
  <div class="buku2d-detail">
    <v-expansion-panels v-model="panel" multiple>
      <v-expansion-panel
        :value="item.sectorId"
        v-for="item in item"
        :key="item.sectorId"
      >
        <v-expansion-panel-title>
          <v-row align="center" style="cursor: pointer !important">
            <v-col cols="6" style="padding: 0 !important">
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
              <v-chip :style="matchChipStyle(item.status) as StyleValue">
                {{ item.status }}
              </v-chip>
            </v-col>
            <v-col
              cols="4"
              style="
                padding: 2px !important;
                display: flex;
                justify-content: start;
              "
            >
              <span class="item-information font-italic ellipsis"
                >Last modified by: {{ item.modifiedBy || " - " }}
                <span style="font-style: normal">|</span> Date:
                {{ formatTimeEngToMonthInd(item.modifiedDate) }}
                <span style="font-style: normal">|</span> Time:
                {{ reformatTimes(item.modifiedDate) }} WIB</span
              >
            </v-col>
          </v-row>
        </v-expansion-panel-title>

        <v-expansion-panel-text>
          <v-row>
            <v-col cols="6">
              <p class="mb-2 text-gradient-grey text-15">Pengaju</p>
              <div class="d-flex align-center">
                <text-ellipsis :text="item.pengaju.name ?? '-'" />
                <div class="ml-2">
                  <edit-approval
                    v-if="item.pengaju.isEdit"
                    :itemDialog="item.pengaju"
                    :item="item"
                    :label-dialog="`Edit Pengaju`"
                    :idSector="item.sectorId"
                    :docID="docID"
                    @onSuccess="reloadContent"
                  />
                </div>
              </div>
            </v-col>
            <v-col cols="6">
              <p class="mb-2 text-gradient-grey text-15">Penyetuju</p>
              <div class="d-flex align-center">
                <text-ellipsis :text="item.penyetuju.name ?? '-'" />
                <div class="ml-2">
                  <edit-approval
                    v-if="item.penyetuju.isEdit"
                    :itemDialog="item.penyetuju"
                    :item="item"
                    :label-dialog="'Edit Penyetuju'"
                    :idSector="item.sectorId"
                    :docID="docID"
                    @onSuccess="reloadContent"
                  />
                </div>
              </div>
            </v-col>
            <v-btn
              class="rounded-lg font-weight-semibold my-2 reset-approval-btn"
              :disabled="!item?.buttonReset"
              min-width="0"
              color="#065695"
              variant="outlined"
              @click="props.onResetApproval(props.docID, item.sectorId)"
            >
              Reset Approval
            </v-btn>
          </v-row>
          <!-- <pre>{{ item }}</pre> -->
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script setup lang="ts">
import { ref, StyleValue } from "vue";
import {
  reformatTimes,
  formatTimeEngToMonthInd,
} from "@/v2/helpers/DateHelper";
import { matchChipStyle } from "@/v2/helpers/color";
import TextEllipsis from "@/v2/components/admin/TextEllipsis.vue";
import EditApproval from "@/v2/components/admin/content/EditApproval.vue";

const emits = defineEmits(["onSuccess"]);

const props = defineProps({
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
  docID: {
    type: String,
    default: "",
  },
  onResetApproval: {
    type: Function,
    required: true,
  },
});

const panel = ref<number[]>([]);

const reloadContent = () => {
  emits("onSuccess", props.docID);
};
</script>

<style scoped>
.item-information {
  color: #797979e5;
  font-size: 13px;
  line-height: 19.5px;
}

:deep(.v-expansion-panel .v-expansion-panel--after-active) {
  border-radius: 10px !important;
}

:deep(
    .v-expansion-panels:not(.v-expansion-panels--variant-accordion)
      > :not(:first-child):not(:last-child):not(.v-expansion-panel--active):not(
        .v-expansion-panel--after-active
      )
  ) {
  border-radius: 10px !important;
}

:deep(.v-expansion-panel:not(:first-child)::after) {
  display: none;
}

:deep(
    .v-expansion-panels:not(.v-expansion-panels--variant-accordion)
      > :last-child:not(:first-child):not(.v-expansion-panel--active):not(
        .v-expansion-panel--after-active
      )
  ) {
  border-radius: 10px !important;
}

:deep(
    .v-expansion-panels:not(.v-expansion-panels--variant-accordion)
      > :first-child:not(:last-child):not(.v-expansion-panel--active):not(
        .v-expansion-panel--before-active
      )
  ) {
  border-radius: 10px !important;
}

:deep(.v-expansion-panel) {
  border-radius: 10px !important;
  margin-bottom: 10px;
}

.reset-approval-btn:disabled {
  background-color: #d9d9d9 !important;
  color: #9e9e9e !important;
  opacity: 1 !important;
  border: none;
}
</style>
