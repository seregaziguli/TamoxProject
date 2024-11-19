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
    } catch (error) {
      setError(error.response ? error.response.data : error);
    }
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
            <p><strong>Title:</strong> {order.title}</p>
            <p><strong>Description:</strong> {order.description}</p>
            <p><strong>Service Type:</strong> {order.service_type_name}</p>
          </div>
        ))}
      </div>

      {selectedOrder && (
        <div className="order-details">
          <h2>Order Details</h2>
          <p><strong>Title:</strong> {selectedOrder.title}</p>
          <p><strong>Description:</strong> {selectedOrder.description}</p>
          <p><strong>Service Type:</strong> {selectedOrder.service_type_name}</p>
          <p><strong>Scheduled Date:</strong> {new Date(selectedOrder.scheduled_date).toLocaleString()}</p>
          <p><strong>Status:</strong> {selectedOrder.status}</p>
          {orderImage && <img src={orderImage} alt="Order Image" className="order-image" />}
        </div>
      )}
    </div>
  );
}
