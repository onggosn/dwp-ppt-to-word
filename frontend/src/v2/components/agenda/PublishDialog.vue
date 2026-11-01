<template>
  <div>
    <Teleport to="body">
      <v-dialog width="450px" v-model="visibility">
        <div style="position: relative; z-index: 9999" class="text-center">
          <v-avatar
            color="white"
            size="80"
            style="margin-bottom: -50px; box-shadow: 0px 2px 10px 0px"
          >
            <v-icon size="70" color="#D6212A">
              {{ icon }}
            </v-icon>
          </v-avatar>
        </div>
        <v-card style="border-radius: 10px; box-shadow: 0px 0px">
          <v-card-title class="mt-15 mx-auto">
            <h3 class="font-weight-bold">{{ title }}</h3>
          </v-card-title>
          <v-btn
            class="mr-2"
            style="position: absolute; right: 0"
            variant="text"
            icon="mdi-close"
            @click="close(true)"
          ></v-btn>
          <v-card-text class="mx-auto pt-0">
            <p class="text-center">{{ desc }}</p>
          </v-card-text>
          <v-card-actions class="pb-3">
            <v-spacer />
            <v-btn
              variant="flat"
              elevation="3"
              class="ml-5 rounded-lg font-weight-bold"
              @click="close(false)"
            >
              Cancel
            </v-btn>
            <v-btn
              variant="flat"
              color="primary"
              elevation="3"
              class="ml-5 rounded-lg font-weight-bold submit-button"
              @click="submit(true)"
            >
              Yes
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </Teleport>
  </div>
</template>

<script lang="ts" setup>
import { defineProps, defineEmits, PropType, computed } from "vue";
type TSize = "sm" | "md" | "lg";

const props = defineProps({
  id: {
    type: String,
    default: "",
  },
  title: {
    type: String,
    default: "",
  },
  desc: {
    type: String,
    default: "",
  },
  size: {
    type: String as PropType<TSize>,
    default: "md",
  },
  icon: {
    type: String,
    default: "",
  },
  visible: {
    type: Boolean,
    default: true,
  },
});
const emit = defineEmits<{
  (e: "submit", value: unknown): void;
  (e: "close", value: boolean): void;
}>();

const close = (value: boolean) => {
  emit("close", value);
};

const submit = (value: unknown) => {
  emit("submit", value);
};

const visibility = computed({
  get() {
    return props.visible;
  },
  set(value: boolean) {
    emit("close", value);
  },
});
</script>

<style>
.submit-button {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
}
</style>
