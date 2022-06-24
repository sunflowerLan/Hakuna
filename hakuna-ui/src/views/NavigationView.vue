<template>
  <div class="navigation">
    <el-container>
      <el-aside
        width="auto"
      >
        <!-- <img class="logo" alt="itest logo" src="../assets/logo.svg" /> -->
        <el-menu
          :collapse="isCollapse"
          default-active="1"
          class="el-menu-vertical-demo"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <router-link to="/main/project">
            <el-menu-item index="1" class="menu-option">
              <i class="el-icon-menu"></i>
              <span slot="title">项目管理</span>
            </el-menu-item>
          </router-link>

          <router-link to="/main/case">
            <el-menu-item index="2" class="menu-option">
              <i class="el-icon-s-grid"></i>
              <span slot="title">用例管理</span>
            </el-menu-item>
          </router-link>

          <router-link to="/main/task">
            <el-menu-item index="3" class="menu-option">
              <i class="el-icon-s-order"></i>
              <span slot="title">任务管理</span>
            </el-menu-item>
          </router-link>

          <router-link to="/main/report">
            <el-menu-item index="4" class="menu-option">
              <i class="el-icon-document-copy"></i>
              <span slot="title">报告管理</span>
            </el-menu-item>
          </router-link>
        </el-menu>
      </el-aside>

      <el-container>
        <el-header>
          <el-row>
            <el-col :span="12" class="header-left">
              <div class="collapseBtn">
                <i
                  class="el-icon-s-unfold"
                  @click="collapseStatus"
                  v-show="isCollapse"
                ></i>
                <i
                  class="el-icon-s-fold"
                  @click="collapseStatus"
                  v-show="collapseBtnClick"
                ></i>
                <!-- <span>接口测试平台</span> -->
              </div>
            </el-col>

            <el-col :span="12" class="header-right">
              <el-link
                :underline="false"
                href="https://element.eleme.io"
                target="_blank"
                >联系我</el-link
              >&nbsp;&nbsp;&nbsp; <span>欢迎~ {{ user }}</span
              >&nbsp;&nbsp;&nbsp;
              <!-- <i class="el-icon-s-custom">{{ username }}</i>&nbsp;&nbsp;&nbsp; -->
              <el-button type="text" @click="logout()">退出</el-button>
            </el-col>
          </el-row>
        </el-header>

        <el-main>
          <el-card style="min-height: 800px">
            <router-view> </router-view>
          </el-card>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import UserApi from "../request/user";

export default {
  computed: {
    onRoutes() {
      if (this.$route.path === "/main/project") {
        return "1";
      } else if (this.$route.path === "/main/case") {
        return "2";
      } else if (this.$route.path === "/main/task") {
        return "3";
      } else if (this.$route.path === "/main/report") {
        return "5";
      }
      return "1";
    },
  },
  data() {
    return {
      user: "",
      collapseBtnClick: true,
      isCollapse: false,
    };
  },
  created() {
    this.user = sessionStorage.getItem("user");
  },
  methods: {
    collapseStatus() {
      this.collapseBtnClick = this.isCollapse;
      this.isCollapse = !this.isCollapse;
    },
    logout() {
      UserApi.logout().then((resp) => {
        if (resp.success === true) {
          sessionStorage.clear();
          this.$router.push({ path: "/login" });
        } else {
          this.$message.error(resp.error.msg);
        }
      });

    },
  },
};
</script>

<style scoped>
.navigation {
  width: 100%;
  height: 100%;
}
.el-header,
.el-footer {
  background-color: #b3c0d1;
  color: #333;
  line-height: 60px;
  font-size: 14px;
}

.header-left {
  text-align: left;
}

.header-right {
  text-align: right;
}

.collapseBtn {
  background-color: transparent;
  border-style: none;
  font-size: 16px;
  padding: 0 5px;
}

.el-container {
  width: 100%;
  height: 100%;
}

.el-aside {
  height: 100%;
  overflow-y: scroll;
  background-color: #b3c0d1;
  color: #343a40;
  text-align: center;
}

.el-main {
  background-color: #e9eef3;
  color: #333;
  text-align: left;
  padding: 5px;
}

.el-menu {
  height: 100%;
}

a {
  text-decoration: none;
}
.router-link-active {
  text-decoration: none;
}

.logo {
  margin-top: 20px;
  margin-bottom: 10px;
  height: 22px;
}
</style>
