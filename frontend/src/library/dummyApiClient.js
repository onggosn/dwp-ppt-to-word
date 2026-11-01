function createResponse(data) {
  return new Promise((resolve) => {
    resolve({ data });
  });
}
const client = {
  getKeySHA256() {
    return createResponse({
      johnCena: 7.076222136955885e306,
      undertaker: "5944525062998229",
      randyOrton:
        "3f8911aa6da1e0807f97e6d02ed1af55e415e4ee696fca7f55c2978f6ac55dfa",
    });
  },

  // {json: "oJoELuzPyUs4oT+7SE96WbZ6/+SAdgiTUei+Ro3TT9hOI3cSYIdwvOPjl5zahUv6"}
  login() {
    return createResponse({
      tranRoleMenu: null,
      user: {
        id: 0,
        username: null,
        name: null,
        nip: null,
        organizationName: null,
        isActive: false,
        email: null,
        isApproved: 0,
        createdDate: "0001-01-01T00:00:00",
        lastModifiedDate: "0001-01-01T00:00:00",
        userIdApproval: null,
        gradeId: null,
        jabatanId: null,
        visualImage: null,
      },
      token: "a3e724e6-6cb8-46e0-a09e-6d1104889766",
      exp_date: "7/9/2022 2:29:06 AM",
      mUserView: {
        id: 7460,
        username: "DMPdemo",
        name: "DMP demo",
        nip: "90190",
        organizationName: "DPSI.DIV SUMBER DAYA PENGEMBANGAN SI",
        isActive: true,
        email: "DMPdemo@bi.go.id",
        isApproved: 1,
        createdDate: "2022-03-30T10:07:12.06",
        lastModifiedDate: "2022-03-30T10:07:12.06",
        userIdApproval: 6053,
        gradeId: 26,
        jabatanId: 1,
        gradeName: "Pelaksana",
        jabatanName: "Analis",
        listUserViewModels: null,
      },
    });
  },

  // {json: "UVi8gPTEQUAvHS94qZ1Ud1RhV1OJjRGixhT+zi8/2G4="}
  getNotificationLimitViewAndTotalNotifByUsername() {
    return createResponse(
      "lfPEZ+90rMOVf5YJmXNAT/pcJuEG3Y6SSGbfrRxXL1hPfiWdMjugdoi9Nu+y24Vrd7zMhvchAsl8Jx/TNs0npg=="
    );
  },

  // {json: "UVi8gPTEQUAvHS94qZ1Ud1RhV1OJjRGixhT+zi8/2G4="}
  getWorspaceInProgressByTaskMember() {
    return createResponse("+m2MgF07PibPH1IPk3RSUw==");
  },

  // {json: "UVi8gPTEQUAvHS94qZ1Ud1RhV1OJjRGixhT+zi8/2G4="}
  getWorspaceDoneByTaskMember() {
    return createResponse("+m2MgF07PibPH1IPk3RSUw==");
  },
};

export default client;
