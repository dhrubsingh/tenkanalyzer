/** @type {import('next').Config} */
const nextConfig = {
  webpack: (config) => {
    config.externals = [...config.externals, '@heroicons/react'];
    return config;
  },
};

module.exports = nextConfig;