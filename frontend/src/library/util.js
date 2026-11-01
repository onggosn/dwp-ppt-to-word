export function dd() {
  if (process.env.VUE_APP_MODE !== "production") {
    undefined;
  }
}

export function randomRequestId() {
  return Math.floor(secureRandomFloat(0, 999999));
}

export function filterFileName(input) {
  //Risalah Rapat_520b8331-c16a-4746-d779-08da58081084.docx
  let temp = input.split("_");
  let typeData = temp[temp.length - 1].split(".")[1];
  temp.pop();
  temp = temp.join("_");
  temp = temp + "." + typeData;
  return temp;
}

export function secureRandomFloat(min = 0, max = 10) {
  const array = new Uint32Array(1);
  window.crypto.getRandomValues(array);
  const randomNumber = array[0] / 0xffffffff;
  return min + randomNumber * (max - min);
}
