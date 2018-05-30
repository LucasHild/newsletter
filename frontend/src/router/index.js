import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Dashboard from '@/components/Dashboard'
import store from '@/store'

Vue.use(Router)
require('@/assets/style.css')

export default new Router({
    routes: [
        {
            path: '/login',
            name: 'Login',
            component: Login
        },
        {
            path: '/',
            name: 'Dashboard',
            component: Dashboard,
            beforeEnter: (to, from, next) => navigationGuard(to, from, next)
        }
    ]
})

let navigationGuard = (to, from, next) => {
    if (store.state.isUserLoggedIn) {
        return next()
    } else {
        return next({
            name: 'Login'
        })
    }
}