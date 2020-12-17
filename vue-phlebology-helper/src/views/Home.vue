<template>
  <v-container fluid full-height>
    <v-toolbar>
      <v-toolbar-title>Просмоторщик</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-row>
        <v-col>
          <PatientPicker></PatientPicker>
        </v-col>
      </v-row>
    </v-toolbar>
    <img :src="src" alt="">
  </v-container>
</template>

<script>
  import PatientPicker from "../components/Pickers/PatientPicker"
  import axios from 'axios';
  import AuthService from '@/services/auth.service';

  export default {
    name: "Dashboard",
    components: {PatientPicker},
    data() {
      return {
        // empty image
        src: ""
      }
    },
    created() {
      let config = {
        // example url
        url: process.env.VUE_APP_API_BASE_URL+'dicom/preview',
        headers: { Authorization: 'Bearer ' + AuthService.checkAccessToken()},
        method: 'GET',
        responseType: 'blob'
      };
      axios(config)
              .then((response) => {
                let reader = new FileReader();
                reader.readAsDataURL(response.data);
                reader.onload = () => {
                  this.src = reader.result;
                }
              });
    }
  }
</script>

<style scoped>
  ::-webkit-scrollbar {
    width: 0;
    background: transparent;
  }
  ::-webkit-scrollbar-thumb {
    background: transparent;
  }
</style>
