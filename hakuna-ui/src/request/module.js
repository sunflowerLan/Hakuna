import request from "@/HttpCommon.js";


class ModuleApi {
  getModuleTree(pid) {
    return request.get("/api/modules/tree" + pid + "/")
  }

  createModule(data) {
    return request.post("/api/modules/", data)
  }

  updateModule(mid) {
    return request.put("/api/modules/" + mid + "/")
  }

  deleteModule(mid) {
    return request.delete("/api/modules/" + mid + "/")
  }

  getModuleCase(mid) {
    return request.get("/api/modules/" + mid + "/cases")
  }
}

export default new ModuleApi();
