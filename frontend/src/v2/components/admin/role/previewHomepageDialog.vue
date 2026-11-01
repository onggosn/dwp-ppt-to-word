<template>
  <v-dialog v-model="dialog" width="680" persistent>
    <v-card class="pa-0 overflow-hidden" elevation="24">
      <v-sheet>
        <div>
          <div class="pt-5 pb-5 text-center text-18 text-blueTheme">
            Preview Homepage Detail
          </div>
          <div
            class="pt-5 text-center text-18"
            style="position: absolute; right: 5px; top: -15px"
          >
            <v-btn class="mx-2" fab small variant="text" @click="close">
              <v-icon color="#C0C0C0"> mdi-close </v-icon>
            </v-btn>
          </div>
        </div>

        <v-btn
          elevation="0"
          class="d-block separatorHorizontal"
          style="cursor: none"
        />
      </v-sheet>

      <v-card-text class="pa-6 bg-preview" style="justify-items: center">
        <div
          v-if="imgSrc != ''"
          style="
            position: relative;
            display: grid;
            place-items: center;
            width: 480px;
          "
        >
          <v-carousel show-arrows="hover" hide-delimiter-background>
            <v-carousel-item>
              <div class="d-flex justify-center align-center h-100">
                <v-img
                  :width="480"
                  class="mx-auto"
                  style="
                    border-radius: 8px;
                    box-shadow: 5px 8px 18px 5px rgba(192, 192, 198, 0.5);
                  "
                  :src="imgSrc"
                ></v-img>
              </div>
            </v-carousel-item>
            <v-carousel-item>
              <div
                class="d-flex justify-center align-center h-100"
                style="z-index: 1"
              >
                <v-img
                  :width="480"
                  style="
                    border-radius: 8px;
                    box-shadow: 5px 8px 18px 5px rgba(192, 192, 198, 0.5);
                  "
                  aspect-ratio="9/16"
                  cover
                  src="@/v2/assets/meeting/Dashboardpreview.png"
                ></v-img>
              </div>
              <v-img
                :width="94"
                style="z-index: 2; position: absolute; top: 20%; left: 77%"
                :src="
                  imgSrc
                    ? imgSrc
                    : '@/v2/assets/meeting/meeting_banner_2026.png'
                "
              ></v-img>
            </v-carousel-item>
          </v-carousel>
        </div>

        <div v-else class="empty-illustration">
          <img
            :src="require('@/v2/assets/empty/no_available_state.svg')"
            class="img-no-available"
          />
        </div>

        <div v-if="1 < 2" class="mt-8 d-flex justify-center">
          <v-btn
            class="btn-done px-10"
            height="44"
            variant="flat"
            @click="close"
          >
            Close Preview
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref } from "vue";

const props = defineProps({
  imgSrc: {
    type: String,
    default: "",
  },
});

const emits = defineEmits(["close"]);

const dialog = ref(false);

function close() {
  dialog.value = false;
  emits("close");
}
</script>

<style scoped>
.header-gradient {
  background: linear-gradient(135deg, #065695 0%, #267dc2 100%);
  position: relative;
}

.btn-close {
  position: absolute;
  right: 12px;
  top: 12px;
  color: rgba(255, 255, 255, 0.7);
}

.bg-preview {
  background-color: #f8fafc;
}

.btn-done {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  border-radius: 12px !important;
  color: white !important;
  font-weight: 700;
  text-transform: none;
  letter-spacing: 0.5px;
}
.v-responsive__sizer ~ .v-responsive__content {
  margin-inline-start: -100%;
  align-content: center;
}
.separatorHorizontal {
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
  height: 1.2px;
  width: 100%;
}
</style>
