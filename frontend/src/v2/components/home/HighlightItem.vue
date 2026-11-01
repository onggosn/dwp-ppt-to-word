<template>
  <v-sheet
    style="border-color: #f0f0f0"
    class="pb-6 border-b-sm border-solid cursor-pointer"
    @click="goToDoc"
  >
    <v-sheet class="d-flex flex-row">
      <div
        style="
          width: 30px;
          height: 39px;
          padding-left: 13px;
          padding-top: 19px;
          margin-right: 15px;
        "
      >
        <img
          width="30px"
          height="39px"
          style="object-fit: cover"
          :src="
            require(`@/v2/assets/home/highlight-${getImageName(
              content.bpName
            )}.png`)
          "
        />
      </div>

      <div style="flex-grow: 1; padding: 8px">
        <div
          class="text-uppercase text-gradient-red font-weight-light cursor-pointer"
          style="
            font-size: 11px;
            font-weight: 500;
            line-height: 12px;
            text-align: left;
            cursor: pointer;
          "
        >
          {{ content.bpName }}
        </div>
        <div
          class="text-newBlack cursor-pointer"
          style="
            font-size: 14px;
            font-weight: 600;
            text-align: left;
            cursor: pointer;
          "
        >
          {{ content.bpDocumentName }}
        </div>
        <div
          class="text-gradient-grey cursor-pointer"
          style="
            font-size: 11px;
            font-weight: 400;
            line-height: 12px;
            text-align: left;
            margin-top: 2px;
            cursor: pointer;
          "
        >
          {{ content.lastApproved }}
          <!--Temuan SIT Sprint 2 2025 DOPM-2116 -> Label semuanya dari BE -->
        </div>
      </div>
    </v-sheet>
  </v-sheet>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import type { TResponseTop10DocByUser } from "@/v2/Type";
import { PropType } from "vue";

const props = defineProps({
  content: {
    type: Object as PropType<TResponseTop10DocByUser>,
    default: function () {
      return {};
    },
  },
});

const router = useRouter();

function goToDoc() {
  router.push({
    name: "v2.rdg-collaboration",
    params: {
      typeRDG: props.content.rdgType,
      idEvent: props.content.idEvent,
      idDoc: props.content.idBPDocument,
    },
  });
}

function getImageName(bpName) {
  if (bpName === "Policy Note") return "pn";
  else if (bpName === "Issue Note") return "in";
  return "aiu";
}
</script>

<style scoped></style>
