'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { itemsCatalog, DELIVERY_CHARGE, HOSTEL_OPTIONS } from '@/data/items';
import { orderAPI } from '@/utils/api';

interface SelectedItem {
  name: string;
  quantity: number;
  price: number;
  unit: string;
}

export default function HomePage() {
  const router = useRouter();
  const { user } = useAuth();
  const [selectedItems, setSelectedItems] = useState<{ [key: string]: SelectedItem }>({});
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: user?.name || '',
    phone: user?.phone || '',
    address: '',
  });

  const subtotal = Object.values(selectedItems).reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );
  const total = subtotal + DELIVERY_CHARGE;

  const handleItemToggle = (category: string, itemName: string, price: number, unit: string) => {
    const key = `${category}-${itemName}`;
    setSelectedItems((prev) => {
      if (prev[key]) {
        const { [key]: _, ...rest } = prev;
        return rest;
      }
      return {
        ...prev,
        [key]: { name: itemName, quantity: 1, price, unit },
      };
    });
  };

  const handleQuantityChange = (key: string, quantity: number) => {
    if (quantity < 1) return;
    setSelectedItems((prev) => ({
      ...prev,
      [key]: { ...prev[key]!, quantity },
    }));
  };

  const handleProceedToPayment = () => {
    if (!formData.name || !formData.phone || !formData.address) {
      alert('Please fill all customer details');
      return;
    }
    if (Object.keys(selectedItems).length === 0) {
      alert('Please select at least one item');
      return;
    }
    // Store form data and selected items in sessionStorage for payment page
    if (typeof window !== 'undefined') {
      sessionStorage.setItem('orderData', JSON.stringify({
        ...formData,
        items: Object.values(selectedItems),
        subtotal,
        deliveryCharge: DELIVERY_CHARGE,
        total,
      }));
    }
    router.push('/payment');
  };

  return (
    <div>
      {/* Customer Details Card */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">📋 Customer Details</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="label">Full Name *</label>
            <input
              type="text"
              className="input-field"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="Enter your name"
            />
          </div>
          <div>
            <label className="label">Phone Number *</label>
            <input
              type="tel"
              className="input-field"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              placeholder="Enter phone number"
            />
          </div>
        </div>
        <div className="mt-4">
          <label className="label">Delivery Address *</label>
          <select
            className="input-field"
            value={formData.address}
            onChange={(e) => setFormData({ ...formData, address: e.target.value })}
          >
            <option value="">Select Hostel</option>
            {HOSTEL_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Items Section */}
      {Object.entries(itemsCatalog).map(([category, items]) => (
        <div key={category} className="card">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">🛍️ {category}</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {items.map((item) => {
              const key = `${category}-${item.name}`;
              const isSelected = !!selectedItems[key];
              return (
                <div
                  key={key}
                  onClick={() => handleItemToggle(category, item.name, item.price, item.unit)}
                  className={`p-3 border-2 rounded-lg cursor-pointer transition-all ${
                    isSelected
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={() => {}}
                        className="w-4 h-4 text-primary-600"
                      />
                      <span className="font-medium text-gray-800">{item.name}</span>
                    </div>
                    <span className="text-primary-600 font-semibold">₹{item.price}</span>
                  </div>
                  <div className="flex items-center justify-between mt-2">
                    <span className="text-sm text-gray-500">per {item.unit}</span>
                    {isSelected && (
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleQuantityChange(key, selectedItems[key].quantity - 1);
                          }}
                          className="w-6 h-6 bg-gray-200 rounded flex items-center justify-center"
                        >
                          -
                        </button>
                        <span className="w-8 text-center">{selectedItems[key].quantity}</span>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleQuantityChange(key, selectedItems[key].quantity + 1);
                          }}
                          className="w-6 h-6 bg-gray-200 rounded flex items-center justify-center"
                        >
                          +
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ))}

      {/* Order Summary */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">📝 Order Summary</h2>
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex justify-between py-2">
            <span className="text-gray-600">Subtotal</span>
            <span className="font-medium">₹{subtotal}</span>
          </div>
          <div className="flex justify-between py-2">
            <span className="text-gray-600">Delivery Charges</span>
            <span className="font-medium">₹{DELIVERY_CHARGE}</span>
          </div>
          <div className="flex justify-between py-2 border-t border-gray-200 mt-2">
            <span className="font-semibold text-lg">Total</span>
            <span className="font-semibold text-lg text-primary-600">₹{total}</span>
          </div>
        </div>
      </div>

      {/* Proceed Button */}
      <button
        onClick={handleProceedToPayment}
        className="btn-primary"
        disabled={loading}
      >
        {loading ? 'Processing...' : 'Proceed to Payment'}
      </button>
    </div>
  );
}