import api from "../api/api"
import { useNavigate } from "react-router-dom"

export default function LogoutButton() {
  const navigate = useNavigate()

  function logout() {
    localStorage.removeItem("access")
    api.defaults.headers.common["Authorization"] = null
    navigate("/login")
  }

  return (
    <button
      onClick={logout}
      className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded"
      title="Logout"
    >
      Logout
    </button>
  )
}
