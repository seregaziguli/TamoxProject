import React, { useState } from "react";
import axios from "axios";

export default function Order() {
  const [orderForm, setOrderForm] = useState({
    description: "",
    serviceTypeName: "",
    scheduledDate: "",
  });

  const onChangeForm = (label, event) => {
    setOrderForm({ ...orderForm, [label]: event.target.value });
  };

  const onSubmitHandler = async (event) => {
    event.preventDefault();

    const orderData = {
      description: orderForm.description,
      service_type_name: orderForm.serviceTypeName, 
      scheduled_date: new Date(orderForm.scheduledDate).toISOString(), 
    };

    try {
      const auth_token = localStorage.getItem("access_token");

      const response = await axios.post(
        "http://localhost:8007/orders",
        orderData,
        {
          headers: {
            "Content-Type": "application/json",
            "access-token": auth_token,
          },
        }
      );
      console.log("Order created successfully:", response.data);
    } catch (error) {
      console.error(
        "Error creating order:",
        error.response ? error.response.data : error
      );
    }
  };

  return (
    <div className="mt-6 ml-6">
      <div className="text-3xl mb-2">New Order</div>

      <form onSubmit={onSubmitHandler}>
        <div className="space-y-3">
          <textarea
            type="text"
            placeholder="Order Description"
            className="block text-sm py-2 px-4 mt-5 h-40 w-72 tracking-wider font-normal rounded-lg border outline-none"
            value={orderForm.description}
            onChange={(e) => onChangeForm("description", e)}
          ></textarea>

          <input
            type="text"
            placeholder="Service Type Name"
            className="block text-sm py-2 px-4 tracking-wider w-72 font-normal rounded-lg border outline-none"
            value={orderForm.serviceTypeName}
            onChange={(e) => onChangeForm("serviceTypeName", e)}
          ></input>

          <input
            type="datetime-local"
            placeholder="Scheduled Date"
            className="block text-sm py-2 px-4 tracking-wider w-72 font-normal rounded-lg border outline-none"
            value={orderForm.scheduledDate}
            onChange={(e) => onChangeForm("scheduledDate", e)}
          ></input>

          <button
            className="order-btn text-xl hover:bg-blue-600 text-white bg-blue-500 px-4 py-2 rounded-lg mt-5"
            type="submit"
          >
            Create
          </button>
        </div>
      </form>
    </div>
  );
}