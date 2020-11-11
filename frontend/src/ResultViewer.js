import React, { useEffect, useState } from "react"
import "./App.css"

export function ResultViewer(props) {
  const { id } = props
  const [progress, setProgress] = useState("")
  const [video, setVideo] = useState(null)
  useEffect(() => {
    let intervalId = 0
    const check = () => {
      fetch("http://localhost:8000/get?id=" + id).then((response) => {
        response.json().then((json) => {
          const status = json["status"]
          if (status === "not_ready") {
            setProgress(json["progress"])
          } else {
            setVideo("http://localhost:8000/getvideo?id=" + json["filename"])
            clearInterval(intervalId)
          }
        })
      })
    }
    intervalId = setInterval(check, 2000)
    check()
  }, [id])
  return (
    <div className="App center">
      <div className="progress">{progress}</div>
      {video && (
        <div>
          <div className="videoplayer">
            <video controls>
              <source src={video} type="video/mp4" />
            </video>
          </div>
          <a className="back_btn" href="/">
            Back
          </a>
        </div>
      )}
    </div>
  )
}
