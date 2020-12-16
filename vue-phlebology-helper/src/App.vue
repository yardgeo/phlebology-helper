<template>
  <v-app>
    <router-view name="appbar"/>
    <router-view name="navbar"/>
    <router-view name="footer"/>
    <v-main>
      <Snackbar></Snackbar>
      <router-view name="content" :key="$route.fullPath"/>
    </v-main>
  </v-app>
</template>
<script>
  import Snackbar from "./components/Snackbar";

  export default {
    components: {Snackbar },
    data: () => ({
      name: "App",
    })
  }
</script>
