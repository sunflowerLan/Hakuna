<template>
  <div class="casedialog">
    <div class="div-line" style="height: 40px">
      <el-select
        v-model="caseForm.method"
        placeholder="请求方法"
        size="small"
        style="width: 15%; float: left"
      >
        <el-option
          v-for="item in methodOption"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        >
        </el-option>
      </el-select>
      <el-input
        v-model="caseForm.url"
        placeholder="URL"
        size="small"
        style="width: 75%; float: left"
      ></el-input>
      <el-button
        type="primary"
        size="small"
        style="float: left"
        @click="sendClick()"
        >发送</el-button
      >
    </div>

    <div class="div-line" style="height: 30px">
      <el-radio v-model="caseForm.params_type" label="params">Params</el-radio>
      <el-radio v-model="caseForm.params_type" label="form">Form-data</el-radio>
      <el-radio v-model="caseForm.params_type" label="json">JSON</el-radio>
    </div>

    <div class="div-line" style="height: 220px">
      <el-tabs v-model="activeName">
        <el-tab-pane label="Headers" name="first">
          <vueJsonEditor
            v-model="caseForm.header"
            :mode="'code'"
          ></vueJsonEditor>
        </el-tab-pane>
        <el-tab-pane label="Params/Body" name="second">
          <vueJsonEditor
            v-model="caseForm.params_body"
            :mode="'code'"
          ></vueJsonEditor>
        </el-tab-pane>
      </el-tabs>
    </div>

    <div class="div-line" style="height: 150px; padding-top: 30px">
      <el-input
        v-model="caseForm.result"
        type="textarea"
        :rows="5"
        placeholder="Response"
      >
      </el-input>
    </div>

    <div class="div-line">
      <el-collapse>
        <el-collapse-item title="断言" name="1">
          <div style="height: 40px">
            <el-radio v-model="caseForm.assert_type" label="include"
              >Include</el-radio
            >
            <el-radio v-model="caseForm.assert_type" label="equal"
              >Equal</el-radio
            >
            <el-button
              class="debug-button"
              type="success"
              plain
              size="small"
              @click="assertclick()"
              >断言</el-button
            >
          </div>
          <div style="height: 120px">
            <el-input
              v-model="caseForm.assert_text"
              type="textarea"
              :rows="5"
              placeholder="Response"
            >
            </el-input>
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>
    <div style="height: 50px">
      <el-input
        v-model="caseForm.name"
        placeholder="请输入用例名称"
        size="small"
        style="width: 60%; float: left"
      ></el-input>
      <el-button
        type="primary"
        size="small"
        style="float: left"
        @click="saveClick()"
        >保存</el-button
      >
    </div>
  </div>
</template>

<script>
import vueJsonEditor from "vue-json-editor";
import CaseApi from "../../request/case";

export default {
  name: "caseDrawer",
  props: ["mid", "cid"],
  components: {
    vueJsonEditor,
  },
  data() {
    return {
      methodOption: [
        {
          value: "get",
          label: "GET",
        },
        {
          value: "post",
          label: "POST",
        },
        {
          value: "put",
          label: "PUT",
        },
        {
          value: "delete",
          label: "DELETE",
        },
      ],
      activeName: "first",
      caseId: this.cid,
      caseForm: {
        name: "",
        module_id: 0,
        url: "https://httpbin.org/get",
        method: "get",
        header: { token: "1111" },
        params_type: "params",
        params_body: { id: "1", name: "test" },
        result: "",
        assert_type: "include",
        assert_text: "",
      },
    };
  },

  mounted() {
    this.caseForm.module_id = this.mid;
    if (this.cid !== 0) {
      // 调用接口获取用例数据
      this.getCaseInfo();
    }
  },

  methods: {
    // 调用接口获取用例数据
    async getCaseInfo() {
      const resp = await CaseApi.getCase(this.cid);
      if (resp.success === true) {
        this.caseForm = resp.item;
        const header = resp.item.header.replace(/'/g, '"')
        const params_body = resp.item.params_body.replace(/'/g, '"')
        this.caseForm.header = JSON.parse(header)
        this.caseForm.params_body = JSON.parse(params_body)
        this.caseForm.module_id = resp.item.module //直接从数据库表中读取数据时，外键显示名称，不带_id
      } else {
        this.$message.error(resp.error.msg);
      }
    },

    // 调试接口
    async sendClick() {
      const reqData = {
        method: this.caseForm.method,
        url: this.caseForm.url,
        header: this.caseForm.header,
        params_type: this.caseForm.params_type,
        params_body: this.caseForm.params_body,
      };
      const resp = await CaseApi.debugCase(reqData);
      if (resp.success === true) {
        this.caseForm.result = resp.item.response;
      } else {
        console.log(resp);
        this.caseForm.result = resp.error.msg;
      }
    },

    // 断言
    async assertclick() {
      const req = {
        response: this.caseForm.result,
        assert_type: this.caseForm.assert_type,
        assert_text: this.caseForm.assert_text,
      };
      const resp = await CaseApi.assertCase(req);
      if (resp.success === true) {
        this.$message.success("断言成功");
      } else {
        this.$message.error(resp.error.msg);
      }
    },

    // 保存用例
    async saveClick() {
      if (this.caseId == 0) {
        const resp = await CaseApi.createCase(this.caseForm);
        if (resp.success === true) {
          this.caseId = resp.item.id;
          this.$message.success("保存成功");
        } else {
          this.$message.error(resp.error.msg);
        }
      } else {
        const resp = await CaseApi.updateCase(this.caseId, this.caseForm);
        if (resp.success === true) {
          this.$message.success("用例修改成功");
        } else {
          this.$message.error(resp.error.msg);
        }
      }
    },
  },
};
</script>

<style>
.casedialog {
  width: 100%;
  height: auto;
  margin-left: 20px;
  margin-right: 20px;
}

.div-line {
  width: 100%;
  height: auto;
  text-align: left;
  margin-bottom: 10px;
}
</style>
