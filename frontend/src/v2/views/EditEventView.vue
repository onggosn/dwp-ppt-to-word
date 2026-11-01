<template>
  <v-row justify="center">
    <v-btn
      color="#065695"
      class="ma-3 rounded-lg"
      variant="outlined"
      :disabled="isDisableAllButton"
      :loading="isLoading"
      @click="startEdit"
    >
      Edit
      <template v-slot:prepend>
        <img :src="require('@/v2/assets/icon/edit.svg')" />
      </template>
    </v-btn>
    <v-dialog
      v-model="dialog"
      persistent
      width="700"
      :retain-focus="false"
      no-click-animation
    >
      <template> </template>
      <v-card class="border-radius-dwp">
        <v-form @submit.prevent="submitForm" class="pl-2 pr-2">
          <v-card-title class="text-center mt-3">
            <h3 class="text-h6 font-weight-regular">Edit Event</h3>
            <v-btn
              density="default"
              icon="mdi-close"
              variant="text"
              class="btn-close"
              @click="dialog = false"
            />

            <hr class="line mt-5 mb-4" />
          </v-card-title>

          <v-card-text>
            <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
              Title<span style="color: red">*</span>
            </p>
            <v-chip class="chip-shadow border-radius-dwp ml-2 mr-2">
              {{ state._title }}
            </v-chip>
            <p class="ml-2 pb-1 mt-4 text-left text-darkBlue font-weight-bold">
              Description<span style="color: red">*</span>
            </p>
            <div class="mx-2 my-2">
              <div ref="myEditor" id="editingEditor" />
            </div>
            <v-textarea
              v-model="state._description"
              variant="solo"
              placeholder="Write your description here"
              class="pl-2 pr-2 textareadescription"
              :error-messages="getErrorMessages(v$._description)"
            ></v-textarea>
            <p class="ml-2 pb-1 mt-2 text-left text-darkBlue font-weight-bold">
              Method<span style="color: red">*</span>
            </p>
            <v-select
              v-model="state._method"
              variant="solo"
              placeholder="Online / Offline / Hybrid"
              class="pl-2 pr-2"
              item-title="value"
              item-value="id"
              :items="eventMethod"
              :error-messages="getErrorMessages(v$._method)"
            ></v-select>

            <template v-if="[1, 3].includes(state._method)">
              <p
                class="ml-2 pb-1 mt-2 text-left text-darkBlue font-weight-bold"
              >
                Main Media<span style="color: red">*</span>
              </p>
              <v-select
                v-model="state._meetingPlatform"
                variant="solo"
                placeholder="MS Teams / Zoom / Webex"
                class="pl-2 pr-2"
                :items="meetingPlatform"
                item-title="platform"
                item-value="id"
                :error-messages="getErrorMessages(v$._meetingPlatform)"
              ></v-select>
            </template>

            <template
              v-if="
                [1, 3].includes(state._method) &&
                [2, 3, 4].includes(state._meetingPlatform)
              "
            >
              <p
                class="ml-2 pb-1 mt-2 text-left text-darkBlue font-weight-bold"
              >
                Main Link<span style="color: red">*</span>
              </p>
              <v-text-field
                v-model="state._eventlink"
                variant="solo"
                type="url"
                placeholder="Put your link here"
                class="pl-2 pr-2"
                :error-messages="
                  getErrorMessages(v$._eventlink, {
                    url: 'Url yang dimasukkan tidak valid',
                    startsWithZoomUs: 'URL must contain http://zoom.us',
                    startsWithWebexCom: 'URL must contain https://webex.com',
                  })
                "
              ></v-text-field>
            </template>

            <template v-if="[1, 3].includes(state._method)">
              <p
                class="ml-2 pb-1 mt-2 text-left text-darkBlue font-weight-bold"
              >
                Backup Media
              </p>
              <v-select
                v-model="state._meetingPlatformBackup"
                variant="solo"
                placeholder="MS Teams / Zoom / Webex"
                class="pl-2 pr-2"
                :items="meetingPlatform"
                item-title="platform"
                item-value="id"
              >
                <template v-slot:item="{ props, item }">
                  <v-list-item
                    v-bind="props"
                    :disabled="item.raw.id == state._meetingPlatform"
                  ></v-list-item>
                </template>
              </v-select>
            </template>

            <template
              v-if="
                [1, 3].includes(state._method) &&
                [2, 3, 4].includes(state._meetingPlatformBackup)
              "
            >
              <p
                class="ml-2 pb-1 mt-2 text-left text-darkBlue font-weight-bold"
              >
                Backup Link
              </p>
              <v-text-field
                v-model="state._eventlinkBackup"
                variant="solo"
                type="url"
                placeholder="Put your link here"
                class="pl-2 pr-2"
              ></v-text-field>
            </template>

            <template v-if="[2, 3].includes(state._method)">
              <p
                class="ml-2 pb-1 mt-2 text-left text-darkBlue font-weight-bold"
              >
                Place<span style="color: red">*</span>
              </p>
              <v-text-field
                v-model="state._eventPlace"
                variant="solo"
                placeholder="Insert your place here"
                class="pl-2 pr-2"
                :error-messages="
                  getErrorMessages(v$._eventPlace, {
                    notRelevantSymbol:
                      'Tempat acara tidak boleh mengandung simbol yang tidak relevan',
                    minLengthValue:
                      'Tempat acara minimal 3 mengandung karakter',
                  })
                "
              >
              </v-text-field>
            </template>

            <v-row no-gutters>
              <v-col cols="12" sm="6">
                <p
                  class="ml-2 pb-1 mt-2 text-left text-darkBlue font-weight-bold"
                >
                  Start <span style="color: red">*</span>
                </p>
                <v-tooltip
                  text="Perubahan tanggal hanya dapat dilakukan pada edit Agenda"
                  location="bottom"
                >
                  <template v-slot:activator="{ props }">
                    <div v-bind="props" class="pl-2 pr-2">
                      <v-chip
                        :text="state._datePickerStart || 'Choose Start Date'"
                        variant="elevated"
                        color="grey-lighten-3"
                        size="large"
                        class="chip-shadow border-radius-dwp chip-with-right-icon"
                        style="margin-left: 0 !important; padding: 1em"
                      >
                        <template v-slot:append>
                          <img
                            :src="require('@/v2/assets/icon/date.svg')"
                            style="
                              filter: grayscale(100%) brightness(1.2)
                                opacity(0.6);
                            "
                            class="date-icon-right"
                          />
                        </template>
                      </v-chip>
                    </div>
                  </template>
                </v-tooltip>
              </v-col>
              <v-col cols="12" sm="6">
                <p
                  class="ml-2 pb-1 mt-2 text-left text-darkBlue font-weight-bold text-white"
                >
                  --
                </p>
                <v-tooltip
                  text="Perubahan waktu hanya dapat dilakukan pada edit Agenda"
                  location="bottom"
                >
                  <template v-slot:activator="{ props }">
                    <div v-bind="props" class="pl-2 pr-2">
                      <v-chip
                        :text="state._startTime || 'Start Time'"
                        variant="elevated"
                        color="grey-lighten-3"
                        size="large"
                        class="chip-shadow border-radius-dwp ml-2 mr-2"
                        style="padding: 1em"
                      />
                    </div>
                  </template>
                </v-tooltip>
              </v-col>
            </v-row>

            <v-row no-gutters>
              <v-col cols="12" sm="6">
                <p
                  class="ml-2 pb-1 mt-2 text-left text-darkBlue font-weight-bold"
                >
                  End<span style="color: red">*</span>
                </p>
                <v-tooltip
                  text="Perubahan tanggal hanya dapat dilakukan pada edit Agenda"
                  location="bottom"
                >
                  <template v-slot:activator="{ props }">
                    <div v-bind="props" class="pl-2 pr-2">
                      <v-chip
                        :text="state._datePickerEnd || 'Choose End Date'"
                        variant="elevated"
                        color="grey-lighten-3"
                        size="large"
                        class="chip-shadow border-radius-dwp chip-with-right-icon ml-2 mr-2"
                        style="margin-left: 0 !important; padding: 1em"
                      >
                        <template v-slot:append>
                          <img
                            :src="require('@/v2/assets/icon/date.svg')"
                            style="
                              filter: grayscale(100%) brightness(1.2)
                                opacity(0.6);
                            "
                            class="date-icon-right"
                          />
                        </template>
                      </v-chip>
                    </div>
                  </template>
                </v-tooltip>
              </v-col>
              <v-col cols="12" sm="6">
                <p
                  class="ml-2 pb-1 mt-2 text-left text-darkBlue font-weight-bold text-white"
                >
                  --
                </p>
                <v-tooltip
                  text="Perubahan waktu hanya dapat dilakukan pada edit Agenda"
                  location="bottom"
                >
                  <template v-slot:activator="{ props }">
                    <div v-bind="props" class="pl-2 pr-2">
                      <v-chip
                        :text="state._endTime || 'End Time'"
                        variant="elevated"
                        color="grey-lighten-3"
                        size="large"
                        class="chip-shadow border-radius-dwp ml-2 mr-2"
                        style="padding: 1em"
                      />
                    </div>
                  </template>
                </v-tooltip>
              </v-col>
            </v-row>

            <p class="ml-2 pb-1 mt-2 text-left text-darkBlue font-weight-bold">
              Participant <span style="color: red">*</span>
            </p>

            <v-autocomplete
              id="participant"
              v-model="state._listParticipant"
              variant="solo"
              placeholder="Add Participant"
              multiple
              chips
              clearable
              :items="searchParticipantResult"
              item-title="value"
              hide-selected
              closable-chips
              :error-messages="
                getErrorMessages(v$._listParticipant, {
                  required: 'Pilih setidaknya 1 participant',
                })
              "
              @update:modelValue="updateParticipant"
              return-object
              v-model:search="searchParticipant"
              class="pl-2 pr-2"
            >
              <template v-slot:item="{ props, item }">
                <v-list-item
                  class="mt-2"
                  v-bind="props"
                  :title="item.raw.value"
                  :subtitle="item.raw.inputEmail"
                ></v-list-item>
              </template>
              <template v-slot:chip="{ props, item }">
                <v-chip
                  variant="flat"
                  v-bind="props"
                  class="px-3 mx-1"
                  :style="{
                    borderRadius: '0.25rem',
                    border: `1px solid ${
                      item.value.id ? '#2279bd' : '#f44336'
                    }`,
                    backgroundColor: item.value.id ? '#e9f5ff' : '#f5e9e9',
                  }"
                >
                  <template v-slot:default>
                    <span
                      :style="{ color: item.value.id ? '#2279bd' : '#f44336' }"
                      >{{ item.value.value ?? item.value.inputEmail }}</span
                    >
                  </template>
                </v-chip>
              </template>
              <template v-slot:append-inner>
                <v-icon
                  v-if="store.getters['userStore/getLoading']"
                  color="primary"
                  dark
                  class="mr-2"
                >
                  mdi-loading mdi-spin
                </v-icon>
              </template>
            </v-autocomplete>

            <p class="ml-2 pb-1 mt-2 text-left text-darkBlue font-weight-bold">
              Organizer <span style="color: red">*</span>
            </p>
            <v-autocomplete
              id="organizer"
              v-model="state._listOrganizer"
              variant="solo"
              placeholder="Add Organizer"
              multiple
              chips
              :items="searchOrganizerResult"
              item-title="value"
              hide-selected
              closable-chips
              @update:modelValue="updateOrganizer"
              return-object
              v-model:search="searchOrganizer"
              class="pl-2 pr-2"
              :error-messages="
                getErrorMessages(v$._listOrganizer, {
                  required: 'Pilih setidaknya 1 organizer',
                })
              "
            >
              <template v-slot:chip="{ props, item }">
                <v-chip
                  v-bind="props"
                  :closable="item.raw.isDelete === true ? true : false"
                  :color="item.raw.isDelete === true ? '' : 'grey'"
                  variant="flat"
                  :style="{
                    borderRadius: '0.25rem',
                    border: `1px solid ${item.raw.id ? '#2279bd' : '#f44336'}`,
                    backgroundColor: item.value.id ? '#e9f5ff' : '#f5e9e9',
                  }"
                  >{{ item.raw.value ?? item.raw.inputEmail }}</v-chip
                >
              </template>
              <template v-slot:item="{ props, item }">
                <v-list-item
                  class="mt-2"
                  v-bind="props"
                  :title="item.raw.value"
                  :subtitle="item.raw.inputEmail"
                ></v-list-item>
              </template>
              <template v-slot:append-inner>
                <v-icon
                  v-if="store.getters['userStore/getLoading']"
                  color="primary"
                  dark
                  class="mr-2"
                >
                  mdi-loading mdi-spin
                </v-icon>
              </template>
            </v-autocomplete>

            <p class="ml-2 pb-1 mt-2 text-left text-darkBlue font-weight-bold">
              Pemrakarsa
            </p>

            <v-autocomplete
              id="pemrakarsa"
              v-model="state._listPemrakarsa"
              variant="solo"
              placeholder="Choose Pemrakarsa"
              multiple
              chips
              clearable
              :items="searchPemrakarsaResult"
              item-title="value"
              hide-selected
              closable-chips
              @update:modelValue="updatePemrakarsa"
              return-object
              v-model:search="searchPemrakarsa"
              class="pl-2 pr-2"
            >
              <template v-slot:item="{ props, item }">
                <v-list-item
                  class="mt-2"
                  v-bind="props"
                  :title="item.raw.value"
                  :subtitle="item.raw.inputEmail"
                ></v-list-item>
              </template>
              <template v-slot:append-inner>
                <v-icon
                  v-if="store.getters['userStore/getLoading']"
                  color="primary"
                  dark
                  class="mr-2"
                >
                  mdi-loading mdi-spin
                </v-icon>
              </template>
              <template v-slot:chip="{ props, item }">
                <v-chip
                  variant="flat"
                  v-bind="props"
                  class="px-3 mx-1"
                  :style="{
                    borderRadius: '0.25rem',
                    border: `1px solid ${
                      item.value.id ? '#2279bd' : '#f44336'
                    }`,
                    backgroundColor: item.value.id ? '#e9f5ff' : '#f5e9e9',
                  }"
                >
                  <template v-slot:default>
                    <span
                      :style="{ color: item.value.id ? '#2279bd' : '#f44336' }"
                      >{{ item.value.value ?? item.value.inputEmail }}</span
                    >
                  </template>
                </v-chip>
              </template>
            </v-autocomplete>

            <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
              Anggota Dewan Gubernur
            </p>

            <v-sheet class="d-flex flex-wrap">
              <template v-for="item in listDewanGubernur" :key="item.id">
                <v-checkbox
                  style="width: 300px"
                  v-model="state._listDewanGubernur"
                  :label="item.value"
                  color="success"
                  :value="item"
                  hide-details
                ></v-checkbox>
              </template>
            </v-sheet>
          </v-card-text>
          <div class="text-right mt-3 pb-5 pr-5">
            <v-btn
              class="btn-prev mr-3"
              @click="dialog = false"
              elevation="4"
              width="100"
              height="45"
              :loading="store.getters['eventStore/getLoading']"
              >Cancel</v-btn
            >
            <v-btn
              class="btn-next"
              elevation="4"
              width="100"
              height="45"
              :loading="store.getters['eventStore/getLoading']"
              :disabled="isSaveDisabled"
              @click="submitForm"
              >Save</v-btn
            >
          </div>
        </v-form>
      </v-card>
    </v-dialog>

    <ModalConfirm
      ref="modalSubmit"
      :form-config="formValidate"
      :is-loading="isLoading"
    >
      <template v-slot:desc>
        <div
          class="txt-message mx-4"
          style="text-align: left; color: grey"
          v-html="formValidate.message"
        ></div>
      </template>

      <template v-slot:btn-action>
        <!-- meetingDetails buttons -->
        <div v-if="popUpType === 'meetingDetails'" class="text-end mt-4">
          <v-btn
            class="btn-prev"
            elevation="4"
            width="100"
            height="45"
            :loading="isLoading"
            @click="processSubmit(formData, 'DontSendNotification')"
            >No, Skip</v-btn
          >
          <v-btn
            class="btn-next ml-2"
            elevation="4"
            width="117"
            height="45"
            :loading="isLoading"
            @click="processSubmit(formData, 'AllParticipant')"
            >Yes, Send</v-btn
          >
        </div>

        <!-- meetingAttendees buttons -->
        <div v-if="popUpType === 'meetingAttendees'" class="text-end mt-4">
          <v-btn
            v-if="!isOutlook"
            class="btn-cancel"
            elevation="4"
            width="198"
            height="45"
            :loading="isLoading"
            @click="processSubmit(formData, 'DontSendNotification')"
            >Don't Send Notification</v-btn
          >
          <v-btn
            class="btn-prev ml-2"
            elevation="4"
            width="132"
            height="45"
            :loading="isLoading"
            @click="processSubmit(formData, 'AllParticipant')"
            >All Participant</v-btn
          >
          <div v-if="isOutlook" class="tooltip-wrapper">
            <v-tooltip
              :text="isDifferentDataOutlookWithDB ? tooltipLabel : ''"
              location="top"
              :disabled="!isDifferentDataOutlookWithDB"
            >
              <template v-slot:activator="{ props }">
                <div v-bind="props" class="btn-wrapper">
                  <v-btn
                    class="btn-next ml-2"
                    elevation="4"
                    width="287"
                    height="45"
                    :loading="isLoading"
                    @click="
                      processSubmit(formData, 'OnlyAddedOrRemovedAttendees')
                    "
                    :disabled="isDifferentDataOutlookWithDB"
                    >Only Added/Removed Attendees</v-btn
                  >
                </div>
              </template>
            </v-tooltip>
          </div>
        </div>
      </template>
    </ModalConfirm>
  </v-row>
