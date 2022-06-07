<template>
    <div id="loginform">
        <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
            <el-form-item label="用户名" prop="name">
                <el-input v-model="ruleForm.name"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="pass">
                <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="确认密码" prop="checkPass">
                <el-input type="password" v-model="ruleForm.checkPass" autocomplete="off"></el-input>
            </el-form-item>
            
            <el-form-item>
                <el-button type="primary" @click="submitForm('ruleForm')">登陆</el-button>
                <el-button @click="resetForm('ruleForm')">重置</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
export default {
    name: 'LoginV',
    data() {
        var validatePass = (rule, value, callback) => {
            if (value === ''){
                callback(new Error('请输入密码'))
            }else {
                if (this.ruleForm.checkPass !== ''){
                    this.$refs.ruleForm.validateField('checkPass');
                }
                callback();
            }
        };
        var validatePass2 = (rule, value, callback) => {
            if (value === ''){
                callback(new Error('请再次输入密码'));
            } else if (value !== this.ruleForm.pass) {
                callback(new Error('两次输入密码不一致'));
            } else {
                callback();
            }
        };
        return {
            ruleForm: {
                name: '',
                pass: '',
                checkPass: ''
            },
            rules: {
                name: [
                    { required: true, message: '请输入用户名', trigger: 'blur' },
                    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
                ],
                pass: [
                    { required: true, message: '请输入密码', trigger: 'blur'},
                    { validator: validatePass, trigger: 'blur'}
                ],
                checkPass: [
                    { required: true, message: '请输入密码', trigger: 'blur'},
                    { validator: validatePass2, trigger: 'blur'}
                ]
            }
        };
    },
    methods: {
        submitForm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    // alert('submit!');
                    this.$axios({
                        method: "post",
                        url: "/users/login",
                        Headers: {
                            "Content-Type": "multipart/form-data"
                        },
                        data: {
                            "username": this.ruleForm["name"],
                            "password": this.ruleForm["pass"],
                            "confirm_password": this.ruleForm["checkPass"]
                        }
                    }).then((respoonse)=> {
                        if (respoonse.data.success) {
                            // 保存token
                            window.localStorage.setItem("token", respoonse.data.item.token);
                            // 保存用户名
                            window.localStorage.setItem("username", respoonse.data.item.username);
                            // 弹出提示
                            this.$message.success("登陆成功");
                            // 跳转页面
                            this.$router.push("/index");
                        } else if (!respoonse.data.success) {
                            this.$message.error(respoonse.data.error.msg)
                        }
                        console.log(respoonse);
                    }).catch(error => {
                        console.log("登陆失败", error);
                    });
                } else {
                    console.log('error submit!!');
                    return false;
                }
            });
        },
        resetForm(formName) {
            this.$refs[formName].resetFields();
        }
    }
}
</script>

<style scoped lang="scss">
#loginform {
    display: flex;
    width: 400px;
    margin: 0 auto;
    justify-content: center;
    align-items: center;
}
</style>