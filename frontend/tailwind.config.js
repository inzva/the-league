/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      typography: () => ({
        DEFAULT: {
          css: {
            "--tw-prose-body": "var(--color-pink-100)",
            "--tw-prose-headings": "var(--color-pink-200)",
            "--tw-prose-bullets": "var(--color-pink-300)",
          },
        },
      }),
    },
  },
};