</template>
<script setup lang="ts">
import {
  ref,
  getCurrentInstance,
  computed,
  reactive,
  watch,
  nextTick,
} from "vue";
import { useStore } from "vuex";
import { required, url, minLength } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import { useRoute } from "vue-router";
import { getErrorMessages, notRelevantSymbol } from "@v2/helpers/validation";
import { responsePromise, removeIrregulerSpace } from "@v2/helpers/utils";
import { TModalConfirm } from "@v2/Type.d";
import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";
import { messageEditEvent } from "@v2/enum/Enum";
// import Editor from "@tinymce/tinymce-vue";
import EditorOutput from "@/v2/components/side-project/ckeditor/build/ckeditor";
import { debounce } from "lodash";
import { useInitializeConfig } from "@/v2/composables/useInitializeConfig";

const { root } = getCurrentInstance() as any;
const response = responsePromise(root);
const isLoading = ref(false);
const emits = defineEmits(["refreshData"]);
const route = useRoute();
const store = useStore();
const { ckEditorLicense } = useInitializeConfig();
const dialog = ref(false);
const popUpType = ref("");
const isOutlook = ref(false);
const isDifferentDataOutlookWithDB = ref(false);
const tooltipLabel = ref(
  "The meeting is updated. Outlook cannot send updates exclusively to added or removed attendees."
);
const eventMethod = ref([]);
const searchParticipant = ref();
const modalSubmit = ref();
const searchParticipantResult = ref<any>([]);
const searchOrganizer = ref();
const searchOrganizerResult = ref<any>([]);
const searchPemrakarsaResult = ref<any>([]);
const searchPemrakarsa = ref();
const listDewanGubernur = ref<any[]>([]);
const meetingPlatform = ref([]);
const isDisableAllButton = computed(
  () => store.getters["meetingStore/getModeDisableBtn"]
);
const listAdg = computed(() => store.getters["meetingStore/getListAdg"]);
const myEditor = ref<HTMLDivElement | string>("");
let editorInstance: any;
const originalDescription = ref("");
const currentEditorData = ref("");
const originalMethod = ref(0);
const originalMeetingPlatform = ref(null);
const originalEventLink = ref("");
const originalMeetingPlatformBackup = ref(null);
const originalEventLinkBackup = ref("");
const originalEventPlace = ref("");
const originalListParticipant = ref([]);
const originalListOrganizer = ref([]);
const originalListPemrakarsa = ref([]);
const originalListDewanGubernur = ref([]);
const startsWithZoomUs = (value: string) => {
  if (!value) return true;
  return value.startsWith("http://zoom.us");
};

