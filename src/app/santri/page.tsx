'use client';

import { useEffect, useState } from 'react';

export default function SantriPage() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => setLoading(false), 600);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
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
              <span className="text-sm text-gray-600">Admin</span>
              <button className="btn btn-secondary btn-sm">Logout</button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Data Santri</h2>
            <button className="btn btn-primary btn-sm">+ Tambah Santri</button>
          </div>
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>NISN</th>
                  <th>Nama</th>
                  <th>Jenis Kelamin</th>
                  <th>Kelas</th>
                  <th>Status</th>
                  <th>Aksi</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>26270136</td>
                  <td>ABUYA KH MUHAMMAD MUHYIDDIN MA</td>
                  <td>Laki-laki</td>
                  <td>Takhosous</td>
                  <td><span className="badge badge-inactive">Non-Aktif</span></td>
                  <td>
                    <button className="btn btn-sm btn-secondary">Detail</button>
                  </td>
                </tr>
                <tr>
                  <td>26270074</td>
                  <td>ADZKIA SAUFA SALSABILA</td>
                  <td>Perempuan</td>
                  <td>1A</td>
                  <td><span className="badge badge-inactive">Non-Aktif</span></td>
                  <td>
                    <button className="btn btn-sm btn-secondary">Detail</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div className="mt-6 card">
          <h3 className="text-sm font-bold text-gray-900 mb-4">Informasi Santri</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-gray-900">Total Santri</p>
                <p className="text-sm text-gray-500">Data Santri sekolah</p>
              </div>
              <span className="text-2xl font-bold text-gray-900">42</span>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-gray-900">Laki-laki</p>
                <p className="text-sm text-gray-500">Peserta didik</p>
              </div>
              <span className="text-2xl font-bold text-gray-900">20</span>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-gray-900">Perempuan</p>
                <p className="text-sm text-gray-500">Peserta didik</p>
              </div>
              <span className="text-2xl font-bold text-gray-900">22</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
