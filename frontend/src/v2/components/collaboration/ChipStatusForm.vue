<template>
  <free-style-shimmer
    :is-loading="true"
    width="100px"
    height="24px"
    border-radius="15px"
    class="pr-4"
    v-if="isLoading"
  />

  <v-chip
    v-else-if="isLoadingAsync"
    size="small"
    class="mr-3 pa-2 font-weight-bold"
    style="background-color: rgb(255, 238, 202); color: rgb(144, 110, 44)"
    :loading="true"
  >
    {{
      asyncType.toLowerCase() === "save"
        ? "Save in progress"
        : "Approval in progress"
    }}
    <v-progress-circular
      class="ml-1"
      color="rgb(144, 110, 44)"
      size="small"
      indeterminate
      style="width: 15px"
    ></v-progress-circular>
  </v-chip>

  <v-menu
    v-else-if="!canNotSeeStatusDoc && isDocument2d"
    open-on-hover
    location="bottom right"
  >
    <template v-slot:activator="{ props }">
      <v-chip
        size="small"
        class="mr-3 pa-2 font-weight-bold"
        :style="
          getColorChipEditor(
            store.getters['collaborationStore/getDocumentStatus']
          )
        "
        :loading="true"
        v-bind="props"
      >
        {{ store.getters["collaborationStore/getDocumentStatus"] }}
      </v-chip>
    </template>

    <div class="d-flex flex-row-reverse">
      <div class="triangle"></div>
    </div>

    <v-list min-width="400" class="py-0">
      <v-list-item class="px-0 pb-0 mb-0 list-container">
        <v-list-item-title class="mx-3 pb-2"
          >Status Persetujuan :
        </v-list-item-title>
        <v-list-item-title
          v-for="(item, idx) in listTooltip"
          :class="[
            item.hasAccess ? 'active-list font-weight-bold' : '',
            'px-4 py-2',
          ]"
          :key="item.sector"
          >{{ `${idx + 1}. ${item.sector}` }}
          <v-chip
            size="small"
            class="ml-2"
            :style="getColorChipEditor(item.status)"
            >{{ item.status }}</v-chip
          ></v-list-item-title
        >
      </v-list-item>
    </v-list>
  </v-menu>

  <v-chip
    v-else-if="!canNotSeeStatusDoc"
    size="small"
    class="mr-3 pa-2 font-weight-bold"
    :style="
      getColorChipEditor(store.getters['collaborationStore/getDocumentStatus'])
    "
    :loading="true"
  >
    {{ store.getters["collaborationStore/getDocumentStatus"] }}
  </v-chip>

  <!-- {{ isLoadingAsync }} -->
</template>
<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { getColorChipEditor } from "@v2/helpers/color";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import { TTypeFlow2d } from "@v2/Type";

const route = useRoute();
const store = useStore();
const isLoading = ref(false);

const listTooltip = ref<TTypeFlow2d[]>([]);

const isLoadingAsync = computed((): boolean => {
  return store.state.documentStore.loadingAsync;
});

const asyncType = computed(() => store.getters["documentStore/getAsyncType"]);

const canNotSeeStatusDoc = computed(
  () =>
    route.params.idDoc === "00000000-0000-0000-0000-000000000000" ||
    (!store.getters["collaborationStore/getListForm"]?.length &&
      store.getters["collaborationStore/getDocumentStatus"] === "Deleted")
);

const isDocument2d = computed(
  () => store.getters["collaborationStore/getDocumentSectoral"]
);

function getTooltip() {
  isLoading.value = true;
  store
    .dispatch("adminStore/getFlowDoc2d", {
      idBPDocument: route.params.idDoc,
    })
    .then((res) => {
      listTooltip.value = res.responseData;
    })
    .finally(() => {
      isLoading.value = false;
    });
}

watch(
  isDocument2d,
  (value) => {
    if (value) getTooltip();
  },
  { immediate: true }
);
</script>
<style lang="css" scoped>
:deep(.v-overlay__content) {
  border-radius: 10px;
}
.active-list {
  background: linear-gradient(92.09deg, #065695 0%, #267dc2 100%) !important;
  color: #ffff !important;
}

.triangle {
  border: 7px solid transparent;
  border-top: 0;
  border-bottom: 15px solid #fff;
  z-index: 50;
  margin-right: 25px;
}
</style>
