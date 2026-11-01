<template>
  <v-card class="time-line">
    <v-container style="padding-top: 1vh !important">
      <v-row no-gutters>
        <v-col cols="1" style="align-self: center">
          <v-btn
            class="ml-3"
            :class="
              current?.isActiveCurrent && current?.isStart
                ? 'button-grey'
                : 'button-red'
            "
            @click="updateStep('Prev')"
            :loading="isLoading"
            :disabled="current?.isActiveCurrent && current?.isStart"
            >Prev</v-btn
          >
        </v-col>
        <v-col cols="10" class="mt-md-n4 mt-lg-n3 mt-xl-0">
          <free-style-shimmer
            v-if="isLoading"
            width="100%"
            height="3vh"
            border-radius="5px"
            color="#DCDCDC"
            class="ml-10 mr-5 mt-4"
          />

          <free-style-shimmer
            v-if="isLoading"
            width="100%"
            height="3vh"
            border-radius="5px"
            color="#DCDCDC"
            class="ml-10 mr-5 mt-2"
          />
          <v-timeline
            v-else
            class="ml-10"
            direction="horizontal"
            line-inset="12"
            side="end"
            align="start"
            truncate-line="both"
            line-color="#D9D9D9"
          >
            <template v-for="(item, index) in listProgress" :key="index">
              <v-timeline-item
                :dot-color="item.isActiveBar ? '#02AA59' : 'grey'"
                :icon="item.isActiveBar ? 'mdi-check' : 'mdi-record'"
                :icon-color="item.isActiveBar ? 'white' : 'white'"
                size="x-small"
                line-inset="2"
              >
                <v-tooltip activator="parent" location="top">{{
                  item.descriptionStep
                }}</v-tooltip>
                <p
                  class="font-weight-bold pl-2 mt-md-n5 mt-lg-n5 mt-xl-n5 text-11"
                  :style="{ color: item.isActiveBar ? '#02AA59' : 'grey' }"
                >
                  {{ item.percentage }}
                </p>
              </v-timeline-item>
            </template>
          </v-timeline>
        </v-col>
        <v-col cols="1" style="align-self: center">
          <v-btn
            :disabled="current?.isActiveCurrent && current?.isEnd"
            :class="
              current?.isActiveCurrent && current?.isEnd
                ? 'button-grey'
                : 'button-green'
            "
            class="mr-10"
            :loading="isLoading"
            @click="updateStep('Next')"
            >Next</v-btn
          >
        </v-col>
      </v-row>
    </v-container>
    <Toast ref="toast" />
  </v-card>
</template>

<script setup lang="ts">
import { defineProps, ref, defineEmits } from "vue";
import { updateStepProgress } from "@/models/document";
import { useRoute } from "vue-router";
// import { useToast } from "vue-toastification";
import { onMounted } from "vue";
import { onUpdated } from "vue";
import Toast from "@/components/utils/ToastComponent.vue";
/* eslint-disable */
const props = defineProps({
  listProgress: Array<any>,
});

const isLoading = ref(false);
const route = useRoute();
const toast = ref();
const emit = defineEmits(["refresh"]);
let current = ref();

onMounted(() => {
  props.listProgress?.filter((element) => {
    if (element.isActiveCurrent) {
      current.value = element;
    }
  });
});

onUpdated(() => {
  props.listProgress?.filter((element) => {
    if (element.isActiveCurrent) {
      current.value = element;
    }
  });
});

const updateStep = (action) => {
  isLoading.value = true;
  props.listProgress?.filter((element) => {
    if (element.isActiveCurrent) {
      current.value = element;
    }
  });

  let togo =
    action == "Next"
      ? current.value.idMDocumentSupportStepNext
      : current.value.idMDocumentSupportStepPrev;
  updateStepProgress(route.params.documentId, togo).then((result) => {
    if (result.status) {
      // toast.success("Success \n" + result.message);
      toast.value.show({
        message: result.message,
        color: "success",
        timeout: 3000,
        icon: "mdi-check",
      });
      emit("refresh", true);
    } else {
      toast.value.show({
        message: result.message,
        color: "error",
        timeout: 3000,
        icon: "mdi-check",
      });
      // toast.value.error(result.message);
    }
    setTimeout(() => (isLoading.value = false), 3000);
  });
};
</script>
<style scoped>
.button-grey {
  background: linear-gradient(92.09deg, darkgrey -46.47%, grey 157.9%);
  color: #fdfdfd;
  border-radius: 15px;
}

.button-green {
  background: linear-gradient(180deg, #00783e 0%, #02aa59 100%);
  color: #fdfdfd;
  border-radius: 15px;
}

.button-red {
  background: linear-gradient(180deg, #d6212a 0%, #ff000d 100%);
  color: #fdfdfd;
  border-radius: 15px;
}
.time-line {
  position: fixed;
  bottom: 0;
  width: 76%;
  height: 10vh;
  margin-left: 15px;
  margin-bottom: 20px;
  text-align: center;
  border-radius: 20px;
  box-shadow: 0px 4px 18px 0px rgba(192, 192, 192, 0.25);
}
</style>
