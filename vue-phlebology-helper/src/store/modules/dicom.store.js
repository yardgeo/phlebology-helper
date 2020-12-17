// State initial object
import API from "@/services/api";

const initialState = () => ({
    patients: [],
    patientIds: [],
    chosenPatient: {}
});


/* Module .store.js */


// VUEX STATE
const state = initialState();


// VUEX GETTERS
const getters = {
    getChosenPatient(state) {
        return state.chosenPatient;
    },
    getPatients(state) {
        return state.patients;
    },
    getPatientsId(state) {
        return state.patientIds;
    },
};


// VUEX ACTIONS
const actions = {
    selectPatient({commit}, user){
        commit("SET_PATIENT", user);
    },
    async fetchPatients({commit}) {


        await API.get('patient/list').then((response) => {
            commit('PATIENT_IDS', response);
        }).catch(e=>{console.log(e);});


        state.patientIds.forEach(async function (id) {
            await API.get('patient/' + id).then((response) => {
                console.log(response);
                commit('PATIENT', response)
            }).catch(e=>{console.log(e);});
        });
    },
};


// VUEX MUTATIONS
const mutations = {
    RESET(state) {
        const newState = initialState();
        Object.keys(newState).forEach(key => {
            state[key] = newState[key]
        });
    },
    SET_PATIENT(state, value) {
        state.chosenPatient = value;
    },
    PATIENT_IDS(state, value) {
        state.patientIds = value;
    },
    PATIENT(state, value) {
        state.patients = state.patients.concat([value]);
    }
};


export default {
    state,
    getters,
    actions,
    mutations
};
