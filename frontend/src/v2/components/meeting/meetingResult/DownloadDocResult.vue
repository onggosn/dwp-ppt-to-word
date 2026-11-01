<template>
  <v-btn variant="text" @click="handleClick" class="pa-1" min-width="0">
    <v-icon
      class="table-content-center"
      color="#267DC2"
      small
      style="
        border: 1px solid;
        border-radius: 4px;
        padding: 13px;
        cursor: pointer;
      "
    >
      mdi-cloud-download</v-icon
    >
    <v-tooltip activator="parent" location="top">Download</v-tooltip>
  </v-btn>
</template>
<script lang="ts" setup>
import clientv2 from "@v2/library/ApiClient";
import { v4 as uuidv4 } from "uuid";

const props = defineProps(["id", "filename"]);
async function handleClick() {
  try {
    const response = await clientv2.downloadDocumentResult({
      data: {
        id: props.id,
        traceId: uuidv4(),
      },
    });

    const link = document.createElement("a");
    link.href = window.URL.createObjectURL(new Blob([response.data]));
    link.setAttribute("download", props.filename);
    document.body.appendChild(link);
    link.click();
  } catch (error) {
    undefined;
  }
}
</script>
