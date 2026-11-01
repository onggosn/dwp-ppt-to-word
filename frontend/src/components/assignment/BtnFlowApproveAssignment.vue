<template>
  <free-style-shimmer
    v-if="isLoading"
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

  <modal-confirm-component
    :formConfirm="formConfirm"
    ref="modal_confirm"
    @action-confirm="doProsess"
  />
</template>

<script>
import client from "@/library/ApiClient";
import ModalConfirmComponent from "../utils/ModalConfirmComponent.vue";
export default {
  name: "BtnFlowApproveAssignment",
  components: { ModalConfirmComponent },
  emits: ["doneProsess"],
  data() {
    return {
      isLoading: false,
      items: [],
      formConfirm: {
        title: "Approve Assignment",
        width: 500,
        btnSubmitLabel: "Approve",
        icon: {
          code: "mdi-alert-circle-outline",
          color: "red",
        },
        message: `<div class="text-center">Approve assignment will permanently finish your <br /> assignment. Are you sure ? </div>`,
      },
    };
  },
  props: {
    id: {
      type: String,
      default: "",
      required: true,
    },
    isDisabled: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    getFlow() {
      this.isLoading = true;
      client
        .getListFlowApprovalAssignment({
          store: this.$store,
          data: {
            id: this.id,
          },
        })
        .then((res) => {
          this.items = res.plainData.responseData;
          this.isLoading = false;
        });
    },
    prosess(item) {
      if (this.isDisabled) return 0;
      if (item.label.toLowerCase() == "submit assignment") {
        this.doProsess(item);
      }
      // approve
      else if (item.label.toLowerCase() == "approve") {
        this.formConfirm = {
          title: "Approve Assignment",
          width: 500,
          btnSubmitLabel: "Approve",
          btnSubmitColor: "btn-active",
          icon: {
            code: "mdi-alert-circle-outline",
            color: "red",
          },
          message: `<div class="text-center">Approve assignment will permanently finish your <br /> assignment. Are you sure ? </div>`,
        };
        this.$refs.modal_confirm.start(item, 10);
      }
      // reject
      else if (item.label.toLowerCase() == "reject") {
        this.formConfirm = {
          title: "Reject Assignment",
          width: 500,
          btnSubmitLabel: "Reject",
          btnSubmitColor: "btn-danger",
          icon: {
            code: "mdi-alert-circle-outline",
            color: "red",
          },
          message: `<div class="text-center">Reject assignment will return your <br /> assignment. Are you sure ?</div>`,
        };
        this.$refs.modal_confirm.start(item, 10);
      }
      // else if(item.label.toLowerCase() == "submit assignment")
    },
    doProsess(item) {
      this.isLoading = true;
      client
        .approveDiscussionAssignment({
          store: this.$store,
          data: item,
        })
        .then((res) => {
          if (res.plainData.responseCode == "011000") {
            this.$root.toast.show({
              message: res.plainData.responseData.description ?? "Success",
              color: "success",
              timeout: 3000,
            });
          } else {
            this.$root.toast.show({
              message: res.plainData.responseMessage,
              color: "warning",
              timeout: 3000,
            });
          }
        })
        .finally(() => {
          this.$refs.modal_confirm.closeModal();
          this.isLoading = false;
          this.getFlow();
          this.$emit("doneProsess");
        });
    },
    getColor(label) {
      label = label.toLowerCase();
      let classColor = {
        approve: "sectionBlue-button",
        reject: "sectionRed-button",
        delete: "sectionRed-button",
      };
      if (this.isDisabled) return "sectionGrey-button";
      return classColor[label] ?? "sectionBlue-button";
    },
  },
  mounted() {
    this.getFlow();
  },
};
</script>

<style scope>
.sectionGrey-button {
  width: 13vw;
  color: #fff !important;

  background: linear-gradient(180deg, #dfdfdf 0%, #e4e2e2 100%);

  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.25);
  border-radius: 10px;
  letter-spacing: 0.1px;
  font-weight: 900;
}

.sectionBlue-button {
  width: 13vw;
  color: #fff !important;

  background: linear-gradient(180deg, #065695 0%, #267dc2 100%);

  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.25);
  border-radius: 10px;
  letter-spacing: 0.1px;
  font-weight: 900;
}

.sectionRed-button {
  width: 13vw;
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
