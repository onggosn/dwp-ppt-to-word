<template>
  <!-- POC: coloured file-type badge (PPTX red, DOCX blue, PDF dark red) -->
  <div class="badge" :class="[size, ext]">
    <span>{{ ext.toUpperCase() }}</span>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{ ext: string; size?: "small" | "large" }>(), {
  size: "small",
});
</script>

<style scoped>
.badge {
  display: inline-flex;
  align-items: flex-end;
  justify-content: center;
  border-radius: 4px 12px 4px 4px;
  color: #fff;
  font-weight: 700;
  background: #9e9e9e;
  flex-shrink: 0;
}
.badge.small {
  width: 24px;
  height: 30px;
  font-size: 6px;
  padding-bottom: 4px;
}
.badge.large {
  width: 56px;
  height: 70px;
  font-size: 13px;
  padding-bottom: 12px;
}
.badge.pptx {
  background: #e8481e;
}
.badge.docx {
  background: #2b6cd4;
}
.badge.pdf {
  background: #c62828;
}
</style>
