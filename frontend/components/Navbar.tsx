'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';

export default function Navbar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  const isActive = (path: string) => pathname === path ? 'text-primary-600' : 'text-gray-600';

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 max-w-4xl">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-2xl">🛒</span>
            <span className="font-bold text-xl text-gray-900">Rocket07</span>
          </Link>

          <div className="flex items-center space-x-6">
            <Link href="/" className={`hover:text-primary-600 transition-colors ${isActive('/')}`}>
              New Order
            </Link>
            <Link href="/orders" className={`hover:text-primary-600 transition-colors ${isActive('/orders')}`}>
              Your Orders
            </Link>
            
            {user ? (
              <div className="flex items-center space-x-3">
                <span className="text-sm text-gray-600">Hi, {user.name}</span>
                <button
                  onClick={logout}
                  className="px-3 py-1.5 text-sm bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
                >
                  Logout
                </button>
              </div>
            ) : (
              <Link
                href="/auth"
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                Login
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}