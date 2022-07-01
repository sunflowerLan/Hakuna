import request from "@/HttpCommon.js";


class ModuleApi {
  getModuleTree(pid) {
    return request.get("/api/module/tree/" + pid + "/")
  }

  createModule(data) {
    return request.post("/api/module/", data)
  }

  updateModule(mid) {
    return request.put("/api/module/" + mid + "/")
  }

  deleteModule(mid) {
    return request.delete("/api/module/" + mid + "/")
  }
}

export default new ModuleApi();
