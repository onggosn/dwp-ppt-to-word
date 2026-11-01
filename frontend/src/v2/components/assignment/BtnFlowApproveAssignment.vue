<template>
  <free-style-shimmer
    v-if="isDataLoading"
    width="13vw"
    height="6vh"
    border-radius="5px"
    color="#DCDCDC"
    class="pa-3"
  />
  <template v-else>
    <div class="d-flex justify-center align-center">
      <v-btn
        v-for="(item, idx) in items"
        class="ma-2"
        :key="idx"
        :class="getColor(item.label)"
        @click="prosess(item)"
      >
        {{ item.label }}
      </v-btn>
    </div>
  </template>
  <ModalConfirm
    ref="modal_confirm"
    :form-config="formConfirm"
    @actionConfirm="doProcess"
    :isLoading="isDataLoading"
  />
</template>

<script setup lang="ts">
import { ref, onMounted, getCurrentInstance } from "vue";
import { responsePromise } from "@v2/helpers/utils";
import { useStore } from "vuex";
import ModalConfirm from "../utils/modal/ModalConfirm.vue";

const props = defineProps({
  id: {
    type: String,
    default: "",
    required: true,
  },
  isDisabled: {
    type: Boolean,
    default: false,
  },
});

const store = useStore();
const { root } = getCurrentInstance() as any;
const response = responsePromise(root);
const items = ref<any>([]);
const isDataLoading = ref<boolean>(false);

const modal_confirm = ref();

const formConfirm = ref({
  title: "Approve Assignment",
  width: 500,
  btnSubmitLabel: "Approve",
  btnSubmitColor: "btn-active",
  icon: {
    code: "mdi-alert-circle-outline",
    color: "red",
    backgrounColor: "white",
    size: 70,
  },
  usingTimeOut: false,
  message: `<div class="text-center">Approve assignment will permanently finish your <br /> assignment. Are you sure ? </div>`,
});

const emit = defineEmits(["doneProcess"]);

function getFlow() {
  isDataLoading.value = true;
  let requestData = {
    id: props.id,
  };
  store
    .dispatch("assignmentStore/GetListFlowApprovalByIdAssignment", requestData)
    .then((res: any) => {
      items.value = res.responseData ? res.responseData : [];
    })
    .finally(() => {
      isDataLoading.value = false;
    });
}

function prosess(item) {
  if (props.isDisabled) return 0;
  if (item.label.toLowerCase() == "submit assignment") {
    doProcess(item);
  }
  // // approve
  else if (item.label.toLowerCase() == "approve") {
    formConfirm.value = {
      title: "Approve Assignment",
      width: 500,
      btnSubmitLabel: "Approve",
      btnSubmitColor: "btn-active",
      icon: {
        code: "mdi-alert-circle-outline",
        color: "red",
        backgrounColor: "white",
        size: 70,
      },
      usingTimeOut: true,
      message: `<div class="text-center">Approve assignment will permanently finish your <br /> assignment. Are you sure ? </div>`,
    };
    modal_confirm.value.show(item, 10);
  }
  // // reject
  else if (item.label.toLowerCase() == "reject") {
    formConfirm.value = {
      title: "Reject Assignment",
      width: 500,
      btnSubmitLabel: "Reject",
      btnSubmitColor: "btn-danger",
      icon: {
        code: "mdi-alert-circle-outline",
        color: "red",
        backgrounColor: "white",
        size: 70,
      },
      usingTimeOut: true,
      message: `<div class="text-center">Reject assignment will return your <br /> assignment. Are you sure ?</div>`,
    };
    modal_confirm.value.show(item, 10);
  }
}

function doProcess(item) {
  isDataLoading.value = true;
  let requestData = item;
  store
    .dispatch("assignmentStore/AssignmentApproval", requestData)
    .then((res: any) => {
      if (res.responseCode == "011000") {
        root.refs.toast.show({
          message: res.responseData.description ?? "Success",
          color: "success",
          timeout: 3000,
        });
      } else {
        root.refs.toast.show({
          message: res.responseMessage,
          color: "warning",
          timeout: 3000,
        });
      }
    })
    .finally(() => {
      isDataLoading.value = false;
      modal_confirm.value.hide();
      getFlow();
      emit("doneProcess");
    })
    .catch(response.error);
}

function getColor(label) {
  label = label.toLowerCase();
  let classColor = {
    approve: "sectionBlue-button",
    reject: "sectionRed-button",
    delete: "sectionRed-button",
  };
  if (props.isDisabled) return "sectionGrey-button";
  return classColor[label] ?? "sectionBlue-button";
}

onMounted(() => {
  getFlow();
});
</script>

<style scope>
.sectionGrey-button {
  color: #fff !important;
  background: linear-gradient(180deg, #dfdfdf 0%, #e4e2e2 100%);
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.25);
  border-radius: 10px;
  letter-spacing: 0.1px;
  font-weight: 900;
}

.sectionBlue-button {
  min-width: 130px;
  color: #fff !important;

  background: linear-gradient(180deg, #065695 0%, #267dc2 100%);

  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.25);
  border-radius: 10px;
  letter-spacing: 0.1px;
  font-weight: 900;
}

.sectionRed-button {
  min-width: 130px;
  color: #fff !important;
  /* Gradient Red */

  background: linear-gradient(180deg, #d6212a 0%, #ff000d 100%);
  /* drop shadow button open file */

  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.25);
  border-radius: 10px;
  letter-spacing: 0.1px;
  font-weight: 900;
}
</style>
