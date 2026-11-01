const LabelToast = (resMessage: string) => {
  const label = {
    success: {
      message: resMessage,
      color: "success",
      timeout: 5000,
      icon: "mdi-check",
    },
    oopss: {
      message: resMessage,
      color: "oopss",
      timeout: 5000,
    },
    warning: {
      message: resMessage,
      color: "warning",
      timeout: 5000,
      icon: "mdi-check",
    },
  };

  return label;
};

export default { LabelToast };
