// State initial object
import API from "@/services/api";

const initialState = () => ({
	accessExpiresIn: null,
	email: null,
	family_name: null,
	first_name: null,
	role: null,
	token: null
});


/* Module .store.js */


// VUEX STATE
const state = initialState();


// VUEX GETTERS
const getters = {
	getRole(state) {
		return state.role;
	}
};


// VUEX ACTIONS
const actions = {
	reset({commit}) {
		commit('RESET');
	},
	async getUserInfo({commit}) {
		API.get('user/info').then(response => {
			if (response) {
				commit('SET', response);
			}
		}).catch(error=>{
			console.log(error);
		})
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
	SET(state, data) {
		state.accessExpiresIn = data.accessExpiresIn;
		state.email = data.email;
		state.family_name = data.family_name;
		state.first_name = data.first_name;
		state.role = data.role;
		state.token = data.token;
	}
};


export default {
	state,
	getters,
	actions,
	mutations
};