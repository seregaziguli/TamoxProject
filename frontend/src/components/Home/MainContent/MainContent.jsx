import React, { useState, useEffect } from "react";
import axios from "axios";
import OrderCard from "../OrderCard/OrderCard";
import OrderDetailModal from "../OrderDetailModal/OrderDetailModal";

export default function MainContent() {
  const [orders, setOrders] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    async function fetchOrders() {
      try {
        const auth_token = localStorage.getItem("access_token");
        const response = await axios.get("http://localhost:8007/orders/all", {
          headers: {
            "Content-Type": "application/json",
            "access-token": auth_token,
          },
        });
        setOrders(response.data);
      } catch (error) {
        const errorMessage =
          error.response?.data?.message || error.message || "Unknown error occurred";
        setError(errorMessage);
      } finally {
        setIsLoading(false);
      }
    }

    fetchOrders();
  }, []);

  const handleOrderClick = async (orderId) => {
    if (!orderId) {
      console.error("Invalid orderId");
      return;
    }

    try {
      const auth_token = localStorage.getItem("access_token");
      const response = await axios.post(
        `http://localhost:8007/orders/${orderId}/process`,
        {},
        {
          headers: {
            "Content-Type": "application/json",
            "access-token": auth_token,
          },
        }
      );
      console.log("Order processed successfully:", response.data);
    } catch (error) {
      const errorMessage =
        error.response?.data?.message || error.message || "Failed to process order";
      console.error("Error processing order:", errorMessage);
    }
  };

  const openModal = (order) => {
    setSelectedOrder(order);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedOrder(null);
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div className="text-red-500">Error: {error}</div>;
  }

  return (
    <div className="w-full flex justify-center">
      <div className="orders-list mt-6">
        <h1 className="text-3xl mb-2">Orders</h1>
        <div className="grid grid-cols-1 gap-4">
          {Array.isArray(orders) && orders.length > 0 ? (
            orders.map((order) => (
              <OrderCard
                key={order.id}
                order={order}
                onProcess={handleOrderClick}
                onOpenModal={openModal}
              />
            ))
          ) : (
            <div>No orders found.</div>
          )}
        </div>

        {isModalOpen && selectedOrder && (
          <OrderDetailModal order={selectedOrder} onClose={closeModal} />
        )}
      </div>
    </div>
  );
}
