<template>
  <div class="pr-2" style="overflow-y: scroll; max-height: 930px">
    <v-card class="container">
      <h1 class="txt-header mb-5">Business Process Stages</h1>
      <v-sheet class="container-section">
        <slot name="persetujuan"></slot>
        <slot name="rekomendasi"></slot>
        <slot name="asesmen"></slot>
      </v-sheet>
    </v-card>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
::-webkit-scrollbar {
  margin-right: 2px;
  width: 8px;
  height: 15px;
}
.container {
  background: white;
  border-radius: 12px;
  padding: 12px 16px 28px 16px;
}
.txt-header {
  font-family: Poppins;
  font-size: 24px;
  font-weight: 600;
  line-height: 36px;
  text-align: left;
  color: #4b4b4b;
}
.container-section {
  display: flex;
  flex-direction: column;
  row-gap: 16px;
}
</style>