const startsWithWebexCom = (value: string) => {
  if (!value) return true;
  return value.startsWith("https://webex.com");
};

const isDescriptionChanged = computed(() => {
  return currentEditorData.value !== originalDescription.value;
});

const isMethodChanged = computed(() => {
  return state._method !== originalMethod.value;
});

const isMeetingPlatformChanged = computed(() => {
  return state._meetingPlatform !== originalMeetingPlatform.value;
});

const isEventLinkChanged = computed(() => {
  return state._eventlink !== originalEventLink.value;
});

const isMeetingPlatformBackupChanged = computed(() => {
  return state._meetingPlatformBackup !== originalMeetingPlatformBackup.value;
});

const isEventLinkBackupChanged = computed(() => {
  return state._eventlinkBackup !== originalEventLinkBackup.value;
});

const isEventPlaceChanged = computed(() => {
  return state._eventPlace !== originalEventPlace.value;
});

const isListParticipantChanged = computed(() => {
  return (
    JSON.stringify(state._listParticipant) !==
    JSON.stringify(originalListParticipant.value)
  );
});

const isListOrganizerChanged = computed(() => {
  return (
    JSON.stringify(state._listOrganizer) !==
    JSON.stringify(originalListOrganizer.value)
  );
});

const isListPemrakarsaChanged = computed(() => {
  return (
    JSON.stringify(state._listPemrakarsa) !==
    JSON.stringify(originalListPemrakarsa.value)
  );
});

