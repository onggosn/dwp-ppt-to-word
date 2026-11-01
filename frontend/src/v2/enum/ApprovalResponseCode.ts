enum ApprovalResponseCode {
  success = "011000",
  failed = "011045",
  oneLeastSubmit = "011046",
  inProgress = "011033",
}

enum DialogFlag {
  cancel = "cancel",
  delete = "delete",
  reject = "reject",
  approve = "approve",
  revision = "revision",
  submit = "submit stp",
  update = "update",
  save = "save",
  approval = "approval",
  finalized = "finalized",
}

export default {
  ApprovalResponseCode,
  DialogFlag,
};
