<template>
    <v-container fluid fill-height>
        <v-layout align-center justify-center>
			<v-flex xs12 sm8 md4>
                <v-card class="elevation-4">
                    <v-card-title class="headline text-truncate">
                        Phlebology Helper
                    </v-card-title>
                    <v-card-text class="pb-0 mb-0">
                        <v-form
                            ref="form"
                            v-model="valid"
                        >
                            <v-text-field
                                label="Эл. почта"
                                name="email"
								autocomplete="username"
                                prepend-icon="mdi-email"
                                :rules="[rules.required, rules.email]"
                                type="email"
                                v-model="signInData.email"
                            />

                            <v-text-field
                                id="password"
                                label="Пароль"
                                name="password"
								autocomplete="current-password"
                                prepend-icon="mdi-lock"
                                :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                                :rules="[rules.required, rules.min]"
                                :type="show ? 'text' : 'password'"
                                v-model="signInData.password"
                                @click:append="show = !show"
                            />
                            <router-link to="/recovery">
                                <p class="caption text-center">Восстановление пароля</p>
                            </router-link>
                        </v-form>
                    </v-card-text>
                    <v-card-actions class="pt-0 mt-0">
                        <v-row>
                            <v-col>
                                <v-btn
                                    block
									color="primary"
                                    large
                                    @click="onSignIn()"
                                >Вход</v-btn>
                            </v-col>
                        </v-row>
                    </v-card-actions>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>
<script>
export default {
	name: "SignIn",
	data: function () {
		return {
			signInData: {
				email: "",
				password: "",
			},
			valid: false,
			show: false,
			rules: {
				required: value => !!value || 'Необходимое поле.',
				min: v => v.length >= 5 || 'Минимум 5 символов',
				email: value => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(value) || 'Неверный формат',
			},
		}
	},
	methods: {
		async onSignIn() {
			let res = await this.$auth.loginEmail(this.signInData);
			if (res !== true) {
				await this.$store.dispatch('Snackbar/set', 'Неверный пароль');
			}
		}
	},
}
</script>
