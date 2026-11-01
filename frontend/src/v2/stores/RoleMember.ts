import client from "@v2/library/Api";
/* eslint-disable */
export default {
  namespaced: true,
  state: {
    roleMembers: [],
  },
  getters: {
    getRoleMembers: (state: any) => {
      return state.roleMembers;
    },
  },
  mutations: {
    setRoleMembers(state: any, newValue: any) {
      state.roleMembers = newValue;
    },
  },
  actions: {
    //dummy
    async getRoleMember({ commit }, id: number) {
      return client({}).post("/DashboardAdmin/AddBPRoleMemberByRoleId", {
        id: id,
      });
    },
    async storeRoleMember({ commit }, req: any) {
      return client({}).post("/DashboardAdmin/AddBPRoleMemberByRoleId", req);
    },
  },
};
