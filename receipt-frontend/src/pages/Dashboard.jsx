import { useEffect, useState } from "react"
import api from "../api/api"
import { useNavigate } from "react-router-dom"
import ReceiptCard from "../components/ReceiptCard"
import LogoutButton from "../components/LogoutButton"

export default function Dashboard() {
  const [receipts, setReceipts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const navigate = useNavigate()

  useEffect(() => {
    async function fetchReceipts() {
      try {
        const res = await api.get("receipts/")
        setReceipts(res.data)
      } catch (err) {
        setError("Failed to load receipts. Please log in.")
        if (err.response && err.response.status === 401) {
          navigate("/login")
        }
      } finally {
        setLoading(false)
      }
    }
    fetchReceipts()
  }, [navigate])

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <header className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Your Receipts</h1>
        <div className="space-x-2">
          <button
            onClick={() => navigate("/upload")}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition"
          >
            Upload Receipt
          </button>
          <LogoutButton />
        </div>
      </header>

      {loading && <p>Loading...</p>}

      {error && <p className="text-red-600 font-medium mb-4">{error}</p>}

      {!loading && receipts.length === 0 && (
        <p className="text-gray-600">No receipts found. Upload some!</p>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {receipts.map((receipt) => (
          <ReceiptCard key={receipt.id} receipt={receipt} />
        ))}
      </div>
    </div>
  )
}
