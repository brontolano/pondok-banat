import './globals.css';

export const metadata = {
  title: 'Pondok Banat | Aplikasi Persekolahan',
  description: 'Platform Manajemen Pondok Banat - Administrasi, Kurikulum, Akademik & Komunikasi',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="id">
      <body suppressHydrationWarning>{children}</body>
    </html>
  );
}
