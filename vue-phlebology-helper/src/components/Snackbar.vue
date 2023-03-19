<template>
    <v-snackbar
            v-model="status"
            :multi-line="!isMobile"
            :timeout="6000"
            :vertical="isMobile"
            top
    >
        <p>{{ $store.state.Snackbar.text }}</p>
        <v-btn
                dark
                text
                @click="onClose"
        >Закрыть
        </v-btn>
    </v-snackbar>
</template>
<script>
    export default {
        name: "Snackbar",
        computed:{
            isMobile() {
                return !this.$vuetify.breakpoint.smAndUp;
            },
            status:{
                get(){
                    return this.$store.state.Snackbar.snackbar;
                },
                set(value) {
                    this.$store.commit('Snackbar/SET', value);
                }
            },
        },
        methods: {
            onClose() {
                this.status = false;
            }
        }
    }
</script>