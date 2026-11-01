// import { createApp } from "vue";
import { createStore } from "vuex";
import { processKeys } from "../library/CryptoHelper";
import CryptoJS from "crypto-js";
import { encryptStorage } from "../library/storage";
import { isNotNullorUndefined } from "../helpers/utils.ts";

import moduleV2 from "@v2/Store.ts";
import moduleOmPro from "@omPro/Store.ts";

const store = createStore({
  state() {
    return {
      notifList: [],
      isNotifNew: false,
      notifNumber: isNotNullorUndefined(localStorage.ente)
        ? encryptStorage.decryptString(localStorage.ente)
        : encryptStorage.getItem("ente"),
      divisi: isNotNullorUndefined(localStorage.dosa)
        ? encryptStorage.decryptString(localStorage.dosa)
        : encryptStorage.getItem("dosa"),
      johnCena: Number(encryptStorage.getItem("johnCena")),
      randyOrton: encryptStorage.getItem("randyOrton"),
      undertaker: isNotNullorUndefined(localStorage.undertaker)
        ? encryptStorage.decryptString(localStorage.undertaker)
        : encryptStorage.getItem("undertaker"),
      teriyaki: isNotNullorUndefined(localStorage.teriyaki)
        ? encryptStorage.decryptString(localStorage.teriyaki)
        : encryptStorage.getItem("teriyaki"),
      yakiniku: isNotNullorUndefined(localStorage.yakiniku)
        ? encryptStorage.decryptString(localStorage.yakiniku)
        : encryptStorage.getItem("yakiniku"),
      cutkey: isNotNullorUndefined(localStorage.ampuni)
        ? encryptStorage.decryptString(localStorage.ampuni)
        : encryptStorage.getItem("ampuni"),
      hpkskc: encryptStorage.getItem("hpkskc"),
      pkc: isNotNullorUndefined(localStorage.akan)
        ? Number(encryptStorage.decryptString(localStorage.akan))
        : Number(encryptStorage.getItem("akan")),
      token: isNotNullorUndefined(localStorage.hamba)
        ? encryptStorage.decryptString(localStorage.hamba)
        : encryptStorage.getItem("hamba"),
      accessToken: isNotNullorUndefined(localStorage.penuh)
        ? encryptStorage.decryptString(localStorage.penuh)
        : encryptStorage.getItem("penuh"),
      username: isNotNullorUndefined(localStorage.yang)
        ? encryptStorage.decryptString(localStorage.yang)
        : encryptStorage.getItem("yang"),
      fullname: isNotNullorUndefined(localStorage.ini)
        ? encryptStorage.decryptString(localStorage.ini)
        : encryptStorage.getItem("ini"),
      kane: isNotNullorUndefined(localStorage.kane)
        ? encryptStorage.decryptString(localStorage.kane)
        : encryptStorage.getItem("kane"),
      urlApim: isNotNullorUndefined(localStorage.uap)
        ? encryptStorage.decryptString(localStorage.uap)
        : encryptStorage.getItem("uap"),
      isDetailTaskShow: true,
      isWorkspaceDetailShow: true,
      task: {},
      divisiDewa: [
        "DMST.GRUP SEKRETARIAT DEWAN GUBERNUR",
        "DMST.GSK.KEL MANAJEMEN RAPAT DEWAN GUBERNUR",
      ],
      modelAlertData: {
        icon: "mdi-help-circle-outline",
        color: "grey",
        title: "no title set",
        message: "no message set",
        confirmText: "Ok",
      },
    };
  },
  getters: {
    isLoggedIn(state) {
      return (
        !!state.username &&
        state.username !== "undefined" &&
        state.username !== "null"
      );
    },
    // encryptionKey(state) {
    //   return CryptoJS.enc.Utf8.parse(state.cutkey);
    // },
    // iv(state) {
    //   return CryptoJS.enc.Utf8.parse(state.undertaker);
    // },
    encryptionKey(state) {
      return state.teriyaki;
    },
    iv(state) {
      return state.yakiniku;
    },
  },
  mutations: {
    checkNotif(state, notif) {
      state.notifList = notif.notificationViewList;
      if (state.notifNumber < notif.totalNotification) {
        state.isNotifNew = true;
      }
    },
    updateNotif(state) {
      state.isNotifNew = false;
      encryptStorage.setItem("ente", state.notifNumber);

      // set local storage
      var ente = encryptStorage.getItem("ente", true);
      localStorage.setItem("ente", ente);
    },
    createNewNotif(state, notif) {
      state.notifList = notif.notificationViewList;
      if (state.notifNumber < notif.totalNotification) {
        state.isNotifNew = true;
      } else {
        if (!state.isNotifNew) {
          state.notifNumber = notif.totalNotification;
          state.isNotifNew = false;
          encryptStorage.setItem("ente", state.notifNumber);

          // set local storage
          var ente = encryptStorage.getItem("ente", true);
          localStorage.setItem("ente", ente);
        }
      }
    },
    updateLoginResponse(state, loginResponse) {
      state.token = loginResponse.token;
      state.username = loginResponse.username;
      state.fullname = loginResponse.fullname;
      state.kane = loginResponse.kane;
      state.divisi = loginResponse.divisi;

      encryptStorage.setItem("hamba", state.token);
      encryptStorage.setItem("yang", state.username);
      encryptStorage.setItem("ini", state.fullname);
      encryptStorage.setItem("kane", state.kane);
      encryptStorage.setItem("dosa", state.divisi);

      var hamba = encryptStorage.getItem("hamba", true);
      var yang = encryptStorage.getItem("yang", true);
      var ini = encryptStorage.getItem("ini", true);
      var kane = encryptStorage.getItem("kane", true);
      var dosa = encryptStorage.getItem("dosa", true);

      // set local storage
      localStorage.setItem("hamba", hamba);
      localStorage.setItem("yang", yang);
      localStorage.setItem("ini", ini);
      localStorage.setItem("kane", kane);
      localStorage.setItem("dosa", dosa);
      localStorage.setItem("isLogout", false);
      localStorage.setItem("sukhoi", loginResponse.sukhoi);
    },
    updateAccessToken(state, apimInfo) {
      state.accessToken = apimInfo?.tokenAPIM;
      state.urlApim =
        apimInfo?.url +
        `${process.env.VUE_APP_ENV === "prod" ? "dmpmiddleware" : "newdmp"}`;

      encryptStorage.setItem("penuh", state.accessToken);
      encryptStorage.setItem("uap", state.urlApim);
      // local storage
      var penuh = encryptStorage.getItem("penuh", true);
      var uap = encryptStorage.getItem("uap", true);
      localStorage.setItem("penuh", penuh);
      localStorage.setItem("uap", uap);
    },
    updateKeys(state, payload) {
      const APP_VERSION = process.env.VUE_APP_VERSION ?? "";
      const VERSION_KEY = "__app_version__";
      state.johnCena = payload.johnCena;
      state.randyOrton = payload.randyOrton;
      state.undertaker = payload.undertaker;
      state.teriyaki = payload.teriyaki;
      state.yakiniku = payload.yakiniku;
      const { pkc, cutkey, hpkskc } = processKeys(payload);

      state.cutkey = cutkey;
      state.pkc = pkc;
      state.hpkskc = hpkskc;

      encryptStorage.setItem("undertaker", state.undertaker);
      encryptStorage.setItem("teriyaki", state.teriyaki);
      encryptStorage.setItem("yakiniku", state.yakiniku);
      encryptStorage.setItem("ampuni", state.cutkey);
      encryptStorage.setItem("akan", state.pkc);

      //set local storage
      var undertaker = encryptStorage.getItem("undertaker", true);
      var teriyaki = encryptStorage.getItem("teriyaki", true);
      var yakiniku = encryptStorage.getItem("yakiniku", true);
      var ampuni = encryptStorage.getItem("ampuni", true);
      var akan = encryptStorage.getItem("akan", true);

      localStorage.setItem("undertaker", undertaker);
      localStorage.setItem("teriyaki", teriyaki);
      localStorage.setItem("yakiniku", yakiniku);
      localStorage.setItem("ampuni", ampuni);
      localStorage.setItem("akan", akan);
      localStorage.setItem(VERSION_KEY, APP_VERSION);
    },
    logout(state) {
      state.johnCena = null;
      state.divisi = null;
      state.randyOrton = null;
      state.undertaker = null;
      state.teriyaki = null;
      state.yakiniku = null;
      state.cutkey = null;
      state.pkc = null;
      state.hpkskc = null;
      state.token = null;
      state.username = null;
      state.kane = null;
      state.accessToken = null;
      sessionStorage.clear();
      localStorage.clear();
      encryptStorage.clear();
    },
    showUnautorize(state, data) {
      state.modelAlertData = data;
    },
  },
  actions: {
    updateKeys(context, payload) {
      context.commit("updateKeys", payload);
    },
    checkNotif(context, payload) {
      context.commit("checkNotif", payload);
    },
    updateNotif(context, payload) {
      context.commit("updateNotif", payload);
    },
    createNewNotif(context, payload) {
      context.commit("createNewNotif", payload);
    },
    updateLoginResponse(context, loginResponse) {
      context.commit("updateLoginResponse", loginResponse);
    },
    updateAccessToken(context, accessToken) {
      context.commit("updateAccessToken", accessToken);
    },
    logout(context) {
      context.commit("logout");
    },
  },
  modules: {
    ...moduleV2,
    ...moduleOmPro,
  },
});

export default store;
