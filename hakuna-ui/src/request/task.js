import request from "@/HttpCommon.js";


class TaskApi {
  getTaskList(projectId) {
    return request.get("/api/tasks/" + projectId + "/list/")
  }

  createTask(data) {
    return request.post("/api/tasks/", data)
  }

  updateTask(taskId, data) {
    return request.put("/api/tasks/" + taskId + "/",data)
  }

  deleteTask(taskId) {
    return request.delete("/api/tasks/" + taskId + "/")
  }

  getTaskDetail(taskId) {
    return request.get("/api/tasks/" + taskId + "/")
  }

  runningTask(taskId) {
    return request.post("/api/tasks/"+ taskId + "/running")
  }

}

export default new TaskApi();
