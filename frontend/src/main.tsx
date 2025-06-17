import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";
import { GlobalStyles, StyledEngineProvider } from "@mui/material";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";

/// https://tanstack.com/router/latest/docs/framework/react/quick-start#srcmaintsx
// Import the generated route tree
import { createRouter, RouterProvider } from "@tanstack/react-router";
import { routeTree } from "./routeTree.gen";

// Create a new router instance
const router = createRouter({ routeTree });

// Register the router instance for type safety
declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <StyledEngineProvider enableCssLayer>
      <GlobalStyles styles="@layer theme, base, mui, components, utilities;" />

      <RouterProvider router={router} />
    </StyledEngineProvider>
  </StrictMode>,
);
