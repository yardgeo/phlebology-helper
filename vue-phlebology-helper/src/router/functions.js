import AuthService from '@/services/auth.service';
import store from '../store';

async function onLoggedIn(next) {
    next();
}
export default {
    updatePageTitleAndMeta(document, to, next) {
        const nearestWithTitle = to.matched.slice().reverse().find(r => r.meta && r.meta.title);
        const nearestWithMeta = to.matched.slice().reverse().find(r => r.meta && r.meta.metaTags);
        if (nearestWithTitle) document.title = nearestWithTitle.meta.title;
        Array.from(document.querySelectorAll('[data-vue-router-controlled]')).map(el => el.parentNode.removeChild(el));
        if (!nearestWithMeta) return next();
        nearestWithMeta.meta.metaTags.map(tagDef => {
            const tag = document.createElement('meta');
            Object.keys(tagDef).forEach(key => {
                tag.setAttribute(key, tagDef[key]);
            });
            tag.setAttribute('data-vue-router-controlled', '');
            return tag;
        }).forEach(tag => document.head.appendChild(tag));
        next();
    },

    async handleUnauthorizedAccess(to, next) {
        const isPublic = !!to.meta.public;
        if (isPublic) {
            next();
        } else {
            let role = store.getters['User/getRole'];
            if (role) {
                await onLoggedIn(next);
            } else {
                const isLoggedIn = !!AuthService.checkAccessToken();
                if (isLoggedIn) {
                    await onLoggedIn(next);
                } else {
                    next('/sign-in');
                }
            }
        }
    },
};

