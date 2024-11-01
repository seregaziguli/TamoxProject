import React, { useState, useEffect } from "react";
import axios from "axios";
import Select from "react-select";
import { useSpring, animated } from "react-spring"; 
import "./MyProfile.css";

export default function MyProfile() {
  const [orders, setOrders] = useState([]);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchOrders() {
      try {
        const auth_token = localStorage.getItem("access_token");
        const response = await axios.get("http://localhost:8002/orders", {
          headers: {
            "Content-Type": "application/json",
            "access-token": auth_token,
          },
        });
        setOrders(response.data);
        setIsLoading(false);
        console.log(response);
      } catch (error) {
        setError(error.response ? error.response.data : error);
        setIsLoading(false);
      }
    }

    fetchOrders();
  }, []);

  const animationProps = useSpring({
    opacity: selectedOrder ? 1 : 0,
    transform: selectedOrder ? "translateY(0)" : "translateY(-20px)",
  });
 
  const orderOptions = orders.map((order) => ({
    value: order.id,
    label: `Order #${order.id} - ${order.description}`,
  }));

  const handleOrderChange = (selectedOption) => {
    const order = orders.find((o) => o.id === selectedOption.value);
    setSelectedOrder(order);
  };

  return (
    <div className="my-profile-container">
      <h1 className="text-2xl mb-4">My Orders</h1>
      {isLoading ? (
        <div>Loading...</div>
      ) : error ? (
        <div>Error: {error}</div>
      ) : (
        <>
          <Select
            className="order-select"
            options={orderOptions}
            onChange={handleOrderChange}
            placeholder="Select an order..."
            isClearable
          />

          {selectedOrder && (
            <animated.div style={animationProps} className="order-details">
              <h2 className="text-xl font-bold">Order Details</h2>
              <p>
                <strong>Service Type:</strong> {selectedOrder.service_type_name}
              </p>
              <p>
                <strong>Address:</strong> {selectedOrder.address.street}, {selectedOrder.address.city}, {selectedOrder.address.zip_code}
              </p>
              <p>
                <strong>Scheduled Date:</strong>{" "}
                {new Date(selectedOrder.scheduled_date).toLocaleString()}
              </p>
              <p>
                <strong>Status:</strong> {selectedOrder.status}
              </p>
            </animated.div>
          )}
        </>
      )}
    </div>
  );
}