const isListDewanGubernurChanged = computed(() => {
  return (
    JSON.stringify(state._listDewanGubernur) !==
    JSON.stringify(originalListDewanGubernur.value)
  );
});

const hasInvalidMember = computed(() =>
  [
    ...state._listParticipant,
    ...state._listOrganizer,
    ...state._listPemrakarsa,
  ].some((i: any) => !i.id)
);

const isSaveDisabled = computed(() => {
  return (
    (!isDescriptionChanged.value &&
      !isMethodChanged.value &&
      !isMeetingPlatformChanged.value &&
      !isEventLinkChanged.value &&
      !isMeetingPlatformBackupChanged.value &&
      !isEventLinkBackupChanged.value &&
      !isEventPlaceChanged.value &&
      !isListParticipantChanged.value &&
      !isListOrganizerChanged.value &&
      !isListPemrakarsaChanged.value &&
      !isListDewanGubernurChanged.value) ||
    hasInvalidMember.value ||
    store.getters["eventStore/getLoading"]
  );
});

const formValidate = ref<TModalConfirm>({
  title: "Send Outlook Update",
  titleClass: "text-20 mb-4",
  message: "",
  btnSubmitLabel: "Yes",
  width: 554,
  btnSubmitColor: "primary-gradient",
  showIcon: false,
});

