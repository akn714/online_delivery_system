'use client';

import { useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';
import { orderAPI } from '@/utils/api';
import { useAuth } from '@/context/AuthContext';

interface OrderItem {
  name: string;
  quantity: number;
  price: number;
}

interface StoredOrderData {
  name: string;
  phone: string;
  address: string;
  items: OrderItem[];
  subtotal: number;
  deliveryCharge: number;
  total: number;
}

export default function PaymentPage() {
  const router = useRouter();
  const { user } = useAuth();

  const [orderData, setOrderData] = useState<StoredOrderData | null>(null);
  const [transactionId, setTransactionId] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    if (typeof window === 'undefined') return;
    if (!user) {
      router.replace('/auth');
      return;
    }

    const rawData = sessionStorage.getItem('orderData');
    if (!rawData) {
      router.replace('/');
      return;
    }

    try {
      setOrderData(JSON.parse(rawData));
    } catch (_error) {
      sessionStorage.removeItem('orderData');
      router.replace('/');
    }
  }, [router, user]);

  const totalAmount = useMemo(() => orderData?.total ?? 0, [orderData]);

  const handlePlaceOrder = async () => {
    if (!user) {
      setError('Please login first to place an order.');
      router.push('/auth');
      return;
    }
    if (!orderData) return;
    if (!transactionId.trim()) {
      setError('Please enter transaction ID.');
      return;
    }

    setSubmitting(true);
    setError('');
    setSuccessMessage('');

    try {
      const { data } = await orderAPI.createOrder({
        name: orderData.name,
        phone: orderData.phone,
        address: orderData.address,
        items: orderData.items,
        transaction_id: transactionId.trim(),
        user_id: user?.id,
      });

      if (typeof window !== 'undefined') {
        sessionStorage.removeItem('orderData');
      }

      setSuccessMessage(`Order placed! ID: ${data.order_id} | OTP: ${data.otp}`);
      setTimeout(() => {
        router.push('/orders');
      }, 1200);
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to place order. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  if (!orderData) {
    return <div className="card">Loading payment details...</div>;
  }

  return (
    <div className="card max-w-2xl mx-auto">
      <h1 className="text-xl font-bold text-gray-900 mb-4">Payment</h1>

      <div className="bg-gray-50 rounded-lg p-4 mb-6">
        <p className="text-gray-700">Pay using UPI to:</p>
        <p className="font-semibold text-primary-700 mt-1">9919262161@ybl</p>
        <p className="text-lg font-bold mt-3">Total Amount: ₹{totalAmount}</p>
      </div>

      <div className="mb-4">
        <label className="label">Transaction ID *</label>
        <input
          type="text"
          className="input-field"
          value={transactionId}
          onChange={(event) => setTransactionId(event.target.value)}
          placeholder="Enter UPI transaction ID"
        />
      </div>

      {error && <p className="text-sm text-red-600 mb-3">{error}</p>}
      {successMessage && <p className="text-sm text-green-700 mb-3">{successMessage}</p>}

      <div className="flex gap-3">
        <button
          type="button"
          onClick={() => router.push('/')}
          className="btn-secondary"
          disabled={submitting}
        >
          Back
        </button>
        <button type="button" onClick={handlePlaceOrder} className="btn-primary" disabled={submitting}>
          {submitting ? 'Placing order...' : 'Place Order'}
        </button>
      </div>
    </div>
  );
}
