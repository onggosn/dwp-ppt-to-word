<template>
  <v-menu
    v-if="
      $props.type === '.doc' ||
      $props.type === '.docx' ||
      $props.initialDocumentExt === '.doc' ||
      $props.initialDocumentExt === '.docx'
    "
    class="pa-1"
    min-width="0"
  >
    <template v-slot:activator="{ props }">
      <v-btn v-bind="props" variant="text" class="pa-1" min-width="0">
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
    <v-list>
      <v-list-item>
        <v-btn variant="text" @click="handleClick('docx')">
          <p>Download format docx</p>
        </v-btn>
      </v-list-item>
      <v-list-item>
        <v-btn variant="text" @click="handleClick('pdf')">
          <p>Download format pdf</p>
        </v-btn>
      </v-list-item>
    </v-list>
  </v-menu>
  <v-menu
    v-else-if="
      $props.type === '.ppt' ||
      $props.type === '.pptx' ||
      $props.initialDocumentExt === '.ppt' ||
      $props.initialDocumentExt === '.pptx'
    "
    class="pa-1"
  >
    <template v-slot:activator="{ props }">
      <v-btn v-bind="props" variant="text" class="pa-1" min-width="0">
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
    <v-list>
      <v-list-item>
        <v-btn variant="text" @click="handleClick('ppt')">
          <p>Download format ppt</p>
        </v-btn>
      </v-list-item>
      <v-list-item>
        <v-btn variant="text" @click="handleClick('pdf')">
          <p>Download format pdf</p>
        </v-btn>
      </v-list-item>
    </v-list>
  </v-menu>
  <v-btn
    v-else
    variant="text"
    @click="handleClick('pdf')"
    class="pa-1"
    min-width="0"
  >
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
const props = defineProps([
  "id",
  "filename",
  "type",
  "initialDocument",
  "initialDocumentExt",
]);
async function handleClick(type: string) {
  try {
    const response = await clientv2.downloadMeetingDocument({
      data: {
        id: props.id,
        exportType: type,
      },
    });

    const link = document.createElement("a");
    link.href = window.URL.createObjectURL(new Blob([response.data]));
    if (type == "pdf") {
      link.setAttribute("download", getDocumentName(props.filename) + ".pdf");
    } else if (props.initialDocument) {
      link.setAttribute("download", props.initialDocument);
    } else {
      link.setAttribute("download", props.filename);
    }
    document.body.appendChild(link);
    link.click();
  } catch (error) {
    undefined;
  }
}

function getDocumentName(filename) {
  return filename.split(".").slice(0, -1).join(".");
}
</script>

<style scoped>
p {
  color: #3a416f;
}
</style>