const initialState = ref({
  _id: "",
  _title: "",
  _description: "",
  _method: 0,
  _meetingPlatform: 0,
  _meetingPlatformBackup: null,
  _eventlink: "",
  _eventlinkBackup: "",
  _eventPlace: "",
  _datePickerStart: "",
  _startTime: "",
  _datePickerEnd: "",
  _endTime: "",
  _listParticipant: [],
  _listOrganizer: [],
  _listPemrakarsa: [],
  _listDewanGubernur: [],
  _popUpNotifType: [],
  _meetingDetailsOutlook: [],
  _meetingAttendeesOutlook: [],
});
const state = reactive({
  ...initialState.value,
});

const rules = computed(() => {
  const localRule = {
    _description: { required },
    _method: { required },
    _meetingPlatform: {},
    _eventlink: {},
    _eventPlace: {},
    _listParticipant: { required },
    _listOrganizer: { required },
    _listDewanGubernur: {},
  };

  if ([1, 3].includes(state._method)) {
    localRule._meetingPlatform = { required };
  }

  if (
    [1, 3].includes(state._method) &&
    [2, 3, 4].includes(state._meetingPlatform)
  ) {
    localRule._eventlink = { required, url };
    if (state._meetingPlatform === 2) {
      localRule._eventlink = {
        ...localRule._eventlink,
        startsWithZoomUs,
      };
    } else if ([3, 4].includes(state._meetingPlatform)) {
      localRule._eventlink = {
        ...localRule._eventlink,
        startsWithWebexCom,
      };
    }
  }

  if ([2, 3].includes(state._method)) {
    Object.assign(localRule._eventPlace, {
      required,
      notRelevantSymbol,
      minLengthValue: minLength(3),
    });
  }
  return localRule;
});
const v$ = useVuelidate(rules, state);

async function initEditor() {
  editorInstance = await EditorOutput.CustomClassic.create(myEditor.value, {
    initialData: state._description,
    updateSourceElementOnDestroy: false,
    toolbar: {
      items: [
        "undo",
        "redo",
        "heading",
        "|",
        "bold",
        "italic",
        "|",
        "link",
        "insertTable",
        "bulletedList",
        "numberedList",
        "|",
      ],
    },
    licenseKey: ckEditorLicense.value,
  });

  // Set initial current editor data
  currentEditorData.value = editorInstance.getData();

  // Listen for content changes in the editor
  editorInstance.model.document.on("change:data", () => {
    const editorData = editorInstance.getData();
    // Update current editor data to track changes
    currentEditorData.value = editorData;
  });
}

const startEdit = async () => {
  listDewanGubernur.value = listAdg.value.map((item: any) => ({
    id: item.id,
    value: item.displayName,
    isGroup: false,
  }));

  store.dispatch("eventStore/fetchListMeetingMethod").then((data) => {
    eventMethod.value = data;
  });

  store.dispatch("eventStore/fetchListMeetingPlatform").then((data) => {
    meetingPlatform.value = data;
  });

  isLoading.value = true;
  store
    .dispatch("eventStore/fetchEditEventData", route.params.idEvent)
    .then((data) => {
      if (Object.keys(data).length === 0) {
        // useToast().error("Failed to fetch data");
        root.refs.toast.show({
          message: "Failed to fetch data from server",
          color: "warning",
          timeout: 3000,
        });
        isLoading.value = false;
      } else {
        state._id = data.idEvent;
        state._title = data.title;
        state._description = data.description;
        state._method = data.idMethod;
        state._meetingPlatform = data.idMeetingPlatform;
        state._meetingPlatformBackup = data.idMeetingBackupPlatform;
        state._eventlink = data.eventlink;
        state._eventlinkBackup = data.eventLinkBackup;
        state._eventPlace = data.eventPlace;
        state._datePickerStart = formatDate(data.startDate);
        state._startTime = formatDateTime(data.startDate);
        state._datePickerEnd = formatDate(data.endDate);
        state._endTime = formatDateTime(data.endDate);
        state._listParticipant = data.listParticipant;
        state._listOrganizer = data.listOrganizer;
        state._listPemrakarsa = data.listPemrakarsa;
        state._listDewanGubernur = data.listAdg;

        originalDescription.value = data.description;
        currentEditorData.value = data.description;
        originalMethod.value = data.idMethod;

        originalMeetingPlatform.value = data.idMeetingPlatform;
        originalEventLink.value = data.eventlink;
        originalMeetingPlatformBackup.value = data.idMeetingBackupPlatform;
        originalEventLinkBackup.value = data.eventLinkBackup;
        originalEventPlace.value = data.eventPlace;
        originalListParticipant.value = JSON.parse(
          JSON.stringify(data.listParticipant)
        );
        originalListOrganizer.value = JSON.parse(
          JSON.stringify(data.listOrganizer)
        );
        originalListPemrakarsa.value = JSON.parse(
          JSON.stringify(data.listPemrakarsa)
        );
        originalListDewanGubernur.value = JSON.parse(
          JSON.stringify(data.listAdg)
        );

        v$.value.$reset();
        dialog.value = true;
        isLoading.value = false;
      }
    });
};
const formData = ref();

