import { useNavigate } from "react-router-dom"

export default function ReceiptCard({ receipt }) {
  const navigate = useNavigate()
  return (
    <div
      onClick={() => navigate(`/edit/${receipt.id}`)}
      className="bg-white rounded shadow p-4 cursor-pointer hover:shadow-lg transition"
    >
      <h2 className="font-semibold text-lg mb-2">{receipt.vendor || "Unknown Vendor"}</h2>
      <p className="text-gray-700">Total: ${receipt.total || "N/A"}</p>
      <p className="text-gray-500 text-sm">
        Date: {receipt.date || "Unknown"}
      </p>
    </div>
  )
}
