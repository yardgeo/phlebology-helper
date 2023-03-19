import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify);

import ru from 'vuetify/es5/locale/ru';

export default new Vuetify({
    lang: {
        locales: { ru },
        current: 'ru',
    },
    theme: {
        dark: true,
        themes: {
            dark: {
                primary: '#6472f3',
                secondary: '#000000',
                accent: '#ff0030',
                error: '#800018',
                info: '#002733',
                success: '#006180',
                warning: '#33000a',
            },
        },
    },
});
