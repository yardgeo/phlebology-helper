import axios from 'axios';
import router from '../router';
import storage from '@/services/web-storage'
import store from '../store';

const API_URL = process.env.VUE_APP_API_BASE_URL + 'auth/';


class AuthService {


    onLoginSuccess(data) {
        store.commit("User/SET", data);

        if (data.token)
            storage.setAccessToken(data.token);

        // if (data.refreshToken)
        //     storage.setRefreshToken(data.refreshToken);

        if (data.accessExpiresIn) {
            let t = Date.now() + data.accessExpiresIn * 1000;
            storage.setExpiry(t);
        }

        router.push('/');
    }


    checkAccessToken() {
        if (!storage.getAccessToken()
            || !storage.getExpiry()
            || !(Date.now() < storage.getExpiry()))
        {
            if (this.tokenRefresh() !== true)
            {
                this.logout();
                return null;
            }
        }
        return storage.getAccessToken();
    }


    loginEmail({email, password})
    {
        let data =
            {
                email: email,
                password: password
            };
        console.log(data);
        return axios.post(API_URL + 'login/email', data, {params: data})
            .then(response => {
                this.onLoginSuccess(response.data);
                return true;
            }).catch(e=>{console.log(e); return e;});
    }


    tokenRefresh() {
        if (!storage.getRefreshToken()) {
            return false;
        }
        let data = {
            refreshToken: storage.getRefreshToken()
        };

        return axios.post(API_URL + 'token/refresh', data)
            .then(response => {
                this.onLoginSuccess(response.data);
                return true;
            }).catch(()=> {return false;})
    }


    logout() {
        storage.removeAccessToken();
        storage.removeRefreshToken();
        storage.removeExpiry();
        router.push('/sign-in');
        store.dispatch('reset');
    }

    getCode(email) {
        return  axios.post(
            API_URL + 'password/recovery',
            {},
            {
                params: {
                    email: email,
                }
            }).then(() => {
            return true;
        }).catch(e=>{console.log(e); return false;});
    }

    checkCode(data) {
        return axios.post(
            API_URL + 'password/recovery/check',
            {},
            {
                params: data
            }).then(() => {
            return true;
        }).catch(e=>{console.log(e); return false;});
    }

    changePassword(data) {
        return  axios.post(
            API_URL + 'password/change',
            {},
            {
                params: data
            }).then(() => {
            router.push('/sign-in');
            return true;
        }).catch(e=>{console.log(e); return false;});
    }
}


export default new AuthService();
