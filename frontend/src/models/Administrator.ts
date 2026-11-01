import client from "@/library/ApiClient";
import store from "@/store/index";
// import administrator from "@/mock/Administrator.js";
// const IS_DATA_MOCK = process.env.VUE_APP_DATA_MOCK;

interface Role {
  username: string;
  name: string;
  satket: string;
  jabatan: string;
  role: Array<RoleDetail>;
}

interface RoleDetail {
  id: number;
  idUser: number;
  username: string;
  idRole: number;
  roleName: string;
}

interface IitemsRole {
  id: number;
  name: string;
}

export async function mGetlistUserAndRole(
  pageNo: number,
  entriesPerPage: number,
  searchKeywoard?: string
): Promise<any> {
  let listUserAndRole: Role[] = [];
  const error = 0;
  await client
    .getListUsernameAndRole({
      data: {
        pageNo: pageNo,
        entriesPerPage: entriesPerPage,
        username: store.state.username,
        searchKeyword: searchKeywoard,
      },
      store: store,
    })
    .then((response): void => {
      const status = response.plainData.responseCode;
      const items = response;
      if (status == "011000") {
        listUserAndRole = items;
      }
    });

  return { list: listUserAndRole, error: error };
}

export async function mGetListRole(): Promise<IitemsRole[]> {
  let listRole: IitemsRole[] = [];
  await client
    .getListAllRole({
      store: store,
    })
    .then((response): void => {
      const status = response.plainData.responseCode;
      const items = response;
      if (status == "011000") {
        listRole = items;
      }
    });

  return listRole;
}

// template
interface TemplateResponse {
  no: number;
  namaFile: string;
  tipeDokumen: string;
  tipeActivity: string;
  tipeTask: string;
}

export async function mGetListTemplate(
  pageNo: number,
  entriesPerPage: number
): Promise<any> {
  let listTemplate: TemplateResponse[] = [];
  const error = 0;

  await client
    .getListTemplate({
      data: {
        pageNo: pageNo,
        entriesPerPage: entriesPerPage,
        username: store.state.username,
      },
      store: store,
    })
    .then((response): void => {
      const status = response.plainData.responseCode;
      const items = response;
      if (status == "011000") {
        listTemplate = items;
      }
    });

  return { list: listTemplate, error: error };
}

export function getListSectionPenyusun(): Promise<any> {
  return client
    .getPenyusunSection({
      store: store,
    })
    .then((response) => {
      switch (response.plainData.responseCode) {
        case "011000": {
          return response.plainData.responseData;
        }
        default: {
          return [];
        }
      }
    });
}
