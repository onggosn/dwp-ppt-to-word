/* eslint-disable */
export const formatTimeAMPM = (dateString: string): string => {
  try {
    const date = new Date(dateString);
    const options: Intl.DateTimeFormatOptions = {
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    };
    return date.toLocaleTimeString("en-US", options);
  } catch (error) {
    return dateString; // Return original if parsing fails
  }
};

export function isToday(someDate) {
  const today = new Date();
  return (
    someDate.getDate() == today.getDate() &&
    someDate.getMonth() == today.getMonth() &&
    someDate.getFullYear() == today.getFullYear()
  );
}

export function reformatTime(input) {
  const date = new Date(input);
  return date.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function reformatDate(input) {
  const date = new Date(input);
  const options: Intl.DateTimeFormatOptions = {
    weekday: "short",
    year: "numeric",
    month: "numeric",
    day: "numeric",
  };

  return date.toLocaleString("en-US", options);
}

export function reformatDateEngWithMonthLong(input, useTwoDigitDay = false) {
  const date = new Date(input);
  const options: Intl.DateTimeFormatOptions = {
    year: "numeric",
    month: "long",
    day: useTwoDigitDay ? "2-digit" : "numeric",
  };

  return date.toLocaleString("en-US", options);
}

export function checkDate(item: string) {
  if (isToday(new Date(item))) {
    return "Today " + reformatTime(new Date(item));
  } else {
    return reformatDate(new Date(item));
  }
}
export function reformatDateLong(start: string, end: string) {
  const startDate = new Date(start);
  const endDate = new Date(end);

  const options: Intl.DateTimeFormatOptions = {
    month: "long",
    day: "numeric",
    year: "numeric",
  };

  if (
    startDate.getDate() === endDate.getDate() &&
    startDate.getMonth() === endDate.getMonth() &&
    startDate.getFullYear() === endDate.getFullYear()
  ) {
    return startDate.toLocaleString("en-US", options);
  } else if (
    startDate.getMonth() === endDate.getMonth() &&
    startDate.getFullYear() === endDate.getFullYear()
  ) {
    const formattedStartDate = startDate.toLocaleString("en-US", {
      month: "long",
      day: "numeric",
    });
    const formattedEndDate = endDate.toLocaleString("en-US", {
      day: "numeric",
    });
    return `${formattedStartDate}-${formattedEndDate}, ${endDate.getFullYear()}`;
  } else if (startDate.getFullYear() === endDate.getFullYear()) {
    const formattedStartDate = startDate.toLocaleString("en-US", {
      month: "long",
      day: "numeric",
    });
    const formattedEndDate = endDate.toLocaleString("en-US", {
      month: "long",
      day: "numeric",
    });
    return `${formattedStartDate}-${formattedEndDate}, ${endDate.getFullYear()}`;
  } else {
    const formattedStartDate = startDate.toLocaleString("en-US", options);
    const formattedEndDate = endDate.toLocaleString("en-US", options);
    return `${formattedStartDate}-${formattedEndDate}`;
  }
}
export function convertDate(date) {
  const dateArray = date.split("/");
  const newDate = `${dateArray[2]}/${dateArray[1]}/${dateArray[0]}`;
  const realNewDate = new Date(newDate);
  return realNewDate;
}

export function formatTimeEngToIndNoDays(stringDate: string | undefined) {
  if (!stringDate) return null;

  const dates = new Date(stringDate);
  const month = dates.getMonth() + 1;
  const year = dates.getFullYear();

  return padTo2Digits(dates.getDate()) + "/" + padTo2Digits(month) + "/" + year;
}

export function formatTimeAddMinutes(dateString: string, addMinutes: number) {
  const dateObject = new Date(dateString);
  dateObject.setMinutes(dateObject.getMinutes() + addMinutes);

  const hours = dateObject.getUTCHours().toString().padStart(2, "0");
  const minutes = dateObject.getUTCMinutes().toString().padStart(2, "0");
  const seconds = dateObject.getUTCSeconds().toString().padStart(2, "0");

  return `${hours}:${minutes}`;
}

function padTo2Digits(num: number) {
  return num.toString().padStart(2, "0");
}

export function getDateFromString(dateString: string) {
  const dateObject = new Date(dateString);

  const year = dateObject.getUTCFullYear();
  const month = (dateObject.getUTCMonth() + 1).toString().padStart(2, "0");
  const day = dateObject.getUTCDate().toString().padStart(2, "0");

  return `${day}/${month}/${year}`;
}

export function addMinutes(dateString: string) {
  const dateObject = new Date(dateString);

  const year = dateObject.getUTCFullYear();
  const month = (dateObject.getUTCMonth() + 1).toString().padStart(2, "0");
  const day = dateObject.getUTCDate().toString().padStart(2, "0");

  return `${day}/${month}/${year}`;
}

export function reformatTimes(inputDate, isHour12 = false) {
  const date = new Date(inputDate);
  return date.toLocaleTimeString("en-US", {
    hour12: isHour12,
    hour: "2-digit",
    minute: "2-digit",
  });
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

export function parseEpoch(datetime: Date) {
  return datetime.getTime();
}

export function getWeekNumber(dateStr: string) {
  // Menerima dateStr dalam format "dd/MM/yyyy"
  if (!dateStr || typeof dateStr !== "string") return "Invalid date";

  const parts = dateStr.split("/");
  const day = parseInt(parts[0], 10);
  const month = parseInt(parts[1], 10) - 1; // JS months are 0-based
  const year = parseInt(parts[2], 10);

  const d = new Date(year, month, day);
  if (isNaN(d.getTime())) return "Invalid date";

  // Ambil hari pertama di bulan tersebut
  const firstDay = new Date(d.getFullYear(), d.getMonth(), 1);
  const firstDayOfWeek = firstDay.getDay();
  const offset = firstDayOfWeek === 0 ? 6 : firstDayOfWeek - 1;
  // Hitung nomor minggu dalam bulan
  const dayOfMonth = d.getDate();
  const weekInMonth = Math.ceil((dayOfMonth + offset) / 7);
  return `M${weekInMonth}`;
}

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  const day = date.getDate();
  const month = date.getMonth() + 1;
  const year = date.getFullYear();

  const formattedDay = String(day).padStart(2, "0");
  const formattedMonth = String(month).padStart(2, "0");

  return `${formattedMonth}/${formattedDay}/${year}`;
}

export function formatDateTime(dateTimeString: string): string {
  const dateTime = new Date(dateTimeString);

  const hours = dateTime.getHours();
  const minutes = dateTime.getMinutes();

  const formattedHours = String(hours).padStart(2, "0");
  const formattedMinutes = String(minutes).padStart(2, "0");

  return `${formattedHours}:${formattedMinutes}`;
}
