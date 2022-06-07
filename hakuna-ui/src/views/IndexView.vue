<template>
<div id="index">
  <el-container>
    <el-header>
      <el-row>
        <div id="logo">
          <img src="../assets/smile.png" alt="" width="60px" height="auto">
        </div>
        <el-link :underline="false" href="https://element.eleme.io" target="_blank">联系我</el-link>&nbsp;&nbsp;&nbsp;
        <i class="el-icon-s-custom">{{username}}</i>&nbsp;&nbsp;&nbsp;
        <el-button type="text">退出</el-button>
      </el-row>
    </el-header>
    <el-container>
        <aside-v></aside-v>
        <project-v></project-v>
        <!-- <el-main>main</el-main> -->
    </el-container>
    <!-- <el-footer>footer</el-footer> -->
  </el-container>
</div>
</template>


<script>
import AsideV from '../components/Aside.vue';
import ProjectV from '../components/Project.vue';


export default {
  data() {
    var username = window.localStorage.getItem('username') || "";
    return {
      'username': username
    }
  },
  components: {
    AsideV,
    ProjectV
  }
}

</script>

<style scoped>
  #index {
    width: 100%;
    height: 100%;
  }

  .el-header {
    width: 100%;
    height: 60px;
    background-color: #B3C0D1;
    color: #333;
    text-align: right;
    line-height: 60px;
    font-size: 14px;
  }

  #logo {
    width: 60px;
    height: 60px;
    display: inline-flex;
    align-items: center;
    float: left;
  }

</style>