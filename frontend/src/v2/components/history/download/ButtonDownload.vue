<template>
  <div class="text-center pr-1 mx-3">
    <v-menu>
      <template v-slot:activator="{ props }">
        <v-btn
          class="btn-dropdown w-100"
          variant="outlined"
          dark
          v-bind="props"
          prepend-icon="mdi-cloud-download"
          :append-icon="icon"
          @click="download"
        >
          <slot />
        </v-btn>
      </template>

      <!-- sprint depan ada dropdown -->
      <v-list v-if="items.length">
        <v-list-item v-for="(item, index) in props.items" :key="index">
          <v-list-item-title
            style="cursor: pointer"
            @click.prevent="action(item.value)"
            >{{ item.value }}</v-list-item-title
          >
        </v-list-item>
      </v-list>
    </v-menu>
  </div>

  <LoadingDownload v-if="downloadLoading" />
</template>
<script lang="ts" setup>
import { ref, computed } from "vue";
import LoadingDownload from "@/v2/components/utils/dialog/LoadingDownload.vue";
import { useDownloadBlob } from "@/v2/composables/useDownloadBlob";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
type TDownloadItem = {
  item: string;
  value: string;
};

const props = defineProps({
  items: {
    type: Array<TDownloadItem>,
    default: () => [],
  },
  icon: {
    type: String,
    default: "",
  },
});

const downloadLoading = ref<boolean>(false);
const store = useStore();
const route = useRoute();

const emit = defineEmits<{ (e: "update", value: string): void }>();
const itemFilter = computed(() => store.getters["historyStore/getItemsFilter"]);

function action(value: string) {
  emit("update", value);
}

async function download(value?: string) {
  if (value) emit("update", value);

  downloadLoading.value = true;

  const payload = {
    search: "",
    workspaceType: itemFilter.value?.workspaceType ?? [],
    monthPeriod: itemFilter.value?.monthPeriod ?? [],
    yearPeriod: itemFilter.value?.yearPeriod ?? [],
    status: itemFilter.value?.status ?? [],
    sortBy: Number(route.query.eventSort) ?? 0,
  };

  try {
    const resp = await store.dispatch(
      "historyStore/downloadHistoryList",
      payload
    );
    useDownloadBlob(resp.data, "history_export", "xlsx");
  } catch (err) {
    console.error(err);
  } finally {
    downloadLoading.value = false;
  }
}
</script>
<style scoped>
.btn-dropdown {
  color: #065695;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
}
</style>
