<template>
  <el-card class="box-card">
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane name="login" id="login-tab">
        <span slot="label" class="tabClass">登 陆</span>
        <div id="loginform">
          <el-form
            :model="loginForm"
            :rules="rules"
            ref="loginForm"
            label-width="100px"
            label-position="left"
          >
            <el-form-item label="用户名" prop="username">
              <el-input v-model="loginForm.username"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input
                type="password"
                v-model="loginForm.password"
                autocomplete="off"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitLogin('loginForm')"
                >登陆</el-button
              >
              <el-button @click="resetForm('loginForm')">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-tab-pane>
      <el-tab-pane name="register" id="register-tab">
        <span slot="label" class="tabClass">注 册</span>
        <div id="registerform">
          <el-form
            :model="registerForm"
            :rules="rules"
            ref="registerForm"
            label-width="100px"
            label-position="left"
          >
            <el-form-item label="用户名" prop="username">
              <el-input v-model="registerForm.username"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input
                type="password"
                v-model="registerForm.password"
                autocomplete="off"
              ></el-input>
            </el-form-item>
            <el-form-item label="确认密码" prop="confirm_password">
              <el-input
                type="password"
                v-model="registerForm.confirm_password"
                autocomplete="off"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitRegister('registerForm')"
                >注册</el-button
              >
              <el-button @click="resetForm('registerForm')">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-tab-pane>
    </el-tabs>
  </el-card>
</template>

<script>
import UserApi from "../request/user";

export default {
  name: "LoginV",
  data() {
    var validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        callback();
      }
    };
    var validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.registerForm.password) {
        callback(new Error("两次输入密码不一致"));
      } else {
        callback();
      }
    };
    return {
      activeName: "login",
      loginForm: {
        username: "admin",
        password: "123456",
      },
      registerForm: {
        username: "",
        password: "",
        confirm_password: "",
      },
      rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
          {
            min: 3,
            max: 20,
            message: "长度在 3 到 20 个字符",
            trigger: "blur",
          },
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          { validator: validatePass, trigger: "blur" },
        ],
        confirm_password: [
          { required: true, message: "请输入确认密码", trigger: "blur" },
          { validator: validatePass2, trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    },
    submitLogin(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // alert('submit!');
          // this.$axios({
          //     method: "post",
          //     url: "/users/login",
          //     Headers: {
          //         "Content-Type": "multipart/form-data"
          //     },
          //     data: {
          //         "username": this.ruleForm["name"],
          //         "password": this.ruleForm["pass"],
          //     }
          // }).then((respoonse)=> {
          //     if (respoonse.data.success) {
          //         // 保存token
          //         window.localStorage.setItem("token", respoonse.data.item.token);
          //         // 保存用户名
          //         window.localStorage.setItem("username", respoonse.data.item.username);
          //         // 弹出提示
          //         this.$message.success("登陆成功");
          //         // 跳转页面
          //         this.$router.push("/index");
          //     } else if (!respoonse.data.success) {
          //         this.$message.error(respoonse.data.error.msg)
          //     }
          //     console.log(respoonse);
          // }).catch(error => {
          //     console.log("登陆失败", error);
          // });
          UserApi.login(this.loginForm).then((resp) => {
            if (resp.success === true) {
              sessionStorage.token = resp.item.token;
              sessionStorage.user = resp.item.username;
              this.$router.push({path: "/main"})
              this.$message.success("登陆成功！");
            } else {
              this.$message.error(resp.error.msg);
            }
          });
        } else {
          return false;
        }
      });
    },

    submitRegister(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          UserApi.register(this.registerForm).then((resp) => {
            if (resp.success === true) {
              this.$message.success("注册成功！");
            } else {
              this.$message.error(resp.error.msg);
            }
          });
        } else {
          return false;
        }
      });
    },

    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
  },
};
</script>

<style scope lang="scss">
.box-card {
  width: 500px;
  float: left;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
}

#loginform,
#registerform {
  width: 400px;
  margin: 0 auto;
}

.tabClass {
  display: block;
  font-size: 16px;
  width: 210px;
}
</style>
