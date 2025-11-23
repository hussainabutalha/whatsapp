import { useEffect, useState } from 'react'
import { getReviews } from './api'
import './App.css'

function App() {
  const [reviews, setReviews] = useState([])

  useEffect(() => {
    const fetchReviews = async () => {
      const data = await getReviews()
      setReviews(data)
    }

    fetchReviews()
    // Poll every 5 seconds to see new reviews
    const interval = setInterval(fetchReviews, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="container">
      <h1>Product Reviews</h1>
      <div className="review-list">
        {reviews.length === 0 ? (
          <p>No reviews yet.</p>
        ) : (
          <table className="review-table">
            <thead>
              <tr>
                <th>Product</th>
                <th>User</th>
                <th>Review</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {reviews.map((review) => (
                <tr key={review.id}>
                  <td>{review.product_name}</td>
                  <td>{review.user_name}</td>
                  <td>{review.product_review}</td>
                  <td>{new Date(review.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default App
