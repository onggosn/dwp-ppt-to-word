export default {
  namespaced: true,
  state: {
    progress: 0,
  },
  getters: {
    getProgress: (state: any) => {
      return state.progress;
    },
  },
  mutations: {
    setProgress(state, value) {
      state.progress = value;
    },
  },
  actions: {
    updateProgress({ commit }, value) {
      commit("setProgress", value);
    },
  },
};
