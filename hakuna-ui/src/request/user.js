import request from "@/HttpCommon.js"
// import axios from "axios"

class UserApi {
  login(data) {
    return request.post("/api/users/login", data)
  }

  logout() {
    return request.get("/api/users/logout")
    // return axios({
    //   method: "get",
    //   url: "/api/users/logout",
    //   timeout: 20000,
    //   headers: {
    //     "Authorization": "Bearer "+ sessionStorage.getItem("token")
    //   }
    // })
  }

  register(data) {
    return request.post("/api/users/register", data)
  }
}

export default new UserApi()