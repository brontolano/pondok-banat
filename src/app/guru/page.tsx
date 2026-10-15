'use client';

export default function GuruPage() {
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
            <h2 className="card-title">Data Guru & Staf</h2>
            <button className="btn btn-primary btn-sm">+ Tambah Guru</button>
          </div>
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>NIP</th>
                  <th>Nama</th>
                  <th>Jabatan</th>
                  <th>Kelas</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>M002</td>
                  <td>MUALLIM MUHAMMAD IDRIS ASY-SYAFI&apos;I</td>
                  <td>Guru</td>
                  <td>-</td>
                  <td><span className="badge badge-active">Aktif</span></td>
                </tr>
                <tr>
                  <td>M003</td>
                  <td>USTADZAH HJ. SYIFA ALAWIYAH KH</td>
                  <td>Wali Kelas</td>
                  <td>1A</td>
                  <td><span className="badge badge-active">Aktif</span></td>
                </tr>
                <tr>
                  <td>M010</td>
                  <td>USTADZAH HJ SALMA UMMU HABIBAH</td>
                  <td>Wali Kelas</td>
                  <td>1A</td>
                  <td><span className="badge badge-active">Aktif</span></td>
                </tr>
                <tr>
                  <td>M005</td>
                  <td>MUALLIM SYARIF MUHAMMAD ALHASANI</td>
                  <td>Wali Kelas</td>
                  <td>1A</td>
                  <td><span className="badge badge-active">Aktif</span></td>
                </tr>
                <tr>
                  <td>M013</td>
                  <td>USTADZAH HJ KHODIJAH ADILLATUL MILLAH</td>
                  <td>Wali Kelas</td>
                  <td>1A</td>
                  <td><span className="badge badge-active">Aktif</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
