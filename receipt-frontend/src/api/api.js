import axios from "axios"

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
})

export function setAuthToken(token) {
  if (token) {
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`
    localStorage.setItem("authToken", token)
  } else {
    delete api.defaults.headers.common["Authorization"]
    localStorage.removeItem("authToken")
  }
}

// On app load, set token from localStorage if present
const storedToken = localStorage.getItem("authToken")
if (storedToken) {
  setAuthToken(storedToken)
}

api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

export default api
