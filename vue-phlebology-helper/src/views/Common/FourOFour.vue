<template>
    <v-container
            class="text-center"
            fill-height
            style="height: calc(100vh - 58px);"
    >
        <v-row align="center">
            <v-col>
                <h1 class="display-2 primary--text">Ошибка 404</h1>
                
                <p>Страницы, которую вы ищите не существует.</p>
                
                <v-btn
                        to='/'
                        color="primary"
                        outlined
                >
                    На главную!
                </v-btn>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    export default {
        name: 'FourOFour',
        created () {
            this.$ssrContext && this.$ssrContext.res.status(404)
        },
    }
</script>