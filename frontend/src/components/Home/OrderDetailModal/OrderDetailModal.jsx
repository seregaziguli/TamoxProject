import React from "react";

export default function OrderDetailModal({ order, onClose }) {
  return (
    <div className="modal-overlay fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div className="modal-content bg-white p-6 rounded-lg shadow-lg animate-fade-in">
        <h2 className="text-2xl mb-4">Order Details</h2>
        <p><strong>Description:</strong> {order.description}</p>
        <p><strong>Service Type:</strong> {order.service_type_name}</p>
        <p><strong>Address:</strong> {order.address.street}, {order.address.city}, {order.address.zip_code}</p>
        <p><strong>Scheduled Date:</strong> {new Date(order.scheduled_date).toLocaleString()}</p>
        <p><strong>Status:</strong> {order.status}</p>

        <div className="flex justify-end mt-4">
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
            onClick={() => {
             
              console.log(`Confirmed order: ${order.id}`);
              onClose(); 
            }}
          >
            Confirm Order
          </button>
          <button
            className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600 ml-2"
            onClick={onClose}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}