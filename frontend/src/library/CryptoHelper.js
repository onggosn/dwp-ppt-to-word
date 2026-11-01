import CryptoJS from "crypto-js";

export function toHex(str) {
  var result = "";
  for (var i = 0; i < str.length; i++) {
    result += str.charCodeAt(i).toString(16);
  }
  var tmp = parseFloat(h2d(result)).toString().split(".");
  return tmp[0] + "." + tmp[1];
}

export function secureRandomFloat(min = 0, max = 10) {
  const array = new Uint32Array(1);
  window.crypto.getRandomValues(array);
  const randomNumber = array[0] / 0xffffffff;
  return min + randomNumber * (max - min);
}

export function createKey(length) {
  var result = "";
  var characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  var charactersLength = characters.length;
  for (var i = 0; i < length; i++) {
    result += characters.charAt(
      Math.floor(secureRandomFloat(0, charactersLength))
    );
  }
  return result;
}

function h2d(s) {
  function add(x, y) {
    var c = 0,
      r = [];
    var x2 = x.split("").map(Number);
    var y2 = y.split("").map(Number);
    while (x2.length || y2.length) {
      var s = (x2.pop() || 0) + (y2.pop() || 0) + c;
      r.unshift(s < 10 ? s : s - 10);
      c = s < 10 ? 0 : 1;
    }
    if (c) r.unshift(c);
    return r.join("");
  }

  var dec = "0";
  s.split("").forEach(function (chr) {
    var n = parseInt(chr, 16);
    for (var t = 8; t; t >>= 1) {
      dec = add(dec, dec);
      if (n & t) dec = add(dec, "1");
    }
  });
  return dec;
}

export function processKeys({ undertaker, randyOrton, johnCena, reyMisterio }) {
  const iv = CryptoJS.enc.Utf8.parse(undertaker);

  const pks = johnCena;
  const publicKey = randyOrton;

  const pkc = toHex(publicKey) * reyMisterio;
  const pkskc = Math.log(pks) + Math.log(reyMisterio);
  const hpkskc = CryptoJS.SHA256(pkskc.toString()).toString();
  const cutkey = hpkskc.substring(0, 32);

  return { iv, cutkey, pkc, hpkskc };
}

export function encryptCustom(payload, encryptionKey) {
  const encryptedJson = CryptoJS.AES.encrypt(payload, encryptionKey, {
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.ZeroPadding,
  }).toString();
  return encryptedJson;
}

export function decryptCustom(data, encryptionKey) {
  var send2 = CryptoJS.AES.decrypt(data, encryptionKey, {
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.ZeroPadding,
  });
  let textPlain = send2.toString(CryptoJS.enc.Utf8);

  return textPlain;
}

// export function decrypt(data, store) {
//   var send2 = CryptoJS.AES.decrypt(data, store.getters.encryptionKey, {
//     iv: store.getters.iv,
//     mode: CryptoJS.mode.CBC,
//     padding: CryptoJS.pad.ZeroPadding,
//   });
//   let textPlain = send2.toString(CryptoJS.enc.Utf8);

//   return JSON.parse(textPlain);
// }

// export function encrypt(payload, store) {
//   const jsonText = JSON.stringify(payload);

//   const encryptedJson = CryptoJS.AES.encrypt(
//     jsonText,
//     store.getters.encryptionKey,
//     {
//       iv: store.getters.iv,
//       mode: CryptoJS.mode.CBC,
//       padding: CryptoJS.pad.ZeroPadding,
//     }
//   ).toString();

//   const finalPayload = {
//     json: encryptedJson,
//   };

//   return finalPayload;
// }

export async function decrypt(data, store) {
  if (process.env.VUE_APP_POC_MOCK === "true") return data; // POC mock: no encryption
  if (data === "undefined" || data === null || data === "") {
    return null;
  }
  const base64Key = store.getters.encryptionKey;
  const base64Nonce = store.getters.iv;

  if (!base64Key || !base64Nonce) {
    throw new Error(
      `[CRYPTO_HELPER] Missing decryption keys: encryptionKey=${base64Key} (${typeof base64Key}), iv=${base64Nonce} (${typeof base64Nonce})`
    );
  }

  const keyBytes = Uint8Array.from(atob(base64Key), (c) => c.charCodeAt(0));
  const nonce = Uint8Array.from(atob(base64Nonce), (c) => c.charCodeAt(0));
  const encryptedBytes = Uint8Array.from(atob(data), (c) => c.charCodeAt(0));

  const cryptoKey = await crypto.subtle.importKey(
    "raw",
    keyBytes,
    { name: "AES-GCM" },
    false,
    ["decrypt"]
  );

  const decrypted = await crypto.subtle.decrypt(
    { name: "AES-GCM", iv: nonce },
    cryptoKey,
    encryptedBytes
  );

  const textPlain = new TextDecoder().decode(decrypted);

  const parsedData = JSON.parse(textPlain);

  return parsedData;
}

export async function encrypt(payload, store) {
  if (process.env.VUE_APP_POC_MOCK === "true") return payload; // POC mock: no encryption
  const jsonText = JSON.stringify(payload);
  const base64Key = store.getters.encryptionKey;
  const base64Nonce = store.getters.iv;

  if (!base64Key || !base64Nonce) {
    throw new Error(
      `[CRYPTO_HELPER] Missing encryption keys: encryptionKey=${base64Key} (${typeof base64Key}), iv=${base64Nonce} (${typeof base64Nonce})`
    );
  }

  const keyBytes = Uint8Array.from(atob(base64Key), (c) => c.charCodeAt(0));
  const nonce = Uint8Array.from(atob(base64Nonce), (c) => c.charCodeAt(0));
  const plaintextBytes = new TextEncoder().encode(jsonText);

  const cryptoKey = await crypto.subtle.importKey(
    "raw",
    keyBytes,
    { name: "AES-GCM" },
    false,
    ["encrypt"]
  );

  const encrypted = await crypto.subtle.encrypt(
    { name: "AES-GCM", iv: nonce },
    cryptoKey,
    plaintextBytes
  );

  const bytes = new Uint8Array(encrypted);
  let binary = "";
  const chunkSize = 0x8000;
  for (let i = 0; i < bytes.length; i += chunkSize) {
    binary += String.fromCharCode(...bytes.subarray(i, i + chunkSize));
  }
  const encryptedJson = btoa(binary);

  const finalPayload = {
    json: encryptedJson,
  };

  return finalPayload;
}
