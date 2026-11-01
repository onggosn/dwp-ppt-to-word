import { helpers } from "@vuelidate/validators";

const defaultErrorMessages = {
  required: "Wajib diisi",
  moreThanStartDate: "Oops! Start date must be earlier than end date",
  moreThanStartTime: "Oops! End time cannot be below start time",
  alphaNumCustom: "Hanya huruf dan angka",
  url: "Url yang dimasukkan tidak valid",
  notRelevantSymbol: "Tidak boleh mengandung simbol yang tidak relevan",
  sharePointRegex:
    'cannot contain the following characters: " * < : > ; ? % # / | \\ .',
  notHasTagHtml: "Tidak boleh mengandung simbol html",
  unique: "Data sudah ada",
};

export function getErrorMessages(
  vuelidateState: any,
  customErrorMessages = {}
) {
  try {
    const result: string[] = [];
    const errorMessages = { ...defaultErrorMessages, ...customErrorMessages };
    // if (typeof vuelidateState === "undefined") return [];
    if ("$dirty" in vuelidateState && vuelidateState.$dirty) {
      vuelidateState.$errors?.forEach((element: any) => {
        const msg = errorMessages[element.$validator] ?? element.$message;
        result.push(msg as string);
      });
      return result;
    } else if (!("$dirty" in vuelidateState)) {
      const msg = errorMessages[vuelidateState.$validator] ?? "validasi gagal";
      result.push(msg as string);
    }
    return result.filter((el) => el);
  } catch (error) {
    return [];
  }
}

export function isError(error: any) {
  return getErrorMessages(error).length <= 0;
}

export function notRelevantSymbol(value: any) {
  // Restrict symbols that do not represent an event place
  // eslint-disable-next-line
  const symbolRegex = /[!@#$%^&*()_+={}\[\]:;"'<>,.?/~`\\|\-]/;
  return !symbolRegex.test(value);
}

export function notHasTagHtml(value: any) {
  // Restrict symbols that do not represent an event place
  // eslint-disable-next-line
  const symbolRegex = /<[^>]*>/;
  return !symbolRegex.test(value);
}

export const timeRegex = helpers.regex(/^(?:[01]\d|2[0-3]):(?:[0-5]\d)$/);

export const alphaNumCustom = helpers.regex(/^[a-zA-Z0-9\-_()\s]+$/i);

export const sharePointRegex = helpers.regex(
  /^([^*"<:.;>?%#/\\|]|\*triwulan\*)*$/
);

export function getNestedErrorMessage(
  parentState: any,
  item: any[],
  customMessage = {}
) {
  const errorMessages = { ...defaultErrorMessages, ...customMessage };

  if (!parentState.$dirty) return [];

  return item.map((d) => {
    return errorMessages[d.$validator] ?? d.$message;
  });
}

export function hasNestedError(parentState: any, item: any[]): boolean {
  return parentState.$dirty && item.length != 0;
}

export const semicolonRegex = helpers.regex(/^[^;]*$/);
