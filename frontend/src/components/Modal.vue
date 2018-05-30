<template>
    <transition name="modal">
        <div class="modal-mask">
        <div class="modal-wrapper">
            <div class="modal-container">

            <div class="modal-header">
                <span>{{ title }}</span>
                <span class="close" @click="$emit('close')">
                    <svg fill="white" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                        <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                        <path d="M0 0h24v24H0z" fill="none"/>
                    </svg>
                </span>

            </div>

            <div class="modal-body">
                <slot></slot>
            </div>

            </div>
        </div>
        </div>
    </transition>
</template>

<script>
export default {
    name: 'modal',

    props: ['title'],

    created() {
        var vm = this
        window.addEventListener('keydown', function (e) {
            // ESC key
            if (e.keyCode == 27) {
                vm.$emit('close')
            }
        })
    }
}
</script>

<style scoped>
.modal-mask {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: table;
    transition: opacity 0.3s ease;
}

.modal-wrapper {
    display: table-cell;
    vertical-align: middle;
}

.modal-container {
    max-width: 750px;
    width: 95%;
    margin: 0px auto;
    border: 0.5px solid rgba(125, 125, 125, 0.15);
    box-shadow: 1px 1px 0.5px rgba(231, 231, 231, 0.54);
    border-radius: 5px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
    transition: all 0.3s ease;
    font-family: Helvetica, Arial, sans-serif;
}

.modal-header {
    width: 100%;
    background: var(--primary-color);
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    color: white;
    padding: 15px 20px;
    -webkit-box-sizing: border-box; /* Safari/Chrome, other WebKit */
    -moz-box-sizing: border-box; /* Firefox, other Gecko */
    box-sizing: border-box; /* Opera/IE 8+ */
}

.close {
    float: right;
    cursor: pointer;
}

.modal-body {
    padding: 15px 20px;
    background: white;
}

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter {
    opacity: 0;
}

.modal-leave-active {
    opacity: 0;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
    -webkit-transform: scale(1.1);
    transform: scale(1.1);
}
</style>
