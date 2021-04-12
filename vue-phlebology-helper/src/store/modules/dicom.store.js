// State initial object
import API from "@/services/api";

const initialState = () => ({
    patients: [],
    studies: [],
    patientIds: [],
    chosenStudy: {},
    chosenPatient: ''
});


/* Module .store.js */


// VUEX STATE
const state = initialState();


// VUEX GETTERS
const getters = {
    getChosenStudy(state) {
        return state.chosenStudy;
    },
    getChosenPatient(state) {
        return state.chosenPatient;
    },
    getPatients(state) {
        return state.patients;
    },
    getStudies(state) {
        return state.studies;
    },
    getPatientsId(state) {
        return state.patientIds;
    },
};


// VUEX ACTIONS
const actions = {
    selectStudy({commit}, index){
        commit("SELECT_STUDY", index);
    },

    selectPatient({commit}, user){
        commit("SET_PATIENT", user);
    },
    async fetchPatients({commit}) {

        await API.get('patient/list').then((response) => {
            commit('PATIENTS', response);
            response.forEach((patient) => commit('PATIENT_ID', patient.id))
        }).catch(e=>{console.log(e);});
    },

    async fetchStudies({commit}, id) {
        console.log(id);
        await API.get(`patient/${id}/studies/list`).then((response) => {
            commit('STUDIES', response);
        }).catch(e=>{console.log(e);});
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
    SELECT_STUDY(state, value) {
        state.chosenStudy = state.studies[value];
    },
    SET_PATIENT(state, value) {
        state.chosenPatient = value;
    },
    PATIENTS(state, value) {
        state.patients = value;
    },
    STUDIES(state, value) {
        state.studies = value;
    },
    PATIENT_ID(state, value) {
        state.patientIds = state.patientIds.concat([value]);
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
