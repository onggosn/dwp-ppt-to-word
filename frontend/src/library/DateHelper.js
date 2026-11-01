export function reformatDate(input) {
  const date = new Date(input); // force LOCAL time,
  const options = {
    weekday: "short",
    year: "numeric",
    month: "numeric",
    day: "numeric",
  };
  return date.toLocaleString("en-GB", options);
}
export function reformatDateNW(input) {
  const date = new Date(input); // force LOCAL time,
  const options = {
    year: "numeric",
    month: "numeric",
    day: "numeric",
  };
  return date.toLocaleString("en-GB", options);
}

export function isToday(someDate) {
  const today = new Date();
  return (
    someDate.getDate() == today.getDate() &&
    someDate.getMonth() == today.getMonth() &&
    someDate.getFullYear() == today.getFullYear()
  );
}

export function reformatTime(input) {
  const date = new Date(input); // force LOCAL time,
  return date.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
  });
}
export function checkDate(item) {
  if (isToday(new Date(item))) {
    return reformatTime(new Date(item));
  } else {
    return reformatDate(new Date(item));
  }
}

export function reformatFormDate(date) {
  if (!date) {
    return null;
  }

  const newDate = new Date(date + "T00:00:00"); // force LOCAL time,
  const options = {
    weekday: "short",
    year: "numeric",
    month: "numeric",
    day: "numeric",
  };
  return newDate.toLocaleString("en-GB", options);
}

export function reformatDateCard(endDate) {
  if (endDate) {
    let date = endDate.substring(0, endDate.indexOf("T"));
    const temp = date.split("-");
    return temp[2] + "/" + temp[1] + "/" + temp[0];
  } else {
    return "-";
  }
}

export function diffMinute(time1, time2) {
  var diff = (time2.getTime() - time1.getTime()) / 1000;
  diff /= 60;
  return Math.round(diff);
  // return Math.abs(Math.round(diff));
}

// export function formatDatePicker(date) {
//   if (!date) return null;

//   date = new Date(date);
//   const day = date.getDate();
//   const month = date.getMonth() + 1;
//   const year = date.getFullYear();

//   return `${day}/${month}/${year}`;
// }

export function getOnlyDate(date) {
  if (!date) return null;

  date = new Date(date);
  const day = date.getDate();
  const month = date.getMonth() + 1;
  const year = date.getFullYear();

  return `${year}-${month < 10 ? "0" + month : month}-${
    day < 10 ? "0" + day : day
  }`;
}
