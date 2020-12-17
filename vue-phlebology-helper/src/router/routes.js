const routes =
    [
        {
            path: '/',
            name: 'Dashboard',
            components: {
                appbar: null,
                navbar: null,
                footer: null,
                content: () => import('../views/Home'),
            },
            meta: {
                title: 'Phlebology helper'
            }
        },
        {
            path: '/sign-in',
            name: 'Sign In',
            components: {
                appbar: null,
                navbar: null,
                footer: null,
                content: () => import('../views/Common/SignIn'),
            },
            meta: {
                public: true,
                title: 'Phlebology helper - Вход'
            }
        },
        {
            path: '/recovery',
            name: 'Recovery',
            components: {
                appbar: null,
                navbar: null,
                footer: null,
                content: () => import('../views/Common/Recovery'),
            },
            meta: {
                public: true,
                title: 'Phlebology helper - Восстановление пароля'
            }
        },
        {
            path: '/404',
            name: 'NotFound',
            components: {
                appbar: null,
                navbar: null,
                footer: null,
                content: () => import('../views/Common/FourOFour'),
            },
            meta: {
                public: true,
                title: 'Phlebology helper - 404',
            }
        },
        {
            path: '*',
            redirect: '/404'
        }
    ];

export default routes
