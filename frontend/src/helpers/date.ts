function padTo2Digits(num: number) {
  return num.toString().padStart(2, "0");
}

export function formatTimeEngtoInd(stringDate: string) {
  const dates = new Date(stringDate);
  const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  const month = dates.getMonth() + 1;
  const year = dates.getFullYear();

  return (
    days[dates.getDay()] +
    ", " +
    padTo2Digits(dates.getDate()) +
    "/" +
    padTo2Digits(month) +
    "/" +
    year
  );
}

export function formatTimeAmPm(stringDate: string) {
  const date = new Date(stringDate);
  let hours = date.getHours();
  const minutes = date.getMinutes();
  const ampm = hours >= 12 ? "PM" : "AM";
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  const resmin = minutes < 10 ? "0" + minutes : minutes;
  const strTime = hours + ":" + resmin + " " + ampm;
  return strTime;
}

export function getDateLabel(
  startDate: string,
  endDate: string,
  idTaskType: number
) {
  const start = formatTimeEngtoInd(startDate);
  const end = formatTimeEngtoInd(endDate);
  const startTime = formatTimeAmPm(startDate);
  const endTime = formatTimeAmPm(endDate);
  const labelTime = [3, 4].includes(idTaskType)
    ? ", " + startTime + "-" + endTime
    : "";
  const result = start + " - " + end + labelTime;
  return result;
}

export function formatTimeEngToIndNoDays(stringDate: string) {
  const dates = new Date(stringDate);
  const month = dates.getMonth() + 1;
  const year = dates.getFullYear();

  return padTo2Digits(dates.getDate()) + "/" + padTo2Digits(month) + "/" + year;
}

export function formatTimeYmd(stringDate: string) {
  const dates = new Date(stringDate);
  const month = dates.getMonth() + 1;
  const year = dates.getFullYear();

  return year + "-" + padTo2Digits(month) + "-" + padTo2Digits(dates.getDate());
}

export function formatTimeEngToMonthInd(stringDate: string) {
  const dates = new Date(stringDate);
  const month = dates.getMonth() + 1;
  const year = dates.getFullYear();

  const strDate =
    dates.getDate() < 10 ? "0" + dates.getDate() : dates.getDate();
  let strMonth = month < 10 ? "0" + month : month;

  if (strMonth == "01") {
    strMonth = "Januari";
  } else if (strMonth == "02") {
    strMonth = "Februari";
  } else if (strMonth == "03") {
    strMonth = "Maret";
  } else if (strMonth == "04") {
    strMonth = "April";
  } else if (strMonth == "05") {
    strMonth = "Mei";
  } else if (strMonth == "06") {
    strMonth = "Juni";
  } else if (strMonth == "07") {
    strMonth = "Juli";
  } else if (strMonth == "08") {
    strMonth = "Agustus";
  } else if (strMonth == "09") {
    strMonth = "September";
  } else if (strMonth == "10") {
    strMonth = "Oktober";
  } else if (strMonth == "11") {
    strMonth = "November";
  } else if (strMonth == "12") {
    strMonth = "Desember";
  }

  return strDate + " " + strMonth + " " + year;
}

export function formatTimeEngToMonthandTimeInd(stringDate: string) {
  const dates = new Date(stringDate);
  const month = dates.getMonth() + 1;
  const year = dates.getFullYear();

  const strDate =
    dates.getDate() < 10 ? "0" + dates.getDate() : dates.getDate();
  let strMonth = month < 10 ? "0" + month : month;

  if (strMonth == "01") {
    strMonth = "Januari";
  } else if (strMonth == "02") {
    strMonth = "Februari";
  } else if (strMonth == "03") {
    strMonth = "Maret";
  } else if (strMonth == "04") {
    strMonth = "April";
  } else if (strMonth == "05") {
    strMonth = "Mei";
  } else if (strMonth == "06") {
    strMonth = "Juni";
  } else if (strMonth == "07") {
    strMonth = "Juli";
  } else if (strMonth == "08") {
    strMonth = "Agustus";
  } else if (strMonth == "09") {
    strMonth = "September";
  } else if (strMonth == "10") {
    strMonth = "Oktober";
  } else if (strMonth == "11") {
    strMonth = "November";
  } else if (strMonth == "12") {
    strMonth = "Desember";
  }

  return (
    strDate + " " + strMonth + " " + year + " " + formatTimeAmPm(stringDate)
  );
}

export function dateDiff(date1: Date, date2: Date) {
  const difference_in_time = date2.getTime() - date1.getTime();
  const difference_in_days = difference_in_time / (1000 * 3600 * 24);
  return difference_in_days;
}
