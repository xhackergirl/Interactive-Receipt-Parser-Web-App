import { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import api from "../api/api"

export default function EditReceipt() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [receipt, setReceipt] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [formData, setFormData] = useState({
    vendor: "",
    total: "",
    date: "",
  })

  useEffect(() => {
    async function fetchReceipt() {
      try {
        const res = await api.get(`receipts/${id}/`)
        setReceipt(res.data)
        setFormData({
          vendor: res.data.vendor || "",
          total: res.data.total || "",
          date: res.data.date || "",
        })
      } catch (err) {
        setError("Failed to load receipt.")
      } finally {
        setLoading(false)
      }
    }
    fetchReceipt()
  }, [id])

  function handleChange(e) {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError("")

    try {
      await api.put(`receipts/${id}/`, formData)
      navigate("/")
    } catch (err) {
      setError("Failed to update receipt.")
    }
  }

  if (loading) return <p className="p-6">Loading...</p>
  if (error) return <p className="p-6 text-red-600">{error}</p>
  if (!receipt) return <p className="p-6">Receipt not found.</p>

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-6">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded shadow-md w-full max-w-md"
      >
        <h2 className="text-2xl font-semibold mb-6 text-center">Edit Receipt</h2>

        <label className="block mb-2 font-medium">Vendor</label>
        <input
          name="vendor"
          type="text"
          value={formData.vendor}
          onChange={handleChange}
          className="w-full border border-gray-300 rounded px-3 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />

        <label className="block mb-2 font-medium">Total</label>
        <input
          name="total"
          type="number"
          step="0.01"
          value={formData.total}
          onChange={handleChange}
          className="w-full border border-gray-300 rounded px-3 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />

        <label className="block mb-2 font-medium">Date</label>
        <input
          name="date"
          type="date"
          value={formData.date}
          onChange={handleChange}
          className="w-full border border-gray-300 rounded px-3 py-2 mb-6 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />

        {error && (
          <div className="mb-4 text-red-600 text-center font-medium">{error}</div>
        )}

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
        >
          Save Changes
        </button>
      </form>
    </div>
  )
}
