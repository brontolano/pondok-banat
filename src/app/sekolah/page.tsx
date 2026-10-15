'use client';

import { useEffect, useState } from 'react';

interface Sekolah {
  id: string;
  kode: string;
  nama: string;
  jenjang: string;
  seksi: string;
}

export default function SekolahPage() {
  const [sekolah, setSekolah] = useState<Sekolah[]>([
    { id: '1', kode: 'Takhosous', nama: 'Takhosous', jenjang: 'Takhosous', seksi: '' },
    { id: '2', kode: '1A', nama: 'Kelas 1A', jenjang: '1', seksi: 'A' },
    { id: '3', kode: '1B', nama: 'Kelas 1B', jenjang: '1', seksi: 'B' },
    { id: '4', kode: '2A', nama: 'Kelas 2A', jenjang: '2', seksi: 'A' },
    { id: '5', kode: '2B', nama: 'Kelas 2B', jenjang: '2', seksi: 'B' },
  ]);
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
            <h2 className="card-title">Daftar Sekolah & Kelas</h2>
            <button className="btn btn-primary btn-sm">+ Tambah Sekolah</button>
          </div>
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>Kode</th>
                  <th>Nama</th>
                  <th>Jenjang</th>
                  <th>Seksio</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {sekolah.map((s) => (
                  <tr key={s.id}>
                    <td>{s.kode}</td>
                    <td>{s.nama}</td>
                    <td>{s.jenjang}</td>
                    <td>{s.seksi || '-'}</td>
                    <td>
                      <span className="badge badge-active">Aktif</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
