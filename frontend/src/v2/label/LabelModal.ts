import type { TModalConfirm } from "@v2/Type.d";

export const formApproveInitial: TModalConfirm = {
  title: "Submit Document",
  message:
    "Submit document will send the document to document mapping before approval. Are you sure?",
  btnSubmitLabel: "Yes",
  width: 554,
  btnSubmitColor: "primary-gradient",
};

export const formFailSubmitInitial: TModalConfirm = {
  title: "Oops",
  message: "",
  btnSubmitLabel: "OK",
  width: 554,
  btnSubmitColor: "primary-gradient",
};

export const formDeleteInitial: TModalConfirm = {
  title: "Delete AIU",
  message: "Are you sure delete this Document ?",
  btnSubmitLabel: "Yes",
  btnSubmitColor: "danger-gradient",
};

export const formSendRevise: TModalConfirm = {
  title: "Send Document",
  message: "Are you sure to send this document?",
  btnSubmitLabel: "Yes",
  btnSubmitColor: "primary-gradient",
  icon: {
    backgrounColor: "white",
    size: 80,
  },
};

export const formFailSignInitial: TModalConfirm = {
  title: "Oops, Visual Sign Required",
  message: `Visual sign is not available.<br /> Please create your visual sign before approving this document.`,
  btnSubmitLabel: "Create visual Sign",
  width: 554,
  btnSubmitColor: "primary-gradient",
  icon: {
    code: "mdi-alert-circle",
    color: "orange",
    backgrounColor: "white",
    size: 95,
  },
};

export const formApproveOnSubmitForm = (btnLabel: string) => {
  const approvalForm: TModalConfirm = {
    title: `${btnLabel} Document`,
    message: `Are you sure to ${btnLabel} this document ? <br /> You will accept all Suggestion when ${btnLabel} this document`,
    btnSubmitLabel: "Yes",
    btnSubmitColor: "primary-gradient",
    width: 554,
    icon: {
      code: "mdi-close-circle-outline",
      color: "red",
      backgrounColor: "white",
      size: 80,
    },
  };

  return approvalForm;
};

export const formApproveOnSubmitWithCheckForm = (btnLabel: string) => {
  const approvalForm: TModalConfirm = {
    title: `${btnLabel} Document`,
    message: `Are you sure to ${btnLabel} this document ? <br /> You will accept all Suggestion when ${btnLabel} this document`,
    btnSubmitLabel: "Yes",
    btnSubmitColor: "primary-gradient",
    width: 554,
    icon: {
      code: "mdi-check-circle",
      color: "success",
      backgrounColor: "white",
      size: 80,
    },
  };

  return approvalForm;
};

export const formApproveOnCloseDialog = (labelCancel: string) => {
  const approveForm: TModalConfirm = {
    title: `Cancel ${labelCancel}`,
    message: "Are you sure to cancel this document ? ",
    btnSubmitLabel: "Next",
    width: 554,
    btnSubmitColor: "danger-gradient",
  };

  return approveForm;
};

export const formCancelOnSaveDesc = (labelCancel: string) => {
  const form: TModalConfirm = {
    title: `Cancel ${labelCancel}`,
    message: "",
    btnSubmitLabel: "Submit",
    btnSubmitColor: "danger-gradient",
  };

  return form;
};

export const formDeleteOnSaveDesc: TModalConfirm = {
  title: "Delete AIU",
  message: "",
  btnSubmitLabel: "Submit",
  btnSubmitColor: "danger-gradient",
};

export const WithoutMemberDialogue = (labelCancel?: string) => {
  const form = {
    reject: {
      // change content modal to reject
      title: "Reject Document",
      //perubahan wording UAT 7 nov 2024
      message: "Are you sure to reject this document?",
      btnSubmitLabel: "Yes",
      width: 554,
      icon: {
        code: "mdi-close-circle-outline",
        color: "red",
        backgrounColor: "white",
        size: 80,
      },
    },
    approve: {
      title: "Approve Document",
      message:
        "Are you sure to approve this document? <br /> You will accept all Suggestion when approve this document",
      btnSubmitLabel: "Yes",
      width: 554,
      btnSubmitColor: "primary-gradient",
    },
    cancel: {
      title: `Cancel ${labelCancel}`,
      message: "Are you sure to cancel this document ?",
      btnSubmitLabel: "Next",
      width: 554,
      btnSubmitColor: "danger-gradient",
    },
    submit: {
      title: "Submit Document",
      message:
        "Submit document will send the document to document mapping before approval. Are you sure?",
      btnSubmitLabel: "Yes",
      width: 554,
      btnSubmitColor: "primary-gradient",
    },
    sendSTP: {
      title: "Send",
      message: `
        <div style="text-align: left;">
          Submit your STP before requesting approval.
          <br/>  
          <b>STP submission is not available after the documents has been approved.</b> 
          <br/> 
          Are you sure you want to send this document for approval?
        </div>
      `,
      btnSubmitLabel: "Yes",
      width: 454,
      btnSubmitColor: "primary-gradient",
    },
    approveSTP: {
      title: "Approve",
      message: `
        <div style="text-align: left;">
          Submit your STP before requesting approval.
          <br/>  
          <strong>STP submission is not available after the documents has been approved.</strong> 
          <br/> 
          Are you sure you want to send this document for approval?
        </div>
      `,
      btnSubmitLabel: "Yes",
      width: 454,
      btnSubmitColor: "primary-gradient",
    },
  };

  return form;
};
