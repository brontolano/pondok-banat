'use client';

import { useEffect, useState } from 'react';

interface DashboardStats {
  totalSantri: number;
  totalGuru: number;
  totalKelas: number;
  terbaru: string;
}

export default function Beranda() {
  const [stats, setStats] = useState<DashboardStats>({
    totalSantri: 0,
    totalGuru: 0,
    totalKelas: 0,
    terbaru: '-',
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In MVP, static data
    // In production, this would be a real API call
    setTimeout(() => {
    setStats({
      totalSantri: 453,
      totalGuru: 54,
      totalKelas: 18,
        terbaru: 'Kegiatan Sekarang',
      });
      setLoading(false);
    }, 500);
  }, []);

  const navItems = [
    { icon: '🏫', label: 'Sekolah', path: '/sekolah' },
    { icon: '👧', label: 'Santri', path: '/santri' },
    { icon: '👩‍🏫', label: 'Guru & Staf', path: '/guru' },
    { icon: '📚', label: 'Kurikulum', path: '/kelas' },
    { icon: '📝', label: 'Nilai & Absensi', path: '/nilai' },
    { icon: '📊', label: 'Laporan', path: '/laporan' },
    { icon: '📢', label: 'Kegiatan', path: '/ruang-kegiatan' },
    { icon: '👨‍👩‍👧', label: 'Wali', path: '/pengasuh' },
    { icon: '🔔', label: 'Berita', path: '/berita' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <h1 className="text-lg font-bold text-gray-900">Pondok Banat</h1>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">
                Selamat Datang, Admin
              </span>
              <button className="btn btn-secondary btn-sm">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                <span className="text-2xl">👧</span>
              </div>
              <div>
                <p className="text-sm text-gray-500">Total Santri</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalSantri}</p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                <span className="text-2xl">👩‍🏫</span>
              </div>
              <div>
                <p className="text-sm text-gray-500">Guru & Staf</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalGuru}</p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-yellow-100 rounded-xl flex items-center justify-center">
                <span className="text-2xl">📚</span>
              </div>
              <div>
                <p className="text-sm text-gray-500">Kelas</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalKelas}</p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
                <span className="text-2xl">📝</span>
              </div>
              <div>
                <p className="text-sm text-gray-500">Data Terbaru</p>
                <p className="text-2xl font-bold text-gray-900 truncate">{stats.terbaru}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Navigation */}
        <div className="card">
          <div className="flex items-center gap-3 mb-6">
            <h2 className="text-lg font-bold text-gray-900">Menu Quick</h2>
            <span className="text-sm text-gray-400">|</span>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
            {navItems.map((item) => (
              <button
                key={item.path}
                className="flex flex-col items-center gap-2 p-4 rounded-xl border border-gray-200 hover:border-primary hover:bg-primary/5 transition-all group"
              >
                <span className="text-2xl">{item.icon}</span>
                <span className="text-sm font-medium text-gray-700 group-hover:text-primary transition">
                  {item.label}
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
          <div className="card">
            <h3 className="text-sm font-bold text-gray-900 mb-4">Aksi Cepat</h3>
            <div className="grid grid-cols-2 gap-3">
              <button className="btn btn-primary btn-sm">
                + Tambah Santri
              </button>
              <button className="btn btn-success btn-sm">
                + Input Nilai
              </button>
              <button className="btn btn-secondary btn-sm">
                📋 Daftar Kelas
              </button>
              <button className="btn btn-secondary btn-sm">
                📊 Laporan Bulanan
              </button>
            </div>
          </div>

          <div className="card">
            <h3 className="text-sm font-bold text-gray-900 mb-4">Status Terbaru</h3>
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <span className="badge badge-wali">Wali Kelas 1A</span>
                <span className="text-sm text-gray-600">Mempelajari KBM</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="badge badge-pengasuh">Wali Orang Tua</span>
                <span className="text-sm text-gray-600">Menerima informasi nilai</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="badge badge-guru">Guru Mekanik</span>
                <span className="text-sm text-gray-600">Mempersiapkan silabus</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="badge badge-admin">Admin</span>
                <span className="text-sm text-gray-600">Mengelola data sekolah</span>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
