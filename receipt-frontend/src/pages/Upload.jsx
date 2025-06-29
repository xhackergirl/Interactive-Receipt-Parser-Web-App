import { useState } from "react"
import api from "../api/api"
import { useNavigate } from "react-router-dom"

export default function Upload() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState("")
  const navigate = useNavigate()

  function handleFileChange(e) {
    const f = e.target.files[0]
    setFile(f)
    setError("")

    if (f) {
      const reader = new FileReader()
      reader.onloadend = () => setPreview(reader.result)
      if (f.type.startsWith("image/")) {
        reader.readAsDataURL(f)
      } else {
        setPreview(null)
      }
    }
  }

  async function handleSubmit(e) {
    e.preventDefault()
    if (!file) {
      setError("Please select an image or PDF file")
      return
    }

    setUploading(true)
    setError("")

    try {
      const formData = new FormData()
      formData.append("receipt_file", file)

      await api.post("upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })

      navigate("/")
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Failed to upload. Make sure your file is an image or PDF."
      )
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-6">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded shadow-md w-full max-w-md"
      >
        <h2 className="text-2xl font-semibold mb-6 text-center">Upload Receipt</h2>

        {error && (
          <div className="mb-4 text-red-600 font-medium text-center">{error}</div>
        )}

        <input
          type="file"
          accept="image/*,application/pdf"
          onChange={handleFileChange}
          className="mb-4"
        />

        {preview && (
          <img
            src={preview}
            alt="Preview"
            className="mb-4 max-h-64 mx-auto object-contain"
          />
        )}

        <button
          type="submit"
          disabled={uploading}
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition disabled:opacity-50"
        >
          {uploading ? "Uploading..." : "Upload"}
        </button>
      </form>
    </div>
  )
}
