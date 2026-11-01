<template>
  <v-dialog v-model="modal" persistent max-width="450px" class="dialog-visible">
    <v-card class="card-loading">
      <v-card-text class="ma-4">
        <p class="text-loading ml-1 mb-2 mt-5">Loading...</p>
        <v-progress-linear
          height="24"
          :model-value="store.getters['loadingStore/getProgress']"
          rounded
        ></v-progress-linear>
        <div class="d-flex justify-space-between mt-2 mb-5">
          <div class="text-loading">
            <slot name="footer-loading">
              {{
                progress == 98 ? "just a bit longer, we're almost there!" : ""
              }}
              <div class="text-loading">{{ progress }} %</div>
            </slot>
          </div>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
<style scoped>
.text-loading {
  color: #3a416f;
  font-size: 12px;
  font-weight: 700;
  line-height: 18px;
}
.card-loading {
  border-radius: 22px !important;
}
.progress-bar {
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%);
}
.text-right {
  text-align: right;
}
:deep(.v-progress-linear__determinate, .v-progress-linear__indeterminate) {
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%);
  border-radius: 12px;
  box-shadow: 0px -2px 4px 0px #00000040 inset !important;
}
:deep(.v-progress-linear__background) {
  background: #8e8c8c !important;
  box-shadow: 10px 8px 4px 2px #000000c4 inset !important;
}
</style>
<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useStore } from "vuex";
const modal = ref<boolean>(true);
const store = useStore();

const progress = computed(() => {
  return store.getters["loadingStore/getProgress"];
});

watch(progress, (newValue) => {
  if (newValue == 100) {
    modal.value = false;
  }
});
</script>
