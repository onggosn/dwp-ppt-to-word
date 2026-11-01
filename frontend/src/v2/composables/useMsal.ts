import { msalInstance, state, graphScopes } from "@v2/library/MsalAuthConfig";
import store from "@/store";
import type { SilentRequest } from "@azure/msal-browser";

let isInitialized = false;
let initializationPromise: Promise<void> | null = null;

export function useMsal() {
  const initializeMsal = async () => {
    if (!isInitialized) {
      if (!initializationPromise) {
        initializationPromise = msalInstance.initialize().then(() => {
          isInitialized = true;
        });
      }
      await initializationPromise;
    }
  };

  const getToken = async (customScopes?: string[]): Promise<string | null> => {
    try {
      await initializeMsal();
      // Prioritas: Ambil account yang aktif
      let account = msalInstance.getActiveAccount();

      // Jika aktif kosong (misal setelah refresh), ambil akun pertama yang tersedia
      if (!account) {
        const allAccounts = msalInstance.getAllAccounts();
        if (allAccounts.length > 0) {
          account = allAccounts[0];
          msalInstance.setActiveAccount(account);
        }
      }

      if (!account) {
        console.warn("No active account found. User might need to login.");
        return null;
      }

      const silentRequest: SilentRequest = {
        scopes: customScopes || graphScopes.scopes,
        account: account,
      };

      const response = await msalInstance.acquireTokenSilent(silentRequest);

      // Update state & store jika perlu agar data tetap sinkron
      state.isAuthenticated = true;
      state.user = response.account;
      store.commit("userStore/setActiveAccount", response.account);
      return response.accessToken;
    } catch (error) {
      console.error("Failed to acquire token silently:", error);
      return null;
    }
  };

  const login = async (
    method: "popup" | "redirect" = "popup",
    email?: string
  ) => {
    try {
      await initializeMsal(); // Pastikan initialized sebelum login

      const activeAccount = msalInstance.getActiveAccount();

      if (activeAccount && email && activeAccount.username === email) {
        state.isAuthenticated = true;
        state.user = activeAccount;
        return;
      }

      const request = {
        ...graphScopes,
        ...(email
          ? { prompt: "login", loginHint: email }
          : { prompt: "select_account" }),
      };

      if (method === "popup") {
        const response = await msalInstance.loginPopup(request);
        msalInstance.setActiveAccount(response.account);
        state.isAuthenticated = true;
        state.user = response.account;
        store.commit("userStore/setActiveAccount", response.account);
      } else {
        await msalInstance.loginRedirect(request);
      }
    } catch (error) {
      console.error("Login error:", error);
    }
  };

  const logoutMsal = async (method: "popup" | "redirect" = "popup") => {
    try {
      await initializeMsal();

      if (!msalInstance) return;

      state.isAuthenticated = false;
      state.user = null;
      store.commit("userStore/setActiveAccount", null);

      if (method === "popup") {
        await msalInstance.logoutPopup({
          mainWindowRedirectUri: window.location.origin,
        });
      } else {
        await msalInstance.logoutRedirect({
          postLogoutRedirectUri: window.location.origin,
        });
      }
    } catch (error) {
      console.error("Logout Error:", error);
      state.isAuthenticated = false;
      state.user = null;
      store.commit("userStore/setActiveAccount", null);
    }
  };

  const handleRedirect = async () => {
    try {
      await initializeMsal();
      const response = await msalInstance.handleRedirectPromise();
      await getToken();
      if (response?.account) {
        msalInstance.setActiveAccount(response.account);
        state.isAuthenticated = true;
        state.user = response.account;
        store.commit("userStore/setActiveAccount", response.account);
      } else {
        const activeAccount = msalInstance.getActiveAccount();
        if (activeAccount) {
          state.isAuthenticated = true;
          state.user = activeAccount;
          store.commit("userStore/setActiveAccount", activeAccount);
        } else {
          try {
            // Mencoba pancing session jika akun tidak ditemukan di memori
            const silentResponse = await msalInstance.ssoSilent(graphScopes);
            msalInstance.setActiveAccount(silentResponse.account);
            state.isAuthenticated = true;
            state.user = silentResponse.account;
            store.commit("userStore/setActiveAccount", silentResponse.account);
          } catch (err) {
            await login("redirect");
            void err;
          }
        }
      }
    } catch (error) {
      console.error("Handle redirect error:", error);
    }
  };

  return { login, logoutMsal, handleRedirect, getToken };
}
