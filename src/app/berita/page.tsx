'use client';

export default function BeritaPage() {
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
            <h2 className="card-title">Berita & Kegiatan</h2>
            <button className="btn btn-primary btn-sm">+ Posting Berita</button>
          </div>

          <div className="space-y-4">
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-bold text-gray-900">Kegiatan Bulan January 2026</h3>
                  <p className="text-sm text-gray-500">10 Januari 2026</p>
                </div>
                <span className="badge badge-wali">Kegiatan</span>
              </div>
              <p className="text-sm text-gray-600 mt-2">
                Mengadakan kegiatan i&apos;tikaf dan pembelajaran umum untuk seluruh santri selama 7 hari.
              </p>
            </div>

            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-bold text-gray-900">Ujian Semester 1</h3>
                  <p className="text-sm text-gray-500">15 Januari 2026</p>
                </div>
                <span className="badge badge-guru">Peserta</span>
              </div>
              <p className="text-sm text-gray-600 mt-2">
                Ujian tengah semester untuk seluruh jenjang klas.
              </p>
            </div>

            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-bold text-gray-900">Peringatan Bagi Santri</h3>
                  <p className="text-sm text-gray-500">08 Januari 2026</p>
                </div>
                <span className="badge badge-warning">Peringatan</span>
              </div>
              <p className="text-sm text-gray-600 mt-2">
                Peringatan kepada santri yang belum memenuhi persyaratan kehadiran.
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
