<template>
  <div class="metadata-header">Document Detail</div>
  <div class="overflow-auto" style="max-height: 400px">
    <div class="my-4">
      <div class="metadata-title">Nama Topik</div>
      <div class="metadata-body">
        {{ generateLabelMetadata(documentItem.title) }}
      </div>
    </div>
    <div class="my-4">
      <div class="metadata-title">Status</div>
      <div
        class="metadata-body"
        :class="getDocumentColor(documentItem.statusName)"
      >
        {{ generateLabelMetadata(documentItem.statusName) }}
      </div>
    </div>
    <div class="my-4">
      <div class="metadata-title">List Document</div>
      <div class="metadata-body">
        {{ generateLabelMetadata(documentItem.materialListDoc) }}
      </div>
    </div>
    <div class="my-4">
      <div class="metadata-title">Event</div>
      <div class="metadata-body">
        {{ generateLabelMetadata(documentItem.eventName) }}
      </div>
    </div>
    <div class="my-4">
      <div class="metadata-title">Tipe Dokumen</div>
      <div class="metadata-body">
        {{ generateLabelMetadata(documentItem.docType) }}
      </div>
    </div>
    <div class="my-4">
      <div class="metadata-title">Satker Pembuat</div>
      <div class="metadata-body">
        {{ generateLabelMetadata(documentItem.satkerPembuat) }}
      </div>
    </div>
    <div class="my-4">
      <div class="metadata-title">Creator</div>
      <div class="metadata-body">
        {{ generateLabelMetadata(documentItem.presenter) }}
      </div>
    </div>
    <div class="my-4">
      <div class="metadata-title">Penyusun</div>
      <div class="metadata-body">
        {{
          documentItem.listPenyusun.filter((elm) => elm).length != 0
            ? documentItem.listPenyusun.join(", ")
            : "-"
        }}
      </div>
    </div>
    <div class="my-4">
      <div class="metadata-title">Pengaju</div>
      <div class="metadata-body">
        {{ generateLabelMetadata(documentItem.pengaju) }}
      </div>
    </div>
    <div class="my-4">
      <div class="metadata-title">Penyetuju</div>
      <div class="metadata-body">
        {{ generateLabelMetadata(documentItem.penyetuju) }}
      </div>
    </div>
    <div class="my-4">
      <div class="metadata-title">Version</div>
      <div class="metadata-body">
        {{ generateLabelMetadata(documentItem.version) }}
      </div>
    </div>
  </div>
  <div class="mt-8">
    <div class="metadata-title">Document Progress</div>
    <FlowApproval :items="documentItem.listApprovals ?? []" />
  </div>
</template>

<script lang="ts" setup>
import FlowApproval from "@v2/components/meeting/MetadataFlowApproval.vue";

import { generateLabelMetadata } from "@/v2/helpers/utils";
import { getDocumentColor } from "@/v2/helpers/color";
import { computed } from "vue";
import { TMaterialMetadata } from "@/v2/Type";
import { useStore } from "vuex";

const store = useStore();
const documentItem = computed((): TMaterialMetadata => {
  return store.state.meetingStore.materialMetadata as TMaterialMetadata;
});
</script>
