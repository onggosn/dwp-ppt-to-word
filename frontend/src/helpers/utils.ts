export function formatBytes(bytes: number, decimals = 2) {
  if (!+bytes) return "0.00 Bytes";

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];

  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
}

export function initialName(name: string, length = 2) {
  let result = "";
  const arrName = name.split(" ");
  if (arrName.length == 1) {
    result = name[0];
  } else {
    for (let index = 0; index < length; index++) {
      const f = arrName[index] ?? "";
      result += f[0];
    }
  }
  return result;
}

export function capitalize(str: string) {
  const arr = str.split(" ");
  for (let i = 0; i < arr.length; i++) {
    arr[i] = arr[i].charAt(0).toUpperCase() + arr[i].slice(1);
  }

  const result = arr.join(" ");
  return result;
}

export function getDatesInRange(strStartDate, strEndDate) {
  const startDate = new Date(strStartDate);
  const endDate = new Date(strEndDate);
  const dates: any[] = [];

  while (startDate <= endDate) {
    dates.push(new Date(startDate));
    startDate.setDate(startDate.getDate() + 1);
  }

  return dates;
}

export function isNotNullorUndefined(value) {
  return value !== null && value !== "" && typeof value !== "undefined";
}

export function getSessionOrLocalStorage(session, local) {
  return isNotNullorUndefined(local) ? local : session;
}

/**
 * filter options base on selected options
 * @param o all of available options
 * @param s selected options
 * @param k option's unique identifier key, default "id"
 * @returns unselected options
 */
export function uniqueOptions(
  o: object[],
  s: object[] | number[] | string[],
  k = "id"
) {
  return o.filter(
    (p) => !s.map((s) => (typeof s == "object" ? s[k] : s)).includes(p[k]),
    []
  );
}

export function getNumberFromString(string: string) {
  return string.match(/\d+(?:\.\d+)?/)?.[0] || "0";
}