const submitForm = () => {
  state._description = currentEditorData.value || editorInstance.getData();

  v$.value.$touch();
  v$.value.$validate().then((valid) => {
    if (valid) {
      const reqData = {
        idEvent: state._id,
        isDescriptionChanged: isDescriptionChanged.value,
        isMethodChanged: isMethodChanged.value,
        isMainMediaChanged: isMeetingPlatformChanged.value,
        isMainLinkChanged: isEventLinkChanged.value,
        isBackupMediaChanged: isMeetingPlatformBackupChanged.value,
        isBackupLinkChanged: isEventLinkBackupChanged.value,
        isPlaceChanged: isEventPlaceChanged.value,
        isOrganizerChanged: isListOrganizerChanged.value,
        isParticipantChanged: isListParticipantChanged.value,
        isPemrakarsaChanged: isListPemrakarsaChanged.value,
        isADGChanged: isListDewanGubernurChanged.value,
        listOrganizer: state._listOrganizer,
        listParticipant: state._listParticipant,
        listPemrakarsa: state._listPemrakarsa,
        listAdg: state._listDewanGubernur,
      };
      store
        .dispatch("eventStore/popUpUpdateEvent", reqData)
        .then((res) => {
          formValidate.value.message = messageEditEvent[res.popUpNotifType];
          if (res.popUpNotifType === "meetingAttendees") {
            formValidate.value.width = 834;
          }
          popUpType.value = res.popUpNotifType;
          isOutlook.value = res.isOutlook;
          isDifferentDataOutlookWithDB.value = res.isDifferentDataOutlookWithDB;
          state._popUpNotifType = res.popUpNotifType;
          state._meetingDetailsOutlook = res.isOutlook;
          formData.value = state;
          modalSubmit.value.show({});
          dialog.value = false;
        })
        .catch(response.error);
    } else {
      nextTick(() => {
        const errorElement = document.querySelector(".v-input--error");
        if (errorElement) {
          errorElement.scrollIntoView({
            behavior: "smooth",
            block: "center",
          });
        }
      });
    }
  });
};

const processSubmit = (state, type) => {
  isLoading.value = true;
  // replace irregular space
  let description = removeIrregulerSpace(state._description);

  let startformatdate = state._datePickerStart.split("/");
  startformatdate =
    startformatdate[2] + "-" + startformatdate[1] + "-" + startformatdate[0];

  let endformatdate = state._datePickerEnd.split("/");
  endformatdate =
    endformatdate[2] + "-" + endformatdate[1] + "-" + endformatdate[0];

  if (state._method == 2) {
    state._eventlink = "";
    state._eventlinkBackup = "";
    state._meetingPlatform = 0;
    state._meetingPlatformBackup = 0;
  }

  const data = {
    title: state._title,
    idEvent: state._id,
    description: description,
    idMethod: state._method,
    idMeetingPlatform: state._meetingPlatform ?? 0,
    idMeetingBackupPlatform: state._meetingPlatformBackup,
    eventlink: state._eventlink,
    eventLinkBackup: state._eventlinkBackup,
    eventPlace: state._eventPlace,
    startDate: `${startformatdate} ${state._startTime}:00`,
    endDate: `${endformatdate} ${state._endTime}:00`,
    listParticipant: state._listParticipant,
    listOrganizer: state._listOrganizer,
    listAdg: state._listDewanGubernur,
    listPemrakarsa: state._listPemrakarsa,
    popUpNotifType: state._popUpNotifType,
    meetingDetailsOutlook: state._meetingDetailsOutlook,
    meetingAttendeesOutlook: type,
  };
  store
    .dispatch("eventStore/updateEvent", data)
    .then((res) => {
      if (res.response && res.response.status === 400) {
        root.refs.toast.show({
          message: "Failed to update event",
          color: "error",
          timeout: 3000,
        });
        isLoading.value = false;
        modalSubmit.value.hide();
        emits("refreshData");
        return;
      }
      root.refs.toast.show({
        message: "Successfully Edited",
        color: "success",
        timeout: 3000,
      });
      isLoading.value = false;
      modalSubmit.value.hide();
      emits("refreshData");
    })
    .catch(response.error);
};

const initalDateLimit = (dateToFormat: string, timeToFormat?: string) => {
  const parts = dateToFormat.split("/");

  const day = parseInt(parts[0], 10);
  const month = parseInt(parts[1], 10) - 1; // Months are zero-based (0 = January, 1 = February, etc.)
  const year = parseInt(parts[2], 10);

  const times = timeToFormat?.split(":") ?? ["00", "00"];
  const hour = parseInt(times[0]) ?? 0;
  const minute = parseInt(times[1]) ?? 0;

  const dateObject = new Date(year, month, day, hour, minute);
  return dateObject;
};

