import { useEffect, useState, type ChangeEvent } from "react"

type TrackingRecord = {
  id: number
  track_id: number
  object_type: string
  camera_id: string
  timestamp: string
  latitude: number
  longitude: number
}

function App() {
  const [records, setRecords] = useState<TrackingRecord[]>([])

  const uploadVideo = async (
  event: ChangeEvent<HTMLInputElement>
) => {
  const file = event.target.files?.[0]

  if (!file) return

  const formData = new FormData()
  formData.append("file", file)

  const response = await fetch(
    "http://127.0.0.1:8000/upload",
    {
      method: "POST",
      body: formData,
    }
  )

  const data = await response.json()

  alert(data.message)
}

  useEffect(() => {
    fetch("http://127.0.0.1:8000/tracking")
      .then((response) => response.json())
      .then((data) => setRecords(data))
      .catch((error) => console.error(error))
  }, [])

  const cars = records.filter(
    (record) => record.object_type === "car"
  ).length

  const trucks = records.filter(
    (record) => record.object_type === "truck"
  ).length

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#0f172a",
        color: "white",
        padding: "30px",
        fontFamily: "Arial",
      }}
    >
      <h1>AI CCTV Surveillance Dashboard</h1>
      <input
  type="file"
  accept="video/*"
  onChange={uploadVideo}
/>

      <div
        style={{
          display: "flex",
          gap: "20px",
          marginBottom: "30px",
        }}
      >
        <div style={cardStyle}>
          <h3>Total Records</h3>
          <h2>{records.length}</h2>
        </div>

        <div style={cardStyle}>
          <h3>Cars Detected</h3>
          <h2>{cars}</h2>
        </div>

        <div style={cardStyle}>
          <h3>Trucks Detected</h3>
          <h2>{trucks}</h2>
        </div>
      </div>

      <h2>Tracking History</h2>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          background: "#1e293b",
        }}
      >
        <thead>
          <tr>
            <th style={cellStyle}>Track ID</th>
            <th style={cellStyle}>Object Type</th>
            <th style={cellStyle}>Camera ID</th>
            <th style={cellStyle}>Timestamp</th>
          </tr>
        </thead>

        <tbody>
          {records.slice(0, 100).map((record) => (
            <tr key={record.id}>
              <td style={cellStyle}>{record.track_id}</td>
              <td style={cellStyle}>{record.object_type}</td>
              <td style={cellStyle}>{record.camera_id}</td>
              <td style={cellStyle}>{record.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

const cardStyle = {
  background: "#1e293b",
  padding: "20px",
  borderRadius: "10px",
  minWidth: "200px",
}

const cellStyle = {
  border: "1px solid #475569",
  padding: "10px",
  textAlign: "left" as const,
}

export default App