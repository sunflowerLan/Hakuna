<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    :before-close="closeDialog"
    class="taskDialog"
    width="1000px"
  >
  <el-form
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-form-item label="统计">
        <div
          id="youChart"
          :style="{ width: '380px', height: '380px' }"
          style="margin: 0 auto"
        ></div>
        <el-table :data="reportData" border style="width: 100%">
          <el-table-column prop="name" label="名称"> </el-table-column>
          <el-table-column prop="tests" label="总数"> </el-table-column>
          <el-table-column prop="passed" label="通过"> </el-table-column>
          <el-table-column prop="failure" label="失败"> </el-table-column>
          <el-table-column prop="error" label="错误"> </el-table-column>
          <el-table-column prop="skipped" label="跳过"> </el-table-column>
          <el-table-column prop="run_time" label="时长"> </el-table-column>
          <el-table-column prop="create_time" label="创建时间">
          </el-table-column>
        </el-table>
      </el-form-item>
      <el-form-item label="详细日志">
        <el-input type="textarea" :rows="10" v-model="detailLog"></el-input>
      </el-form-item>

      <el-form-item style="text-align: right">
        <div class="dialog-footer">
          <el-button @click="closeDialog()">关闭</el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script>
import ReportApi from "../../request/report"
import * as echarts from "echarts"


export default{
  name: "ReportDialog",
  props: ["rid"],
  components: {},
  data() {
    return{
      showTitle: "查看报告",
      dialogVisible: true,
      detailLog: "",
      reportData:[],
      chartOption: {
        tooltip: {
          trigger: "item",
        },
        legend: {
          top: "5%",
          left: "center",
        },
        series: [
          {
            name: "比例",
            type: "pie",
            radius: "50%",
            data: [
              { value: 1, name: "跳过" },
              { value: 10, name: "通过" },
              { value: 3, name: "失败" },
              { value: 2, name: "错误" },
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      },
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initEChart()
    })
  },
  methods: {
    // 关闭对话框
    closeDialog() {
      this.$emit("cancel", {});
    },

    // 初始化图表
    async initEChart() {
      var myChart = echarts.init(document.getElementById("youChart"))
      const resp = await ReportApi.getReportDetail(this.rid)
      this.chartOption.series[0].data = []
      if (resp.success === true) {
        console.log("resp--->", resp.item)
        console.log("option--->", this.chartOption.series[0].data)
        this.reportData.push(resp.item)
        this.chartOption.series[0].data.push({
          value: resp.item.skipped,
          name: "跳过",
        })
        this.chartOption.series[0].data.push({
          value: resp.item.passed,
          name: "通过",
        })
        this.chartOption.series[0].data.push({
          value: resp.item.failure,
          name: "失败",
        })
        this.chartOption.series[0].data.push({
          value: resp.item.error,
          name: "错误",
        })
        this.detailLog = resp.item.result
        // this.reportData = resp.item
        // this.$message.success("查询成功！")
      } else {
        this.$message.error("查询失败！")
      }
      myChart.setOption(this.chartOption)
    },

  }
}

</script>