<template>
  <!-- POC: static copy of the document "Content" panel (real one: contentManagement/TableOfContent.vue) -->
  <v-card class="mx-auto overflow-auto toc mt-4" height="calc(100vh - 2rem)">
    <div class="d-flex justify-space-between mb-4 align-center mx-4 mt-3">
      <p class="font-weight-bold">Content</p>
      <div class="d-flex" style="gap: 8px">
        <v-btn icon size="x-small" color="#267dc2" flat>
          <v-icon color="white">mdi-eye</v-icon>
        </v-btn>
        <v-btn icon size="x-small" color="#267dc2" flat>
          <v-icon color="white">mdi-plus</v-icon>
        </v-btn>
      </div>
    </div>
    <v-divider />

    <div class="px-3 pt-3">
      <div v-for="folder in folders" :key="folder.name" class="mb-1">
        <div
          class="d-flex align-center folder-row"
          @click="folder.open = !folder.open"
        >
          <v-icon size="20" color="#4b4b4b">
            {{ folder.open ? "mdi-folder-open-outline" : "mdi-folder-outline" }}
          </v-icon>
          <span class="ml-3 text-14 fw-500 folder-name">{{ folder.name }}</span>
          <v-spacer />
          <v-icon size="18" color="#4b4b4b">
            {{ folder.open ? "mdi-menu-up" : "mdi-menu-down" }}
          </v-icon>
        </div>
        <div v-if="folder.open && folder.items.length" class="doc-list">
          <div
            v-for="doc in folder.items"
            :key="doc"
            class="d-flex align-center doc-row"
            :class="{ active: doc === props.activeDoc }"
          >
            <span class="text-13 doc-name">{{ doc }}</span>
            <v-spacer />
            <v-icon
              size="16"
              :color="doc === props.activeDoc ? '#f57c00' : '#9e9e9e'"
            >
              mdi-clock-outline
            </v-icon>
            <v-icon size="16" color="#4b4b4b">mdi-menu-down</v-icon>
          </div>
        </div>
      </div>

      <v-divider class="my-3" color="#267dc2" :thickness="2" />
      <p class="text-14 fw-500 mb-2">Reference</p>
      <div
        v-for="ref in references"
        :key="ref"
        class="d-flex align-center folder-row mb-1"
      >
        <v-icon size="20" color="#4b4b4b">mdi-folder-outline</v-icon>
        <span class="ml-3 text-14 folder-name">{{ ref }}</span>
        <v-spacer />
        <v-icon size="18" color="#4b4b4b">mdi-menu-down</v-icon>
      </div>
    </div>
  </v-card>
</template>

<script setup lang="ts">
import { reactive } from "vue";

const props = defineProps<{ activeDoc: string }>();

// eslint-disable-next-line vue/no-setup-props-destructure -- static POC tree, built once
const rdg = [
  "RDGB_Bulan Tahun_Buku 1a Asesmen Moneter",
  "RDGB_Bulan Tahun_Buku 1b Asesmen Makroprudensial",
  "RDGB_Bulan Tahun_Buku 1c Asesmen Sistem Pembayaran",
  "RDGB_Bulan Tahun_Buku 2a Summary Asesmen, Proyeksi, dan Rekomendasi Moneter",
  "RDGB_Bulan Tahun_Buku 2b Summary Asesmen, Proyeksi, dan Rekomendasi Makroprudensial",
  "RDGB_Bulan Tahun_Buku 2c Summary Asesmen, Proyeksi, dan Rekomendasi Sistem Pembayaran",
  props.activeDoc,
  "RDGB_Bulan Tahun_Butir Keputusan",
  "RDGB_Bulan Tahun_Risalah RDG",
];

const folders = reactive([
  { name: "RDG", open: true, items: rdg },
  ...["KBKU", "SORE", "SOPS", "SOMA", "SOEM", "RSOPS", "RSOMA", "RSOEM"].map(
    (name) => ({ name, open: false, items: [] as string[] })
  ),
]);

const references = ["Analisis Indikator Utama", "Policy Note"];
</script>

<style scoped>
.toc {
  border-radius: 12px;
}
.folder-row {
  cursor: pointer;
  padding: 6px 4px;
}
.folder-name {
  color: #4b4b4b;
}
.doc-list {
  border-left: 2px solid #267dc2;
  margin-left: 6px;
  padding-left: 10px;
}
.doc-row {
  padding: 4px 0;
  gap: 4px;
}
.doc-name {
  color: #267dc2;
  font-weight: 500;
  line-height: 1.35;
}
.doc-row.active .doc-name {
  color: #e53935;
  font-weight: 700;
}
</style>
