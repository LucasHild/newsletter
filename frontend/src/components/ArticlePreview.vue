<template>
    <div class="article-preview">
        <Modal v-if="showModal" title="Edit article" @close="showModal = false">
            <input v-model="data.title" placeholder="Title">
            <input v-model="data.image" placeholder="Link to Image">
            <input v-model="data.link" placeholder="Link">
            <textarea v-model="data.description" placeholder="Description"/>

                            <p>{{ noAutoFillIn }}</p>

            <div v-if="noAutoFillIn == undefined">
                <h4>Auto-Fill-In for Blog Articles</h4>
                <p class="blog-suggestion" v-for="blogArticle in lastBlogArticles" @click="setDataFromBlogArticle(blogArticle)" :key="blogArticle.permalink">
                    {{ blogArticle.title }}
                </p>
            </div>

            <p @click="saveModal" class="button">Save</p>
        </Modal>

        <div class="grid">
            <div class="left" v-if="data.image" :style="'background-image: url(' + data.image + ')'"></div>
            <div class="left" v-else :style="'background-image: url(' + require('@/assets/no-image.jpg') + ')'"></div>
            <div class="right">
                <h3>{{ data.title || 'No title' }}</h3>
                <p>{{ data.description || 'No description' }}</p>
                <a v-if="data.link" class="visit-button button" :href="data.link" target="_blank">Visit</a>
                <div class="icons">
                    <svg class="edit-icon" @click="showEditModal" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                        <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                        <path d="M0 0h24v24H0z" fill="none"/>
                    </svg>
                    <svg class="delete-icon" @click="deleteArticle" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                        <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
                        <path d="M0 0h24v24H0z" fill="none"/>
                    </svg>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Api from '@/Api'

export default {
    name: 'article-preview',

    props: ['data', 'no-auto-fill-in'],

    data() {
        return {
            showModal: true,
            lastBlogArticles: [],
        }
    },

    created() {
        Api.getBlogArticles()
            .then(response => {
                this.lastBlogArticles = response.data.slice(0, 3)
            })

    },

    methods: {
        showEditModal() {
            this.showModal = true
        },

        saveModal() {
            this.showModal = false
        },

        deleteArticle() {
            this.$emit('delete', this.data.id)
        },

        setDataFromBlogArticle(blogArticle) {
            this.data.title = blogArticle.title
            this.data.image = 'https://blog.lucas-hild.de' + blogArticle.image
            this.data.link = 'https://blog.lucas-hild.de/' + blogArticle.permalink
            this.data.description = blogArticle.description
        }
    }
}
</script>

<style scoped>
.article-preview {
    min-height: 200px;
    margin-bottom: 25px;
}

.grid {
    display: grid;
    grid-template-columns: 310px auto;
    grid-template-columns: 1fr 2fr;
    grid-column-gap: 20px;
    min-height: 200px;
}

.left {
    height: 100%;
    background-position: center;
    background-size: cover;
    background-repeat: no-repeat;
}

.right {
    position: relative;
}

.visit-button:hover {
    color: rgb(196, 196, 196);
}

.icons {
    position: absolute;
    top: 20px;
    right: 20px;
}

.edit-icon:hover {
    cursor: pointer;
    fill: var(--primary-color);
}

.delete-icon:hover {
    cursor: pointer;
    fill: var(--red);
}

.blog-suggestion {
    cursor: pointer;
}

.blog-suggestion:hover {
    color: var(--primary-color);
}
</style>