<template>
  <div class="case">
    <div class="selectPro">
      <el-form :inline="true">
        <el-form-item label="项目">
          <el-select
            v-model="projectValue"
            filterable
            size="medium"
            placeholder="请选择项目"
            @change="changeProject"
          >
            <el-option
              v-for="item in projectOption"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="medium" @click="createCase"
            >创建用例</el-button
          >
        </el-form-item>
      </el-form>
    </div>
    <div class="moduleCase">
      <el-card class="moduleTree">
        <el-button
          type="text"
          icon="el-icon-circle-plus-outline"
          @click="createRootModule"
          >根节点
        </el-button>
        <el-tree
          :data="moduleData"
          node-key="id"
          default-expand-all=""
          :expand-on-click-node="false"
          @node-click="nodeClick"
        >
          <span class="custom-tree-node" slot-scope="{ node, data }">
            <span style="float: left">{{ node.label }}</span>
            <span style="float: right">
              <el-button type="text" size="mini" @click="() => append(data)">
                <i class="el-icon-circle-plus-outline"></i>
              </el-button>
              <el-button
                type="text"
                size="mini"
                @click="() => remove(node, data)"
              >
                <i class="el-icon-delete"></i>
              </el-button>
            </span>
          </span>
        </el-tree>
      </el-card>

      <div class="caseTable">
        <el-table
          :data="casesData"
          border
          style="width: 100%"
        >
          <el-table-column prop="id" label="ID" width="50"> </el-table-column>
          <el-table-column prop="name" label="名称" width="180">
          </el-table-column>
          <el-table-column prop="method" label="方法" width="80">
          </el-table-column>
          <el-table-column prop="url" label="URL" width="180">
          </el-table-column>
          <el-table-column prop="module.name" label="模块" width="100">
          </el-table-column>
          <el-table-column prop="create_time" label="创建时间">
          </el-table-column>
          <el-table-column fixed="right" label="操作" width="100">
            <template slot-scope="scope">
              <el-button
                @click="caseRowClick(scope.row)"
                type="text"
                size="small"
              >查看
              </el-button>
              <el-button type="text" size="small" @click="caseRowDelete(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 用例编辑抽屉 -->
      <el-drawer
        :title="caseTitle"
        :visible.sync="drawer"
        direction="rtl"
        :before-close="caseDrawerClose"
        size="50%"
      >
        <CaseDialog
          v-if="drawer"
          :mid="currentModule"
          :cid="currentCase"
        ></CaseDialog>
      </el-drawer>
    </div>

    <!-- 创建模块 -->
    <ModuleDialog
      v-if="dialogFlag"
      :projectId="projectValue"
      :projectLabel="projectLabel"
      :rootId="rootFlag"
      :parentObj="parentObj"
      @cancel="closeDialog"
    ></ModuleDialog>
  </div>
</template>

<script>
import ProjectApi from "../../request/project";
import ModuleApi from "../../request/module";
import CaseApi from "../../request/case";
import CaseDialog from "../../components/case/CaseDialog.vue";
import ModuleDialog from "../../components/case/ModuleDialog.vue";

export default {
  components: {
    CaseDialog,
    ModuleDialog,
  },
  data() {
    return {
      projectOption: [],
      projectValue: 0,
      projectLabel: "",
      req: {
        page: 1,
        size: 20,
      },
      moduleData: [],
      dialogFlag: false,
      parentObj: {},
      casesData: [],
      drawer: false,
      caseTitle: "",
      currentModule: 0, // 当前选中的模块
      currentCase: 0, // 当前选中的用例
    };
  },

  mounted() {
    this.initProjectList();
    // this.initModuleList(this.projectValue);
  },

  methods: {
    // 初始化项目列表
    async initProjectList() {
      const resp = await ProjectApi.getProjects(this.req);
      if (resp.success === true) {
        this.projectValue = resp.items[0].id;
        this.projectLabel = resp.items[0].name;
        this.projectOption = resp.items;
        // this.$message.success("查询成功！");

        this.initModuleList(this.projectValue);
      } else {
        this.$message.error("查询失败！");
      }
    },

    // 修改选中项目
    changeProject(value) {
      console.log("change project value: ", value);
      this.projectValue = value;
      this.projectLabel = this.projectOption.find(
        (item) => item.id === value
      ).name;

      this.initModuleList(value);
    },

    // 查询模块列表
    async initModuleList(pid) {
      console.log("init project value: ", pid);
      this.moduleData = [];
      const resp = await ModuleApi.getModuleTree(pid);
      if (resp.success === true) {
        this.moduleData = resp.items;
        // this.$message.success("查询成功！");
      } else {
        this.$message.info(resp.error.msg);
      }
    },

    // 创建根节点
    createRootModule() {
      this.dialogFlag = true;
      this.rootFlag = true;
    },

    // 添加子节点
    append(data) {
      this.dialogFlag = true;
      this.rootFlag = false;
      this.parentObj = data;
    },

    // 移除子节点
    remove(node, data) {
      ModuleApi.deleteModule(data.id).then((resp) => {
        if (resp.success === true) {
          this.$message.success("删除成功！");
          this.initModuleList(this.projectValue);
        } else {
          this.$message.error(resp.error.msg);
        }
      });
    },

    // 关闭创建模块页面
    closeDialog() {
      this.dialogFlag = false;
      this.parentObj = {};
      this.initModuleList(this.projectValue);
    },

    // 点击模块
    nodeClick(data) {
      this.currentModule = data.id;
      this.getCaseList(data.id);
    },

    // 获取模块下的所有用例
    async getCaseList(mid) {
      const resp = await CaseApi.getModuleCases(mid);
      if (resp.success === true) {
        this.casesData = resp.items;
        // this.$message.success("查询成功！");
      } else {
        this.$message.error("查询失败！");
      }
    },

    // 创建用例
    createCase() {
      if (this.currentModule == 0) {
        this.$message.info("请选择模块节点！");
      } else {
        this.drawer = true;
        this.caseTitle = "创建用例";
      }
    },

    // 选中用例记录
    caseRowClick(row) {
      this.currentCase = row.id;
      this.drawer = true;
      this.caseTitle = "查看用例";
    },
    // 删除选中用例
    caseRowDelete(row) {
      this.currentCase = row.id;
      CaseApi.deleteCase(this.currentCase).then((resp)=>{
        if(resp.success == true) {
          this.$message.success("删除成功！")
          this.getCaseList(this.currentModule)
        } else {
          this.$message.error(resp.error.msg)
        }
      })
    },

    // 关闭抽屉
    caseDrawerClose() {
      this.drawer = false
      this.getCaseList(this.currentModule)
    }
  },
};
</script>

<style scoped>
.moduleCase {
  margin-top: 10px;
}

.moduleTree {
  width: 28%;
  float: left;
}

.caseTable {
  width: 70%;
  float: right;
}
</style>
