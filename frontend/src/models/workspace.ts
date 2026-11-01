import client from "@/library/ApiClient";
import store from "@/store/index";

interface Workspace {
  endDate: string;
  idStatus: number;
  idWorkspace: string;
  idWorkspaceLevel: number;
  idWorkspaceType: number;
  monthPeriod: string;
  status: string;
  username: string;
  workspaceName: string;
  yearPeriod: string;
}

export async function mWorkspaceInProgress(
  level: number,
  seeAll = false
): Promise<any> {
  let isCanSeeAll = false;
  let workspaceList: Workspace[] = [];
  await client
    .getListWorkspaceByStatusAndLevel({
      data: {
        username: store.state.username,
        idStatus: 10,
        idWorkspaceLevel: level,
      },
      store: store,
    })
    .then((response): void => {
      const status = response.plainData.responseCode;
      const items = response.plainData.responseData.listWorkspace;
      if (status == "011000") {
        switch (true) {
          case seeAll: {
            workspaceList = items;
            break;
          }
          case items.length > 3 && !seeAll: {
            let i = 0;
            items.forEach((element) => {
              if (i < 3) {
                workspaceList.push(element);
              }
              i++;
            });
            isCanSeeAll = true;
            break;
          }
          default:
            workspaceList = items;
            break;
        }
      }
    });

  return { list: workspaceList, seeAll: isCanSeeAll };
}

export async function mWorkspaceNotStarted(
  level: number,
  seeAll = false
): Promise<any> {
  let isCanSeeAll = false;
  let workspaceList: Workspace[] = [];
  await client
    .getListWorkspaceByStatusAndLevel({
      data: {
        username: store.state.username,
        idStatus: 9,
        idWorkspaceLevel: level,
      },
      store: store,
    })
    .then((response): void => {
      const status = response.plainData.responseCode;
      const items = response.plainData.responseData.listWorkspace;
      if (status == "011000") {
        switch (true) {
          case seeAll: {
            workspaceList = items;
            break;
          }
          case items.length > 3 && !seeAll: {
            let i = 0;
            items.forEach((element) => {
              if (i < 3) {
                workspaceList.push(element);
              }
              i++;
            });
            isCanSeeAll = true;
            break;
          }
          default:
            workspaceList = items;
            break;
        }
      }
    });

  return { list: workspaceList, seeAll: isCanSeeAll };
}

export async function mWorkspacePast(
  level: number,
  seeAll = false
): Promise<any> {
  let isCanSeeAll = false;
  let workspaceList: Workspace[] = [];
  await client
    .getListWorkspaceByStatusAndLevel({
      data: {
        username: store.state.username,
        idStatus: 11,
        idWorkspaceLevel: level,
      },
      store: store,
    })
    .then((response): void => {
      const status = response.plainData.responseCode;
      const items = response.plainData.responseData.listWorkspace;
      if (status == "011000") {
        switch (true) {
          case seeAll: {
            workspaceList = items;
            break;
          }
          case items.length > 3 && !seeAll: {
            let i = 0;
            items.forEach((element) => {
              if (i < 3) {
                workspaceList.push(element);
              }
              i++;
            });
            isCanSeeAll = true;
            break;
          }
          default:
            workspaceList = items;
            break;
        }
      }
    });

  return { list: workspaceList, seeAll: isCanSeeAll };
}
