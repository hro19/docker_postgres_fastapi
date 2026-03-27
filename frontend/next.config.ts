import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async redirects() {
    return [
      {
        source: "/post/add",
        destination: "/posts/add",
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
