import React from "react";

export default function OrderCard({ order, onProcess, onOpenModal }) {
  return (
    <div className="order-card p-4 bg-gray-200 rounded-lg">
      {order.image_url && (
        <img
          src={order.image_url}
          alt="Order Thumbnail"
          className="w-16 h-16 object-cover rounded-lg mb-2"
        />
      )}
      <h2 className="text-xl font-bold">{order.description}</h2>
      <p>Service Type: {order.service_type_name}</p>
      <p>Scheduled Date: {new Date(order.scheduled_date).toLocaleString()}</p>
      <p>Status: {order.status}</p>
      <div className="flex justify-between mt-2">
        <button
          className="order-btn text-lg hover:bg-blue-600 text-white bg-blue-500 px-4 py-2 rounded-lg"
          onClick={() => onProcess(order.id)}
        >
          Process Order
        </button>
        <button
          className="order-btn text-lg hover:bg-green-600 text-white bg-green-500 px-4 py-2 rounded-lg"
          onClick={() => onOpenModal(order)}
        >
          View Details
        </button>
      </div>
    </div>
  );
}
