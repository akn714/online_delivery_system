'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { configAPI } from '@/utils/api';
import { HOSTEL_OPTIONS } from '@/data/items';

interface CartItem {
  name: string;
  quantity: number;
  price: number;
  unit: string;
}

interface ProfileData {
  name: string;
  phone: string;
}

const getSavedHostel = () => {
  if (typeof window === 'undefined') return '';
  return localStorage.getItem('delivery_hostel') || '';
};

const normalizeCart = (value: string | null) => {
  if (!value) return {};

  try {
    const parsed = JSON.parse(value);
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) return {};

    return Object.entries(parsed).reduce<Record<string, CartItem>>((acc, [key, item]) => {
      const cartItem = item as Partial<CartItem>;
      const quantity = Number(cartItem.quantity);
      const price = Number(cartItem.price);

      if (
        typeof key === 'string' &&
        typeof cartItem.name === 'string' &&
        typeof cartItem.unit === 'string' &&
        Number.isFinite(quantity) &&
        quantity > 0 &&
        Number.isFinite(price)
      ) {
        acc[key] = {
          name: cartItem.name,
          quantity,
          price,
          unit: cartItem.unit,
        };
      }

      return acc;
    }, {});
  } catch {
    return {};
  }
};

export default function CartPage() {
  const router = useRouter();
  const { user } = useAuth();

  const [cartItems, setCartItems] = useState<Record<string, CartItem>>({});
  const [profile, setProfile] = useState<ProfileData>({ name: '', phone: '' });

  const [selectedHostel, setSelectedHostel] = useState('');
  const [deliveryCharge, setDeliveryCharge] = useState(9);

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [cartHydrated, setCartHydrated] = useState(false);
  const [checkoutError, setCheckoutError] = useState('');

  useEffect(() => {
    if (typeof window === 'undefined') return;

    setCartItems(normalizeCart(localStorage.getItem('delivery_cart')));
    setSelectedHostel(getSavedHostel());

    const savedProfile = localStorage.getItem('delivery_profile');
    if (savedProfile) {
      try {
        setProfile(JSON.parse(savedProfile));
      } catch {
        localStorage.removeItem('delivery_profile');
      }
    }

    setCartHydrated(true);
  }, []);

  useEffect(() => {
    async function loadConfig() {
      try {
        const { data } = await configAPI.getConfig();
        setDeliveryCharge(data.data.delivery_charge);
      } catch (error) {
        console.error('Failed to load config:', error);
      } finally {
        setLoading(false);
      }
    }

    loadConfig();
  }, []);

  useEffect(() => {
    if (typeof window === 'undefined' || !cartHydrated) return;
    localStorage.setItem('delivery_cart', JSON.stringify(cartItems));
    window.dispatchEvent(new Event('delivery_cart_updated'));
  }, [cartHydrated, cartItems]);

  const cartEntries = Object.entries(cartItems);

  const subtotal = useMemo(
    () => cartEntries.reduce((sum, [, item]) => sum + item.price * item.quantity, 0),
    [cartEntries]
  );

  const total = subtotal + deliveryCharge;

  const handleQuantityChange = (key: string, quantity: number) => {
    if (quantity < 1) return;
    setCartItems((prev) => ({
      ...prev,
      [key]: { ...prev[key], quantity },
    }));
  };

  const handleRemoveItem = (key: string) => {
    setCartItems((prev) => {
      const { [key]: _removed, ...rest } = prev;
      return rest;
    });
  };

  const handleHostelChange = (value: string) => {
    setSelectedHostel(value);
    localStorage.setItem('delivery_hostel', value);
    if (value) setCheckoutError('');
  };

  const handleProceedToPayment = () => {
    if (cartEntries.length === 0) return;

    if (!selectedHostel) {
      setCheckoutError('Please select your hostel before checkout.');
      return;
    }

    const resolvedProfile = {
      name: profile.name || user?.name || '',
      phone: profile.phone || user?.phone || '',
      address: selectedHostel,
    };

    if (typeof window !== 'undefined') {
      localStorage.setItem('delivery_hostel', selectedHostel);
      sessionStorage.setItem(
        'orderData',
        JSON.stringify({
          ...resolvedProfile,
          items: cartEntries.map(([, item]) => item),
          subtotal,
          deliveryCharge,
          total,
        })
      );
    }

    setSubmitting(true);
    setCheckoutError('');
    router.push('/payment');
  };

  return (
    <div className="space-y-4 md:space-y-6">

      <div className="card shadow-sm">
        <h1 className="text-xl font-extrabold md:text-2xl">Your Cart</h1>
        <p className="mt-1 text-xs text-[var(--text-muted)] md:text-sm">
          Review selected items and continue to payment.
        </p>
      </div>

      {!loading && cartEntries.length === 0 && (
        <div className="card py-10 text-center">
          <p className="text-[var(--text-muted)]">Your cart is empty.</p>
          <Link href="/" className="btn-primary mt-4 inline-flex">
            Go Shopping
          </Link>
        </div>
      )}

      {!loading && cartEntries.length > 0 && (
        <div className="grid gap-4 lg:grid-cols-[1fr_360px]">

          {/* CART ITEMS */}
          <div className="space-y-3">
            {cartEntries.map(([key, item]) => (
              <div key={key} className="card">
                <div className="flex justify-between">
                  <h3 className="font-bold">{item.name}</h3>
                  <button onClick={() => handleRemoveItem(key)}>Remove</button>
                </div>

                <div className="flex justify-between mt-2">
                  <div className="flex gap-2 items-center">
                    <button onClick={() => handleQuantityChange(key, item.quantity - 1)}>-</button>
                    <span>{item.quantity}</span>
                    <button onClick={() => handleQuantityChange(key, item.quantity + 1)}>+</button>
                  </div>

                  <span className="font-bold">Rs. {item.price * item.quantity}</span>
                </div>
              </div>
            ))}
          </div>

          {/* SUMMARY */}
          <div className="card sticky top-24 space-y-4">

            <h2 className="text-xl font-bold">Order Summary</h2>

            <div className="space-y-2 text-sm">

              <div className="flex justify-between">
                <span>Subtotal</span>
                <span>Rs. {subtotal}</span>
              </div>

              <div className="flex justify-between">
                <span>Delivery Fee</span>
                <span>Rs. {deliveryCharge}</span>
              </div>

              {/* HOSTEL SELECT */}
              <div className="space-y-1">
                <label className="text-sm font-semibold">Select Hostel</label>
                <select
                  value={selectedHostel}
                  onChange={(e) => handleHostelChange(e.target.value)}
                  className="w-full border rounded p-2"
                >
                  <option value="">-- Select Hostel --</option>
                  {HOSTEL_OPTIONS.map((h) => (
                    <option key={h.value} value={h.value}>
                      {h.label}
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex justify-between font-bold border-t pt-2">
                <span>Total</span>
                <span className="text-[var(--primary)]">Rs. {total}</span>
              </div>

            </div>

            {checkoutError && (
              <p className="text-red-600 text-sm">{checkoutError}</p>
            )}

            <button
              onClick={handleProceedToPayment}
              disabled={submitting}
              className="btn-primary w-full"
            >
              {submitting ? 'Processing...' : 'Proceed to Payment'}
            </button>

            <Link href="/" className="btn-outline block text-center">
              Continue Shopping
            </Link>

          </div>
        </div>
      )}
    </div>
  );
}