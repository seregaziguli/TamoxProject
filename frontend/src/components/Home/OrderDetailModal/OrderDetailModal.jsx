import React, { useState, useEffect } from "react";

export default function OrderDetailModal({ order, onClose }) {
  const [orderImage, setOrderImage] = useState(order.image_url || "");

  useEffect(() => {
    if (order.image_url) {
      fetchImage(order.image_url).then((fetchedUrl) => {
        setOrderImage(fetchedUrl);
      });
    }
  }, [order.image_url]);

  const fetchImage = async (imageUrl) => {
    try {
      const response = await axios.get(`http://localhost:8007/get_image`, {
        params: { url: imageUrl },
      });
      return response.data.image_url;
    } catch (error) {
      console.error("Error fetching image:", error.response || error);
      return null;
    }
  };

  return (
    <div className="modal-overlay fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div className="modal-content bg-white p-6 rounded-lg shadow-lg animate-fade-in">
        <h2 className="text-2xl mb-4">Order Details</h2>
        <p><strong>Description:</strong> {order.description}</p>
        <p><strong>Service Type:</strong> {order.service_type_name}</p>
        <p><strong>Scheduled Date:</strong> {new Date(order.scheduled_date).toLocaleString()}</p>
        <p><strong>Status:</strong> {order.status}</p>

        {orderImage && (
          <div className="mt-4">
            <strong>Image:</strong>
            <img
              src={orderImage}
              alt="Order Illustration"
              className="mt-2 max-w-full h-auto"
            />
          </div>
        )}

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
