import request from "@/HttpCommon.js";
import axios from "axios";

axios.defaults.headers.common['Authorization'] = "Bearer " + sessionStorage.getItem('token');

class ProjectApi {
  getProjects(data) {
    return request.get("/api/projects/list", data);
  }

  getProject(id) {
    return request.get("/api/projects/" + id);
  }

  createProject(data) {
    return request.post("/api/projects/", data);
  }

  updateProject(id, data) {
    return request.put("/api/projects/" + id, data);
  }

  deleteProject(id) {
    return request.delete("/api/projects/" + id);
  }

  uploadImage(data) {
    return axios({
      method: "post",
      url: "/api/projects/upload/",
      timeout: 20000,
      data: data,
    });
  }

  deleteImage(data) {
    return request.get("/api/projects/image/delete", data);
  }
}

export default new ProjectApi();
