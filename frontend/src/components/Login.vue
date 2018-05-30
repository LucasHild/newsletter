<template>
    <div class="login" :style="'background-image: url(' + require('@/assets/login-background.jpg') + ')'">
        <div class="box">
            <h1>Login</h1>
            <form @submit.prevent="login">
                <input v-model="username" type="text" placeholder="username">
                <input v-model="password" type="password" placeholder="password">
                <p class="message">{{ message }}</p>
                <input type="submit" value="Login">
            </form>
        </div>
    </div>
</template>

<script>
import Api from '@/Api'

export default {
    name: 'login',

    data() {
        return {
            username: '',
            password: '',
            message: null
        }
    },

    methods: {
        login() {
            Api.login(this.username, this.password)
                .then(response => {
                    this.$store.dispatch('setToken', response.data.token)
                    this.$router.push({ name: 'Dashboard' })
                })
                .catch(e => {
                    this.message = e.response.data.error
                })
        }
    }
}
</script>

<style scoped>
.login {
    width: 100vw;
    height: 100vh;
    background-position: center;
    background-size: cover;
    background-repeat: no-repeat;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.box {
    background-color: white;
    max-width: 500px;
    width: 90%;
    margin: auto;
    padding: 20px;
}

input[type="submit"] {
    background: var(--primary-color);
    color: white;
    cursor: pointer;
}

.message {
    color: var(--red);
}
</style>