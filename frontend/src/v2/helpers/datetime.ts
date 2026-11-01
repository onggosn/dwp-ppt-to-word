const months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];
/**
 * Change data string format.
 * @param {string} dateStr - "2024-02-24T00:00:00".
 * @return {string} - in "February 24, 2024" format
 */

export const formatDate = (inputDate) => {
  // Parse the input date string
  const dateParts = inputDate.split("-");
  const year = parseInt(dateParts[0]);
  const month = parseInt(dateParts[1]) - 1; // Months are zero-based in JavaScript Date object
  const day = parseInt(dateParts[2]);

  // Create a Date object
  const date = new Date(year, month, day);

  // Format the date
  const formattedDate = months[date.getMonth()] + " " + day + ", " + year;

  return formattedDate;
};

export function formatDateYmd(date: any): any {
  const d: Date = new Date(date);
  let month: string = "" + (d.getMonth() + 1);
  let day: string = "" + d.getDate();
  const year: number = d.getFullYear();

  if (month.length < 2) month = "0" + month;
  if (day.length < 2) day = "0" + day;

  return [year, month, day].join("-");
}

export function reformatTime(input: any): any {
  if (input !== null && input !== undefined) {
    const date: Date = new Date(input); // force LOCAL time,
    return date.toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
    });
  } else {
    return null;
  }
}

export function getTimeRange(
  startTime: string,
  endTime: string,
  type = "hour"
): number {
  const start: Date = new Date(startTime);
  const end: Date = new Date(endTime);

  // Calculate the time difference in milliseconds
  const timeDifference: number = end.getTime() - start.getTime();

  // Convert milliseconds to hours, minutes, and seconds
  const hours: number = Math.floor(timeDifference / (1000 * 60 * 60));

  const minutes: number = Math.floor(timeDifference / (1000 * 60));

  const seconds: number = Math.floor(timeDifference / 1000);

  if (type == "minute") return minutes;
  else if (type == "second") return seconds;
  return hours;
}

export function calculateDaysBetweenDates(
  startDateStr: string,
  endDateStr: string
): number {
  // Convert input date strings to Date objects
  const startDate = new Date(startDateStr);
  const endDate = new Date(endDateStr);

  // Convert both dates to milliseconds
  const startMilliseconds = startDate.getTime();
  const endMilliseconds = endDate.getTime();

  // Calculate the difference in milliseconds
  const millisecondsPerDay = 1000 * 60 * 60 * 24; // Number of milliseconds in a day
  const differenceMilliseconds = Math.abs(endMilliseconds - startMilliseconds);

  // Convert the difference back into days
  const daysDifference = Math.ceil(differenceMilliseconds / millisecondsPerDay);
  return daysDifference;
}

export function getDateWithoutTime(date: Date | string): string {
  // Create a new date object to avoid modifying the original date
  const dateObject = typeof date === "string" ? new Date(date) : new Date(date);

  // Set hours, minutes, seconds, and milliseconds to zero
  dateObject.setHours(0, 0, 0, 0);

  // Format date components with padding
  const year = dateObject.getFullYear();
  const month = String(dateObject.getMonth() + 1).padStart(2, "0");
  const day = String(dateObject.getDate()).padStart(2, "0");

  return `${year}-${month}-${day}`;
}

/**
 * generate year for options.
 * @return {string[]} - in "['2021','2022','2023']" format
 */
export function getYearPicker() {
  const currentYear = new Date().getFullYear();
  // 5 years before the current date
  const minYear = currentYear - 5;
  // 10 years ahead of the current date
  const maxYear = currentYear + 100;

  const years: string[] = [];

  for (let year = minYear; year <= maxYear; year++) {
    years.push(year.toString());
  }

  return years;
}

/**
 * generate time.
 * @return {string[]} - in "['00:00', '00:30', '01:00']" format
 */
export function generateTime() {
  return [
    "00:00",
    "00:30",
    "01:00",
    "01:30",
    "02:00",
    "02:30",
    "03:00",
    "03:30",
    "04:00",
    "04:30",
    "05:00",
    "05:30",
    "06:00",
    "06:30",
    "07:00",
    "07:30",
    "08:00",
    "08:30",
    "09:00",
    "09:30",
    "10:00",
    "10:30",
    "11:00",
    "11:30",
    "12:00",
    "12:30",
    "13:00",
    "13:30",
    "14:00",
    "14:30",
    "15:00",
    "15:30",
    "16:00",
    "16:30",
    "17:00",
    "17:30",
    "18:00",
    "18:30",
    "19:00",
    "19:30",
    "20:00",
    "20:30",
    "21:00",
    "21:30",
    "22:00",
    "22:30",
    "23:00",
    "23:30",
  ];
}

/**
 *
 * @param {string} dateToFormat - "30/05/2024".
 * @param {string} timeToFormat - "02:00".
 * @return {string} - in "Fri May 17 2024 00:00:00 GMT+0700 (Indochina Time)" format
 */
export function initalDateLimit(dateToFormat: string, timeToFormat?: string) {
  const parts = dateToFormat.split("/");

  const day = parseInt(parts[0], 10);
  const month = parseInt(parts[1], 10) - 1; // Months are zero-based (0 = January, 1 = February, etc.)
  const year = parseInt(parts[2], 10);

  const times = timeToFormat?.split(":") ?? ["00", "00"];
  const hour = parseInt(times[0]) ?? 0;
  const minute = parseInt(times[1]) ?? 0;

  const dateObject = new Date(year, month, day, hour, minute);

  return dateObject;
}

/**
 * format timestamp to object date and time
 * @param {string} timestamp - "2024-05-15T20:12:34.42".
 * @return {Object} - in {date: "07/05/24", time: "10:50"} format
 */
export function convertTimestamp(timestamp: string) {
  const dateObj = new Date(timestamp);
  const hour = dateObj.getHours();
  const minute = dateObj.getMinutes();
  const day = dateObj.getDate();
  const month = dateObj.getMonth() + 1;

  const convertedTimestamp = {
    date: `${day}/${month}/${dateObj.getFullYear().toString().slice(2)}`,
    time: `${hour}:${minute < 10 ? `0${minute}` : minute}`,
  };

  return convertedTimestamp;
}
