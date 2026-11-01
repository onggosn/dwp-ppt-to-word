<template>
  <p class="mt-5 pt-0 ml-6 text-left font-weight-bold txt-header">
    {{ item.title || "-" }}
  </p>

  <v-card
    style="
      border-radius: 12px;
      height: 500px;
      box-shadow: 0px 4px 18px 0px rgba(192, 192, 192, 0.25);
    "
    class="ml-6 pl-4 mr-5 mt-5"
  >
    <paragraph-shimmer
      v-if="isLoading"
      :is-loading="true"
      :lines="15"
      :random-size="true"
      class="mt-5 mr-5"
    />
    <v-sheet class="d-flex ml-4 mr-4 mt-4" v-if="!isLoading">
      <v-sheet class="me-auto">
        <v-btn v-if="item.liveStatus" class="ml-0 btn-live">
          <span class="txt-white-btn">Live</span>
        </v-btn>
      </v-sheet>
      <v-sheet class="">
        <v-btn
          class="btn-join mr-3 text-white font-weight-regular"
          @click="openMeeting"
          v-if="['Online', 'Hybrid'].includes(item.method)"
          :disabled="
            handleDisableJoin(
              item.eventlink === 'EventLink' ||
                item.eventlink === '' ||
                !item.eventlink
            )
          "
        >
          Join
          <template #prepend>
            <img :src="require('@/v2/assets/icon/camera.svg')" />
          </template>
        </v-btn>
      </v-sheet>
      <v-sheet class="mr-3" v-if="item.isDelete">
        <v-btn
          color="#D6212A"
          class="rounded-lg"
          variant="outlined"
          @click="showDelete"
        >
          Delete
          <template v-slot:prepend>
            <v-icon class="table-content-center" color="#D6212A" small>
              mdi-delete
            </v-icon>
          </template>
        </v-btn>
      </v-sheet>
      <v-sheet class="mr-3" v-if="item.isCancel">
        <v-btn
          color="#FF000D"
          class="rounded-lg"
          variant="outlined"
          @click="showCancelEvent"
        >
          Cancel Event
          <template v-slot:prepend>
            <v-icon class="table-content-center" color="#D6212A" small>
              mdi-sync-off
            </v-icon>
          </template>
        </v-btn>
      </v-sheet>
      <v-sheet class="mr-3" v-if="item.isPublish">
        <v-btn
          color="#00783E"
          class="rounded-lg"
          variant="outlined"
          @click="showPublishEvent"
        >
          Publish Event
          <template v-slot:prepend>
            <v-icon class="table-content-center" color="#02AA59" small>
              mdi-access-point
            </v-icon>
          </template>
        </v-btn>
      </v-sheet>
      <v-sheet class="mr-3">
        <edit-event-view v-if="item.isEdit" @refreshData="emits('refresh')" />
      </v-sheet>
    </v-sheet>

    <v-card-text>
      <v-row no-gutters>
        <v-col cols="6">
          <p class="txt-title">Time</p>
          <div class="d-flex align-center">
            <v-icon
              color="#b5b5b5"
              size="23"
              icon="mdi-clock-outline"
              class="mr-2"
            />
            <p class="text-newBlack font-weight-medium text-13">
              {{
                item.eventstart && item.eventend
                  ? reformatDateLong(item.eventstart, item.eventend)
                  : "-"
              }}
            </p>
          </div>

          <div class="d-flex align-center">
            <v-icon
              color="#fff"
              size="23"
              icon="mdi-clock-outline"
              class="mr-2"
            />
            <p class="text-newBlack font-weight-medium text-13">
              {{ item.eventstart ? reformatTimes(item.eventstart) : "-" }}
              -
              {{ item.eventend ? reformatTimes(item.eventend) : "-" }} WIB
            </p>
          </div>

          <p class="txt-title mt-5">Method</p>
          <div class="d-flex align-center">
            <p class="text-newBlack font-weight-medium text-13">
              {{ item.method || "-" }}
            </p>
          </div>

          <template v-if="['Online'].includes(item.method)">
            <p class="txt-title mt-5">Media</p>
            <div class="d-flex align-center">
              <v-icon
                color="#b5b5b5"
                size="23"
                icon="mdi-map-marker-outline"
                class="mr-2 align-self-start"
              />
              <p class="text-newBlack font-weight-medium text-13">
                {{ item.platform || "-" }}
              </p>
            </div>
          </template>

          <template v-if="['Offline'].includes(item.method)">
            <p class="txt-title mt-5">Place</p>
            <div class="d-flex align-center">
              <v-icon
                color="#b5b5b5"
                size="23"
                icon="mdi-map-marker-outline"
                class="mr-2 align-self-start"
              />
              <p class="text-newBlack font-weight-medium text-13">
                {{ item.eventplace || "-" }}
              </p>
            </div>
          </template>
          <template v-if="['Hybrid'].includes(item.method)">
            <p class="txt-title mt-5">Media / Place</p>
            <div class="d-flex align-center">
              <v-icon
                color="#b5b5b5"
                size="23"
                icon="mdi-map-marker-outline"
                class="mr-2 align-self-start"
              />
              <p class="text-newBlack font-weight-medium text-13">
                {{ item.platform + " / " + item.eventplace || "-" }}
              </p>
            </div>
          </template>

          <p class="txt-title">Participant</p>
          <div class="d-flex align-center">
            <v-icon
              color="#b5b5b5"
              size="23"
              icon="mdi-account-outline"
              class="mr-2 align-self-start"
            />
            <div style="overflow-y: auto; max-height: 150px; margin-top: 5px">
              <p class="text-newBlack font-weight-medium text-13">
                {{
                  showMoreParticipants || !item.participants
                    ? item.participants
                    : truncatedParticipants
                }}
                <span class="txt-blue-btn">
                  <a
                    v-if="shouldShowMoreLink"
                    @click="toggleParticipants"
                    style="cursor: pointer"
                  >
                    {{
                      showMoreParticipants ? "\nSee Less <<" : "\nSee More>>"
                    }}
                  </a>
                </span>
              </p>
            </div>
          </div>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
  <ModalConfirm
    ref="modal"
    :form-config="formDelete"
    @action-confirm="deleteMeeting"
  />
  <ModalConfirm
    ref="modalPublish"
    :form-config="formPublish"
    @action-confirm="publishEvent"
  />
  <ModalConfirm
    ref="modalCancel"
    :form-config="formCancel"
    :isLoading="loading"
    @action-confirm="cancelEvent"
  />
