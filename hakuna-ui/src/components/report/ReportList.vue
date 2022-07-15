<template>
  <div class="reportList">
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
      </el-form>
    </div>

    <div class="reportTable">
    <el-table :data="reportData" border style="width: 100%">
        <el-table-column prop="id" label="ID"> </el-table-column>
        <el-table-column prop="name" label="名称"> </el-table-column>
        <el-table-column prop="tests" label="总数"> </el-table-column>
        <el-table-column prop="passed" label="通过">
          <template slot-scope="scope">
            <el-tag type="success"> {{ scope.row.passed }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="error" label="错误">
          <template slot-scope="scope">
            <el-tag type="danger"> {{ scope.row.error }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="failure" label="失败">
          <template slot-scope="scope">
            <el-tag type="warning"> {{ scope.row.failure }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="skipped" label="跳过">
          <template slot-scope="scope">
            <el-tag type="info"> {{ scope.row.skipped }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="run_time" label="时长"> </el-table-column>
        <el-table-column prop="create_time" label="创建"> </el-table-column>
        <el-table-column fixed="right" label="操作" width="150">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="showReport(scope.row)"
              >查看</el-button
            >
            <el-button type="text" size="small" @click="deleteReport(scope.row)"
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
    <reportDialog
      v-if="dialogFlag"
      :rid="reportId"
      @cancel="closeDialog"
    ></reportDialog>
  </div>
</template>

<script>
import ProjectApi from "../../request/project"
import ReportApi from "../../request/report"
import ReportDialog from "../../components/report/ReportDialog.vue"


export default{
  name: "ReportList",
  components: {ReportDialog},
  data() {
    return{
      projectValue: 1,
      projectOption: [],
      projectLabel: "",
      req: {
        page: 1,
        size: 20,
      },
      total: 50,
      reportId: "",
      reportData: [],
      dialogFlag: false
    }
  },
  mounted() {
    this.initProjectList()
  },
  methods: {
    // 初始化项目列表
    async initProjectList() {
      const resp = await ProjectApi.getProjects(this.req);
      if (resp.success === true) {
        this.projectValue = resp.items[0].id;
        this.projectLabel = resp.items[0].name;
        this.projectOption = resp.items;
        this.initReportList();
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
      this.initReportList(value);
    },
    // 初始化测试报告
    async initReportList(){
      const resp = await ReportApi.getReportList(this.projectValue);
      if (resp.success === true) {
        this.reportData = resp.items;
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

    closeDialog() {
      this.dialogFlag = false;
    },
    // 展示测试报告
    showReport(row){
      this.reportId = row.id,
      this.dialogFlag = true
    },

    // 删除报告
    async deleteReport(row) {
      const resp = await ReportApi.deleteReport(row.id)
      if (resp.success === true) {
        this.initProjectList()
        this.$message.success("删除成功！")
      } else {
        this.$message.error("删除失败！")
      }
    },
  }
}

</script>