const limitDateEnd = ref<Date>(initalDateLimit(state._datePickerStart));

watch(
  () => state._datePickerStart,
  (val) => (limitDateEnd.value = initalDateLimit(val))
);

watch(
  () => state._meetingPlatform,
  (val) => {
    if (val == state._meetingPlatformBackup) {
      state._meetingPlatformBackup = null;
      state._eventlinkBackup = "";
    }
  }
);

const debouncedFetchSearchParticipant = debounce((val: string, type) => {
  if (val.length < 3) return;

  const trimmedSearch: string[] = [];
  val
    .replace(/"/g, "")
    .split(";")
    .forEach((part) => {
      if (part.trim() === "") return;
      const regex = /<[^>]*@[^>]*>/;
      const matchingMail = part.match(regex);
      if (matchingMail !== null) {
        trimmedSearch.push(matchingMail[0].slice(1, -1));
      } else {
        trimmedSearch.push(part.trim());
      }
    });
  const payload = {
    query: trimmedSearch,
    isEvent: true,
  };

  store.dispatch("userStore/SearchUserAndGroupNew", payload).then((result) => {
    result.forEach((item) => {
      item.isDelete = store.state.username == item.username ? false : true;
    });
    const unmatchedEmails = getUnmatchedEmails(trimmedSearch, result);
    if (type === "participant") {
      searchParticipantResult.value = result;
      if (trimmedSearch.length > 1) {
        searchParticipant.value = "";
        state._listParticipant = [
          ...state._listParticipant.filter(
            (p: any) => !result.some((r) => r.id === p.id)
          ),
          ...(result as never[]),
          ...unmatchedEmails,
        ];
      }
      validateUsers("participant");
    }
    if (type === "organizer") {
      searchOrganizerResult.value = result;
      if (trimmedSearch.length > 1) {
        searchOrganizer.value = "";
        state._listOrganizer = [
          ...state._listOrganizer.filter(
            (o: any) => !result.some((r) => r.id === o.id)
          ),
          ...(result as never[]),
          ...unmatchedEmails,
        ];
      }
      validateUsers("organizer");
    }
    if (type === "pemrakarsa") {
      searchPemrakarsaResult.value = result;
      if (trimmedSearch.length > 1) {
        searchPemrakarsa.value = "";
        state._listPemrakarsa = [
          ...state._listPemrakarsa.filter(
            (p: any) => !result.some((r) => r.id === p.id)
          ),
          ...(result as never[]),
          ...unmatchedEmails,
        ];
      }
      validateUsers("pemrakarsa");
    }
  });
}, 500);

const getUnmatchedEmails = (trimmedSearch: string[], searchResults: any[]) => {
  return trimmedSearch
    .map((email) =>
      !searchResults.some((r) => r.inputEmail === email)
        ? {
            id: null,
            value: null,
            inputEmail: email,
            isGroup: false,
            organizationName: "",
            isDelete: true,
          }
        : null
    )
    .filter((item) => item !== null) as never[];
};

watch(searchParticipant, (val) => {
  debouncedFetchSearchParticipant(val, "participant");
});

watch(searchOrganizer, (val) => {
  debouncedFetchSearchParticipant(val, "organizer");
});

watch(searchPemrakarsa, (val) => {
  debouncedFetchSearchParticipant(val, "pemrakarsa");
});

watch(
  () => myEditor.value,
  (val) => {
    if (val) {
      initEditor();
    }
  }
);

// Watch dialog state to reset tracking when closed
watch(
  () => dialog.value,
  (newVal) => {
    if (!newVal) {
      // Reset tracking when dialog is closed
      originalDescription.value = "";
      currentEditorData.value = "";
      originalMethod.value = 0;
      originalEventLink.value = "";
      originalMeetingPlatformBackup.value = null;
      originalEventLinkBackup.value = "";
      originalEventPlace.value = "";
      originalListParticipant.value = [];
      originalListOrganizer.value = [];
      originalListPemrakarsa.value = [];
      originalListDewanGubernur.value = [];
    }
  }
);

const validateUsers = (t: "participant" | "organizer" | "pemrakarsa") => {
  const userTypes = [
    { type: "participant", list: state._listParticipant },
    { type: "organizer", list: state._listOrganizer },
    { type: "pemrakarsa", list: state._listPemrakarsa },
  ];
  const selectedType = userTypes.find((u) => u.type === t);
  if (!selectedType) return;

  const otherTypes: string[] = [];
  const validationMessages: string[] = [];

  const users = userTypes
    .filter((u) => u.type !== t)
    .reduce((acc, curr) => {
      otherTypes.push(curr.type);
      curr.list.map((item: any) => {
        item.validationType = curr.type;
      });
      return [...acc, ...curr.list];
    }, [] as any[]);

  const filteredList = selectedType.list.filter((sItem: any) => {
    const isExist = users.find((oItem) => {
      const match = oItem.id === sItem.id || oItem.value === sItem.value;
      if (match) {
        sItem.validationType = oItem.validationType;
      }
      return match;
    });
    if (!isExist) {
      return sItem;
    } else {
      validationMessages.push(
        `${sItem.value} telah menjadi ${sItem.validationType}`
      );
      return false;
    }
  });

  if (t == "participant") state._listParticipant = [...filteredList];
  if (t == "organizer") state._listOrganizer = [...filteredList];
  if (t == "pemrakarsa") state._listPemrakarsa = [...filteredList];

  if (validationMessages.length > 0) {
    root.refs.toast.show({
      message: `User ${validationMessages.join(", ")}`,
      color: "warning",
      timeout: 3000,
    });
  }
};

const updateParticipant = () => {
  const html = document.getElementById("participant");
  if (html) html.blur();
  validateUsers("participant");
};

const updateOrganizer = () => {
  const html = document.getElementById("organizer");
  if (html) html.blur();
  validateUsers("organizer");
};

const updatePemrakarsa = () => {
  const html = document.getElementById("pemrakarsa");
  if (html) html.blur();
  validateUsers("pemrakarsa");
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  const day = date.getDate();
  const month = date.getMonth() + 1; // Month is zero-based, so we add 1
  const year = date.getFullYear();

  // Pad single digit day or month with leading zero
  const formattedDay = String(day).padStart(2, "0");
  const formattedMonth = String(month).padStart(2, "0");

  // Construct the formatted date string
  const formattedDate = `${formattedDay}/${formattedMonth}/${year}`;

  return formattedDate;
};

function formatDateTime(dateTimeString: string) {
  const dateTime = new Date(dateTimeString);

  // Extract the time portion
  const hours = dateTime.getHours();
  const minutes = dateTime.getMinutes();

  // Pad single digit hour or minute with leading zero
  const formattedHours = String(hours).padStart(2, "0");
  const formattedMinutes = String(minutes).padStart(2, "0");

  // Construct the formatted date and time strings
  const formattedTime = `${formattedHours}:${formattedMinutes}`;

  return formattedTime;
}
</script>

<style scoped>
/*
:deep(.ck.ck-sticky-panel) {
  display: none !important;
}
  */

:deep(.v-textarea .v-field__input) {
  height: 1px !important;
  background: red !important;
  display: contents;
}
:deep(.ck.ck-toolbar.ck-toolbar_grouping) {
  display: none;
}

:deep(.ck.ck-content.ck-editor__editable) {
  padding: 10px;
  border: 1px solid #dfdfdf;
  border-radius: 0 0 11px 11px;
  /* margin-bottom: 20px; */
  height: 200px;
  box-shadow: 0px 3px 1px -2px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)),
    0px 2px 2px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)),
    0px 1px 5px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.12));
}
:deep(.v-chip.v-chip--density-default.chip-shadow) {
  box-shadow: 0px 3px 1px -2px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)),
    0px 2px 2px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)),
    0px 1px 5px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.12));
  height: 56px;
  width: 98%;
  color: grey !important;
  border: none;
  background: #dfdfdf !important;
  font-size: 16px;
  margin: 10px;
}