</template>

<script setup lang="ts">
import { reformatDateLong, reformatTimes } from "@/v2/helpers/DateHelper";
import { ref, computed, getCurrentInstance, nextTick } from "vue";
import EditEventView from "@/v2/views/EditEventView.vue";
import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";
import { defineComponent } from "vue";
import { TModalConfirm, TResponsePromise } from "@v2/Type.d";
import { responsePromise } from "@v2/helpers/utils";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";

const emits = defineEmits(["refresh"]);

defineComponent({
  components: {
    EditEventView,
  },
});

const prop = defineProps({
  isLoading: {
    type: Boolean,
    default: false,
  },
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
});

const { root } = getCurrentInstance() as any;
const response = responsePromise(root);
const route = useRoute();
const router = useRouter();
const store = useStore();
const loading = ref(false);
const isDisableAllButton = computed(
  () => store.getters["meetingStore/getModeDisableBtn"]
);

function openMeeting() {
  const newTab = window.open(prop.item.eventlink, "_blank");
  if (newTab) {
    newTab.focus();
  }
}
const showMoreParticipants = ref(false);

const truncatedParticipants = computed(() => {
  const firstBatch = getBatchParticipant(20).firstBatch;
  return firstBatch.join(", ");
});

const shouldShowMoreLink = computed(() => {
  const lastBatch = getBatchParticipant(20).lastBatch;
  return lastBatch?.length > 0;
});

const toggleParticipants = () => {
  showMoreParticipants.value = !showMoreParticipants.value;
};

//delete meeting
const modal = ref();
const formDelete = ref<TModalConfirm>({
  title: "Delete Meeting",
  message: "Are you sure delete this Meeting? ",
  btnSubmitLabel: "Yes",
  usingTimeOut: false,
});

const modalPublish = ref();
const modalCancel = ref();
const formPublish = ref<TModalConfirm>({
  title: "Publish Event",
  titleClass: "mb-4 font-weight-bold text-h6",
  message:
    "Publishing this event will send outlook notifications to all participants. Are you sure you want to proceed?",
  btnSubmitLabel: "Yes",
  width: 554,
  btnSubmitColor: "primary-gradient",
  showIcon: false,
});

