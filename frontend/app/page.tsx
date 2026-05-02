'use client';

import { useEffect, useState } from 'react';
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

const ITEM_IMAGE_MAP: Record<string, string> = {
  'White Bread': 'white_bread_metro_gold.png',
  'Bhuja Chana': 'roasted_chana_250gm.jpg',
  'Maggie (Small - 75g)': 'maggie_small_packet.jpg',
  'Maggie (Family Pack - 400g)': 'maggie_family_pack.jpg',
  'Moongfali': 'moongfali_peanut_250gm.jpg',
  'Soyabean (Packet)': 'soyachunks_fortune_packet.jpg',
  'Soyabean (Open - Small)': 'soyabean_chunks_open_250gm.jpeg',
  'Macaroni / Pasta': 'fusli_pasta_microni_250gm.jpeg',
  'Sugar (Chini)': 'suger_chini_250gm.jpg',
  'Glucose D (200g)': 'glucose_d_small.jpg',
  'Glucose D (400g)': 'glucose_d_large.jpeg',
  'Jam (Small)': 'kissan_mixed_fruit_jam_small.jpeg',
  'Jam (Big)': 'kissan_mixed_fruit_jam_large.jpeg',
  'Colgate (Small)': 'colgate_toothpaste_small.jpg',
  'Colgate (Medium)': 'colgate_toothpaste_large.webp',
  'Colgate (Big)': 'colgate_toothpaste_large.webp',
  'Closeup (Small)': 'close_up_toothpaste.jpg',
  'Closeup (Big)': 'close_up_toothpaste.jpg',
  'Sensodyne Toothpaste': 'sensodine_toothpaste.jpeg',
  'Coffee (Nescafe - 50g)': 'nescafe_coffee_small_packet.webp',
  'Coffee (Nescafe - 100g)': 'nescafe_coffee_medium.jpg',
  'Coffee (Nescafe - 200g)': 'nescafe_coffee_large.jpeg',
  'Mustard Oil (Sarso Tel)': 'sarso_tel_sudhh_ghani_1kg.jpg',
  'Fortune Oil': 'sarso_tel_fortune_1kg.jpg',
  'Garam Masala (Whole)': 'khada_garam_masala_packet.jpeg',
  'Garam Masala (Packet)': 'khada_garam_masala_packet.jpeg',
  'Kacha Chana': 'kacha_chana_250gm.jpg',
  'Makhana': 'makhana_100gm.jpeg',
  'Kaju (Cashew)': 'kaju_100gm.jpg',
  'Pista (Packet)': 'fresh_ pista_packet.jpg',
  'Badam (Almond)': 'badam_100gm.jpg',
  'Practical File (Physics - 30 Pages)': 'practical_file_physics.jpg',
  'Practical File (Physics - 60 Pages)': 'practical_file_physics.jpg',
  'Practical File (Chemistry - 30 Pages)': 'practical_file_chemistry.jpg',
  'Practical File (Chemistry - 60 Pages)': 'practical_file_chemistry.jpg',
  'Practical File (General - 30 Pages)': 'practical_file_general.jpeg',
  'Practical File (General - 60 Pages)': 'practical_file_general.jpeg',
  'Drawing Book (A3 - 36 pages)': 'engineering_drawing_36page.jpg',
  'Drawing Book (A3 - 56 pages)': 'engineering_drawing_56page.jpg',
  'Pen (Cheap)': 'elkos_pen_4rupees.jpg',
  'Pen (Medium)': 'elkos_pen_5rupees.jpg',
  'Pen (Good)': 'elkos_pen_10rupees.jpg',
  'Pencil': 'natraj_pencil.png',
  'Eraser': 'eraser_apsara.jpg',
  'Sharpener': 'pencil_sharpner_plastic.jpg',
  'A4 Size Pages (500 sheets)': 'a4_size_paper_500pages.jpg',
  'Stapler': 'stapler.jpg',
  'Staple Pins': 'staples_pin_box.jpeg',
  'Sticky Notes': 'sticky_notes_small_packet.jpeg',
  'Fevicol (Small)': 'fevicol_small.jpg',
  'Fevicol (Medium)': 'fevicol_small.jpg',
  'Fevicol (Big)': 'fevicol_small.jpg',
  'Double-Sided Tape (Small)': 'cello_tape_small.jpeg',
  'Double-Sided Tape (Big)': 'cello_tape_small.jpeg',
  'Spiral Notebook (Plain - 100 Pages)': 'spiral_notebook_100pg.jpg',
  'Spiral Notebook (Plain - 200 Pages)': 'spiral_notebook_200pg.jpeg',
  'Spiral Notebook (Lined - 100 Pages)': 'spiral_notebook_100pg.jpg',
  'Register (A4 Rough - 100 Pages)': 'register_a4_rough.jpg',
  'Register (A4 Rough - 200 Pages)': 'register_a4_rough_a4.jpg',
  'Graph Book': 'graph_book.jpg',
  'Cello Tape': 'cello_tape_small.jpeg',
  'Highlighter': 'highlighter.jpeg',
  'Banana': 'fresh_bannana_500gm.webp',
  'Pomegranate (Anaar)': 'pomegranate_anar_500gm.jpg',
  'Mango': 'mango_aam_500gm.jpg',
  'Apple': 'fresh_apple_500gm.jpg',
  'Orange (Santara)': 'orange_santara_500gm.jpg',
  'Papaya (Papita)': 'fresh_papaya_1kg.jpg',
  'Kiwi': 'fresh_kiwi_1piece.jpg',
  'Coconut (Nariyal)': 'nariyal_water.webp',
  'Grapes (Angoor)': 'fresh_angoor_250gm.jpg',
  'Eggs (30 pieces)': 'eggs_tray_30_piece_180rupees.jpg',
  'Raw Chicken (500g)': 'raw_chicken_500gm_120rupees.jpg',
};

