// State initial object
import API from "@/services/api";

const initialState = () => ({
    patients: [],
    studies: [],
    patientIds: [],
    chosenStudy: {},
    chosenSeries: null,
    chosenPatient: '',
    stateUploaded: false,
    currentSliceNumber: 0,
});


/* Module .store.js */


// VUEX STATE
const state = initialState();
window.state = state;


// VUEX GETTERS
const getters = {
    getCurrentSliceNumber(state) {
        return state.currentSliceNumber;
    },
    getChosenStudy(state) {
        return state.chosenStudy;
    },
    getChosenSeries(state) {
        return state.chosenSeries;
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
    async selectStudy({commit}, index){
        await API.get(`studies/${state.studies[index].id}`).then((response) => {
            commit("SELECT_STUDY", response);
        }).catch(e=>{console.log(e);});
    },

    async selectSeries({commit}, index){
        await API.get(`series/${state.chosenStudy.series[index].id}`).then((response) => {
            commit("SELECT_SERIES", response);
        }).catch(e=>{console.log(e);});
    },

    changeCurrentSliceNumber({commit}, number){
        commit("CHANGE_SLICE_NUMBER", number);
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

    async uploadState({commit}, options) {
      await API.post(`series/${options.series_id}/state`, options.state).then(() => {
          commit('UPLOAD_STATE');
      }).catch(e=>{console.log(e); return false;});
      return true;
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
        state.chosenStudy = value;
    },
    SELECT_SERIES(state, value) {
        state.chosenSeries = value;
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
    UPLOAD_STATE(state) {
        state.stateUploaded = true;
    },
    CHANGE_SLICE_NUMBER(state, value) {
      state.currentSliceNumber = value;
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