const formCancel = ref<TModalConfirm>({
  title: "Cancel Event",
  titleClass: "mb-4 font-weight-bold text-h6",
  message:
    "Are you sure to cancel this event? <br />This action will cancel the event and recall all notifications that have already been sent.",
  btnSubmitLabel: "Yes",
  width: 554,
  btnSubmitColor: "primary-red-gradient",
  showIcon: false,
});

function getBatchParticipant(split: number) {
  const arrParticipants = prop.item.participants?.split(", ");
  const splitIndex = Math.min(arrParticipants?.length, split);
  const firstBatch = arrParticipants?.slice(0, splitIndex);
  const lastBatch = arrParticipants?.slice(splitIndex);
  return {
    firstBatch: firstBatch,
    lastBatch: lastBatch,
  };
}

function handleDisableJoin(linkInvalid: boolean) {
  if (isDisableAllButton.value) {
    return isDisableAllButton.value;
  } else {
    return linkInvalid;
  }
}

function showDelete() {
  modal.value.show({});
}

function showPublishEvent() {
  modalPublish.value.show();
}

function showCancelEvent() {
  modalCancel.value.show();
}

function deleteMeeting() {
  store
    .dispatch("eventStore/deleteEvent", {
      id: route.params.idEvent,
    })
    .then((res) => {
      const responseData = {
        responseCode: res.responseCode,
        responseMessage: res.responseMessage,
        responseData: { description: "Successfully deleted" },
      } as TResponsePromise;
      response.success(responseData, function () {
        router.push({ name: "v2.meeting-management" });
      });
    })
    .catch(response.error);
}

function publishEvent() {
  store
    .dispatch("eventStore/publishEvent", {
      id: route.params.idEvent,
    })
    .then(() => {
      root.refs.toast.show({
        message: "Successfully Publish event",
        color: "success",
        timeout: 3000,
      });

      nextTick(() => {
        modalPublish.value.hide();
      });
    })
    .catch(response.error);
}

function cancelEvent() {
  loading.value = true;
  store
    .dispatch("eventStore/cancelEvent", {
      id: route.params.idEvent,
    })
    .then(() => {
      root.refs.toast.show({
        message: "Successfully cancel event",
        color: "success",
        timeout: 3000,
      });
    })
    .catch(() => {
      root.refs.toast.show({
        message: "Failed cancel event",
        color: "error",
        timeout: 9000,
      });
    })
    .finally(() => {
      modalCancel.value.hide();
      loading.value = false;
      emits("refresh");
    });
}
</script>

<style scoped>
.card-detail {
  border-radius: 16px;
  background: var(--White-Colot, #fff);
  box-shadow: 0px 4px 18px 0px rgba(192, 192, 192, 0.25);
  background-size: 100% 100%;
  height: 100%;
  overflow-y: auto;
  position: sticky;
}
.btn-live {
  display: inline-flex;
  padding: 4px 12px;
  justify-content: center;
  align-items: center;
  gap: 8px;
  border-radius: 4px;
  background: var(
    --Gradient-Red,
    linear-gradient(180deg, #d6212a 0%, #ff000d 100%)
  );
  box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.25);
}
.btn-join {
  display: flex;
  height: 36px;
  padding: 8px 14px;
  align-items: flex-end;
  justify-content: flex-end;
  border-radius: 8px;
  background: var(
    --Gradient-Blue,
    linear-gradient(180deg, #065695 0%, #267dc2 100%)
  );
}
.btn-edit {
  display: flex;
  padding: 6px 12px;
  align-items: center;
  gap: 4px;
  border-radius: 10px;
  border: 1px solid var(--Gradient-Blue, #065695);
}
.txt-white-btn {
  text-align: center;
  font-family: Poppins;
  font-size: 14px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
  background: linear-gradient(0deg, #fff 0%, #fff 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.txt-blue-btn {
  font-family: Poppins;
  font-size: 14px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
  background: var(
    --Gradient-Blue,
    linear-gradient(180deg, #065695 0%, #267dc2 100%)
  );
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.txt-header {
  color: var(--Black-NEW-VERSION, #4b4b4b);
  font-family: Poppins;
  font-size: 32px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
}
.txt-title {
  background: var(
    --Grey,
    linear-gradient(
      93deg,
      rgba(121, 121, 121, 0.9) 0%,
      rgba(187, 187, 187, 0.9) 152.21%
    )
  );
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-family: Poppins;
  font-size: 15px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
  margin-top: 10px;
}
.txt-item {
  color: var(--Black-NEW-VERSION, #4b4b4b);
  font-family: Poppins;
  font-size: 15px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
}
</style>
