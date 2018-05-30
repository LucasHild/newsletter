<template>
    <div class="dashboard" :style="'background-image: url(' + require('@/assets/login-background.jpg') + ')'">
        <Modal v-if="showPreview" title="Preview" @close="showPreview = false">
            <iframe class="preview" style="width: 100%; height: 500px" frameBorder="0" :src="`https://app.mailerlite.com/emails/view/${mailId}`"></iframe>
        </Modal>
        <div class="box">
            <a href="https://app.mailerlite.com/subscribers/view" class="mailerlite-link" target="_blank">Subscribers on Mailerlite</a>
            <h1>Newsletter</h1>

            <input type="text" v-model="subject" placeholder="Subject">
            <input type="text" v-model="introduction" placeholder="Introduction">

            <h2>Neue Artikel auf meinem Blog</h2>
            <ArticlePreview v-for="article in blogArticles" :data="article" :key="article.id" @delete="deleteArticle"/>
            <svg class="add-article" @click="addArticle('blog')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
                <path d="M0 0h24v24H0z" fill="none"/>
            </svg>


            <h2>Top 3 Artikel</h2>
            <ArticlePreview v-for="article in topArticles" :data="article" :key="article.id" @delete="deleteArticle"/>
            <svg class="add-article" @click="addArticle('top')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
                <path d="M0 0h24v24H0z" fill="none"/>
            </svg>

            <p>Fill out this field, if you want to update a campaign, that already exists.</p>
            <input type="text" v-model="campaignId" placeholder="Campaign ID">
            <input type="text" v-model="mailId" placeholder="Mail ID">

            <p v-if="message.visible" :class="{ 'message-error': message.type == 'error', 'message-success': message.type == 'success' }">{{ message.text }}</p>

            <div>
                <p class="button" @click="upload">Upload</p>
                <p v-if="campaignId" @click="send" class="button">Send</p>
            </div>
        </div>
    </div>
</template>

<script>
import Api from '@/Api'
import ArticlePreview from '@/components/ArticlePreview'

export default {
    name: 'dashboard',

    components: { ArticlePreview },

    data() {
        return {
            subject: `Lucas Hild - ${this.getMonthAndYear()}`,
            introduction: '',
            blogArticles: [],
            topArticles: [],
            currentId: 0,
            campaignId: null,
            mailId: null,
            showPreview: false,
            message: {
                visible: false,
                type: null,
                text: null
            }
        }
    },

    methods: {
        addArticle(type) {
            let newArticle = {
                id: this.currentId,
                title: '',
                image: '',
                link: '',
                description: ''
            }

            if (type == 'blog') {
                this.blogArticles.push(newArticle)
            } else {
                this.topArticles.push(newArticle)
            }

            this.currentId++
        },

        deleteArticle(id) {
            this.blogArticles = this.blogArticles.filter(article => article.id != id)
            this.topArticles = this.topArticles.filter(article => article.id != id)
        },

        getMonthAndYear() {
            let date = new Date()
            let month
            let year = date.getUTCFullYear()

            switch (date.getMonth()) {
                case 0:
                    month = 'Januar'
                    break;
                case 1:
                    month = 'Februar'
                    break;
                case 2:
                    month = 'März'
                    break;
                case 3:
                    month = 'April'
                    break;
                case 4:
                    month = 'Mai'
                    break;
                case 5:
                    month = 'Juni'
                    break;
                case 6:
                    month = 'Juli'
                    break;
                case 7:
                    month = 'August'
                    break;
                case 8:
                    month = 'September'
                    break;
                case 9:
                    month = 'Oktober'
                    break;
                case 10:
                    month = 'November'
                    break;
                case 11:
                    month = 'Dezember'
                    break;
            }

            return `${month} ${year}`
        },

        upload() {
            Api.upload(this.campaignId, this.subject, this.introduction, this.blogArticles, this.topArticles)
                .then(request => {
                    this.campaignId = request.data.campaign_id
                    this.mailId = request.data.mail_id
                    this.showPreview = true
                    this.message = {
                        visible: true,
                        text: 'Uploaded successfully!',
                        type: 'success'
                    }
                })
                .catch(e => {
                    this.message = {
                        visible: true,
                        text: e.response.data.error,
                        type: 'success'
                    }
                })
        },

        send() {
            Api.send(this.campaignId)
                .then(request => {
                    this.message = {
                        visible: true,
                        text: 'Sent successfully!',
                        type: 'success'
                    }
                })
                .catch(e => {
                    this.message = {
                        visible: true,
                        text: e.response.data.error,
                        type: 'success'
                    }
                })
        }
    }
}
</script>

<style scoped>
.dashboard {
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
    max-width: 1000px;
    width: 90%;
    margin: auto;
    padding: 20px;
    max-height: 90vh;
    overflow: scroll;
}

.mailerlite-link {
    display: block;
    text-align: right;
}

.add-article {
    background-color: var(--primary-color);
    fill: white;
    width: 50px;
    border-radius: 50%;
    cursor: pointer;
    margin-bottom: 50px;
}

.preview {
    width: 100%;
}

.message-error {
    color: var(--red);
}

.message-success {
    color: var(--green);
}
</style>