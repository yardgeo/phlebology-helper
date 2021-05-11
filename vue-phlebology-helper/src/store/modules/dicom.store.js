// State initial object
import API from "@/services/api";

const initialState = () => ({
    patients: [],
    studies: [],
    patientIds: [],
    chosenStudy: '',
    chosenSeries: null,
    chosenPatient: '',
    stateUploaded: false,
    segmentData: [],
    markedSlice: [],
    currentSliceNumber: 0,
});


/* Module .store.js */


// VUEX STATE
const state = initialState();
window.state = state;


// VUEX GETTERS
const getters = {
    getSegmentData(state) {
        return state.segmentData;
    },
    getMarkedSlices(state) {
        return state.markedSlice;
    },
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
        if (typeof index === 'undefined') {
            return ;
        }
        await API.get(`studies/${state.studies[index].id}`).then((response) => {
            commit("SELECT_STUDY", response);
        }).catch(e=>{console.log(e);});
    },

    async selectSeries({commit}, index){
        commit("SET_MARKED_SLICE", []);
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

    markSlice({commit}, drawInfo){
        let slices = drawInfo.map(dI => dI.slice);
        commit("SET_MARKED_SLICE", slices);
    },

    async fetchPatients({commit}) {

        await API.get('patient/list').then((response) => {
            console.log(response);
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

    async fetchSegment({commit}, id) {
        await API.get(`dicom/${id}/segment`).then((response) => {
            commit('FETCH_SEGMENT', response);
        }).catch(e=>{console.log(e); return false;});
        return true;
    },

    async fetchStudies({commit}, id) {
        commit('SELECT_STUDY', {});
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
    SET_MARKED_SLICE(state, value) {
        state.markedSlice = value;
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
    FETCH_SEGMENT(state, value) {
        state.segmentData = value;
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
