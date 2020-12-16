<template>
	<v-container fluid fill-height>
		<v-layout align-center justify-center>
			<v-flex xs12 sm8 md4>
				<v-card class="elevation-4">
					<v-card-text class="pb-0 mb-0">
						<v-form v-model="valid1">
							<v-tab-transition>
								<v-text-field
									ref="email"
									label="Эл. почта"
									autocomplete="username"
									v-show="!firstStep && !secondStep"
									prepend-icon="mdi-email"
									:rules="[rules.required, rules.email]"
									type="email"
									v-model="email"
								></v-text-field>
							</v-tab-transition>
						</v-form>
						<v-form v-model="valid2">
							<v-tab-transition>
								<v-text-field
									label="Код"
									autocomplete="one-time-code"
									v-show="firstStep && !secondStep"
									:rules="[rules.required, rules.code]"
									v-model="code"
								></v-text-field>
							</v-tab-transition>
						</v-form>
						<v-form v-model="valid3">
							<v-text-field
								autocomplete="username"
								type="username"
								v-show="false"
							/>
							<v-tab-reverse-transition>
								<v-text-field
									label="Новый пароль"
									name="new-password"
									autocomplete="new-password"
									v-show="!firstStep && secondStep"
									v-model="password1"
									prepend-icon="mdi-lock"
									:append-icon="show ? 'mdi-eyeOff' : 'mdi-eye'"
									:rules="[rules.required, rules.min]"
									:type="show ? 'text' : 'password'"
									@click:append="show = !show"
								/>
							</v-tab-reverse-transition>
							<v-tab-reverse-transition>
								<v-text-field
									label="Повторите пароль"
									name="confirm-new-password"
									autocomplete="new-password"
									v-model="password2"
									v-show="!firstStep && secondStep"
									prepend-icon="mdi-lock"
									:append-icon="show2 ? 'mdi-eyeOff' : 'mdi-eye'"
									:rules="[rules.required, rules.min, rules.passwordsMatch]"
									:type="show2 ? 'text' : 'password'"
									@click:append="show2 = !show2"
								/>
							</v-tab-reverse-transition>
						</v-form>

					</v-card-text>
					<v-card-actions class="pt-0 mt-0">
						<v-row>
							<v-col cols="12">
								<v-fade-transition>
									<v-btn
										v-show="!firstStep && !secondStep"
										:loading="checkingEmail"
										block
										:disabled="!valid1"
										large
										@click.stop="onGetCode()"
										color="primary"
									>Получить код</v-btn>
								</v-fade-transition>
								<v-fade-transition>
									<v-btn
										v-show="firstStep && !secondStep"
										:loading="resetting"
										:disabled="!valid2"
										block
										large
										@click.stop="onCheck()"
										color="primary"
									>Проверить код</v-btn>
								</v-fade-transition>
								<v-fade-transition>
									<v-btn
										v-show="!firstStep && secondStep"
										:loading="resetting"
										block
										:disabled="!valid3"
										large
										@click.stop="onReset()"
										color="primary"
									>Обновить пароль</v-btn>
								</v-fade-transition>
							</v-col>
						</v-row>
					</v-card-actions>
				</v-card>
			</v-flex>
		</v-layout>
	</v-container>
</template>
<script>
import axios from "axios";
export default {
	name: "Recovery",
	data: function() {
		return {
			valid1: true,
			valid2: true,
			valid3: true,
			checkingEmail: false,
			resetting: false,
			email: "",
			code: '',
			firstStep: false,
			secondStep: false,
			password1: '',
			password2: '',
			rules: {
				required: value => !!value || 'Необходимое поле ',
				min: v => v.length >= 4 || 'Минимум 4 знака',
				email: value => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(value) || 'Неверный формат',
				code: value => /^[0-9]{6}$/.test(value) || 'Код состоит из 6 цифр',
				passwordsMatch: value => this.password1 === value || "Пароли не совпадают"
			},
			show: false,
			show2: false,
		}
	},
	methods: {
		onGetCode() {
			this.checkingEmail = true;
			setTimeout(async ()=>{
				try {
					await axios.post(
						process.env.VUE_APP_API_BASE_URL+'auth/password/recovery',
						{},
						{
							params: {
								email: this.email,
							}
						});
					this.firstStep = true;
					this.secondStep = false;
				} catch (e) {
					this.$store.dispatch("Snackbar/set", "Такого пользователя нет в системе");
				}
				this.checkingEmail = false;
			},0);
		},
		onCheck() {
			this.checkingEmail = true;
			setTimeout(async ()=>{
				try {
					await axios.post(
						process.env.VUE_APP_API_BASE_URL+'auth/password/recovery/check',
						{},
						{
							params: {
								email: this.email,
								recoveryCode: this.code
							}
						});
					this.firstStep = false;
					this.secondStep = true;
				} catch (e) {
					this.$store.dispatch("Snackbar/set", "Неверный код");
				}
				this.checkingEmail = false;
			},0);
		},
		onReset() {
			this.checkingEmail = true;
			setTimeout(async ()=>{
				try {
					await axios.post(
						process.env.VUE_APP_API_BASE_URL+'auth/password/change',
						{},
						{
							params: {
								email: this.email,
								recoveryCode: this.code,
								newPassword: this.password2
							}
						});
					this.$router.push('/sign-in');
				} catch (e) {
					this.$store.dispatch("Snackbar/set", "Произошла ошибка. Попробуйте еще раз.");
				}
				this.checkingEmail = false;
			},0);
		}
	}
}
</script>
