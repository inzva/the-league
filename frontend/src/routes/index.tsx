import { Container, Typography } from "@mui/material";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <Container className="flex min-h-screen items-center justify-center">
      <Typography variant="h1" fontWeight={700}>
        The League
      </Typography>
    </Container>
  );
}
