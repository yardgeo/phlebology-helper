// State initial object
const initialState = () => ({
    snackbar: false,
    text: null,
});


/* Module .store.js */


// VUEX STATE
const state = initialState();


// VUEX GETTERS
const getters = {};


// VUEX ACTIONS
const actions = {
    reset({commit}) {
        commit('RESET');
    },
    set({commit}, message) {
        commit("MESSAGE", message ? message : "Для выбранных параметров отсутствуют данные");
        commit("SET", true);
    }
};


// VUEX MUTATIONS
const mutations = {
    RESET(state) {
        const newState = initialState();
        Object.keys(newState).forEach(key => {
            state[key] = newState[key]
        });
    },
    SET(state, value) {
        state.snackbar = value;
    },
    MESSAGE(state, value) {
        state.text = value;
    }
};


export default {
    state,
    getters,
    actions,
    mutations
};
