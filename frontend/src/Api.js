import axios from 'axios'
import router from '@/router'
import store from '@/store'

export const apiURL = process.env.API_URL || 'http://lanseuo.herokuapp.com/api'

let Api = () => {
    return axios.create({
        baseURL: apiURL,
        headers: {
            Authorization: `JWT ${store.state.token}`
        }
    })
}

export default {
    login(username, password) {
        console.log(Api());

        return Api().post('login', { username, password })
    },

    getBlogArticles() {
        return axios.get('https://blog.lucas-hild.de/api/posts')
    },

    upload(campaignId, subject, introduction, blogArticles, topArticles) {
        return Api().post('newsletter/upload', { campaignId, subject, introduction, blogArticles, topArticles })
    },

    send(campaignId) {
        return Api().post('newsletter/send', { campaignId })
    }
}