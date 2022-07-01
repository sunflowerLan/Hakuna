<template>
  <div class="task">
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
          <el-button type="primary" size="medium" @click="createTask"
            >创建任务</el-button
          >
        </el-form-item>
      </el-form>
    </div>

    <div>
      <el-table :data="taskData" border style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"> </el-table-column>
        <el-table-column prop="name" label="名称"> </el-table-column>
        <el-table-column prop="describe" label="描述"> </el-table-column>
        <el-table-column prop="create_time" label="创建"> </el-table-column>
        <el-table-column prop="update_time" label="更新"> </el-table-column>
        <el-table-column prop="status" label="状态">
          <template slot-scope="scope">
            <div v-if="scope.row.status === 0">
              <el-tag type="info"> 未执行</el-tag>
            </div>
            <div v-else-if="scope.row.status === 1">
              <el-tag type="success"> 执行中</el-tag>
            </div>
            <div v-else-if="scope.row.status === 2">
              <el-tag> 已执行</el-tag>
            </div>
            <div v-else>
              <el-tag type="danger"> 未知 </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="150">
          <template slot-scope="scope">
            <el-button @click="runTask(scope.row)" type="text" size="small"
              >执行</el-button
            >
            <el-button type="text" size="small" @click="editTask(scope.row)"
              >编辑</el-button
            >
            <el-button type="text" size="small" @click="deleteTask(scope.row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div style="width: 100%; text-align: right">
      <el-pagination
        background
        @current-change="handleCurrentChange"
        layout="prev, pager, next"
        :page-size="req.size"
        :total="total"
      >
      </el-pagination>
    </div>

    <!-- 引入子组件 -->
    <TaskDialog
      v-if="taskDialog"
      :title="taskTitle"
      :pid="projectValue"
      :tid="taskId"
      @cancel="closeDialog"
    ></TaskDialog>
  </div>
</template>

<script>
import ProjectApi from "../../request/project";
import TaskApi from "../../request/task";
import TaskDialog from "../../components/task/TaskDialog.vue";

export default {
  name: "TaskList",
  components: {
    TaskDialog,
  },
  data() {
    return {
      projectValue: 1,
      projectOption: [],
      projectLabel: "",
      req: {
        page: 1,
        size: 20,
      },
      total: 50,
      taskData: [],
      taskId: 0,
      taskDialog: false,
      taskTitle: "",
      taskHeartbeat: null,
    };
  },

  mounted() {
    this.initProjectList();
    this.taskHeartbeat = setInterval(() => {
      this.initTaskList()
    }, 5000)
  },
  destroyed() {
    // 销毁时候清除定时器
    clearInterval(this.taskHeartbeat)
  },
  methods: {
    // 初始化项目列表
    async initProjectList() {
      const resp = await ProjectApi.getProjects(this.req);
      if (resp.success === true) {
        this.projectValue = resp.items[0].id;
        this.projectLabel = resp.items[0].name;
        this.projectOption = resp.items;
        this.initTaskList();
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
      this.initTaskList(value);
    },

    // 初始化任务记录
    async initTaskList() {
      const resp = await TaskApi.getTaskList(this.projectValue);
      if (resp.success === true) {
        this.taskData = resp.items;
        // this.$message.success("查询成功！");
      } else {
        this.$message.info(resp.error.msg);
      }
    },

    // 跳转到第几页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
      this.req.page = val
      this.initProjectList()
    },

    // 创建任务
    createTask() {
      this.taskDialog = true;
      this.taskTitle = "create";
    },
    // 编辑任务
    editTask(row) {
      this.taskId = row.id;
      this.taskDialog = true;
      this.taskTitle = "edit";
    },

    // 删除任务
    async deleteTask(row) {
      const resp = await TaskApi.deleteTask(row.id)
      if(resp.success == true) {
          this.initProjectList()
          this.$message.success("删除成功！")
        } else {
          this.$message.error(resp.error.msg)
        }
    },
    // 执行任务
    async runTask(row) {
      const resp = await TaskApi.runningTask(row.id)
      if (resp.success === true) {
        this.initProjectList()
        this.$message.success("执行成功！")
      } else {
        this.$message.error("执行失败！")
      }
    },

    closeDialog() {
      this.taskDialog = false;
    }
  },
};
</script>
