/** @type {import('next').NextConfig} */
const nextConfig = {
  // Next.js 16+ allows basePath and assetPrefix out of the box
  // Optional: disable image optimization for simpler deployment
  images: {
    unoptimized: true,
  },
  // Allow source maps for easier debugging
  compiler: {
    // Optional: reduce bundle size by removing dev-only code
  },
};

export default nextConfig;
