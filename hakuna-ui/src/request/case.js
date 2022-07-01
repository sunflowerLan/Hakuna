import request from "@/HttpCommon.js"

class CaseApi {
  debugCase(data) {
    return request.post("/api/cases/debug/", data)
  }

  assertCase(data) {
    return request.post("/api/cases/assert/", data)
  }

  createCase(data) {
    return request.post("/api/cases/", data)
  }

  getModuleCases(mid) {
    return request.get("/api/cases/" + mid + "/cases")
  }

  getCase(cid) {
    return request.get("/api/cases/" + cid + "/")
  }

  deleteCase(cid) {
    return request.delete("/api/cases/" + cid + "/")
  }

  updateCase(cid, data) {
    return request.put("/api/cases/" + cid + "/", data)
  }
}

export default new CaseApi()