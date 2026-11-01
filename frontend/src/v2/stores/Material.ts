import client from "@v2/library/Api";

export default {
  namespaced: true,
  state: {},
  getters: {},
  mutations: {},
  actions: {
    /* eslint-disable */
    async getListAccessMemberPresentationMaterial({ commit }, request:any) {
      return client({}).post("/Event/getListAccessMemberPresentationMaterial", request);
    },
    async searchEventPresentationMaterialByUsernameAndGroupId({commit}, request:any){
      return client({}).post("/MUser/SearchEventPresentationMaterialByUsernameAndGroupId", request)
    },
    async searchEventPresentationMaterialOrgParByUsernameAndGroupId({commit}, request:any){
      return client({}).post("/MUser/SearchEventPresentationMaterialOrgParByUsernameAndGroupId", request)
    },
    async searchEventPresentationMaterialByUsername({commit}, request:any){
      return client({}).post("/MUser/SearchUserEventPresentationMaterialByUsername", request).then((res: any) => {
        return new Promise((resolve) => {
          return resolve(res.map((elm: any) => {
            elm.department = elm.jabatanSatker;
            elm.inputName = elm.value;
            return elm;
          }));
        });
      })
    },
    async addMemberPresentationMaterial({commit}, request: any){
      return client({}).post("/Event/addMemberPresentationMaterial", request)
    },
    async deleteMemberPresentationMaterial({ commit }, request:any) {
      return client({}).post("/Event/deleteMemberPresentationMaterial", request);
    },
    async updateMemberPresentationMaterial({ commit }, request) {
      return client({}).post("/Event/updateMemberPresentationMaterial", request);
    },
    // meeting result
    async getListAccessMemberHasilPembahasan({ commit }, request) {
      return client({}).post("/Event/getListAccessMemberHasilPembahasan", request);
    },
    async addMemberHasilPembahasan({ commit }, request) {
      return client({}).post("/Event/addMemberHasilPembahasan", request);
    },
    async deleteMemberHasilPembahasan({ commit }, request) {
      return client({}).post("/Event/deleteMemberHasilPembahasan", request);
    },
    async updateMemberHasilPembahasan({ commit }, request) {
      return client({}).post("/Event/updateMemberHasilPembahasan", request);
    }, 
  },
};
