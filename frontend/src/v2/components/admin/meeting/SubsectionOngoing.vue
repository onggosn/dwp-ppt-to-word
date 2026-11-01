<template>
  <v-sheet class="my-3">
    <v-expansion-panels v-model="panel">
      <v-expansion-panel :value="item.bpID">
        <v-expansion-panel-title>
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
            <v-chip :style="getColorChip(item.bpStatus)">
              {{ item.bpStatus }}
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
              <DocumentOnGoing :item="list" />
            </div>
          </div>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-sheet>
</template>
<script setup lang="ts">
/* eslint-disable */
import DocumentOnGoing from "@/v2/components/admin/meeting/DocumentOnGoing.vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import { computed, getCurrentInstance, ref, watch } from "vue";
import { secureRandomFloat } from "@/v2/helpers/utils";
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
const route = useRoute();
const loading = ref<boolean>(false);
const panel = ref<number[]>([]);
const items = ref<any[]>([]);
const instance = ref<any>(getCurrentInstance()?.root.refs);

const searchMode = computed(() => store.getters["globalStore/getStatusSearch"]);
const searchValue = computed(() => store.getters["globalStore/getSearch"]);
const filterValue = computed(() => store.getters["adminStore/getItemsFilter"]);

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
      store.commit("adminStore/setRefreshList", secureRandomFloat());
    });
};

watch(panel, (newValue) => {
  if (newValue) getSectionList(newValue);
});

function getSectionList(idMBPDocumentTemplate: number | number[]) {
  loading.value = true;
  let payload = {
    idBP: idMBPDocumentTemplate,
    eventSearching: searchMode.value ? searchValue.value : "",
    status: searchMode.value ? [] : filterValue.value.status ?? [],
    pic: searchMode.value ? [] : filterValue.value.picFilter ?? [],
    dateStart: searchMode.value ? null : filterValue.value.dateSince || null,
    dateEnd: searchMode.value ? null : filterValue.value.dateTo || null,
    eventSort: searchMode.value ? 1 : route.query.eventSort,
  };

  store
    .dispatch("adminStore/getListSubDetailSectionOg", payload)
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
