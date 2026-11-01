const defaultErrorMessages = {
  required: "Wajib diisi",
  moreThanStartDate: "Oops! Start date must be earlier than end date",
  moreThanStartTime: "Oops! End time cannot be below start time",
  alphaNumCustom: "Hanya huruf dan angka",
};

export function getErrorMessages(vuelidateState, customErrorMessages = {}) {
  try {
    let result = [];
    if (!vuelidateState.$dirty) {
      return result;
    }

    const errorMessages = { ...defaultErrorMessages, ...customErrorMessages };

    vuelidateState.$errors.forEach((element) => {
      let msg = errorMessages[element.$validator] ?? element.$message;
      result.push(msg);
    });
    return result;
  } catch (error) {
    return [];
  }
}

export function isError(error) {
  return getErrorMessages(error).length <= 0;
}
