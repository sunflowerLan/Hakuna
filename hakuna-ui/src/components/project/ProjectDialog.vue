<template>
  <el-dialog :title="showTitle" :visible.sync="dialogVisible">
    <el-form
      :model="projectForm"
      :rules="rules"
      ref="ruleForm"
      label-width="100px"
    >
      <el-form-item label="名称" prop="name">
        <el-input v-model="projectForm.name"></el-input>
      </el-form-item>
      <el-form-item label="描述" prop="desc">
        <el-input type="textarea" v-model="projectForm.describe"></el-input>
      </el-form-item>
      <el-form-item label="图片" prop="image">
        <div id="image">
          <el-upload
            action="''"
            :before-upload="beforeUpload"
            accept="image/jpeg,image/gif,image/png"
            list-type="picture-card"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :file-list="fileList"
          >
            <i class="el-icon-plus"></i>
          </el-upload>
          <el-dialog :visible.sync="imageVisible">
            <img width="100%" :src="imageUrl" alt="" />
          </el-dialog>
        </div>
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
import ProjectApi from '../../request/project.js';

export default {
  name: "projectDialog",
  props: ["title", "pid"],
  data() {
    return {
      showTitle: "",
      dialogVisible: true,
      projectForm: {
        name: "",
        describe: "",
        image: "",
      },
      rules: {
        name: [
          { required: true, message: "请输入项目的名称", trigger: "blur" },
        ],
      },

      fileList: [],
      imageUrl: "",
      imageVisible: false,
      disabled: false,
    };
  },
  mounted() {
    if (this.title == "create") {
      this.showTitle = "创建项目";
    } else if (this.title == "edit") {
      this.showTitle = "编辑项目";
      this.initProject();
    }
  },

  methods: {
    closeDialog() {
      this.$emit("cancel", {});
    },

    initProject(){
      ProjectApi.getProject(this.pid).then((resp)=> {
        if(resp.success === true){
          this.projectForm = resp.item
          this.fileList.push({
            name: resp.item.image,
            url: "/static/images/" + resp.item.image
          })
          this.$message.success("获取项目详情成功！")
        } else {
          this.$message.error("获取项目详情失败！")
        }
      })
    },

    // 创建/编辑项目
    submitForm(formName){
      this.$refs[formName].validate((valid) => {
        if(valid) {
          if(this.title == "create"){
            ProjectApi.createProject(this.projectForm).then((resp)=>{
              if(resp.success === true){
                this.closeDialog()
                this.$message.success("创建成功！")
              }else {
                this.$message.error(resp.error.message)
              }
            })
          } else if(this.title == "edit"){
            ProjectApi.updateProject(this.pid, this.projectForm). then((resp)=> {
              if(resp.success === true) {
                this.closeDialog()
                this.$message.success("编辑成功！")
              } else {
                this.$message.error(resp.error.message)
              }
            })
          }
        }else {
          return false
        }
      })
    },

    beforeUpload(file) {
      let form = new FormData();
      form.append("file", file);
      ProjectApi.uploadImage(form).then((resp) => {
        if(resp.data.success === true){
          this.projectForm.image = resp.data.item.name
          const imagePath = "/static/images/" + resp.data.item.name

          this.fileList.push({
            name: file.name,
            url: imagePath,
          })
          this.$message.success("上传成功！")
        }else {
          this.$message.error(resp.data.error.msg)
        }
      })
      return true
    },
    handleRemove(file) {
      // 从fileList中删除
      this.fileList.forEach(function(item, index, arr){
        if(item.name == file.name){
          arr.splice(index, 1)
        }
      })

      // 后端文件删除：相同图片，在后端存的是相同名称，如果删除，其他项目引用会获取失败
      // ProjectApi.deleteImage({file_url: file.url}).then((resp)=>{
      //   if(resp.success === true ){
      //     this.$message.success("删除图片！")
      //   }else {
      //     this.$message.error(resp.error.msg)
      //   }
      // })
    },
    handlePreview(file) {
      this.imageUrl = file.url;
      this.imageVisible = true;
    },
  },
};
</script>
