import client from "@/library/ApiClient";
import store from "@/store/index";

interface Profile {
  id: number;
  username: string;
  name: string;
  employeeNumber: string;
  organizationName: string;
  isActive: boolean;
  email: string;
  gradeId: number;
  positionId: number;
  gradeName: string;
  positionName: string;
  visualImage: string;
}

export function getProfile(): Promise<Profile> {
  const profile: Profile = {} as Profile;
  return client
    .GetUserByUsername({
      store: store,
      data: {
        username: store.state.username,
      },
    })
    .then((response) => {
      profile.id = response.plainData[0].id;
      profile.username = response.plainData[0].username;
      profile.name = response.plainData[0].name;
      profile.employeeNumber = response.plainData[0].nip;
      profile.organizationName = response.plainData[0].organizationName;
      profile.isActive = response.plainData[0].isActive;
      profile.email = response.plainData[0].email;
      profile.gradeId = response.plainData[0].gradeId;
      profile.positionId = response.plainData[0].jabatanId;
      profile.gradeName = response.plainData[0].gradeName;
      profile.positionName = response.plainData[0].jabatanName;
      profile.visualImage = response.plainData[0].visualImage;

      return profile;
    })
    .catch(() => {
      return null;
    });
}

export async function getVisualSign(): Promise<string> {
  return client
    .GetVisualSignByUsername({
      store: store,
      data: {
        username: store.state.username,
      },
    })
    .then((response) => {
      return response.plainData?.responseData?.visualImage ?? "";
    })
    .catch(() => {
      return "";
    });
}