:deep(.v-chip.v-chip--density-default) {
  height: calc(var(--v-chip-height) + 0px);
  border-radius: 5px;
  background: #e9f5ff;
  border: 1px solid #6eb3ea;
  color: #065391;
  padding: 10px;
  margin-right: 5px;
  margin-bottom: 5px;
}

:deep(.dp__overlay) {
  border-radius: 10px;
}
:deep(.dp__instance_calendar) {
  box-shadow: 1px 1px 7px 3px #7393b3;
  border-radius: 5px;
  padding: 10px;
}

:deep(.dp__arrow_top) {
  display: none;
}

:deep(.v-textarea .v-field) {
  --v-textarea-control-height: var(--v-input-control-height);
  background: white;
  border-radius: 12px;
}
:deep(.v-field.v-field--appended) {
  border-radius: 12px !important;
}

:deep(.v-text-field .v-field) {
  border-radius: 12px;
}

:deep(.ck .ck-sticky-panel__content) {
  border-top-left-radius: 10px !important;
  border-top-right-radius: 10px !important;
  box-shadow: 0px 3px 1px -2px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)),
    0px 2px 2px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)),
    0px 1px 5px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.12));
}

:deep(.ck .ck-toolbar) {
  border-radius: 10px;
}

:deep(.ck.ck-editor__main > .ck-editor__editable:not(.ck-focused)) {
  pointer-events: auto;
  cursor: auto;
}

:deep(.ck.ck-editor__main > .ck-editor__editable:not(.ck-focused)) {
  border: 0 !important;
}

.btn-close {
  position: absolute;
  right: 0;
  top: 0;
  margin-top: 10px;
  margin-right: 10px;
}

.line {
  border: none; /* Remove the default border */
  height: 2px; /* Set the height of the hr */
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
}

.btn-next {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  border-radius: 10px !important;
  border-color: #267dc2 !important;
  padding-left: 16px !important;
  padding-right: 16px !important;
  font-size: 14px !important;
  color: white;
  font-weight: 900;
}

.btn-prev {
  background: white;
  border-radius: 10px !important;
  /* border-color: #267dc2 !important; */
  padding-left: 16px !important;
  padding-right: 16px !important;
  font-size: 14px !important;

  color: #267dc2;
  font-weight: 900;
}

.btn-cancel {
  background: white;
  border-radius: 10px !important;
  /* border-color: #267dc2 !important; */
  padding-left: 16px !important;
  padding-right: 16px !important;
  font-size: 14px !important;

  color: #ff000d;
  font-weight: 900;
}

:deep(.v-messages__message) {
  font-family: "Poppins", sans-serif;
}

.chip-with-right-icon {
  width: 100% !important;
  display: flex !important;
}

.chip-with-right-icon ::v-deep .v-chip__append {
  margin-left: auto !important;
  margin-right: 8px !important;
  display: flex !important;
  align-items: center !important;
}

.tooltip-wrapper {
  display: inline-block;
}

.btn-wrapper {
  display: inline-block;
  pointer-events: auto;
}

.btn-wrapper .v-btn:disabled {
  pointer-events: auto !important;
}
</style>
