<template>
  <v-btn
    v-if="buttonLabel.toLowerCase() === DialogFlag.reject"
    :loading="isLoading || disableAllApprovalButton"
    @click="approveWithoutMemberDialog(data.buttonLabel)"
    class="mr-4 rounded-lg font-weight-bold primary-red-gradient"
    width="120"
  >
    Reject
  </v-btn>
  <v-btn
    v-else-if="canSubmit"
    :loading="isLoading || disableAllApprovalButton"
    :disabled="!data.isactivesubmit"
    @click="modalSubmitStp.showDialog()"
    class="mr-4 rounded-lg font-weight-bold white-gradient"
    width="120"
  >
    {{ data.buttonLabel }}
  </v-btn>
  <v-btn
    v-else-if="buttonLabel.toLowerCase() === DialogFlag.finalized"
    class="mr-4 rounded-lg font-weight-bold px-10 white-gradient"
    :loading="isLoading"
    @click="modalFinalizeDocument.showDialog()"
  >
    {{ data.buttonLabel }}
  </v-btn>
  <v-btn
    v-else-if="!data.needUserApproved"
    :class="[
      buttonLabel.toLowerCase() === DialogFlag.revision ||
      buttonLabel.toLowerCase() === DialogFlag.update
        ? 'danger-gradient'
        : 'primary-gradient',
    ]"
    :loading="isLoading || disableAllApprovalButton"
    @click="approveWithoutMemberDialog(data.buttonLabel)"
    class="mr-4 rounded-lg font-weight-bold primary-gradient"
    width="120"
  >
    {{ data.buttonLabel }}
  </v-btn>
  <v-btn
    v-else-if="buttonLabel.toLowerCase() === DialogFlag.cancel"
    :loading="isLoading || disableAllApprovalButton"
    @click="approveWithoutMemberDialog(data.buttonLabel)"
    class="danger-gradient mr-4 rounded-lg font-weight-bold"
    width="120"
  >
    {{ data.buttonLabel }}
  </v-btn>
  <v-btn
    v-else-if="buttonLabel.toLowerCase() === DialogFlag.delete"
    :loading="isLoading || disableAllApprovalButton"
    @click="showDelete"
    class="danger-gradient mr-4 rounded-lg font-weight-bold"
    width="120"
  >
    {{ data.buttonLabel }}
  </v-btn>
  <!-- send revision button -->
  <v-btn
    v-else-if="canSendRevision"
    class="mr-4 rounded-lg font-weight-bold px-10 primary-gradient"
    :loading="isLoading"
    @click="onOpenModalRevise"
  >
    Send
  </v-btn>
  <v-btn
    v-else-if="data.isInputDocumentNo"
    class="mr-4 rounded-lg font-weight-bold px-10 primary-gradient"
    :loading="isLoading"
    @click="modalSendDocument.showDialog()"
  >
    {{ data.buttonLabel }}
  </v-btn>
  <CustomDialog
    v-else
    @handleShowDialog="handleShowDialog"
    :showDialogProps="isShowDialog"
    :buttonLabel="data.buttonLabel"
    :buttonClass="[getStyle(data).color, 'mr-4 rounded-lg', 'font-weight-bold']"
    :loading="disableAllApprovalButton"
    buttonWidth="120"
    title="Assign"
  >
    <hr class="line mt-4 mb-4" />
    <v-form v-if="isRisalahRdg" @submit.prevent>
      <Steppy v-model:step="step" :tabs="tabs">
        <template #1>
          <v-row class="text-left">
            <v-col :cols="12">
              <TextBlueGradient text="Rubrik Risalah" />
              <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
                Tahun Rubrik<span class="text-danger">*</span>
              </p>
              <v-text-field
                v-model="formApproval.rubrikYear"
                :hide-details="isError(v$.rubrikYear)"
                :error-messages="
                  getErrorMessages(v$.rubrikYear, { required: 'Required' })
                "
                variant="solo"
                placeholder="input tahun rubrik here"
                class="px-2 mt-1"
                @blur="v$.rubrikYear.$touch()"
              ></v-text-field>
            </v-col>
            <v-col :cols="12">
              <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
                Nomor Risalah<span class="text-danger">*</span>
              </p>
              <v-text-field
                v-model="formApproval.risalahNumber"
                :hide-details="isError(v$.risalahNumber)"
                :error-messages="
                  getErrorMessages(v$.risalahNumber, {
                    numeric: 'Data input must be a number. Please check again',
                    required: 'Required',
                  })
                "
                variant="solo"
                placeholder="input nomor risalah here"
                class="px-2 mt-1"
                @blur="v$.risalahNumber.$touch()"
              ></v-text-field>
            </v-col>
            <v-col :cols="12">
              <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
                Tanggal RDG<span class="text-danger">*</span>
              </p>
              <v-text-field
                v-model="formApproval.rdgDate"
                :hide-details="isError(v$.rdgDate)"
                :error-messages="
                  getErrorMessages(v$.rdgDate, {
                    numeric: 'Data input must be a number. Please check again',
                    required: 'Required',
                    limit: `Data input must be between 1 and ${tanggalRdg}. Please cheack again.`,
                  })
                "
                variant="solo"
                placeholder="input tanggal RDG here"
                class="px-2 mt-1"
                @blur="v$.rdgDate.$touch()"
              ></v-text-field>
            </v-col>
          </v-row>
        </template>
        <template #2>
          <v-row class="text-left">
            <v-col :cols="12">
              <TextBlueGradient text="Penyusun & Pengaju" />
              <div class="text-left">
                <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
                  Penyusun<span class="text-danger">*</span>
                </p>
                <SearchBar
                  v-model="formApproval.organizer"
                  :items="itemsMemberApproval"
                  :appendIcon="true"
                  :rules="[validateItem]"
                  :isRequired="true"
                />
              </div>
              <div class="mt-2 text-left">
                <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
                  Pengaju<span class="text-danger">*</span>
                </p>
                <SearchBar
                  v-model="formApproval.applicant"
                  :items="itemsMemberApproval"
                  :appendIcon="true"
                  :rules="[validateItem]"
                  :isRequired="true"
                />
              </div>
            </v-col>
          </v-row>
        </template>
        <template #3>
          <v-row class="text-left">
            <v-col :cols="12">
              <TextBlueGradient text="Penyetuju" />
              <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
                Penyetuju<span class="text-danger">*</span>
              </p>
              <ApprovalPenyetuju
                :list-adg="memberListADG"
                :meeting-leader="meetingLeader || undefined"
                :is-checked-members-available="isCheckedMembersAvailable"
                @handleChecked="handleIsChecked"
              />
              <span v-if="isShowApproverError" class="text-danger text-13">
                The number of approvers did not meet the quorum (minimum 4
                approvers). Please check again
              </span>
            </v-col>
          </v-row>
        </template>
      </Steppy>
      <div class="d-flex justify-end mb-2">
        <v-btn
          v-if="step === 1"
          elevation="3"
          class="btn-cancel"
          @click="handleShowDialog"
        >
          Cancel
        </v-btn>
        <v-btn v-else elevation="3" class="btn-cancel" @click="backStep">
          Back
        </v-btn>
        <v-btn
          v-if="step !== tabs.length"
          @click="nextStep"
          type="submit"
          class="ml-2 rounded-lg font-weight-bold primary-gradient"
          :loading="isLoading"
        >
          Next
        </v-btn>
        <v-btn
          v-else
          @click="submitDocument"
          type="submit"
          class="ml-2 rounded-lg font-weight-bold primary-gradient"
          :loading="isLoading"
        >
          Send
        </v-btn>
      </div>
    </v-form>
    <v-form v-else @submit.prevent="submitForm()">
      <SearchBar
        v-model="selectedItem"
        :items="itemsMemberApproval"
        :appendIcon="true"
        :rules="[validateItem]"
        :isRequired="true"
      />
      <div class="d-flex justify-end">
        <v-btn
          type="submit"
          class="mr-4 rounded-lg font-weight-bold primary-gradient"
          :loading="isLoading"
        >
          Send
        </v-btn>
      </div>
    </v-form>
  </CustomDialog>

  <v-dialog v-model="showDialogAssign" max-width="800" persistent>
    <v-card v-if="showStepCancel === 1" class="py-3 px-6 rounded-12">
      <div class="d-flex justify-space-between align-center border-bottom">
        <div></div>
        <div class="text-darkBlue font-weight-bold">Assign</div>
        <div>
          <v-btn
            icon="mdi-close"
            variant="plain"
            @click="closeDialog()"
          ></v-btn>
        </div>
      </div>
      <div class="pt-3">
        <v-form @submit.prevent="handleSaveDesc()">
          <SearchBar
            v-model="selectedItem"
            :items="itemsMemberApproval"
            :appendIcon="true"
            :rules="[validateItem]"
            :isRequired="true"
          />
          <div class="d-flex justify-end">
            <v-btn
              elevation="3"
              class="mr-4 rounded-lg font-weight-bold primary-red-gradient"
              type="submit"
            >
              Next
            </v-btn>
          </div>
        </v-form>
      </div>
    </v-card>
    <div
      v-if="showStepCancel === 2"
      class="modal-container d-flex flex-column"
      style="border-radius: 10px"
      :style="{ 'min-width': '550px' }"
    >
      <span
        @click="handleCloseReason(1)"
        class="closeModal pointer-click"
        style="
          text-align: end;
          position: absolute;
          right: 1px;
          top: 1vh;
          cursor: pointer;
        "
      >
        <img
          class="pointer-click"
          style="height: 25px; position: relative; left: -11px"
          :src="require('@v2/assets/icon/close.svg')"
        />
      </span>
      <div style="position: relative" class="text-center">
        <slot name="icon-img">
          <v-avatar
            :color="'white'"
            size="90"
            style="
              margin-top: -60px;
              filter: drop-shadow(#9b9b9b 1px 1px 1.5px);
            "
          >
            <img :src="'/images/cancelNotif2.png'" style="width: 75px" />
          </v-avatar>
        </slot>
      </div>
      <div class="text-center my-1">
        <p
          class="mb-0 text-17"
          style="font-weight: 700; color: #3a416f; padding-top: 20px"
        >
          {{ formApprove.title }}
        </p>
        <p class="mb-0 text-17" style="font-weight: 700; color: #3a416f">
          <v-textarea
            v-model="reasonCancel"
            variant="solo"
            auto-grow
            :placeholder="textareaPlaceholder"
            class="pl-2 pr-2 pt-5 textareadescription"
          ></v-textarea>
        </p>
        <div class="mt-2 text-15 text-center">
          <slot name="text-area" />
        </div>
      </div>
      <div class="text-end mt-1">
        <v-btn
          @click="handleCloseReason(1)"
          class="mr-2 rounded-lg btn"
          :loading="isLoading"
          style="background: #fff; color: rgba(6, 86, 149, 1)"
        >
          Cancel
        </v-btn>
        <v-btn
          :class="['ml-2 rounded-lg btn', formApprove.btnSubmitColor]"
          :loading="isLoading"
          @click="handleSubmitCancel()"
        >
          {{ formApprove.btnSubmitLabel }}
        </v-btn>
      </div>
    </div>
  </v-dialog>

  <ModalConfirm
    ref="modalSubmit"
    :form-config="formApprove"
    @action-confirm="submitDocument()"
  >
    <template
      v-if="
        buttonLabel.toLowerCase() !== DialogFlag.reject && !props.data?.isSubmit
      "
      v-slot:icon-img
    >
      <v-avatar
        size="100"
        style="margin-top: -60px; filter: drop-shadow(#9b9b9b 2px 2px 3px)"
      >
        <img
          :src="
            imageCancelNotif
              ? '/images/cancelNotif.png'
              : '/images/checkNotif2.png'
          "
          style="width: 90px"
        />
      </v-avatar>
    </template>
    <template
      v-else-if="
        props.data?.isSubmit && buttonLabel.toLowerCase() === DialogFlag.reject
      "
      v-slot:icon-img
    >
      <v-avatar
        color="white"
        size="80"
        style="margin-top: -60px; filter: drop-shadow(#9b9b9b 2px 2px 3px)"
      >
        <img src="/images/cancelNotif2.png" style="width: 83px" />
      </v-avatar>
    </template>
    <template v-else-if="props.data?.isSubmit" v-slot:icon-img>
      <v-avatar color="white" size="80" style="margin-top: -60px">
        <img
          :src="
            imageCancelNotif
              ? '/images/cancelNotif2.png'
              : '/images/checkNotif2.png'
          "
          style="width: 83px"
        />
      </v-avatar>
    </template>
    <template v-if="canRejectWithComment && sendReviseStep === 2" v-slot:desc>
      <v-scroll-x-transition mode="in-out" hide-on-leave>
        <div class="mb-0 text-17" style="font-weight: 700; color: #3a416f">
          <v-textarea
            v-model="reasonReject"
            variant="solo"
            auto-grow
            placeholder="Masukkan alasan Anda menolak dokumen ini"
            class="pl-2 pr-2 pt-5 textareadescription"
          ></v-textarea>
        </div>
      </v-scroll-x-transition>
    </template>
    <template v-if="canRejectWithComment" v-slot:btn-action>
      <div v-if="sendReviseStep === 2">
        <v-btn
          class="ml-2 rounded-lg white-gradient btn"
          @click="sendReviseStep = 1"
          :loading="isLoading || disableAllApprovalButton"
        >
          Cancel
        </v-btn>
        <v-btn
          :class="[
            'mr-4 rounded-lg font-weight-bold ml-3',
            reasonReject ? 'danger-gradient' : 'grey-gradient',
          ]"
          @click="submitDocument()"
          :loading="isLoading || disableAllApprovalButton"
          :disabled="!reasonReject"
        >
          Submit
        </v-btn>
      </div>
    </template>
  </ModalConfirm>
  <ModalConfirm
    ref="modalFailedSubmit"
    :form-config="failSubmit"
    :is-warning="true"
    @action-confirm="cancelSubmitDocument()"
  >
    <template v-slot:icon-img>
      <img
        :src="require('@/v2/assets/icon/failed-submit-warning.png')"
        style="
          width: 80px;
          margin-top: -60px;
          filter: drop-shadow(#9b9b9b 2px 2px 3px);
        "
      />
    </template>
  </ModalConfirm>
  <ModalConfirm
    ref="modalDelete"
    :form-config="formDelete"
    @action-confirm="approveWithMemberDialog"
  />
  <ModalConfirm
    ref="confirmApprove"
    :form-config="formDelete"
    @action-confirm="approveWithMemberDialog"
  />

  <!-- modal send revision -->
  <ModalConfirm ref="confirmRevision" :form-config="formSendRevise">
    <template v-slot:icon-img>
      <div
        class="mx-auto"
        style="
          width: 80px;
          margin-top: -50px;
          filter: drop-shadow(#9b9b9b 1px 1px 1.5px);
          border-radius: 50%;
          background-color: #ffff;
        "
      >
        <img
          :src="require('@/v2/assets/workspace/paper-plane.svg')"
          class="mx-auto px-2 py-2"
        />
      </div>
    </template>
    <template v-slot:desc>
      <v-scroll-x-transition group mode="in-out" hide-on-leave>
        <div v-if="sendReviseStep === 1">
          <p class="txt-message mx-4 my-2 text-15 text-center">
            Which rejection type did you choose?
          </p>
          <div class="d-flex justify-center" style="gap: 10px">
            <div
              class="w-33 img-revision-container"
              @click="selectRevisionType('minor')"
            >
              <img
                :src="require('@/v2/assets/icon/icon-minor.svg')"
                class="mx-auto px-3 py-3"
              />
              <p>Minor</p>
            </div>
            <div
              class="w-33 img-revision-container"
              @click="selectRevisionType('substance')"
            >
              <img
                :src="require('@/v2/assets/icon/icon-substance.svg')"
                class="mx-auto px-3 py-3"
              />
              <p>Substance</p>
            </div>
          </div>
        </div>

        <div v-if="sendReviseStep === 2">
          <p class="txt-message mx-4">Are you sure to send this document?</p>
        </div>
      </v-scroll-x-transition>
    </template>
    <template v-slot:btn-action>
      <div class="d-none" />
      <v-scroll-x-transition mode="in-out" hide-on-leave>
        <div v-if="sendReviseStep === 2">
          <v-btn
            class="ml-2 rounded-lg white-gradient btn"
            @click="sendReviseStep = 1"
            :loading="isLoading || disableAllApprovalButton"
          >
            Back
          </v-btn>
          <v-btn
            class="mr-4 rounded-lg font-weight-bold primary-gradient ml-3"
            @click="submitDocument"
            :loading="isLoading || disableAllApprovalButton"
          >
            Send
          </v-btn>
        </div>
      </v-scroll-x-transition>
    </template>
  </ModalConfirm>
  <ModalConfirm
    ref="modalFailedSign"
    :form-config="formFailSign"
    @action-confirm="onOpenModalVisualSign()"
  />

  <VisualSignDialog
    ref="modalVisualSignDialog"
    @uploadSuccess="onSuccessSubmitVisualSign()"
  />

  <ModalSubmit
    ref="modalSubmitStp"
    @submit="approveWithoutMemberDialog(data.buttonLabel, $event)"
  />
  <!-- modal send revision end -->
  <ModalSendDocument
    ref="modalSendDocument"
    :searchItem="itemsMemberApproval"
    @submit="submitDocument($event)"
  />
  <ModalFinalizeDocument
    ref="modalFinalizeDocument"
    :searchItem="itemsMemberApproval"
    :id-bpdoc="idDoc"
  />
</template>

<script setup lang="ts">
import {
  computed,
  getCurrentInstance,
  ref,
  onMounted,
  watch,
  nextTick,
} from "vue";

import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";

import { Steppy } from "vue3-steppy";

import { numeric, required } from "@vuelidate/validators";

import useVuelidate from "@vuelidate/core";

import CustomDialog from "@v2/components/utils/dialog/CustomDialog.vue";
import SearchBar from "@v2/components/utils/dialog/SearchBar.vue";
import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";
import ModalSubmit from "@v2/components/collaboration/approval/SubmitModal.vue";
import ModalSendDocument from "@v2/components/collaboration/approval/SendDocumentModal.vue";
import ModalFinalizeDocument from "@v2/components/collaboration/approval/FinalizeDocument.vue";
import VisualSignDialog from "@v2/components/collaboration/approval/VisualSignDialog.vue";

import {
  TApprovalPenyetuju,
  TButtonLabel,
  TModalConfirm,
  TRequestApproval,
  TRevisionType,
  TListEForm,
} from "@/v2/Type";

import ApprovalEnum from "@/v2/enum/ApprovalResponseCode";

import {
  getErrorMessages,
  isError,
  notHasTagHtml,
} from "@/v2/helpers/validation";

import {
  formApproveInitial,
  formApproveOnCloseDialog,
  formApproveOnSubmitForm,
  formCancelOnSaveDesc,
  formDeleteInitial,
  formDeleteOnSaveDesc,
  formFailSubmitInitial,
  WithoutMemberDialogue,
  formSendRevise,
  formFailSignInitial,
} from "@/v2/label/LabelModal";

import ToastLabel from "@/v2/label/LabelToast";
import TextBlueGradient from "../../utils/text/TextBlueGradient.vue";
import ApprovalPenyetuju from "./ApprovalPenyetuju.vue";
import { getMaxDay, secureRandomFloat } from "@v2/helpers/utils";
import Enum from "@/v2/enum/Enum";

const props = defineProps({
  data: {
    type: Object,
    default: null,
  },
  isDocSectoral: {
    type: Boolean,
    default: false,
  },
  approvalData: {
    type: Object,
    default: () => ({}),
  },
});

const store = useStore();
const route = useRoute();
const router = useRouter();

const { root } = getCurrentInstance() as any;

const emits = defineEmits(["refreshToc"]);

const { ApprovalResponseCode, DialogFlag } = ApprovalEnum;
const { LabelToast } = ToastLabel;
const { idBpDocument } = Enum;

const step = ref(1);

const listAdgMembersChecked = ref<Array<TApprovalPenyetuju>>([]);

const tabs = computed(() => {
  const local = [
    {
      title: "Step 1",
      iconSuccess: null,
      isValid: true,
    },
    {
      title: "Step 2",
      iconSuccess: null,
      isValid: true,
    },
    {
      title: "Step 3",
      iconSuccess: null,
      isValid: true,
    },
  ];

  return local;
});

const showStepCancel = ref(1);
const currentAdgCheckedIndex = ref(0);

const modalSubmitStp = ref();
const idStpSubmit = ref<TListEForm>();
const modalSubmit = ref();
const reasonCancel = ref();

const modalFailedSubmit = ref();
const modalDelete = ref();
const modalFailedSign = ref();
const modalVisualSignDialog = ref();
const itemsMemberApproval = ref<any>();
//send document siaran pers
const modalSendDocument = ref();
const modalFinalizeDocument = ref();

const idBpDocNextContent = ref<string>();
const textareaPlaceholder = ref("");

const selectedItem = ref<string | null>(null);

const isLoading = ref(false);
const showDialogAssign = ref(false);
const isCheckedMembersAvailable = ref<boolean>(false);
const isShowDialog = ref<boolean>(false);
const isShowApproverError = ref<boolean>(false);

const memberListADG = ref<TApprovalPenyetuju[]>([]);

const meetingLeader = ref<TApprovalPenyetuju | null>(null);
// send revision
const confirmRevision = ref();
const sendReviseStep = ref<number>(1);
const sendReviseType = ref<TRevisionType>("reject");
// reject witch reason
const reasonReject = ref<string>("");

const alertLabelCancel = computed(() => {
  return store.getters["collaborationStore/getAlartLabelCancel"];
});

const disableAllApprovalButton = computed(() => {
  return store.getters["collaborationStore/getDisableAllApprovalButton"];
});

const getReasonCancel = computed(() => {
  return store.getters["collaborationStore/getReasonCancel"];
});

const tanggalRdg = computed(() => {
  return getMaxDay(store.getters["collaborationStore/getEventKop"].end);
});

const canSubmit = computed((): boolean => {
  return (
    props.data?.buttonLabel.toLowerCase() === DialogFlag.submit &&
    !props.data?.needUserApproved
  );
});

const canSendRevision = computed(() => {
  return (
    props.data?.typeRisalah &&
    props.data?.sendType?.toLowerCase() === DialogFlag.reject
  );
});

const canRejectWithComment = computed(() => {
  return (
    props.data?.typeRisalah &&
    props.data?.buttonLabel?.toLowerCase() === DialogFlag.reject
  );
});

const buttonLabel = computed(() => {
  return props.data.buttonLabel;
});

const imageCancelNotif = computed(() => {
  return (
    buttonLabel.value.toLowerCase() === DialogFlag.cancel ||
    buttonLabel.value.toLowerCase() === DialogFlag.delete
  );
});

const documentStatusId = computed(() => {
  return store.getters["collaborationStore/getDocumentStatusId"];
});

const idDoc = computed(() => {
  return route.params.idDoc;
});

const isRisalahRdg = computed(() => {
  const { typeRisalah, sendType } = props.approvalData;
  return typeRisalah && sendType === "origin";
});

const ApprovalRules = computed(() => {
  const local = {
    risalahNumber: {},
    organizer: {},
    applicant: {},
    rubrikYear: {},
    rdgDate: {},
  };

  if (step.value == 1) {
    local.risalahNumber = { required, notHasTagHtml, numeric };
    local.rubrikYear = { required, numeric };
    local.rdgDate = {
      required,
      numeric,
      limit: (value: any) => {
        const validate = value >= 1 && value <= tanggalRdg.value;
        return validate;
      },
    };
  }

  if (step.value == 2) {
    local.applicant = { required };
    local.organizer = { required };
  }

  return local;
});

const formApproval = ref({
  risalahNumber: "",
  organizer: "",
  applicant: "",
  rubrikYear: "",
  rdgDate: "",
});

watch(step, (val) => {
  if (val === 3) {
    const checkedMembers = memberListADG.value.filter(
      (member) => member.isPresent === true
    );

    listAdgMembersChecked.value = [...checkedMembers];
  }
});

const v$ = useVuelidate(ApprovalRules, formApproval);

const formApprove = ref<TModalConfirm>(formApproveInitial);

const failSubmit = ref<TModalConfirm>(formFailSubmitInitial);

const formDelete = ref<TModalConfirm>(formDeleteInitial);

const formFailSign = ref<TModalConfirm>(formFailSignInitial);

const validateItem = (value) => {
  return !!value || "member selection is required";
};
// send revision
const onOpenModalRevise = () => {
  sendReviseStep.value = 1;
  confirmRevision.value.show({});
};

const onOpenModalVisualSign = () => {
  modalFailedSign.value.hide();
  modalVisualSignDialog.value.show({});
};

const selectRevisionType = (type: TRevisionType) => {
  sendReviseType.value = type;
  sendReviseStep.value = 2;
};
// send revision end

const hideCustomDialog = () => {
  isShowDialog.value = false;
};

const getStyle = (item) => {
  switch (item.buttonLabel.toLowerCase()) {
    case DialogFlag.reject: {
      return {
        color: "primary-red-gradient",
      };
    }
    default: {
      return {
        color: "primary-gradient",
      };
    }
  }
};

const getUserApproval = () => {
  const reqData = props.isDocSectoral
    ? {
        id: route.params.idDoc,
        idSector: props.data.idMSector,
      }
    : {
        id: route.params.idDoc,
      };

  store.dispatch("eFormStore/GetListBpDocApproval", reqData).then((res) => {
    if (res) {
      const { responseData } = res;

      const data = responseData.map((el: any) => {
        const { value: name, id, jabatanSatker: department } = el;

        return {
          name,
          type: "person",
          id,
          inputName: el.value,
          value: el.value,
          department,
        };
      });

      itemsMemberApproval.value = data;
    }
  });
};

const onSuccessSubmitVisualSign = () => {
  if (
    [31, 32, 36, 60].includes(
      store.getters["collaborationStore/getDocumentStatusId"]
    )
  ) {
    approveWithoutMemberDialog(props.data.buttonLabel);
    return;
  }

  submitForm();
};

const submitForm = () => {
  if (!selectedItem.value) return;

  const reqData: any = props.data;
  reqData.userApproval = selectedItem.value;

  if (reasonCancel.value !== null) {
    reqData.reason = reasonCancel.value;
  }

  hideCustomDialog();

  formApprove.value = formApproveOnSubmitForm(reqData.buttonLabel);

  modalSubmit.value.show({});
};

const processSubmit = (data?: TListEForm) => {
  const { id } = props.data;

  isLoading.value = true;
  store.commit("collaborationStore/setDisableAllApprovalButton", true);

  modalSubmit.value.hide();

  const payload = {
    id,
  };

  if (data) {
    Object.assign(payload, {
      idEformSource: data.listIdEform,
      isAppend: data.isAppend,
    });
  }

  store.commit("collaborationStore/increstReloadTrackChanges");
  store
    .dispatch("eFormStore/submitSTPMappingByUsername", payload)
    .then((res) => {
      const { responseCode, responseMessage } = res;

      if (responseCode === ApprovalResponseCode.success) {
        root.refs.toast.show(LabelToast(responseMessage).success);

        return;
      }

      if (responseCode === ApprovalResponseCode.failed) {
        failSubmit.value.message = responseMessage;
        modalFailedSubmit.value.show({});

        return;
      }

      if (responseCode === ApprovalResponseCode.oneLeastSubmit) {
        const message =
          responseMessage ??
          "At least 1 mapping must be filled in before submitting";

        root.refs.toast.show(LabelToast(message).oopss);

        return;
      }
    })
    .catch((err) => {
      const { responseMessage } = err.response.data;

      const message = responseMessage ?? "Internal server error";

      root.refs.toast.show(LabelToast(message).warning);
    })
    .finally(() => {
      isLoading.value = false;
      store.commit("collaborationStore/setDisableAllApprovalButton", false);
    });
};

const handleCloseReason = (temp: any) => {
  showStepCancel.value = temp;
};

const closeDialog = () => {
  if (!props.data) return;

  const btnLabel = buttonLabel.value.toLowerCase();

  showDialogAssign.value = false;

  if (btnLabel === DialogFlag.cancel) {
    formApprove.value = formApproveOnCloseDialog(alertLabelCancel.value);
    modalSubmit.value.show({});
  } else if (btnLabel === DialogFlag.delete) {
    modalDelete.value.show({});
  }
};

const handleSubmitCancel = () => {
  if (selectedItem.value && reasonCancel.value) {
    const reqData: any = props.data;

    reqData.userApproval = selectedItem.value;
    reqData.reason = reasonCancel.value;

    processApprove(reqData);

    return;
  }
};

const cancelSubmit = () => {
  showDialogAssign.value = true;
  selectedItem.value = null;
  reasonCancel.value = null;
  showStepCancel.value = 1;
  modalSubmit.value.hide();
  modalSubmit.value = 1;
};

const submitDocument = (data?: any) => {
  const btnLabel = buttonLabel.value.toLowerCase();

  const reqData: any = props.data;

  if (data?.nomorSiaranPers) {
    Object.assign(reqData, {
      documentNo: data.nomorSiaranPers,
      userApproval: data.penyetuju,
    });
  }

  if (canRejectWithComment.value && sendReviseStep.value === 1) {
    sendReviseStep.value = 2;

    return;
  }

  if (btnLabel === DialogFlag.submit) {
    processSubmit(idStpSubmit.value);
    return;
  }

  if (btnLabel === DialogFlag.cancel) {
    cancelSubmit();
    return;
  }

  processApprove(reqData);
};

const handleSaveDesc = () => {
  if (!selectedItem.value) return;

  const reqData: any = props.data;
  reqData.userApproval = selectedItem.value;
  showStepCancel.value = 2;

  const btnLabel = buttonLabel.value.toLowerCase();

  if (btnLabel === DialogFlag.cancel) {
    formApprove.value = formCancelOnSaveDesc(alertLabelCancel.value);
    textareaPlaceholder.value = "Masukkan alasan Anda membatalkan dokumen ini";

    return;
  }

  if (btnLabel === DialogFlag.delete) {
    formApprove.value = formDeleteOnSaveDesc;
    textareaPlaceholder.value = "Masukkan alasan Anda menghapus dokumen ini";

    return;
  }
};

const processApprove = (reqData: TRequestApproval) => {
  if (!validateApprovalRequirements()) return;

  store.commit("documentStore/setOnLoadingButtonState", false);

  prepareRequestData(reqData);

  modalSubmit.value.hide();
  isLoading.value = true;

  store.commit("collaborationStore/setDisableAllApprovalButton", true);

  store.commit("collaborationStore/increstReloadTrackChanges");

  if (
    !reqData.needUserApproved &&
    reqData.buttonLabel.toLowerCase() === DialogFlag.approve &&
    reqData.lastApprove
  ) {
    store.commit("documentStore/setLoadingAsync", true);
  }

  if (isRisalahRdg.value) {
    addRisalahRdgData(reqData);
  }

  setTimeout(() => {
    if (reqData.isRevision) {
      revisionProcess(reqData);

      return;
    }

    handleApprovalProcess(reqData);
  }, 2000);
};

const addRisalahRdgData = (reqData: TRequestApproval) => {
  const {
    organizer: userApprovalPenyusun,
    applicant: userApprovalPengaju,
    risalahNumber: documentNo,
    rubrikYear,
    rdgDate: dateRDG,
  } = formApproval.value;

  const newMappedApprover = memberListADG.value.map((member) => {
    const { id, isPresent } = member;

    return {
      id,
      isPresent,
    };
  });

  Object.assign(reqData, {
    documentNo,
    sendType: "origin",
    userOtherApproval: {
      userApprovalPenyusun,
      userApprovalPengaju,
      newMappedApprover,
    },
    rubrikYear,
    dateRDG,
  });
};

const validateApprovalRequirements = () => {
  const checkedMembers = listAdgMembersChecked.value.filter(
    (member) => member.isPresent === true
  );

  if (checkedMembers.length < 4 && isRisalahRdg.value) {
    isShowApproverError.value = true;
    return false;
  }
  return true;
};

const prepareRequestData = (reqData: TRequestApproval) => {
  // Set reason from store if not provided
  if (!reqData.reason) {
    reqData.reason = getReasonCancel.value;
  }

  // Handle object reason
  if (reqData.reason && typeof reqData.reason === "object") {
    reqData.reason = reqData.reason.value;
  }

  // Set send type for revision
  if (canSendRevision.value) {
    reqData.sendType = sendReviseType.value;
  }

  // Set reject reason
  if (canRejectWithComment.value) {
    reqData.reason = reasonReject.value;
  }
};

const handleApprovalProcess = (reqData: TRequestApproval) => {
  store
    .dispatch("eFormStore/doApproval", reqData)
    .then(handleApprovalSuccess)
    .catch(handleApprovalError)
    .finally(resetLoadingStates);
};

const handleApprovalSuccess = (res: any) => {
  const flowCheck = secureRandomFloat();
  const { responseCode, responseMessage } = res;

  if (responseCode == "011041") {
    store.commit("documentStore/setLoadingAsync", false);
    modalFailedSign.value.show();
    return;
  }

  const successCodes = [
    ApprovalResponseCode.success,
    ApprovalResponseCode.inProgress,
  ];

  store.commit("collaborationStore/setDocumentFlowCheck", flowCheck);
  store.commit("collaborationStore/setLoaderChip", flowCheck);
  emits("refreshToc");

  if (!successCodes.includes(responseCode)) return;

  root.refs.toast.show(LabelToast(responseMessage).success);

  const btnLabel = buttonLabel.value.toLowerCase();
  const isApproveStatus42 =
    documentStatusId.value === 42 && btnLabel === DialogFlag.approve;

  if (isApproveStatus42) {
    if (responseCode === ApprovalResponseCode.inProgress) {
      store
        .dispatch("documentStore/checkStatusAsyncDocument", {
          id: idDoc.value,
          type: DialogFlag.approval,
        })
        .then(() => {
          store.commit("contentStore/setReloadToc", secureRandomFloat());
          nextTick(() => {
            reloadNextContent();
          });
        });
    } else {
      reloadNextContent();
    }
    return;
  }

  if (responseCode === ApprovalResponseCode.inProgress) {
    store.dispatch("documentStore/checkStatusAsyncDocument", {
      id: idDoc.value,
      type: DialogFlag.approval,
    });
    return;
  }

  store.dispatch("documentStore/fetchDocumentStatus", idDoc.value);
};

const handleApprovalError = (err: any) => {
  if (!err.response?.data) return;

  const { responseMessage, responseCode } = err.response.data;

  if (responseCode === ApprovalResponseCode.oneLeastSubmit) {
    const errMessage =
      responseMessage ??
      "At least 1 mapping must be filled in before submitting";

    root.refs.toast.show(LabelToast(errMessage).oopss);
    store.dispatch("documentStore/fetchFormDocument", idDoc.value);
    return;
  }

  root.refs.toast.show(LabelToast(responseMessage).warning);
};

const resetLoadingStates = () => {
  isLoading.value = false;
  showDialogAssign.value = false;
  showStepCancel.value = 1;
  store.commit("collaborationStore/setDisableAllApprovalButton", false);
  store.commit("documentStore/setOnLoadingButtonState", true);
};

const reloadNextContent = () => {
  const req = {
    idBPDocument: idDoc.value as string,
  };

  store.dispatch("eFormStore/getNextVersionToLoad", req).then((data) => {
    if (data && data.responseData) {
      const { idBPDocument } = data.responseData;

      idBpDocNextContent.value = idBPDocument;

      if (!idBpDocNextContent.value) {
        idBpDocNextContent.value = idBpDocument.default;

        store.dispatch(
          "documentStore/fetchFormDocument",
          idBpDocNextContent.value
        );
      }

      const params = {
        typeRDG: route.params.typeRDG as string,
        idEvent: route.params.idEvent as string,
        idDoc: idBpDocNextContent.value as string,
      };

      router.push({
        name: "v2.rdg-collaboration",
        params,
      });
    }
  });
};

const revisionProcess = (reqData: TRequestApproval) => {
  modalSubmit.value.hide();

  isLoading.value = true;
  store.commit("collaborationStore/setDisableAllApprovalButton", true);
  store.commit("documentStore/setOnLoadingButtonState", false);

  store
    .dispatch("eFormStore/doRevisi", reqData)
    .then((res) => {
      if (res) {
        if (res.responseCode == "011041") {
          modalFailedSign.value.show();
          return;
        }
        const resCode = [
          ApprovalResponseCode.success,
          ApprovalResponseCode.inProgress,
        ];

        const flowCheck = secureRandomFloat();

        const { responseCode, responseMessage } = res;

        if (resCode.includes(responseCode)) {
          const type =
            props.data?.buttonLabel.toLowerCase() === DialogFlag.save
              ? DialogFlag.save
              : DialogFlag.approval;

          store.commit("collaborationStore/setDocumentFlowCheck", flowCheck);

          root.refs.toast.show(LabelToast(responseMessage).success);

          if (responseCode === ApprovalResponseCode.inProgress) {
            store.dispatch("documentStore/checkStatusAsyncDocument", {
              id: idDoc.value,
              type,
            });

            return;
          }

          store.dispatch("documentStore/fetchFormDocument", idDoc.value);
        }
      }
    })
    .catch((err) => {
      if (err && err.response) {
        const { responseMessage } = err.response.data;

        root.refs.toast.show(LabelToast(responseMessage).warning);
      }
    })
    .finally(() => {
      isLoading.value = false;
      store.commit("collaborationStore/setDisableAllApprovalButton", false);
      store.commit("documentStore/setOnLoadingButtonState", true);
    });
};

const approveWithoutMemberDialog = (val: TButtonLabel, data?: any) => {
  const buttonLabel = val.toLowerCase();
  sendReviseStep.value = 1;
  hideCustomDialog();

  if (buttonLabel === DialogFlag.reject) {
    formApprove.value = WithoutMemberDialogue().reject;
  }

  if (buttonLabel === DialogFlag.approve) {
    formApprove.value = WithoutMemberDialogue().approve;
  }

  if (buttonLabel == DialogFlag.save) {
    formApprove.value = formApproveOnSubmitForm(props.data.buttonLabel);
  }

  if (buttonLabel === DialogFlag.revision) {
    revisionProcess(props.data as TRequestApproval);

    return 1;
  }

  if (buttonLabel === DialogFlag.update) {
    submitDocument();

    return;
  }

  if (buttonLabel === DialogFlag.cancel) {
    formApprove.value = WithoutMemberDialogue(alertLabelCancel.value).cancel;
  }

  if (buttonLabel === DialogFlag.submit) {
    idStpSubmit.value = data;
    modalSubmitStp.value.onclose();
    formApprove.value = WithoutMemberDialogue().submit;
  }
  modalSubmit.value.show({});
};

const showDelete = () => {
  modalDelete.value.show({});
};

const approveWithMemberDialog = () => {
  showDialogAssign.value = true;
  modalDelete.value.hide();
};

const cancelSubmitDocument = () => {
  modalFailedSubmit.value.hide();
};

const nextStep = () => {
  v$.value.$validate().then((res) => {
    if (res) {
      if (step.value === tabs.value.length) return;

      step.value++;
      v$.value.$reset();
    }
  });
};

const backStep = () => {
  if (step.value === 1) return;

  step.value--;
};

const handleIsChecked = (val) => {
  const { id: adgId, idx: adgIndex } = val;

  currentAdgCheckedIndex.value = adgIndex;

  const currentChecked = memberListADG.value.find(
    (member) => member.id === adgId
  );

  const isMemberExists = listAdgMembersChecked.value.find(
    (member) => member.id === adgId
  );

  if (currentChecked) {
    currentChecked.isPresent = !currentChecked.isPresent;
  }

  if (currentChecked?.isPresent && !isMemberExists) {
    Object.assign(currentChecked, { index: adgIndex });
    listAdgMembersChecked.value.push(currentChecked);
  }

  updateMeetingMembers();
};

const updateMeetingMembers = () => {
  const checkedMembers = listAdgMembersChecked.value.filter(
    (member) => member.isPresent === true
  );

  if (checkedMembers.length > 0) {
    const sortedByIndex = checkedMembers.sort((a, b) => a.index - b.index);
    meetingLeader.value = sortedByIndex[0];
    isCheckedMembersAvailable.value = true;
  }

  if (checkedMembers.length === 0) {
    isCheckedMembersAvailable.value = false;
  }
};

const handleShowDialog = () => {
  const btnLabel = props.data.buttonLabel.toLowerCase();
  if (btnLabel === DialogFlag.approve && props.data.typeRisalah) {
    hideCustomDialog();
    return approveWithoutMemberDialog(props.data.buttonLabel);
  }

  isShowDialog.value = !isShowDialog.value;
};

onMounted(() => {
  getUserApproval();

  store.dispatch("userStore/fetchListADGDetail").then((res) => {
    memberListADG.value = res;

    if (props.approvalData && props.approvalData.documentNo) {
      const { documentNo } = props.approvalData;
      formApproval.value.risalahNumber = documentNo;
    }
  });
});
</script>
<style scoped>
.blue-gradient {
  background: linear-gradient(
    89.96deg,
    #065695 35.16%,
    rgba(255, 255, 255, 0) 101.03%
  );
  border-radius: 5px;
}

.btn-cancel {
  background: linear-gradient(#fff -46.47%, #fff 157.9%);
  border-radius: 10px;
  font-weight: 800;
  color: #065695 !important;
}

.text-uppercase {
  text-transform: uppercase;
}

.white-gradient {
  background: #ffff;
  color: #065695;
}

.danger-gradient {
  background: linear-gradient(92.09deg, #d6212a -46.47%, #ff000d 157.9%);
  border-radius: 20px;
  color: white;
}

.modal-container {
  border-radius: 20px;
  margin: 0px auto;
  padding: 20px 30px;
  background: #ffffff;
  box-shadow: 0px -4px 4px rgb(0 0 0 / 25%), 0px 4px 4px rgb(0 0 0 / 25%);
  backdrop-filter: blur(6px);
}

:deep(.steppy) {
  margin-left: 8vw;
  margin-right: 8vw;
}

:deep(.number) {
  display: none !important;
}

:deep(.wrapper-steppy) {
  padding: 25px 10px 0px 10px !important;
}

:deep(.steppy-pane) {
  box-shadow: none !important;
  margin: 60px 0 0 0 !important;
  padding: 25px 0 !important;
}
:deep(.steppy-item.success .steppy-item-counter) {
  border: 8px solid #267dc2 !important;
}

:deep(.steppy-item-counter) {
  height: 20px !important;
  width: 20px !important;
  border: 5px solid grey !important;
  background-color: white !important;
}

:deep(.current .steppy-item-counter) {
  border: 5px solid #065695 !important;
}

:deep(.steppy-item.success .steppy-item-counter .icon-success) {
  width: 15px !important;
  height: 15px !important;
  fill: white !important;
  background-color: #267dc2 !important;
  border-radius: 50% !important;
}

:deep(.steppy-item-title) {
  font-size: 14px !important;
  font-weight: 900 !important;
  color: #3a416f !important;
  white-space: nowrap !important;
}

:deep(.steppy-progress) {
  background: #d9d9d9 !important;
  height: 3px !important;
}

:deep(.steppy-progress-bar) {
  background: #267dc2 !important;
  height: 3px !important;
}

:deep(.controls) {
  display: none !important;
}

:deep(.number) {
  display: none !important;
}

.img-revision-container {
  border-radius: 10px;
  border-style: solid;
  border-color: #babcca;
}

.img-revision-container:hover {
  border-color: #267dc2;
}

.txt-message {
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

.grey-gradient {
  background: linear-gradient(89.96deg, rgb(24, 23, 23) 31.5%, #bbbbbb 101.03%);
  border-radius: 5px;
  color: white;
}
:deep(.v-text-field .v-input__details) {
  padding-inline-start: 0px !important;
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
</style>
