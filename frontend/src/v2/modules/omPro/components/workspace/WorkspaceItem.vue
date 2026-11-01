<template>
  <v-sheet class="item-card">
    <v-row v-if="props.isLoading">
      <v-col cols="12">
        <free-style-shimmer
          width="100%"
          height="32px"
          border-radius="10px"
          color="#d3d3d3"
        />
      </v-col>
    </v-row>
    <v-row
      v-else
      align="center"
      style="cursor: pointer !important"
      @click="getDetailRdgm(props.item.id)"
    >
      <v-col cols="4" style="padding: 0 !important">
        <p
          class="font-weight-bold"
          style="
            color: #4b4b4b;
            max-height: 24px;
            overflow: hidden;
            padding-right: 32px;
            text-overflow: ellipsis;
            white-space: nowrap;
          "
          v-html="highlightText(props.item.eventName)"
        ></p>
      </v-col>
      <v-col
        cols="4"
        style="padding: 0 !important; display: flex; justify-content: center"
      >
        <p class="font-weight-bold text-14" style="color: #4b4b4b">
          {{ props.item && formatDate(props.item.eventDate) }}
        </p>
      </v-col>
      <v-col
        cols="3"
        style="padding: 2px !important; display: flex; justify-content: center"
      >
        <v-chip
          variant="flat"
          :color="getEventStatusColor(item.eventStatus).background"
          :style="[
            'font-weight: 600',
            'color:' + getEventStatusColor(item.eventStatus).color + ';',
          ]"
          >{{ props.item && props.item.eventStatus }}</v-chip
        >
      </v-col>
      <v-col
        cols="1"
        style="padding: 0 !important; display: flex; justify-content: end"
      >
        <v-btn icon="mdi-chevron-right" elevation="0"></v-btn>
      </v-col>
    </v-row>
  </v-sheet>
</template>

<script setup lang="ts">
import { formatDate } from "@omPro/helpers/datetime";
import { getEventStatusColor } from "@omPro/helpers/color";
import { useRouter } from "vue-router";

const props = defineProps({
  isLoading: {
    type: Boolean,
    default: false,
  },
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
  query: {
    type: String,
    default: "",
  },
});

const router = useRouter();

const highlightText = (query: string) => {
  const escapedQuery = props.query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return query.replaceAll(
    RegExp("(" + escapedQuery + ")", "ig"),
    `<span class="highlight">$1</span>`
  );
};
const getDetailRdgm = (param: any) => {
  router.push({
    name: "om.workspace-management-rdgm-detail",
    params: { idEvent: param },
  });
};
</script>

<style scoped>
.item-card {
  padding: 16px 36px;
  border-radius: 12px;
  background-color: rgba(255, 255, 255, 1);

  /* Shadow 1 */
  box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.12);
}
.item-card:hover {
  background-color: rgba(255, 255, 255, 0);
  transition: background-color 0.2s ease-in-out;
}
:deep(.highlight) {
  background: orange;
}
</style>
@/v2/helpers/datetime