const buildImagePath = (fileName: string) => `/Item%20Images/${encodeURIComponent(fileName)}`;

const toSlug = (value: string) =>
  value
    .toLowerCase()
    .replace(/\(.*?\)/g, '')
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '');

function ItemImage({ itemName }: { itemName: string }) {
  const mapped = ITEM_IMAGE_MAP[itemName];
  const slug = toSlug(itemName);
  const candidates = [
    mapped,
    `${slug}.jpg`,
    `${slug}.jpeg`,
    `${slug}.png`,
    `${slug}.webp`,
  ].filter((value, index, array): value is string => Boolean(value) && array.indexOf(value) === index);

  const [candidateIndex, setCandidateIndex] = useState(0);
  const [failed, setFailed] = useState(candidates.length === 0);

  if (failed) {
    return (
      <div className="w-14 h-14 rounded-md bg-gray-100 flex items-center justify-center text-xl">
        🛍️
      </div>
    );
  }

  return (
    <img
      src={buildImagePath(candidates[candidateIndex])}
      alt={itemName}
      className="w-14 h-14 rounded-md object-cover border border-gray-200 bg-white"
      loading="lazy"
      onError={() => {
        if (candidateIndex < candidates.length - 1) {
          setCandidateIndex((prev) => prev + 1);
          return;
        }
        setFailed(true);
      }}
    />
  );
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

  useEffect(() => {
    if (user) {
      setFormData((prev) => ({
        ...prev,
        name: user.name || prev.name,
        phone: user.phone || prev.phone,
      }));
    }
  }, [user]);

  const subtotal = Object.values(selectedItems).reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );
  const LAUNCH_DATE = '2026-05-03';
  const isLaunchDay = typeof window === 'undefined'
    ? false
    : new Date().toISOString().slice(0, 10) === LAUNCH_DATE;
  const deliveryCharge = isLaunchDay ? 0 : DELIVERY_CHARGE;
  const total = subtotal + deliveryCharge;

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
    if (!user) {
      alert('Please login first to place an order.');
      router.push('/auth');
      return;
    }
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
        deliveryCharge,
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
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            {category === "Non-Veg" ? "🥩" : "🛍️"} {category}
          </h2>
          {category === "Non-Veg" && (
            <div className="mb-4 p-3 bg-orange-50 border border-orange-200 rounded-lg">
              <p className="text-sm text-orange-800 font-medium">
                📦 Delivery of non-vegetarian products will be made separately at 5:30 PM.
              </p>
            </div>
          )}
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
                    <div className="flex items-center space-x-3">
                      <ItemImage itemName={item.name} />
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
            <span className="font-medium">₹{deliveryCharge}</span>
          </div>
          <div className="flex justify-between py-2 border-t border-gray-200 mt-2">
            <span className="font-semibold text-lg">Total</span>
            <span className="font-semibold text-lg text-primary-600">₹{total}</span>
          </div>
        </div>

        {isLaunchDay && (
          <div className="mt-4 rounded-lg border border-green-200 bg-green-50 p-4 text-green-900">
            <p className="text-sm font-semibold">🎉 Delivery free for today</p>
            <p className="text-sm text-green-800">Sunday launch offer: enjoy zero delivery charges on all orders.</p>
          </div>
        )}
      </div>

      {/* Proceed Button */}
      {!user && (
        <p className="text-sm text-amber-700 mb-3">
          Login is required before proceeding to payment.
        </p>
      )}
      <button
        onClick={handleProceedToPayment}
        className="btn-primary"
        disabled={loading || !user}
      >
        {!user ? 'Login to Continue' : loading ? 'Processing...' : 'Proceed to Payment'}
      </button>
    </div>
  );
}