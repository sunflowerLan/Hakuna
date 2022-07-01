<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    :before-close="closeDialog"
    class="moduleDialog"
    width="500px"
  >
    <el-form
      :model="moduleForm"
      :rules="rules"
      ref="ruleForm"
      label-width="100px"
    >
      <el-form-item label="项目" prop="name">
        <el-input v-model="projectName" disabled></el-input>
      </el-form-item>
      <el-form-item label="父节点" v-if="parentObj.label !== ''">
        <el-input v-model="parentName" disabled></el-input>
      </el-form-item>
      <el-form-item label="名称" prop="name">
        <el-input v-model="moduleForm.name"></el-input>
      </el-form-item>
      <el-form-item style="text-align: right">
        <el-button @click="closeDialog">取消</el-button>
        <el-button type="primary" @click="submitForm('ruleForm')"
          >确定</el-button
        >
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script>
import ModuleApi from "../../request/module";

export default {
  name: "ModuleDialog",
  props: ["projectId", "projectLabel", "rootId", "parentObj"],
  components: {},
  data() {
    return {
      showTitle: "",
      dialogVisible: true,
      projectName: this.projectLabel,
      parentName: this.parentObj.label,
      moduleForm:{
        name:"",
        project_id: 0,
        parent_id: 0,
      },
      rules: {
        name: [
          { required: true, message: "请输入模块的名称", trigger: "blur" },
        ],
      }
    };
  },
  mounted() {
    this.moduleForm.project_id = this.projectId
    if (this.rootId == true) {
      this.showTitle = "创建根节点"
    } else {
      this.showTitle = "创建子节点"
      this.moduleForm.parent_id = this.parentObj.id
    }
  },

  methods: {
    // 关闭模块编辑页面
    closeDialog() {
      this.$emit("cancel", {});
    },

    // 创建/编辑模块
    submitForm(formName){
      this.$refs[formName].validate((valid) => {
        if(valid) {
          ModuleApi.createModule(this.moduleForm).then((resp)=> {
            if(resp.success === true){
              this.closeDialog()
              this.$message.success("创建成功！")
            }else {
              this.$message.error(resp.error.message)
            }
          })
        }else {
          return false
        }
      })
    },
  },
};
</script>

<style>
.moduleDialog {
  text-align: center;
}
</style>