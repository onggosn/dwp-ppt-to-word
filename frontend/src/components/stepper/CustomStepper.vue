<template>
  <v-sheet class="paddingan">
    <v-timeline direction="horizontal">
      <v-timeline-item
        class="first-item"
        size="small"
        dot-color="#065695"
        icon="mdi-check"
        icon-color="white"
      >
        <template v-slot:opposite>
          <div>
            <div class="text-darkBlue">Step 1</div>
          </div>
        </template>
      </v-timeline-item>

      <template v-for="item in itemNumberValue" :key="item">
        <template v-if="item % 2 == 0">
          <v-timeline-item
            size="small"
            :dot-color="getDotColor(item + 1)"
            :icon="getIcon(item + 1)"
            :icon-color="getIconColor(item + 1)"
          >
            <template v-slot:opposite>
              <div>
                <div class="text-darkBlue">Step {{ item + 1 }}</div>
              </div>
            </template>
          </v-timeline-item>
        </template>
        <template v-else>
          <v-timeline-item
            size="small"
            :dot-color="getDotColor(item + 1)"
            :icon="getIcon(item + 1)"
            :icon-color="getIconColor(item + 1)"
          >
            <div>
              <div class="text-darkBlue">Step {{ item + 1 }}</div>
            </div>
          </v-timeline-item>
        </template>
      </template>

      <v-timeline-item
        v-if="(itemNumberValue + 2) % 2 == 0"
        class="last-item"
        size="small"
        :dot-color="getDotColor(itemNumberValue + 2)"
        :icon="getIcon(itemNumberValue + 2)"
        :icon-color="getIconColor(itemNumberValue + 2)"
      >
        <div>
          <div class="text-darkBlue" style="margin-left: -2vw">
            Step {{ itemNumberValue + 2 }}
          </div>
        </div>
      </v-timeline-item>
      <v-timeline-item
        v-else
        class="last-item"
        size="small"
        :dot-color="getDotColor(itemNumberValue + 2)"
        :icon="getIcon(itemNumberValue + 2)"
        :icon-color="getIconColor(itemNumberValue + 2)"
      >
        <template v-slot:opposite>
          <div>
            <div class="text-darkBlue" style="margin-left: -2vw">
              Step {{ itemNumberValue + 2 }}
            </div>
          </div>
        </template>
      </v-timeline-item>
    </v-timeline>
  </v-sheet>
</template>

<script setup lang="ts">
import { ref, defineProps } from "vue";

const props = defineProps({
  itemNumber: {
    type: Number,
    default: 0,
  },
  currentStep: {
    type: Number,
    default: 0,
  },
});

const getDotColor = (item: number) => {
  if (item === props.currentStep) {
    return "#065695";
  } else if (item < props.currentStep) {
    return "#065695";
  } else {
    return "#797979";
  }
};

const getIcon = (item: number) => {
  if (item === props.currentStep) {
    return "mdi-check";
  } else if (item < props.currentStep) {
    return "mdi-check";
  } else {
    return "mdi-circle-slice-8";
  }
};

const getIconColor = (item: number) => {
  if (item === props.currentStep) {
    return "#eeeeee";
  } else if (item < props.currentStep) {
    return "#eeeeee";
  } else {
    return "#eeeeee";
  }
};

const itemNumberValue = ref(props.itemNumber - 2);
</script>

<style scoped>
:deep(.v-timeline-item__body) {
  padding-right: 0 !important;
}

:deep(.v-timeline-item__opposite) {
  padding-right: 0 !important;
}

.paddingan {
  padding-left: 10vw;
  padding-right: 10vw;
}

.text-darkBlue {
  color: var(--Text, #3a416f);
  text-align: center;
  font-family: Poppins;
  font-size: 15px;
  font-style: normal;
  font-weight: 900;
  line-height: 150%; /* 19.5px */
  letter-spacing: 0.013px;
}
</style>
