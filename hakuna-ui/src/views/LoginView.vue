<template>
    <div class="login">
        <img alt="logo" width="200px" height=auto src="../assets/logo.png" />
        <LoginV msg="Welcome to Hakuna" />
    </div>
</template>

<script>
// @ is an alias to /src
import LoginV from "@/components/Login.vue";

export default {
    name: "LoginView",
    components: {
        LoginV,
    },
};
</script>

<style scoped>
.login img{
    width: 220px;
    height: auto;
    margin: 50px auto 50px;
    display: flex;
    justify-content: center;
    align-items: center;
}

</style>