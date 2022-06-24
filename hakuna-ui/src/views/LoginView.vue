<template>
    <div class="login">
        <el-row>
          <el-col :span="12">
            <div class="main">
              <img id="logo" alt="logo" width="200px" height=auto src="../assets/logo.png" />
              <div class="main-desc">
                <h2>接口测试平台</h2>
                <p>包含项目管理、模块用例管理、任务执行、测试报告等功能</p>
              </div>
            </div>
          </el-col>
          <el-col :span="12">
            <LoginV msg="Welcome to Hakuna" />
          </el-col>
        </el-row>
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
.login {
  width: 100%;
  margin: 200px auto;
}
.main{
  float: right;
  margin-right: 20px;
  justify-content: center;
  align-items: center;
}

#logo {
  width: 200px;
  height: auto;
}

</style>