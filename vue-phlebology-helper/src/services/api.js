import axios from 'axios';
import AuthService from '@/services/auth.service';

const API = axios.create({
    baseURL: process.env.VUE_APP_API_BASE_URL,
});

API.interceptors.request.use(function (config) {
    config.headers.Authorization = 'Bearer ' + AuthService.checkAccessToken();
    return config;
}, function(error) {
    console.log('Request Error:');
    console.log(error);
});

API.interceptors.response.use(function (response) {
    if (response.status === 200) {
        return response.data;
    } else {
        console.log(response.status);
        return null;
    }
}, function (error) {
    console.log('Response Error:');
    console.log(error);
});

export default API;
