<template>
  <v-btn
    v-if="selected.length"
    variant="outlined"
    class="btn-create mx-2"
    @click="handleDownload()"
  >
    <v-icon icon="mdi-cloud-download" />
    <span class="mx-1">Download {{ selected.length }} Selected</span>
  </v-btn>
  <Teleport to="body">
    <loading-spinner v-if="isLoading" />
  </Teleport>
</template>
<script lang="ts" setup>
import LoadingSpinner from "@/components/loading/LoadingSpinner.vue";
import { useDownloadBlob } from "@/v2/composables/useDownloadBlob";
import { ref, computed, PropType } from "vue";
import clientv2 from "@v2/library/ApiClient";
import { v4 as uuidv4 } from "uuid";
import { useStore } from "vuex";
type TTypeDownload = "material" | "result";

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
  type: {
    type: String as PropType<TTypeDownload>,
    default: "material",
  },
  selected: {
    type: Array<string>,
    default: () => [],
  },
});

const isLoading = ref<boolean>(false);
const store = useStore();

const eventName = computed((): any => {
  const name = store.state?.meetingStore.meetingItem?.eventName ?? "downloaded";
  return name.replace(/ /g, "_");
});

async function downloadAllMaterial() {
  isLoading.value = true;
  try {
    const data = {
      id: props.selected,
      traceId: uuidv4(),
    };
    const response = await clientv2.downloadAllDocument({ data });
    const fileName = `Presentation_material-${eventName.value}`;
    useDownloadBlob(response.data, fileName, "zip");
  } catch (error) {
    undefined;
  }

  isLoading.value = false;
}

async function downloadAllMaterialResult() {
  isLoading.value = true;
  try {
    const data = {
      id: props.selected,
      traceId: uuidv4(),
    };
    const response = await clientv2.downloadAllDocumentResult({ data });
    const fileName = `Hasil_pembahasanl-${eventName.value}`;
    useDownloadBlob(response.data, fileName, "zip");
  } catch (error) {
    undefined;
  }

  isLoading.value = false;
}

function handleDownload() {
  if (props.type === "material") downloadAllMaterial();
  if (props.type === "result") downloadAllMaterialResult();
}
</script>
