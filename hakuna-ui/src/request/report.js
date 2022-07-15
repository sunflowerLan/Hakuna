import request from "@/HttpCommon.js";


class ReportApi {
  getReportList(projectId) {
    return request.get("/api/reports/" + projectId + "/list/")
  }

  deleteReport(reportId) {
    return request.delete("/api/reports/" + reportId + "/")
  }

  getReportDetail(reportId) {
    return request.get("/api/reports/" + reportId + "/")
  }

}

export default new ReportApi();
