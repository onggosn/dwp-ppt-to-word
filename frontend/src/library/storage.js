const { EncryptStorage } = require("encrypt-storage");

// Example of secret_key variable in an .env file
export const encryptStorage = new EncryptStorage(
  process.env.VUE_APP_KPOM3UTUOL_TJ8ULNKY0X,
  {
    storageType: "sessionStorage",
    stateManagementUse: true,
  }
);
export default encryptStorage;
