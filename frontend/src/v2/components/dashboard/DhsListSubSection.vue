<template>
  <v-sheet class="my-3">
    <v-expansion-panels v-model="panel">
      <v-expansion-panel :value="item.idBp">
        <v-expansion-panel-title>
          <template v-slot:actions="{ expanded }">
            <v-icon
              class="border-icon-expansion-default pr-10"
              :icon="expanded ? 'mdi-chevron-up' : 'mdi-chevron-down'"
            />
          </template>
          <v-col cols="7" style="padding: 0 !important">
            <p class="font-weight-bold ellipsis-1">
              {{ item.bpName }}
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
            <v-chip :style="getColorChip(item.statusName)">
              {{ item.statusName }}
            </v-chip>
          </v-col>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-row v-if="loading" class="mx-5 my-5">
            <v-col v-for="i in 3" :key="i" cols="12">
              <free-style-shimmer
                width="100%"
                height="40px"
                border-radius="10px"
                color="#d3d3d3"
              />
            </v-col>
          </v-row>
          <div v-else>
            <div v-for="list in items" :key="list.docID">
              <DhsListDocument :item="list" />
            </div>
          </div>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-sheet>
</template>
<script setup lang="ts">
import DhsListDocument from "@v2/components/dashboard/DhsListDocument.vue";
import { useStore } from "vuex";
import { ref, watch } from "vue";
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const props = defineProps({
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
});

const store = useStore();
const loading = ref<boolean>(false);
const panel = ref<number[]>([]);
const items = ref<any[]>([]);

watch(panel, (newValue) => {
  if (newValue) getSectionList(newValue);
});

function getSectionList(idMBPDocumentTemplate: number | number[]) {
  loading.value = true;
  const payload = {
    idBp: idMBPDocumentTemplate,
  };
  store
    .dispatch("documentsStore/GetListContent", payload)
    .then((res: any) => {
      items.value = res.responseData;
    })
    .finally(() => {
      loading.value = false;
    });
}

function getColorChip(value: string) {
  if (value?.toLocaleLowerCase() === "in progress")
    return {
      "background-color": "rgba(255, 238, 202, 1)",
      color: "rgba(144, 110, 44, 1)",
    };
  if (value?.toLocaleLowerCase() === "done")
    return {
      "background-color": "rgba(232, 246, 235, 1)",
      color: "rgba(28, 163, 51, 1)",
    };
}
</script>
<style scoped>
:deep(.v-expansion-panel__shadow) {
  box-shadow: 0px 4px 18px 0px rgba(192, 192, 192, 0.25) !important;
}
</style>
