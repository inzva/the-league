import tailwindcss from "@tailwindcss/vite";
import { tanstackRouter } from "@tanstack/router-plugin/vite";
import react from "@vitejs/plugin-react-swc";
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    // https://tanstack.com/router/latest/docs/framework/react/routing/installation-with-vite
    tanstackRouter({
      target: "react",
      autoCodeSplitting: true,
    }),

    // https://tailwindcss.com/docs/installation/using-vite
    tailwindcss(),
    react(),
  ],

  // for gh-pages
  base: "/the-league/",
});
