/** @type {import('next').Config} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb'
    }
  }
};

export default nextConfig;