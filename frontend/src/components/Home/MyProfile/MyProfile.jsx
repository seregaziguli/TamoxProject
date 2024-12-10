import React, { useState, useEffect } from "react";
import axios from "axios";
import "./MyProfile.css";

export default function MyProfile() {
  const [orders, setOrders] = useState([]);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [orderImage, setOrderImage] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const auth_token = localStorage.getItem("access_token");
        const response = await axios.get("http://localhost:8007/orders", {
          headers: {
            "Content-Type": "application/json",
            "access-token": auth_token,
          },
        });
        setOrders(response.data);
      } catch (error) {
        setError(error.response ? error.response.data : error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchOrders();
  }, []);

  const fetchOrderDetails = async (order) => {
    try {
      const auth_token = localStorage.getItem("access_token");
      const response = await axios.get(
        `http://localhost:8007/orders/images/${order.image_url}`,
        {
          headers: {
            "Content-Type": "application/json",
            "access-token": auth_token,
          },
          responseType: "arraybuffer",
        }
      );
      const imageBlob = new Blob([response.data], { type: "image/jpeg" });
      const imageUrl = URL.createObjectURL(imageBlob);
      setOrderImage(imageUrl);
      setSelectedOrder(order);
      document.body.classList.add("no-scroll");
    } catch (error) {
      setError(error.response ? error.response.data : error);
    }
  };

  const deleteOrder = async (orderId) => {
    try {
      const auth_token = localStorage.getItem("access_token");
      await axios.delete(`http://localhost:8007/orders/${orderId}`, {
        headers: {
          "Content-Type": "application/json",
          "access-token": auth_token,
        },
      });
      setOrders((prevOrders) =>
        prevOrders.filter((order) => order.id !== orderId)
      );
      closeModal();
    } catch (error) {
      setError(error.response ? error.response.data : error);
    }
  };

  const closeModal = () => {
    setSelectedOrder(null);
    setOrderImage(null);
    document.body.classList.remove("no-scroll");
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="my-profile-container">
      <h1 className="text-2xl mb-4">My Orders</h1>
      <div className="order-grid">
        {orders.map((order) => (
          <div
            key={order.id}
            className="order-card"
            onClick={() => fetchOrderDetails(order)}
          >
            <h2>Order #{order.id}</h2>
            <p>
              <strong>Title:</strong> {order.title}
            </p>
            <p>
              <strong>Description:</strong> {order.description}
            </p>
            <p>
              <strong>Service Type:</strong> {order.service_type_name}
            </p>
          </div>
        ))}
      </div>

      {selectedOrder && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>Order Details</h2>
            <p>
              <strong>Title:</strong> {selectedOrder.title}
            </p>
            <p>
              <strong>Description:</strong> {selectedOrder.description}
            </p>
            <p>
              <strong>Service Type:</strong> {selectedOrder.service_type_name}
            </p>
            <p>
              <strong>Scheduled Date:</strong>{" "}
              {new Date(selectedOrder.scheduled_date).toLocaleString()}
            </p>
            <p>
              <strong>Status:</strong> {selectedOrder.status}
            </p>
            {orderImage && (
              <img src={orderImage} alt="Order" className="order-image" />
            )}
            <div className="modal-buttons">
              <button onClick={closeModal}>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  width="24"
                  height="24"
                  color="#000000"
                  fill="none"
                >
                  <path
                    d="M19.0005 4.99988L5.00049 18.9999M5.00049 4.99988L19.0005 18.9999"
                    stroke="currentColor"
                    stroke-width="1.5"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </button>
              <button
                onClick={() => deleteOrder(selectedOrder.id)}
                className="modal-delete-btn"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
