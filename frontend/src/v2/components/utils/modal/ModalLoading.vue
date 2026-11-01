<template>
  <Teleport to="body">
    <v-dialog
      v-model="isShow"
      persistent
      max-width="540px"
      class="dialog-visible"
    >
      <div
        class="d-flex flex-column bg-white rounded-lg px-10 py-16"
        style="align-items: center; justify-content: center; gap: 24px"
      >
        <svg
          width="61"
          height="61"
          viewBox="0 0 61 61"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          style="animation: rotate--spinner 1s linear infinite"
        >
          <path
            fill="#9e9e9e"
            fill-rule="evenodd"
            d="M30.115 8.604a21.51 21.51 0 1 0 0 43.021 21.51 21.51 0 0 0 0-43.02M0 30.116C0 13.483 13.483 0 30.115 0c16.633 0 30.116 13.483 30.116 30.116S46.748 60.232 30.115 60.232 0 46.748 0 30.116"
            clip-rule="evenodd"
            opacity=".2"
          />
          <path
            fill="#9e9e9e"
            fill-rule="evenodd"
            d="M30.11 8.604a21.4 21.4 0 0 0-14.876 5.975 4.302 4.302 0 0 1-5.952-6.213A30 30 0 0 1 30.111 0a4.302 4.302 0 0 1 0 8.604"
            clip-rule="evenodd"
          />
        </svg>
        <p class="text-center" style="font-size: 18px; color: #616161">
          {{ text || "Loading" }}
        </p>
      </div>
    </v-dialog>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from "@vue/reactivity";

defineProps<{ text?: string }>();

const isShow = ref(false);

function show() {
  isShow.value = true;
}

function hide() {
  isShow.value = false;
}

defineExpose({
  show,
  hide,
});
</script>
